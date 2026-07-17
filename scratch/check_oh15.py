from bs4 import BeautifulSoup
import re

html = open('oh15.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
desc = soup.find('div', class_='pdp-tabs__description')

if desc:
    # Try to find the manual/pdf part
    pdf_nodes = desc.find_all(string=re.compile("PDF", re.I))
    for node in pdf_nodes:
        print("FOUND PDF:", repr(node))
        p = node.parent
        print(f"Parent: {p.name}, class: {p.get('class')}")
        while p and p.name != 'div' and p != desc:
            p = p.parent
        print(f"Enclosing Div class: {p.get('class') if p else None}")

    data_nodes = desc.find_all(string=re.compile("Data", re.I))
    for node in data_nodes:
        print("FOUND Data:", repr(node))
