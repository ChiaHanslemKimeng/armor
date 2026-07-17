import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://www.brownells.com/guns/rifles/semi-auto-rifles/"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
html = resp.text

# Let's try to find if there is a JSON state or script tag containing products
match = re.search(r'__PRELOADED_STATE__\s*=\s*({.*?});', html)
if match:
    print("Found PRELOADED_STATE!")
    with open("brownells_state.json", "w", encoding="utf-8") as f:
        f.write(match.group(1))
else:
    # Let's use bs4
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for a in soup.find_all('a', href=True):
        if '/guns/rifles/' in a['href'] and '-rifle/' in a['href']:
            links.add(a['href'])
    print("Found links:")
    for link in list(links)[:5]:
        print(link)
