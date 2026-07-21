filepath = r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\trigger_times.html'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "elif request.GET.cat == 'adventure'" in line:
        print(f'--- Context around line {i+1} ---')
        for j in range(max(0, i-3), min(len(lines), i+3)):
            print(f'{j+1}: {lines[j].strip()}')
