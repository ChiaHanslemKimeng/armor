from bs4 import BeautifulSoup

html = open('prod.html', encoding='utf-8').read()
soup = BeautifulSoup(html, 'html.parser')
desc = soup.find('div', class_='pdp-tabs__description')
if desc:
    # Find "Available options"
    avail = desc.find(string=lambda t: t and 'Available options' in t)
    if avail:
        print("Found Available options text.")
        parent = avail.parent
        print(f"Parent tag: {parent.name}, class: {parent.get('class')}")
        
        # Let's see if there is a table nearby
        table = desc.find('table')
        if table:
            print("Table found in description.")
            print(str(table)[:200])
else:
    print("No pdp-tabs__description found.")
