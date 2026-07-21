import re

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/catalog/trigger_times.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Section class
content = content.replace('<section class="container py-4 my-3 text-white">', '<section class="container py-4 my-3 text-dark">')

# 2. Schools
content = content.replace('class="bg-warning text-white text-center py-2 fw-bold font-monospace small"', 'class="bg-warning text-dark text-center py-2 fw-bold font-monospace small"')
content = content.replace('<h1 class="font-outfit fw-bold text-white" style="font-size: 3rem;">Gunsmithing Schools</h1>', '<h1 class="font-outfit fw-bold text-dark" style="font-size: 3rem;">Gunsmithing Schools</h1>')
content = content.replace('<div class="content-article mx-auto text-white"', '<div class="content-article mx-auto text-dark"')

# 3. Preparedness
content = content.replace('<h1 class="font-outfit fw-bold text-white" style="font-size: 3rem;">Emergency Preparedness 101</h1>', '<h1 class="font-outfit fw-bold text-dark" style="font-size: 3rem;">Emergency Preparedness 101</h1>')

# 4. Sharing links
content = content.replace('class="text-white text-decoration-none text-center"', 'class="text-dark text-decoration-none text-center"')

# 5. Sports Month
content = content.replace('<h2 class="font-outfit fw-bold text-white">Shooting Sports Month</h2>', '<h2 class="font-outfit fw-bold text-dark">Shooting Sports Month</h2>')
content = content.replace('<h2 class="font-outfit fw-bold text-white" style="font-size: 2.5rem;">Trigger Feed</h2>', '<h2 class="font-outfit fw-bold text-dark" style="font-size: 2.5rem;">Trigger Feed</h2>')

# 6. Sunday Gunday
content = content.replace('<h1 class="font-outfit fw-bold text-white" style="font-size: 3rem;">SUNDAY GUNDAY</h1>', '<h1 class="font-outfit fw-bold text-dark" style="font-size: 3rem;">SUNDAY GUNDAY</h1>')

# 7. Fallback cards
content = content.replace('bg-dark text-white', 'bg-white text-dark')
content = content.replace('<h4 class="font-outfit fw-bold text-white mb-2">', '<h4 class="font-outfit fw-bold text-dark mb-2">')

# Spacing fixes
# Schools image spacing
content = re.sub(r'<!-- SCHOOLS CONTENT -->\s*<div class="mb-4">', r'<!-- SCHOOLS CONTENT -->\n    <div class="mb-2">', content)
content = re.sub(r'</div>\s*<div class="text-center mb-5">\s*<h1 class="font-outfit fw-bold text-dark" style="font-size: 3rem;">Gunsmithing Schools</h1>', r'</div>\n    <div class="text-center mb-3">\n        <h1 class="font-outfit fw-bold text-dark" style="font-size: 3rem;">Gunsmithing Schools</h1>', content)

# Preparedness image spacing
content = re.sub(r'<!-- PREPAREDNESS CONTENT -->\s*<div class="mb-4">', r'<!-- PREPAREDNESS CONTENT -->\n    <div class="mb-2">', content)
content = re.sub(r'</div>\s*<div class="text-center mb-5">\s*<h1 class="font-outfit fw-bold text-dark" style="font-size: 3rem;">Emergency Preparedness 101</h1>', r'</div>\n    <div class="text-center mb-3">\n        <h1 class="font-outfit fw-bold text-dark" style="font-size: 3rem;">Emergency Preparedness 101</h1>', content)

# Sports Month image spacing
content = re.sub(r'<!-- FEED LAYOUT \(SPORTS MONTH / SUNDAY GUNDAY / NEWS\) -->\s*{% if request.GET.cat == \'sports-month\' %}\s*<div class="mb-5">', r'<!-- FEED LAYOUT (SPORTS MONTH / SUNDAY GUNDAY / NEWS) -->\n    \n    {% if request.GET.cat == \'sports-month\' %}\n    <div class="mb-2">', content)

# Sunday Gunday spacing
content = content.replace('<div class="text-center mb-5 mt-4">', '<div class="text-center mb-3 mt-4">')

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/catalog/trigger_times.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated trigger_times.html")
