import os
import re
import json
import math
import requests
import decimal
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone
from apps.catalog.models import Product, ProductImage, Category, Brand, ScraperTask

class Command(BaseCommand):
    help = 'Dynamic web crawler for product catalog.'

    def add_arguments(self, parser):
        parser.add_argument('--from-url', type=str, help='The URL to scrape products from')
        parser.add_argument('--to-url', type=str, help='The URL to end scraping')
        parser.add_argument('--task-id', type=str, help='The UUID of the ScraperTask for live logs')
        parser.add_argument('--target-category', type=str, help='The category slug')

    def log_live(self, task, message):
        timestamped = f"[{timezone.now()}] {message}\n"
        if task:
            task.logs += timestamped
            task.save(update_fields=['logs'])
        self.stdout.write(message)

    def handle(self, *args, **options):
        source_url = options.get('from_url')
        to_url = options.get('to_url')
        task_id = options.get('task_id')
        target_category_slug = options.get('target_category') or 'scraped-products'

        task = None
        if task_id:
            try:
                task = ScraperTask.objects.get(id=task_id)
            except ScraperTask.DoesNotExist:
                pass

        if not source_url:
            self.log_live(task, "ERROR: No source URL provided.")
            if task:
                task.status = 'failed'
                task.save(update_fields=['status'])
            return

        self.log_live(task, f"Starting Advanced Deep Crawler...")
        self.log_live(task, f"Target Catalog URL: {source_url}")
        
        self.log_live(task, "Deleting all existing products to ensure a clean slate...")
        ProductImage.objects.all().delete()
        Product.objects.all().delete()
        self.log_live(task, "Clean slate confirmed.")

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        try:
            resp = requests.get(source_url, headers=headers, timeout=15)
            resp.raise_for_status()
        except Exception as e:
            self.log_live(task, f"Failed to fetch catalog page: {e}")
            if task:
                task.status = 'failed'
                task.save(update_fields=['status'])
            return

        # 1. Pagination Extraction
        total_pages = 1
        try:
            m = re.search(r'var filterModel = (\{.*?\});', resp.text)
            if m:
                f_data = json.loads(m.group(1))
                t_count = f_data.get('totalCount', 0)
                p_size = f_data.get('pageSize', 32)
                if t_count and p_size:
                    total_pages = math.ceil(t_count / p_size)
                    self.log_live(task, f"Found {t_count} total products across {total_pages} pages.")
        except Exception as e:
            self.log_live(task, f"Could not parse pagination (falling back to single page): {e}")

        product_links = set()
        
        for p in range(1, total_pages + 1):
            page_url = source_url if p == 1 else f"{source_url}?page={p}"
            self.log_live(task, f"Scanning catalog page {p}/{total_pages}...")
            try:
                page_resp = requests.get(page_url, headers=headers, timeout=15)
                page_soup = BeautifulSoup(page_resp.text, 'html.parser')
                for a in page_soup.find_all('a', href=True):
                    href = a['href']
                    # Look for URLs with at least 5 segments (e.g. /guns/rifles/semi-auto-rifles/product-name/)
                    if '/guns/' in href and href.endswith('/') and len(href.split('/')) > 5:
                        if not href.startswith('http'):
                            href = "https://www.brownells.com" + href
                        product_links.add(href)
            except Exception as e:
                self.log_live(task, f"Failed to read page {p}: {e}")

        if not product_links:
            self.log_live(task, "Could not find any product links.")
            if task:
                task.status = 'completed'
                task.save(update_fields=['status'])
            return

        self.log_live(task, f"Discovered {len(product_links)} unique product URLs to scrape.")

        import urllib.parse
        parsed = urllib.parse.urlparse(to_url) if to_url else None
        qs = urllib.parse.parse_qs(parsed.query) if parsed else {}
        cat_slug = qs.get('category', [target_category_slug])[0]
        sub_slug = qs.get('sub', [None])[0]

        # Ensure Category and Brand
        parent_category, _ = Category.objects.get_or_create(
            slug=cat_slug,
            defaults={'name': cat_slug.replace('-', ' ').title()}
        )
        
        if sub_slug:
            category, _ = Category.objects.get_or_create(
                slug=sub_slug,
                defaults={'name': sub_slug.replace('-', ' ').title(), 'parent': parent_category}
            )
        else:
            category = parent_category

        brand, _ = Brand.objects.get_or_create(slug="scraped-brand", defaults={'name': "Scraped Brand"})

        GALLERY_REL_DIR = os.path.join('catalog', 'products', 'gallery')
        GALLERY_ABS_DIR = os.path.join(settings.MEDIA_ROOT, GALLERY_REL_DIR)
        os.makedirs(GALLERY_ABS_DIR, exist_ok=True)

        scraped_count = 0
        for i, link in enumerate(product_links, 1):
            self.log_live(task, f"[{i}/{len(product_links)}] Visiting: {link}")
            try:
                p_resp = requests.get(link, headers=headers, timeout=15)
                p_resp.raise_for_status()
            except Exception as e:
                self.log_live(task, f"  -> Failed to fetch: {e}")
                continue

            p_soup = BeautifulSoup(p_resp.text, 'html.parser')

            # Extract internal JSON state
            json_data = {}
            m = re.search(r'var currentProduct = JSON\.parse\("(.*?)"\);', p_resp.text)
            if m:
                raw = m.group(1).encode('utf-8').decode('unicode_escape')
                try:
                    json_data = json.loads(raw).get('viewModel', {})
                except Exception as e:
                    self.log_live(task, f"  -> JSON Warning: {e}")

            # Title and Brand Parsing
            title = json_data.get('displayName') or json_data.get('title')
            if not title:
                title_el = p_soup.find('h1')
                title = title_el.text.strip() if title_el else "Unknown Product"

            # Parse Brand from Title (e.g., 'SMITH & WESSON - M&P 15-22' -> 'SMITH & WESSON')
            brand_name = "Unknown Brand"
            if " - " in title:
                brand_name = title.split(" - ")[0].strip().title()
            else:
                brand_name = title.split(" ")[0].title()
            brand, _ = Brand.objects.get_or_create(slug=brand_name.replace(" ", "-").lower()[:50], defaults={'name': brand_name})

            # Price
            price_val = decimal.Decimal('0.00')
            if json_data.get('listingPrice'):
                price_val = decimal.Decimal(str(json_data['listingPrice']))
            elif json_data.get('formattedProductCurrentPrice'):
                price_str = re.sub(r'[^\d\.]', '', json_data.get('formattedProductCurrentPrice'))
                try: price_val = decimal.Decimal(price_str)
                except: pass

            if price_val <= 0:
                meta_price = p_soup.find('meta', property='product:price:amount')
                if not meta_price:
                    meta_price = p_soup.find('span', string=re.compile(r'\$\d+\.\d{2}'))
                price_str = meta_price['content'] if meta_price and meta_price.has_attr('content') else getattr(meta_price, 'text', '0.00')
                price_str = re.sub(r'[^\d\.]', '', price_str)
                try:
                    price_val = decimal.Decimal(price_str)
                except:
                    pass

            if price_val <= 0:
                self.log_live(task, f"  -> Skipping {title} because no price was found.")
                continue

            # Deep HTML Description Extraction
            rich_desc = ""
            desc_container = p_soup.find('div', class_='pdp-tabs__description')
            if desc_container:
                # Remove unwanted tags, including tables that hold duplicate options
                for tag in desc_container.find_all(['img', 'iframe', 'script', 'style', 'picture', 'video', 'svg', 'table']):
                    tag.decompose()
                # Remove "Available options" text blocks
                for text_node in desc_container.find_all(string=re.compile(r"Available options", re.I)):
                    if text_node.parent and text_node.parent.name in ['h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'b', 'div', 'p', 'span']:
                        text_node.parent.decompose()
                    else:
                        text_node.extract()
                
                # Remove SEO boilerplate ("What is the...")
                for text_node in desc_container.find_all(string=re.compile(r"What is the", re.I)):
                    if text_node.parent and text_node.parent.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'b', 'div', 'p', 'span']:
                        text_node.parent.decompose()
                    else:
                        text_node.extract()
                
                # Remove SEO boilerplate ("Check out... available Online at Brownells")
                for text_node in desc_container.find_all(string=re.compile(r"available Online at Brownells", re.I)):
                    if text_node.parent and text_node.parent.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'strong', 'b', 'div', 'p', 'span']:
                        text_node.parent.decompose()
                    else:
                        text_node.extract()
                        
                for a_tag in desc_container.find_all('a'):
                    a_tag.unwrap()
                # Extract inner HTML of the container
                rich_desc = "".join([str(c) for c in desc_container.contents]).strip()
            
            # Fallback to meta description if HTML extraction failed
            if not rich_desc:
                desc_el = p_soup.find('meta', property='og:description')
                rich_desc = desc_el['content'] if desc_el else "No description available."
            
            # Short description for list views
            desc_el = p_soup.find('meta', property='og:description')
            short_desc = desc_el['content'] if desc_el else "No description available."
            # Clean SEO boilerplate from short description
            short_desc = re.sub(r'Check out.*?available Online at Brownells.*', '', short_desc, flags=re.I).strip()
            if not short_desc:
                short_desc = title[:200]
                
            # Parse Restrictions
            restriction_dict = json_data.get('restriction') or {}
            if restriction_dict.get('extraTextToDisplayOnPdp'):
                restriction_html = restriction_dict['extraTextToDisplayOnPdp']
                if restriction_html:
                    r_soup = BeautifulSoup(restriction_html, 'html.parser')
                    for tag in r_soup.find_all(['img', 'iframe', 'script', 'style', 'picture', 'video', 'svg']):
                        tag.decompose()
                    for a_tag in r_soup.find_all('a'):
                        a_tag.unwrap()
                    clean_restriction = "".join([str(c) for c in r_soup.contents]).strip()
                    if clean_restriction:
                        rich_desc += f"\n\n<h3>Restrictions & Policies</h3>\n{clean_restriction}"

            # SKU (ensure it does not say SCRAPE if we can avoid it)
            sku = json_data.get('sku') or json_data.get('code') or f"BRWN-{str(hash(link))[-6:]}"

            # Dynamic Specifications
            spec_dict = {}
            spec_list = json_data.get('specifications', [])
            for spec in spec_list:
                if 'key' in spec and 'value' in spec:
                    spec_dict[spec['key']] = spec['value']
            
            # Extract Variants (e.g., SELECT ARMORY CONFIGURATION)
            variants_list = json_data.get('specificationSelectionModel', [])
            if variants_list:
                rich_desc += "\n\n<h3>Configuration Options</h3>\n<ul>"
                for variant_group in variants_list:
                    group_name = variant_group.get('label', 'Options')
                    for option in variant_group.get('options', []):
                        opt_val = option.get('value', '')
                        opt_price = option.get('price', '')
                        if opt_val:
                            rich_desc += f"<li><strong>{group_name}:</strong> {opt_val} "
                            if opt_price:
                                rich_desc += f"(+${opt_price})"
                                # Also inject to specifications JSON
                                spec_dict[f"{group_name} Option"] = f"{opt_val} (+${opt_price})"
                            rich_desc += "</li>"
                rich_desc += "</ul>"

            product, created = Product.objects.update_or_create(
                slug=sku.lower(),
                defaults={
                    'name': title[:255],
                    'sku': sku[:100],
                    'price': price_val,
                    'short_description': short_desc[:500],
                    'rich_description': rich_desc,
                    'specifications': spec_dict,
                    'brand': brand,
                    'is_active': True
                }
            )
            product.categories.add(parent_category)
            product.categories.add(category)
            
            action = "CREATED" if created else "UPDATED"
            self.log_live(task, f"  -> {action}: {title[:40]}... (Price: ${price_val})")

            # Extract Images from JSON and raw HTML
            product.images.all().delete()
            gallery_links = []
            
            # 1. Try JSON
            if 'productImages' in json_data and isinstance(json_data['productImages'], list):
                for img_obj in json_data['productImages']:
                    if 'zoomUrl' in img_obj and img_obj['zoomUrl']:
                        gallery_links.append(img_obj['zoomUrl'])
                    elif 'thumbnailUrl' in img_obj and img_obj['thumbnailUrl']:
                        gallery_links.append(img_obj['thumbnailUrl'])
            elif json_data.get('thumbnailImageUrl'):
                gallery_links.append(json_data['thumbnailImageUrl'])
            
            # Remove thumbnail logic forcing thumbnail first, as it's usually a close-up
            
            # 2. Try Regex fallback on raw HTML
            img_links = re.findall(r'/globalassets/[^\s\"\'\?]+\.(?:jpg|png)', p_resp.text)
            for img_url in img_links:
                img_lower = img_url.lower()
                if 'mega-menus' not in img_lower and 'site-settings' not in img_lower and 'logo' not in img_lower and 'brand' not in img_lower and 'privacy' not in img_lower and 'icons' not in img_lower:
                    gallery_links.append(img_url)
            
            # Clean URLs to remove cropped versions and deduplicate
            cleaned_gallery = []
            for link in gallery_links:
                if '/globalassets/' in link:
                    link = '/globalassets/' + link.split('/globalassets/')[-1]
                if not link.startswith('http'):
                    link = "https://www.brownells.com" + link
                if link not in cleaned_gallery:
                    cleaned_gallery.append(link)
            
            # Sort images to put full guns (_1, _2) before close-ups (_3, _4)
            def natural_sort_key(s):
                return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]
            cleaned_gallery.sort(key=natural_sort_key)

            gallery_links = cleaned_gallery[:6]

            if gallery_links:
                for idx, img_url in enumerate(gallery_links):
                    filename = img_url.split('/')[-1]
                    if '?' in filename:
                        filename = filename.split('?')[0]
                    if len(filename) < 5:
                        continue
                        
                    abs_path = os.path.join(GALLERY_ABS_DIR, filename)
                    rel_path = os.path.join(GALLERY_REL_DIR, filename).replace('\\', '/')

                    try:
                        img_resp = requests.get(img_url, headers=headers, stream=True, timeout=15)
                        img_resp.raise_for_status()
                        with open(abs_path, 'wb') as f:
                            for chunk in img_resp.iter_content(chunk_size=8192):
                                f.write(chunk)
                                
                        ProductImage.objects.create(
                            product=product,
                            image=rel_path,
                            alt_text=f"{title[:150]} Image {idx+1}",
                            is_primary=(idx == 0),
                            sort_order=idx
                        )
                        self.log_live(task, f"  -> Attached Image {idx+1}: {filename}")
                    except Exception as e:
                        self.log_live(task, f"  -> Failed to download {filename}: {e}")
            else:
                self.log_live(task, "  -> No images found.")

            scraped_count += 1

        self.log_live(task, f"Crawler Finished! Successfully scraped {scraped_count} products.")
        
        if task:
            task.status = 'completed'
            task.save(update_fields=['status'])
