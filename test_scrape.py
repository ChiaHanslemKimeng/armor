import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://www.brownells.com/the-trigger-times/how-to/rifle-builds--installs/brn22-build/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    bc = re.findall(r'players\.brightcove\.net/([^/]+)', html)
    print("Brightcove accounts:", set(bc))
    
    b_scripts = re.findall(r'src="([^"]+brightcove[^"]+)"', html)
    print("Brightcove scripts:", b_scripts)
except Exception as e:
    print('Error:', e)
