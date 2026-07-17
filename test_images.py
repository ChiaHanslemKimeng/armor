import re

with open('prod.html', encoding='utf-8') as f:
    html = f.read()

links = re.findall(r'/globalassets/[^\s\"\'\?]+\.jpg', html)
print(list(set(links)))
