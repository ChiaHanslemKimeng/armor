from bs4 import BeautifulSoup
import re

html = open('prod.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
desc = soup.find('div', class_='pdp-tabs__description')

if desc:
    # Print the raw text of the description to see what we're working with
    print(desc.text[:500])
    print("...")
    
    # Try to find the manual/pdf part
    pdf_nodes = desc.find_all(string=re.compile("PDF", re.I))
    for node in pdf_nodes:
        print("FOUND PDF:", repr(node))
        p = node.parent
        print(f"Parent: {p.name}, class: {p.get('class')}")
        while p and p.name != 'div' and p != desc:
            p = p.parent
        print(f"Enclosing Div class: {p.get('class') if p else None}")

    # Check for "What is the"
    what = desc.find_all(string=re.compile("What is the", re.I))
    for node in what:
        print("FOUND What:", repr(node))
        print(f"Parent: {node.parent.name}, class: {node.parent.get('class')}")

