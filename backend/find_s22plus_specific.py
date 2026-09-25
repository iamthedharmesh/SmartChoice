from pathlib import Path
import re
from bs4 import BeautifulSoup
from urllib.parse import unquote

folder = Path(r".\data\image-check\batch6\Samsung_Galaxy_S22_Plus_5G")
page = folder / "s22_plus_product_page.html"

html = page.read_text(encoding="utf-8")
html_decoded = unquote(html).replace("\\/", "/")

patterns = [
    r'https?://[^"\'\s<>]+',
    r'//[^"\'\s<>]+'
]

seen = set()
results = []

keywords = [
    "s22-plus",
    "s22_plus",
    "s22plus",
    "s906",
    "s22%2b",
    "s22%2B",
    "s22+"
]

for pattern in patterns:

    for match in re.findall(pattern, html_decoded, flags=re.I):

        url = match

        if url.startswith("//"):
            url = "https:" + url

        url = url.replace("&amp;", "&")

        low = url.lower()

        if not any(k.lower() in low for k in keywords):
            continue

        if not re.search(r'\.(jpg|jpeg|png|webp)', low):
            continue

        if url in seen:
            continue

        seen.add(url)
        results.append(url)

print("=" * 80)
print("S22+ SPECIFIC IMAGE CANDIDATES")
print("Candidates:", len(results))

for i, url in enumerate(results, 1):
    print(f"[{i}] {url}")

print()
print("DONE")
