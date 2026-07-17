import re
import json

html = open('prod.html', encoding='utf-8').read()
m = re.search(r'var currentProduct = JSON\.parse\("(.*?)"\);', html)
data = json.loads(m.group(1).encode('utf-8').decode('unicode_escape'))['viewModel']
for k in data.keys():
    v = data[k]
    if isinstance(v, str) and ('<p>' in v or '<h1>' in v or 'Quick Factory Specs' in v or 'description' in k.lower()):
        print(f"Key: {k}")
