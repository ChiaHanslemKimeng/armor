import re

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/catalog/home.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the card container
content = content.replace(
    '<div class="glass-card p-0 h-100 d-flex flex-column border shadow-sm transition-all hover-glass bg-dark text-white rounded-4 overflow-hidden" style="border-color: #334155 !important;">',
    '<div class="glass-card p-0 h-100 d-flex flex-column border shadow-sm transition-all hover-glass bg-white text-dark rounded-4 overflow-hidden">'
)

# Replace the h5
content = content.replace(
    '<h5 class="font-outfit fw-bold text-white mb-2 line-clamp-2" style="line-height: 1.4; min-height: 2.8em; color: #ffffff !important;">',
    '<h5 class="font-outfit fw-bold text-dark mb-2 line-clamp-2" style="line-height: 1.4; min-height: 2.8em;">'
)

# Replace the p
content = content.replace(
    '<p class="small text-secondary mb-3 line-clamp-3" style="line-height: 1.5; color: #cbd5e1 !important;">',
    '<p class="small text-secondary mb-3 line-clamp-3" style="line-height: 1.5;">'
)

# Replace the border-top
content = content.replace(
    '<div class="d-flex justify-content-between align-items-center mt-auto border-top pt-3" style="border-color: rgba(255,255,255,0.1) !important;">',
    '<div class="d-flex justify-content-between align-items-center mt-auto border-top pt-3">'
)

# Replace the small
content = content.replace(
    '<small class="text-secondary font-monospace" style="color: #94a3b8 !important;">',
    '<small class="text-secondary font-monospace">'
)

with open('c:/Users/HANSLEM_KIMENG/Desktop/WEB/Armor/templates/catalog/home.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated home.html")
