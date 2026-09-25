import requests
from pathlib import Path

url = "https://www.samsung.com/ba/smartphones/galaxy-s/galaxy-s22-plus-phantom-black-256gb-sm-s906bzkgeuc/"

folder = Path(r".\data\image-check\batch6\Samsung_Galaxy_S22_Plus_5G")
folder.mkdir(parents=True, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

print("Downloading:")
print(url)

try:
    r = requests.get(url, headers=headers, timeout=30)

    print("Status:", r.status_code)

    if r.status_code == 200:
        path = folder / "s22_plus_product_page.html"
        path.write_text(r.text, encoding="utf-8")

        print("Saved:", path)
        print("Size:", len(r.text), "bytes")
    else:
        print("Could not download page.")

except Exception as e:
    print("ERROR:", e)

print()
print("S22+ PRODUCT PAGE DOWNLOAD COMPLETE")
