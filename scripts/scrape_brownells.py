import os
import sys
import re
import json
import urllib.request
import django
import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from urllib.parse import urljoin

# Setup Django Environment
sys.path.append(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'armor_project.settings')
django.setup()

from apps.catalog.models import Product, Category, Brand, ProductImage

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def parse_product_page(url, category):
    print(f"Scraping product: {url}")
    html = fetch_html(url)
    soup = BeautifulSoup(html, 'lxml')

    # Get Name
    name_tag = soup.find('h1')
    name = name_tag.text.strip() if name_tag else "Unknown Product"

    # Get Brand
    brand_name = "Brownells" # Default
    brand_tag = soup.find('a', class_=re.compile(r'brand', re.I))
    if brand_tag:
        brand_name = brand_tag.text.strip()
    brand, _ = Brand.objects.get_or_create(name=brand_name, defaults={'slug': brand_name.lower().replace(' ', '-')[:150]})

    # Get Price
    price = 1000.00 # Default
    price_tag = soup.find(string=re.compile(r'\$\d+\.\d{2}'))
    if price_tag:
        match = re.search(r'\$(\d+\.\d{2})', price_tag)
        if match:
            price = float(match.group(1).replace(',', ''))
    
    # Get SKU
    sku = "SKU-UNKNOWN"
    sku_match = re.search(r'MFR \#:?\s*([A-Z0-9\-]+)', html, re.I)
    if sku_match:
        sku = sku_match.group(1).strip()
    else:
        # Generate SKU from URL
        sku = url.split('/')[-2].upper()[:20]

    # Get Description
    description = ""
    desc_tag = soup.find('div', class_=re.compile(r'description|details', re.I))
    if desc_tag:
        description = desc_tag.text.strip()[:490]
    else:
        description = "A reliable semi-automatic rifle."

    # Get Specifications
    specifications_dict = {}
    
    # Look for tables (typically specs)
    tables = soup.find_all('table')
    for table in tables:
        for row in table.find_all('tr'):
            cols = row.find_all(['th', 'td'])
            if len(cols) == 2:
                key = cols[0].text.strip().replace(':', '')
                val = cols[1].text.strip()
                if key and val:
                    specifications_dict[key] = val
                    
    # Also look for definition lists or div-based specs
    spec_divs = soup.find_all('div', class_=re.compile(r'spec', re.I))
    for div in spec_divs:
        labels = div.find_all('span', class_=re.compile(r'label|name', re.I))
        values = div.find_all('span', class_=re.compile(r'value|data', re.I))
        if len(labels) == len(values):
            for l, v in zip(labels, values):
                specifications_dict[l.text.strip().replace(':', '')] = v.text.strip()

    # Get Restrictions
    restrictions = []
    rest_tags = soup.find_all(string=re.compile(r'Restriction|Warning|FFL Required|Cannot ship to', re.I))
    for r in rest_tags:
        text = r.strip()
        if len(text) > 5 and len(text) < 150:
            restrictions.append(text)
    
    if not restrictions:
        restrictions = ["FFL Required for Firearm Transfer"]
        
    specifications_dict['Restrictions'] = restrictions

    # Get Image
    img_url = None
    og_img = soup.find('meta', property='og:image')
    if og_img and og_img.get('content'):
        img_url = og_img['content']
    else:
        # Fallback to looking for img tags
        img_tag = soup.find('img', class_=re.compile(r'main-image|product-image', re.I))
        if img_tag and img_tag.get('src'):
            img_url = urljoin(url, img_tag['src'])

    # Create Product
    product, created = Product.objects.update_or_create(
        sku=sku,
        defaults={
            'name': name[:255],
            'slug': name.lower().replace(' ', '-')[:255] + f'-{sku.lower()}',
            'brand': brand,
            'category': category,
            'price': price,
            'short_description': description[:500],
            'rich_description': description,
            'specifications': specifications_dict,
            'is_active': True,
        }
    )

    print(f"{'Created' if created else 'Updated'} product: {product.name}")

    # Handle Image
    if img_url:
        print(f"Downloading image from {img_url}")
        try:
            image_content = requests.get(img_url).content
            
            # Remove existing primary image to avoid duplicates
            ProductImage.objects.filter(product=product).delete()
            
            p_img = ProductImage(product=product, is_primary=True)
            filename = f"{sku}_{os.path.basename(img_url.split('?')[0])}"
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                filename += '.jpg'
            p_img.image.save(filename, ContentFile(image_content), save=True)
            print(f"Saved image: {filename}")
        except Exception as e:
            print(f"Error downloading image: {e}")

def main():
    base_url = 'https://www.brownells.com'
    list_url = f'{base_url}/guns/rifles/semi-auto-rifles/'
    
    # Get or create categories by slug
    rifles_cat, _ = Category.objects.get_or_create(slug='rifles', defaults={'name': 'Rifles'})
    semi_auto_cat, _ = Category.objects.get_or_create(slug='semi-auto', defaults={'name': 'Semi-Auto', 'parent': rifles_cat})
    
    print(f"Fetching product list from {list_url}")
    html = fetch_html(list_url)
    
    # Find product links. Exclude obvious category links (which usually end in -rifles/)
    links = re.findall(r'href=\"(/guns/rifles/semi-auto-rifles/[^\"]+)\"', html)
    unique_links = []
    for l in links:
        l_clean = urljoin(base_url, l.rstrip('/'))
        if l_clean not in unique_links and '?' not in l_clean and not l_clean.endswith('-rifles'):
            unique_links.append(l_clean)
    
    print(f"Found {len(unique_links)} potential product links.")
    
    count = 0
    for link in unique_links:
        if count >= 5:
            break
        try:
            parse_product_page(link, semi_auto_cat)
            count += 1
        except Exception as e:
            print(f"Failed to process {link}: {e}")

if __name__ == '__main__':
    main()
