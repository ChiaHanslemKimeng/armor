import urllib.request
import re
import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://www.brownells.com/'
}

urls = [
    'https://www.brownells.com/guns/rifles/semi-auto-rifles/super-duty-mod1-5.56x45-nato-semi-auto-rifle/',
    'https://www.brownells.com/guns/rifles/semi-auto-rifles/mcx-spear-7.62x51-nato-semi-auto-rifle/',
    'https://www.brownells.com/guns/rifles/semi-auto-rifles/dd5-v4-7.62x51-nato-semi-auto-rifle/',
    'https://www.brownells.com/guns/rifles/semi-auto-rifles/m4a1-carbine-socom-5.56x45-nato-semi-auto-rifle/',
    'https://www.brownells.com/guns/rifles/semi-auto-rifles/saint-victor-v2-5.56-nato-semi-auto-ar-15-rifle/'
]

for url in urls:
    print("--------------------------------------------------")
    print("URL:", url.split('/')[-2])
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8', errors='ignore')
            
            # Find price in schema or spans
            schema_prices = re.findall(r'[\"\']price[\"\']\s*:\s*([0-9\.]+)|[\"\']price[\"\']\s*:\s*[\"\']([0-9\.]+)[\"\']', content, re.I)
            schema_prices = [p[0] or p[1] for p in schema_prices if p[0] or p[1]]
            print("Schema Prices:", sorted(list(set(schema_prices))))
            
            dollar_prices = re.findall(r'\$\s*([0-9,]+\.[0-9]{2})', content)
            dollar_prices = sorted(list(set([p.replace(',', '') for p in dollar_prices])))
            print("Dollar Prices ($X.XX):", dollar_prices[:10])
            
            # Look for specific price class/id around price
            price_snippets = re.findall(r'<[^>]*(?:price|amount|current-price)[^>]*>([^<]+)</[^>]+>', content, re.I)
            print("Price Snippets:", [html.unescape(s.strip()) for s in price_snippets if '$' in s or s.strip().replace('.','').isdigit()][:5])
            
            # Look for exact h1
            h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.I | re.S)
            if h1s:
                print("H1 Title:", html.unescape(re.sub(r'<[^>]+>', '', h1s[0]).strip()))
                
            # Check for specification table or specs list
            specs = re.findall(r'<dt[^>]*>(.*?)</dt>\s*<dd[^>]*>(.*?)</dd>|<th[^>]*>(.*?)</th>\s*<td[^>]*>(.*?)</td>', content, re.I | re.S)
            clean_specs = []
            for s in specs:
                k = html.unescape(re.sub(r'<[^>]+>', '', s[0] or s[2]).strip())
                v = html.unescape(re.sub(r'<[^>]+>', '', s[1] or s[3]).strip())
                if k and v and len(k) < 50 and len(v) < 100:
                    clean_specs.append(f"{k}: {v}")
            print("Specs found count:", len(clean_specs))
            if clean_specs:
                print("Sample specs:", clean_specs[:5])
    except Exception as e:
        print("Error:", e)
