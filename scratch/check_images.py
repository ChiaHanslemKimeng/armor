import re
html = open('prod.html', encoding='utf-8').read()
img_links = re.findall(r'/globalassets/[^\s\"\'\?]+\.(?:jpg|png)', html)
print(list(set(img_links)))
