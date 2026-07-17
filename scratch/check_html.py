from bs4 import BeautifulSoup
import sys

html = open('prod.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
desc = soup.find('div', class_='pdp-tabs__description')
if desc:
    print("Found description block.")
    imgs = desc.find_all('img')
    links = desc.find_all('a')
    print(f"Images found: {len(imgs)}")
    print(f"Links found: {len(links)}")
    
    # Show first 500 chars of text
    print("--- TEXT ---")
    print(desc.text.strip()[:500])
else:
    print("No pdp-tabs__description found.")
