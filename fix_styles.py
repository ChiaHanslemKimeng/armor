import re

filepath = r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\trigger_times.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Add a style block at the very top (after block content)
style_block = """
<style>
/* Override the global !important light-mode rules for these dark cards */
.news-card-dark {
    background-color: #1e293b !important;
    border-color: #334155 !important;
    color: #cbd5e1 !important;
}
.news-card-dark h2, .news-card-dark h4 {
    color: #ffffff !important;
}
.news-card-dark p.text-secondary {
    color: #94a3b8 !important;
}
.news-card-dark .content-article p {
    color: #cbd5e1 !important;
}
</style>
"""

# Insert style block right after {% block content %}
if "{% block content %}" in text and "<style>" not in text:
    text = text.replace("{% block content %}", "{% block content %}\n" + style_block)

# Add news-card-dark class to the cards in the news section
text = text.replace('class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white"',
                    'class="card border-0 shadow-lg rounded-4 overflow-hidden bg-dark text-white news-card-dark"')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('trigger_times.html styles updated.')
