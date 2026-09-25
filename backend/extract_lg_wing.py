from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import re

page = Path(r".\data\image-check\batch4\LG_Wing_5G\official_page.html")
html = page.read_text(encoding="utf-8")

soup = BeautifulSoup(html, "html.parser")

seen = set()
results = []

for img in soup.find_all("img"):

    for attr in ["src", "data-src", "data-original", "data-lazy-src"]:

        value = img.get(attr)

        if not value:
            continue

        value = urljoin(
            "https://www.lg.com/nl/lg-mobile-phones/smartphones/wing-5g-aurora-grey/",
            value
        )

        if value in seen:
            continue

        seen.add(value)

        low = value.lower()

        if any(x in low for x in [
            "logo",
            "icon",
            "favicon",
            "sprite",
            "placeholder"
        ]):
            continue

        if re.search(r"\.(jpg|jpeg|png|webp)(\?|$)", low):
            results.append(value)

print("LG Wing image candidates:")
print()

for i, url in enumerate(results[:20], 1):
    print(f"[{i}] {url}")
