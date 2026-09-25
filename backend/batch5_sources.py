import requests
from pathlib import Path

pages = {
    "Motorola_Edge_30_5G":
        "https://en-in.support.motorola.com/app/answers/detail/a_id/165533/~/reset-the-motorola-edge-30",

    "Motorola_Edge_30_Fusion_5G":
        "https://en-in.support.motorola.com/app/answers/detail/a_id/167147/~/reset-the-motorola-edge-30-fusion"
}

root = Path(r".\data\image-check\batch5")
root.mkdir(parents=True, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

for name, url in pages.items():

    folder = root / name
    folder.mkdir(exist_ok=True)

    print("=" * 70)
    print(name)
    print(url)

    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()

        path = folder / "official_page.html"
        path.write_text(r.text, encoding="utf-8")

        print("Downloaded:", path)
        print("Size:", len(r.text), "bytes")

    except Exception as e:
        print("ERROR:", e)

print()
print("BATCH 5 SOURCE PAGES COMPLETE")
