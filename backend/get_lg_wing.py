import requests
from pathlib import Path

url = "https://www.lg.com/nl/lg-mobile-phones/smartphones/wing-5g-aurora-grey/"

folder = Path(r".\data\image-check\batch4\LG_Wing_5G")
folder.mkdir(parents=True, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

path = folder / "official_page.html"
path.write_text(r.text, encoding="utf-8")

print("Downloaded:", path)
print("Size:", len(r.text), "bytes")
