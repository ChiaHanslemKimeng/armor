import os
import django
import urllib.request
import urllib.parse
import re
import json
from django.core.management.base import BaseCommand
from apps.catalog.models import TriggerTimesVideo

class Command(BaseCommand):
    help = 'Scrape Trigger Times videos'

    def add_arguments(self, parser):
        parser.add_argument('--from-url', type=str, help='The URL to scrape from')
        parser.add_argument('--target-category', type=str, help='The category slug')

    def handle(self, *args, **options):
        from_url = options.get('from_url')
        to_category = options.get('target_category') or 'scraped-videos'

        if not from_url:
            self.stdout.write("Error: --from-url is required")
            return

        self.stdout.write(f"Fetching from: {from_url}")
        req = urllib.request.Request(from_url, headers={'User-Agent': 'Mozilla/5.0'})
        
        try:
            html = urllib.request.urlopen(req).read().decode('utf-8')
        except Exception as e:
            self.stdout.write(f"Failed to fetch {from_url}: {e}")
            return

        match = re.search(r'resultItems:\s*(\[.*?\]),?\n', html)
        if not match:
            self.stdout.write("Could not find video data (resultItems array) in the page.")
            return

        json_str = match.group(1)
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            self.stdout.write(f"Error parsing JSON: {e}")
            return

        self.stdout.write(f"Found {len(data)} videos. Starting import for category: {to_category}...")
        
        # Delete old ones in this category to prevent duplicates
        TriggerTimesVideo.objects.filter(category=to_category).delete()

        count = 0
        for idx, item in enumerate(data):
            title = item.get('title', 'Unknown')
            image_url = item.get('imageUrl', '')
            
            if image_url and image_url.startswith('/'):
                image_url = 'https://www.brownells.com' + image_url
                
            self.stdout.write(f"Searching YouTube for: {title}")
            query = "Brownells " + title + " youtube"
            search_url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
            
            search_req = urllib.request.Request(search_url, headers={'User-Agent': 'Mozilla/5.0'})
            video_url = ""
            try:
                search_html = urllib.request.urlopen(search_req).read().decode('utf-8')
                yt_match = re.search(r'"videoId":"([^"]{11})"', search_html)
                if yt_match:
                    vid = yt_match.group(1)
                    video_url = f"https://www.youtube.com/embed/{vid}"
                    self.stdout.write(f" -> Found YouTube ID: {vid}")
                else:
                    self.stdout.write(f" -> Warning: Could not find YouTube ID. Setting blank URL.")
            except Exception as e:
                self.stdout.write(f" -> Error searching YouTube: {e}")
                
            TriggerTimesVideo.objects.create(
                title=title,
                video_url=video_url,
                thumbnail_url=image_url,
                category=to_category,
                is_featured=(idx == 0) # Make the first one featured
            )
            count += 1

        self.stdout.write(f"Successfully imported {count} videos into the '{to_category}' category!")