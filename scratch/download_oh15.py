import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}
resp = requests.get('https://www.brownells.com/guns/rifles/semi-auto-rifles/oh-15-300-blackout-semi-auto-rifle/', headers=headers)
with open('oh15.html', 'w', encoding='utf-8') as f:
    f.write(resp.text)
print("Saved oh15.html")
