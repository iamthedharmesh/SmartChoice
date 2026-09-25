from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import re

root = Path(r".\data\image-check\batch5")

for folder in sorted(root.iterdir()):

    if not folder.is_dir():
        continue

    page = folder / "official_page.html"

    if not page.exists():
        continue

    print()
    print("=" * 70)
    print(folder.name)

    html = page.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")

    seen = set()
    results = []

    base = "https://en-in.support.motorola.com/"

    for img in soup.find_all("img"):

        values = [
            img.get("src"),
            img.get("data-src"),
            img.get("data-original"),
            img.get("data-lazy-src")
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
                "placeholder"
            ]):
                continue

            if re.search(r"\.(jpg|jpeg|png|webp)(\?|$)", low):
                results.append(value)

    print("Image candidates:", len(results))

    for i, url in enumerate(results[:20], 1):
        print(f"[{i}] {url}")
