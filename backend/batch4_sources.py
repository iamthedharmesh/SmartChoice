import requests
from pathlib import Path

urls = {
    "Google_Pixel_6_Pro": "https://blog.google/products-and-platforms/devices/pixel/meet-pixel-6-pixel-6-pro/",
    "LG_Wing_5G": "https://www.lg.com/us/mobile-phones/wing-5g"
}

root = Path(r".\data\image-check\batch4")
root.mkdir(parents=True, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

for name, url in urls.items():

    folder = root / name
    folder.mkdir(exist_ok=True)

    print("=" * 70)
    print(name)
    print(url)

    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()

        output = folder / "source_page.html"
        output.write_text(r.text, encoding="utf-8")

        print("Downloaded:", output)

    except Exception as e:
        print("ERROR:", e)

print()
print("BATCH 4 SOURCE PAGES COMPLETE")
