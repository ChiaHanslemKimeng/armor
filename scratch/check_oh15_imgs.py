import re
html = open('oh15.html', encoding='utf-8').read()
img_links = re.findall(r'/globalassets/[^\s\"\'\?]+\.(?:jpg|png)', html)
for img in set(img_links):
    print(img)
