import re
import json

html = open('prod.html', encoding='utf-8').read()
m = re.search(r'var currentProduct = JSON\.parse\("(.*?)"\);', html)
if m:
    raw = m.group(1).encode('utf-8').decode('unicode_escape')
    try:
        data = json.loads(raw)
        print("Keys:", data.keys())
        if 'viewModel' in data:
            print("ViewModel Keys:", data['viewModel'].keys())
            if 'productImages' in data['viewModel']:
                print("Images:", len(data['viewModel']['productImages']))
            # Find variations and long descriptions
            print("Title:", data['viewModel'].get('displayName') or data['viewModel'].get('title'))
            print("Variants in viewModel?", [k for k in data['viewModel'].keys() if 'variant' in k.lower()])
            print("Options in viewModel?", [k for k in data['viewModel'].keys() if 'option' in k.lower()])
            
            # Print any fields that might contain HTML descriptions
            for k, v in data['viewModel'].items():
                if isinstance(v, str) and ('<p>' in v or '<h1>' in v or 'What is the' in v or 'Quick Factory Specs' in v):
                    print(f"HTML Content in {k}: {v[:100]}...")
                    
        if 'specificationSelectionModel' in data:
            print("spec selection?", data['specificationSelectionModel'][:1])
    except Exception as e:
        print("JSON parse error:", e)
else:
    print("No match found")
