from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import requests
import re

page = Path(r".\data\image-check\batch4\Google_Pixel_6_Pro\source_page.html")
html = page.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

seen = set()
candidates = []

for img in soup.find_all("img"):

    values = [
        img.get("src"),
        img.get("data-src"),
        img.get("data-original"),
        img.get("data-lazy-src"),
    ]

    srcset = img.get("srcset")
    if srcset:
        values += [
            x.strip().split(" ")[0]
            for x in srcset.split(",")
        ]

    for value in values:

        if not value:
            continue

        value = urljoin(
            "https://blog.google/products-and-platforms/devices/pixel/meet-pixel-6-pixel-6-pro/",
            value
        )

        if value in seen:
            continue

        seen.add(value)

        low = value.lower()

        if any(x in low for x in [
            "logo", "icon", "favicon", "sprite",
            "google-play", "youtube", "facebook",
            "twitter", "instagram"
        ]):
            continue

        if re.search(r"\.(jpg|jpeg|png|webp)(\?|$)", low):
            candidates.append(value)

for meta in soup.find_all("meta"):

    prop = meta.get("property") or meta.get("name")
    content = meta.get("content")

    if (
        prop
        and content
        and prop.lower() in [
            "og:image",
            "twitter:image"
        ]
    ):
        if content not in candidates:
            candidates.append(content)

print("Pixel 6 Pro image candidates:")
print()

for i, url in enumerate(candidates[:15], 1):
    print(f"[{i}] {url}")
