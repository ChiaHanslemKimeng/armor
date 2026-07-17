import urllib.request

urls = [
    ('springfield_1', 'https://www.springfield-armory.com/wp-content/uploads/2021/10/ST916556BMLC-1.jpg'),
    ('springfield_2', 'https://www.springfield-armory.com/wp-content/uploads/2021/10/ST916556BMLC-2.jpg'),
    ('geissele_1', 'https://media.geissele.com/files/products/SD-MOD1-DDC-H.jpg'),
    ('geissele_2', 'https://geissele.com/media/catalog/product/s/d/sd-mod1-ddc-1.jpg'),
    ('daniel_1', 'https://danieldefense.com/media/catalog/product/d/d/dd5-v4-blk-1.jpg'),
    ('sigsauer_1', 'https://www.sigsauer.com/media/catalog/product/m/c/mcx-spear-4.jpg'),
    ('colt_1', 'https://www.colt.com/Colt_Backend/media/productImages/Rifles/LE6920-OEM1/LE6920-OEM1-1.jpg'),
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for name, url in urls:
    try:
        req = urllib.request.Request(url, headers=headers)
        r = urllib.request.urlopen(req, timeout=8)
        ct = r.headers.get('Content-Type', 'unknown')
        cl = r.headers.get('Content-Length', 'unknown')
        print(f'OK [{name}] {ct} {cl}b -> {url}')
    except Exception as e:
        print(f'FAIL [{name}] {e}')
