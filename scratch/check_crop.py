import re
html = open('prod.html', encoding='utf-8').read()
crop_links = re.findall(r'[^"\']*crop[^"\']*', html, re.IGNORECASE)
print(list(set(crop_links))[:10])
