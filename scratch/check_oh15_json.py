import re
import json

html = open('oh15.html', encoding='utf-8').read()
m = re.search(r'var currentProduct = JSON\.parse\(\"(.*?)\"\);', html)
if m:
    data = json.loads(m.group(1).encode('utf-8').decode('unicode_escape'))['viewModel']
    for key, value in data.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            print(f"List {key}: {len(value)} items")
            print(value[0])
        elif isinstance(value, str) and len(value) > 100:
            if "PDF" in value or "Data >" in value:
                print(f"Found in {key}: {value[:100]}")
