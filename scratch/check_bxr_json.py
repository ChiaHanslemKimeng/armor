import re
import json

html = open('bxr.html', encoding='utf-8').read()
m = re.search(r'var currentProduct = JSON\.parse\(\"(.*?)\"\);', html)
if m:
    data = json.loads(m.group(1).encode('utf-8').decode('unicode_escape'))['viewModel']
    print(json.dumps(data, indent=2)[:2000])
