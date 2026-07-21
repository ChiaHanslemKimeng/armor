filepath = r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\trigger_times.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace "{% endif %}</section>" with "</section>" since there is already an {% endif %} before it.
text = text.replace("{% endif %}</section>", "</section>")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print("Removed extra endif at section close.")
