with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(r"\'images/glocks_and_armor_logo.png\'", r"'images/glocks_and_armor_logo.png'")

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed base.html')
