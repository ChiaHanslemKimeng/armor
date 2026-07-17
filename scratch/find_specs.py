from bs4 import BeautifulSoup
import re

html = open('prod.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
specs = soup.find(string=re.compile("Quick Factory Specs"))
if specs:
    parent = specs.parent
    while parent and parent.name not in ['div', 'section']:
        parent = parent.parent
    print(f"Parent tag: {parent.name}")
    print(f"Parent class: {parent.get('class')}")
    print(f"Parent id: {parent.get('id')}")
else:
    print("Not found as string, maybe in json")
