import re

with open(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\trigger_times.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Close the inner if block right before {% elif request.GET.cat == 'adventure' %}
target_elif = "{% elif request.GET.cat == 'adventure' %}"
if target_elif in text:
    # insert {% endif %} before it
    text = text.replace(target_elif, "{% endif %}\n\n    " + target_elif)

# 2. Remove the extra {% endif %} at the very end.
# Look for "{% endif %}</section>" and replace with "</section>"
target_end = "{% endif %}</section>"
if target_end in text:
    # Replace ONLY the last occurrence if there are multiple, but there should only be one at the end.
    text = text.replace(target_end, "</section>")

with open(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\trigger_times.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("trigger_times.html syntax fixed!")
