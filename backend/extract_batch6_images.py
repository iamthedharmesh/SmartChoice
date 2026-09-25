from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import re

root = Path(r".\data\image-check\batch6")

for folder in sorted(root.iterdir()):

    if not folder.is_dir():
        continue

    page = folder / "official_page.html"

    if not page.exists():
        continue

    print()
    print("=" * 80)
    print(folder.name)

    html = page.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    seen = set()
    results = []

    # Extract from image elements
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
                "https://news.samsung.com/in/"
                if "Samsung" in folder.name
                else "https://in.nothing.tech/",
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

    # Search raw HTML too
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

    print("Image candidates:", len(results))

    for i, url in enumerate(results[:50], 1):
        print(f"[{i}] {url}")

print()
print("BATCH 6 IMAGE EXTRACTION COMPLETE")
