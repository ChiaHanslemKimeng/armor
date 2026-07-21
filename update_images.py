import re

def update_images(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # Create mapping of URL to local image
    urls = re.findall(r'https://images.unsplash.com/photo-[a-z0-9\-]+\?q=80&w=1200', text)
    
    # Let's map sequentially to our 5 images
    local_images = [
        '{% static "images/news/tactical_gear.png" %}',
        '{% static "images/news/rifle_scope.png" %}',
        '{% static "images/news/shooting_range.png" %}',
        '{% static "images/news/gunsmithing_workbench.png" %}',
        '{% static "images/news/hunter_dawn.png" %}',
    ]
    
    for i, url in enumerate(urls):
        local_img = local_images[i % len(local_images)]
        # Replace only one occurrence at a time to cycle through them
        text = text.replace(url, local_img, 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f'Updated images in {filepath}')

update_images(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\trigger_times.html')
update_images(r'c:\Users\HANSLEM_KIMENG\Desktop\WEB\Armor\templates\catalog\home.html')

print('Images updated.')
