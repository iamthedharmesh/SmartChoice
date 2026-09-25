from pathlib import Path
import re
from urllib.parse import unquote

page = Path(
    r".\data\image-check\batch6\Samsung_Galaxy_S22_Plus_5G\s22_plus_product_page.html"
)

html = unquote(page.read_text(encoding="utf-8"))
html = html.replace("\\/", "/").replace("&amp;", "&")

# Get image-like URLs
patterns = [
    r'https?://[^"\'\s<>\\]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>\\]*)?',
    r'//[^"\'\s<>\\]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>\\]*)?'
]

all_urls = []

for pattern in patterns:
    all_urls.extend(re.findall(pattern, html, flags=re.I))

unique = []

for url in all_urls:

    if url.startswith("//"):
        url = "https:" + url

    url = url.replace("\\u002F", "/")
    url = url.replace("\\/", "/")

    if url not in unique:
        unique.append(url)

candidates = []

for match in re.finditer(r"(Galaxy S22\+|SM-S906)", html, flags=re.I):

    start = max(0, match.start() - 8000)
    end = min(len(html), match.end() + 8000)

    section = html[start:end]

    for url in unique:

        if url in section and url not in candidates:
            candidates.append(url)

print("=" * 80)
print("ALL S22+ CONTEXT IMAGE CANDIDATES")
print("Candidates:", len(candidates))
print()

for i, url in enumerate(candidates, 1):
    print(f"[{i}] {url}")

print()
print("DONE")
