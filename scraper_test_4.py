import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://www.brownells.com/guns/rifles/semi-auto-rifles/mp-fpc-10mm-auto-semi-auto-rifle/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, 'html.parser')

title = soup.find('h1')
print("Title:", title.text.strip() if title else "Not found")

meta_price = soup.find('meta', property='product:price:amount')
if not meta_price:
    meta_price = soup.find('span', text=re.compile(r'\$\d+'))
print("Price:", meta_price['content'] if meta_price and meta_price.has_attr('content') else getattr(meta_price, 'text', 'Not found'))

image = soup.find('meta', property='og:image')
print("Image:", image['content'] if image else "Not found")

desc = soup.find('meta', property='og:description')
print("Desc:", desc['content'] if desc else "Not found")
