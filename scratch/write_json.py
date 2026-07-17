import re
import json

html = open('prod.html', encoding='utf-8').read()
m = re.search(r'var currentProduct = JSON\.parse\("(.*?)"\);', html)
if m:
    data = json.loads(m.group(1).encode('utf-8').decode('unicode_escape'))['viewModel']
    with open('scratch/prod_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print("Wrote JSON to scratch/prod_data.json")
