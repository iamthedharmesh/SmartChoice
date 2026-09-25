import requests
from pathlib import Path

pages = {
    "Motorola_Edge_30_5G":
        "https://www.motorola.in/smartphones-motorola-edge-30-3/p",

    "Motorola_Edge_30_Fusion_5G":
        "https://www.motorola.in/motorola-edge-30-fusion/p"
}

root = Path(r".\data\image-check\batch5")
root.mkdir(parents=True, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

for name, url in pages.items():

    folder = root / name
    folder.mkdir(exist_ok=True)

    print("=" * 70)
    print(name)
    print(url)

    try:
        r = requests.get(
            url,
            headers=headers,
            timeout=30
        )

        print("Status:", r.status_code)

        if r.status_code != 200:
            print("Could not download page.")
            continue

        path = folder / "product_page.html"
        path.write_text(r.text, encoding="utf-8")

        print("Saved:", path)
        print("Size:", len(r.text))

    except Exception as e:
        print("ERROR:", e)

print()
print("DONE")
