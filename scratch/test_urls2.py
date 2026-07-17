import urllib.request
import io
from PIL import Image

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

tests = [
    # Geissele Super Duty Mod1 - try multiple URL patterns
    ('GEI-1', 'https://www.geissele.com/media/catalog/product/0/3/03-326s_geissele_super_duty_semi-auto_rifle_mod1_ddc_right.jpg'),
    ('GEI-2', 'https://www.geissele.com/media/catalog/product/g/e/geissele-super-duty-mod1-1.jpg'),
    # Springfield Armory SAINT Victor V2
    ('SPR-1', 'https://www.springfield-armory.com/wp-content/uploads/2024/01/ST916556BML-1.jpg'),
    ('SPR-2', 'https://www.springfield-armory.com/wp-content/uploads/2022/05/ST916556BMLC-main.jpg'),
    # Colt M4A1
    ('COL-1', 'https://www.colt.com/Colt_Backend/media/productImages/Rifles/LE6920-OEM1/LE6920OEM1_1.jpg'),
    ('COL-2', 'https://www.colt.com/Colt_Backend/media/productImages/Rifles/M4A1-SOCOM/M4A1-SOCOM-1.jpg'),
    # Daniel Defense DD5 V4
    ('DAN-1', 'https://danieldefense.com/media/catalog/product/d/d/dd5v4_blk_1.jpg'),
    ('DAN-2', 'https://danieldefense.com/media/catalog/product/d/d/dd5-v4-7-62-nato-1.jpg'),
    # Sig MCX Spear  
    ('SIG-1', 'https://www.sigsauer.com/media/catalog/product/m/c/mcx-spear-4.jpg'),
    ('SIG-2', 'https://www.sigsauer.com/media/catalog/product/r/0/r0mcxspear-762-16b-ct-1.jpg'),
    ('SIG-3', 'https://www.sigsauer.com/media/catalog/product/m/c/mcx-spear-762-16-ct-1.jpg'),
]

for name, url in tests:
    try:
        req = urllib.request.Request(url, headers=headers)
        r = urllib.request.urlopen(req, timeout=10)
        data = r.read()
        ct = r.headers.get('Content-Type', 'unknown')
        try:
            img = Image.open(io.BytesIO(data))
            size = img.size
        except:
            size = '?'
        print(f'OK [{name}] {len(data)}b {size} -> {url}')
    except Exception as e:
        print(f'FAIL [{name}] {e}')
