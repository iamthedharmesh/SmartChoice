from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import re

root = Path(r".\data\image-check\batch5")

for folder in sorted(root.iterdir()):

    if not folder.is_dir():
        continue

    page = folder / "product_page.html"

    if not page.exists():
        continue

    print()
    print("=" * 80)
    print(folder.name)

    html = page.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    seen = set()
    results = []

    base = "https://www.motorola.in/"

    # Collect image URLs from HTML attributes
    for img in soup.find_all("img"):

        values = [
            img.get("src"),
            img.get("data-src"),
            img.get("data-original"),
            img.get("data-lazy-src"),
            img.get("data-image")
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

            value = urljoin(base, value)

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
                "banner"
            ]):
                continue

            if re.search(r"\.(jpg|jpeg|png|webp)(\?|$)", low):
                results.append(value)

    # Also search raw HTML for image URLs
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
                "loader"
            ]):
                continue

            results.append(value)

    print("Image candidates:", len(results))

    for i, url in enumerate(results[:50], 1):
        print(f"[{i}] {url}")

print()
print("MOTOROLA IMAGE EXTRACTION COMPLETE")
