import os
import django
import urllib.request
import urllib.parse
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armor_project.settings')
django.setup()

from apps.catalog.models import TriggerTimesVideo

videos = TriggerTimesVideo.objects.all()

for video in videos:
    query = "Brownells " + video.title + " youtube"
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(query)
    
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        # Find first watch?v= id
        match = re.search(r'"videoId":"([^"]{11})"', html)
        if match:
            vid = match.group(1)
            video.video_url = f"https://www.youtube.com/embed/{vid}"
            video.save()
            print(f"Updated {video.title} -> {vid}")
        else:
            print(f"Could not find YouTube ID for {video.title}")
    except Exception as e:
        print(f"Error searching {video.title}: {e}")
