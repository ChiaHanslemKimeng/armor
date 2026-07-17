from bs4 import BeautifulSoup

html = open('prod.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
desc = soup.find('div', class_='pdp-tabs__description')
if desc:
    print("Is Quick Factory Specs in description?", "Quick Factory Specs" in desc.text)
else:
    print("No description.")
