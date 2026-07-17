from bs4 import BeautifulSoup
import re

html = open('oh15.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
desc = soup.find('div', class_='pdp-tabs__description')
if desc:
    nodes = desc.find_all(string=re.compile("available Online at Brownells", re.I))
    for node in nodes:
        print("FOUND NODE:", repr(node))
        print("Parent:", node.parent.name)
        print("Full Parent Text:", repr(node.parent.text))
