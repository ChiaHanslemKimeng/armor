with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

header_start = content.find('<header class="header-main-bar')
header_end = content.find('</header>') + 9
print(content[header_start:header_end])
