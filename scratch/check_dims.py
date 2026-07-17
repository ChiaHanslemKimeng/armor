import requests
from PIL import Image
from io import BytesIO

urls = [
    'https://www.brownells.com/globalassets/10000/d8/l_100034679_3.jpg',
    'https://www.brownells.com/globalassets/10000/d0/l_100034679_42.jpg',
    'https://www.brownells.com/globalassets/10000/d0/l_100034679_4.jpg',
    'https://www.brownells.com/globalassets/10000/d8/l_100034679_32.jpg'
]

for url in urls:
    try:
        resp = requests.get(url)
        img = Image.open(BytesIO(resp.content))
        print(url, img.size)
    except Exception as e:
        print(url, str(e))
