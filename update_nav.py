import re

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace mobile logo
mobile_pattern = r'(<a class="navbar-brand d-flex align-items-center m-0" href="/">\s*<img src="{% static \'images/glocks_and_armor_logo.png\' %}" alt="Glocks And Armor" style="height: 40px; object-fit: contain;">)(\s*</a>)'
mobile_replacement = r'\1\n                        <span class="fw-bold font-outfit text-dark ms-2 fs-6 tracking-tight">Glocks And Armor</span>\2'
content = re.sub(mobile_pattern, mobile_replacement, content, count=1)

# Replace desktop logo
desktop_pattern = r'(<a class="navbar-brand d-flex align-items-center gap-3 font-outfit fw-black fs-3 text-dark tracking-tight text-decoration-none" href="/">\s*<img src="{% static \'images/glocks_and_armor_logo.png\' %}" alt="Glocks And Armor" style="height: 50px; object-fit: contain;">)(\s*</a>)'
desktop_replacement = r'\1\n                        <span class="fs-4">Glocks And Armor</span>\2'
content = re.sub(desktop_pattern, desktop_replacement, content, count=1)

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated logo text.")
