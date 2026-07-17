import os
import re
import urllib.parse
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.catalog.models import TriggerTimesVideo

class Command(BaseCommand):
    help = 'Scrape Trigger Times videos from a URL and save them to the database'

    def add_arguments(self, parser):
        parser.add_argument('--from-url', type=str, help='The URL to scrape videos from (e.g. Brownells Trigger Times page)')
        parser.add_argument('--to-url', type=str, help='The target local URL to extract category from (e.g. http://127.0.0.1:8000/trigger-times/?cat=rifle-builds)')

    def handle(self, *args, **options):
        from_url = options.get('from_url')
        to_url = options.get('to_url')
        
        if not from_url:
            self.stdout.write(self.style.ERROR("Error: --from-url is required"))
            return
            
        category = 'rifle-builds'
        if to_url:
            parsed = urllib.parse.urlparse(to_url)
            qs = urllib.parse.parse_qs(parsed.query)
            category = qs.get('cat', [category])[0]
            
        self.stdout.write(self.style.SUCCESS(f"Starting Scraper..."))
        self.stdout.write(f"Source URL: {from_url}")
        self.stdout.write(f"Target Category: {category}")
        
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            resp = requests.get(from_url, headers=headers, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to fetch {from_url}: {e}"))
            return
            
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Helper function to extract videos from a soup
        def extract_videos_from_soup(page_soup, source_url):
            found = []
            
            # Method 1: Look for YouTube iframes directly
            iframes = page_soup.find_all('iframe')
            for iframe in iframes:
                src = iframe.get('src', '')
                if 'youtube.com/embed' in src or 'youtube-nocookie.com/embed' in src:
                    m = re.search(r'embed/([^?&]+)', src)
                    if m:
                        vid_id = m.group(1)
                        title = iframe.get('title')
                        if not title or 'youtube video player' in title.lower():
                            # Try to find a heading nearby or h1 on the page
                            h1 = page_soup.find('h1')
                            if h1:
                                title = h1.text.strip()
                        if not title or title.strip() == '':
                            title = f"Trigger Times Video {vid_id}"
                            
                        found.append({
                            'title': title,
                            'video_url': f"https://www.youtube.com/embed/{vid_id}",
                            'thumbnail_url': f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg"
                        })
                        
            # Method 2: Look for 'a' tags pointing to youtube
            a_tags = page_soup.find_all('a', href=re.compile(r'youtube\.com/watch\?v='))
            for a_tag in a_tags:
                href = a_tag['href']
                m = re.search(r'v=([^&]+)', href)
                if m:
                    vid_id = m.group(1)
                    title = a_tag.text.strip()
                    if not title:
                        h1 = page_soup.find('h1')
                        title = h1.text.strip() if h1 else f"Video Feature {vid_id}"
                        
                    found.append({
                        'title': title,
                        'video_url': f"https://www.youtube.com/embed/{vid_id}",
                        'thumbnail_url': f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg"
                    })
            return found

        videos_found = []
        
        # Method 1: Extract videos cleanly using BeautifulSoup
        main_videos = extract_videos_from_soup(soup, from_url)
        videos_found.extend(main_videos)
        
        # Method 2: Fallback, extract ALL YouTube IDs embedded anywhere in the raw HTML/JS
        # This bypasses the need to visit sub-links because the main page often embeds the JSON data
        raw_html = resp.text
        yt_ids = re.findall(r'(?:youtube\.com/embed/|youtu\.be/|v=)([a-zA-Z0-9_-]{11})', raw_html)
        
        for vid_id in set(yt_ids):
            # If not already found by Method 1
            if not any(v['video_url'].endswith(vid_id) for v in videos_found):
                # We don't have the exact title, so we use a placeholder that user can edit later
                # Or try to find it in the HTML JSON blob
                title_match = re.search(vid_id + r'.*?\"title\"\s*:\s*\"([^\"]+)\"', raw_html, re.IGNORECASE)
                title = title_match.group(1) if title_match else f"Trigger Times Video {vid_id}"
                
                videos_found.append({
                    'title': title[:255],
                    'video_url': f"https://www.youtube.com/embed/{vid_id}",
                    'thumbnail_url': f"https://img.youtube.com/vi/{vid_id}/maxresdefault.jpg"
                })

        if not videos_found:
            self.stdout.write(self.style.WARNING("No videos found on the page."))
            return
            
        self.stdout.write(f"Total {len(videos_found)} unique videos extracted. Saving to database...")
        
        # Clear existing videos in this category to prevent stale data
        TriggerTimesVideo.objects.filter(category=category).delete()
        self.stdout.write("Cleaned old videos for this category.")
        
        for idx, v in enumerate(videos_found):
            is_featured = (idx == 0) # Make the first video the featured one
            obj = TriggerTimesVideo.objects.create(
                video_url=v['video_url'],
                category=category,
                title=v['title'][:255],
                thumbnail_url=v['thumbnail_url'],
                is_featured=is_featured
            )
            self.stdout.write(self.style.SUCCESS(f"Added: {v['title']}"))
                
        self.stdout.write(self.style.SUCCESS(f"Successfully scraped and saved {len(videos_found)} videos to category '{category}'!"))
