import requests
import re
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}
url = 'https://www.brownells.com/guns/rifles/semi-auto-rifles/bxr-22lr-chromoly/'
resp = requests.get(url, headers=headers)
with open('bxr.html', 'w', encoding='utf-8') as f:
    f.write(resp.text)

print("Downloaded bxr.html")
img_links = re.findall(r'/globalassets/[^\s\"\'\?]+\.(?:jpg|png)', resp.text)
for img in set(img_links):
    print(img)
    
soup = BeautifulSoup(resp.text, 'html.parser')
desc = soup.find('div', class_='pdp-tabs__description')
if desc:
    print("DESC TEXT:")
    print(desc.text[:500])
