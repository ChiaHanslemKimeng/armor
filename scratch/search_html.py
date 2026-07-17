import re
html = open('prod.html', encoding='utf-8').read()
match = re.search(r'Available options', html, re.IGNORECASE)
if match:
    start = max(0, match.start() - 100)
    end = min(len(html), match.end() + 200)
    print(html[start:end])
else:
    print("Not found in prod.html")
