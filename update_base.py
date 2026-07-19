import re

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Meta updates
content = re.sub(r'Glocks And Armor \| Personal Firearms', r'Glocks And Armor | Personal Firearms', content)
content = re.sub(r'"Glocks And Armor Defense"', r'"Glocks And Armor Defense"', content)
content = re.sub(r'content="Glocks And Armor"', r'content="Glocks And Armor"', content)
content = re.sub(r'"name": "Glocks And Armor"', r'"name": "Glocks And Armor"', content)
content = content.replace("{% static 'images/sniper_rifle.png' %}", "{% static 'images/glocks_and_armor_logo.png' %}")

# Header logo
content = re.sub(r'<div class="d-flex align-items-center justify-content-center rounded-3 p-2 shadow-sm" style="width:45px; height:45px; background: #0f172a; color: #ffb800; border: 2px solid #ffb800;">\s*<i class="bi bi-crosshair fs-4"></i>\s*</div>\s*<span>ARMOR<span style="color: #d97706;" class="fw-bold">SYSTEMS</span></span>', r'<img src="{% static \'images/glocks_and_armor_logo.png\' %}" alt="Glocks And Armor" style="height: 50px; object-fit: contain;">', content, count=1)

# Footer logos
content = re.sub(r'<span>ARMOR<span style="color: #ffb800;">SYSTEMS</span></span>', r'<img src="{% static \'images/glocks_and_armor_logo.png\' %}" alt="Glocks And Armor" style="height: 40px; object-fit: contain;">', content)

# Check if there's any remaining GLOCKS AND ARMOR
content = re.sub(r'Glocks And Armor', r'Glocks And Armor', content)
content = re.sub(r'GLOCKS AND ARMOR', r'GLOCKS AND ARMOR', content)

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully")
