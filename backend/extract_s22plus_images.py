from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import re

folder = Path(r".\data\image-check\batch6\Samsung_Galaxy_S22_Plus_5G")
page = folder / "s22_plus_product_page.html"

html = page.read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")

seen = set()
results = []

# Images from HTML tags
for img in soup.find_all("img"):

    values = [
        img.get("src"),
        img.get("data-src"),
        img.get("data-original"),
        img.get("data-lazy-src"),
        img.get("data-image"),
        img.get("data-srcset")
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
            "https://www.samsung.com/ba/",
            value
        )

        value = value.replace("\\/", "/")

        if value in seen:
            continue

        seen.add(value)

        low = value.lower()

        if any(x in low for x in [
            "logo",
            "icon",
            "favicon",
            "sprite",
            "placeholder",
            "loader",
            "tracking"
        ]):
            continue

        if re.search(r"\.(jpg|jpeg|png|webp)(\?|$)", low):
            results.append(value)

# Search raw HTML for Samsung image URLs
patterns = [
    r'https?://[^"\'\s<>]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]*)?',
    r'//[^"\'\s<>]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]*)?'
]

for pattern in patterns:

    for match in re.findall(pattern, html, flags=re.I):

        value = match

        if value.startswith("//"):
            value = "https:" + value

        value = value.replace("\\/", "/")

        if value in seen:
            continue

        seen.add(value)

        low = value.lower()

        if any(x in low for x in [
            "logo",
            "icon",
            "favicon",
            "sprite",
            "placeholder",
            "loader",
            "tracking"
        ]):
            continue

        results.append(value)

print("=" * 80)
print("Samsung Galaxy S22 Plus 5G")
print("Image candidates:", len(results))

for i, url in enumerate(results[:80], 1):
    print(f"[{i}] {url}")

print()
print("S22+ IMAGE EXTRACTION COMPLETE")
