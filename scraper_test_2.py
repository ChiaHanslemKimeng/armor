import requests
import json
import re

url = "https://www.brownells.com/guns/rifles/semi-auto-rifles/mp-fpc-10mm-auto-semi-auto-rifle/"
headers = {"User-Agent": "Mozilla/5.0"}
html = requests.get(url, headers=headers).text

match = re.search(r'__PRELOADED_STATE__\s*=\s*({.*?});', html)
if match:
    data = json.loads(match.group(1))
    print("Found Preloaded State JSON!")
    with open("product_state.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
else:
    print("No preloaded state found")
