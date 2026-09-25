import requests
from pathlib import Path

images = {
    "nothing_black":
        "https://cdn.shopify.com/s/files/1/0586/3270/0077/products/phone1black1600x2160.png?v=1658472623",

    "nothing_white":
        "https://cdn.shopify.com/s/files/1/0586/3270/0077/products/phone1white1600x2160.png?v=1658472623"
}

folder = Path(r".\data\image-check\batch6\Nothing_Phone_1")
folder.mkdir(parents=True, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

for name, url in images.items():

    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()

        path = folder / f"{name}.png"
        path.write_bytes(r.content)

        print("Downloaded:", path)
        print("Size:", len(r.content), "bytes")
        print("Content-Type:", r.headers.get("Content-Type"))

    except Exception as e:
        print("ERROR:", name, e)

print()
print("NOTHING PHONE 1 CANDIDATES DOWNLOADED")
