import requests
from bs4 import BeautifulSoup
import json

url = "https://www.brownells.com/guns/rifles/semi-auto-rifles/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
html = requests.get(url, headers=headers).text

soup = BeautifulSoup(html, 'html.parser')
products = []
for el in soup.find_all('script', type='application/ld+json'):
    try:
        data = json.loads(el.string)
        if isinstance(data, list):
            for item in data:
                if item.get('@type') == 'Product':
                    products.append(item)
        elif data.get('@type') == 'Product':
            products.append(data)
    except Exception as e:
        pass

print(f"Found {len(products)} products via JSON-LD")
if products:
    print(json.dumps(products[0], indent=2))
