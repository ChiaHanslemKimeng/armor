filepath = r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\trigger_times.html'
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(r"\'adventure\'", "'adventure'")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print('Backslashes removed.')
