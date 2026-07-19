with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/catalog/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<div class="col-lg-8">', '<div class="col-lg-8 text-center text-lg-start mx-auto">')

# Also, let's fix the alignment of the badge wrappers to center them on mobile
content = content.replace('<div class="d-flex flex-wrap align-items-center gap-2 mb-3">', '<div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start gap-2 mb-3">')
content = content.replace('<div class="d-flex flex-wrap gap-3 align-items-center">', '<div class="d-flex flex-wrap gap-3 align-items-center justify-content-center justify-content-lg-start">')

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/catalog/home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated home.html successfully")
