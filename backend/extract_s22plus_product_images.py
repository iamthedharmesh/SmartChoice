from pathlib import Path
import re
from urllib.parse import unquote

page = Path(
    r".\data\image-check\batch6\Samsung_Galaxy_S22_Plus_5G\s22_plus_product_page.html"
)

html = unquote(page.read_text(encoding="utf-8"))
html = html.replace("\\/", "/").replace("&amp;", "&")

# Find all image-like URLs anywhere in the page
patterns = [
    r'https?://[^"\'\s<>\\]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>\\]*)?',
    r'//[^"\'\s<>\\]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>\\]*)?'
]

all_urls = []

for pattern in patterns:
    all_urls.extend(re.findall(pattern, html, flags=re.I))

# Normalize and deduplicate
unique = []

for url in all_urls:

    if url.startswith("//"):
        url = "https:" + url

    url = url.replace("\\u002F", "/")
    url = url.replace("\\/", "/")

    if url not in unique:
        unique.append(url)

# Keep URLs close to S22+/SM-S906 references
candidates = []

for match in re.finditer(r"(Galaxy S22\+|SM-S906)", html, flags=re.I):

    start = max(0, match.start() - 8000)
    end = min(len(html), match.end() + 8000)

    section = html[start:end]

    for url in unique:

        if url in section and url not in candidates:
            candidates.append(url)

print("=" * 80)
print("SAMSUNG GALAXY S22+ PRODUCT IMAGES")
print("Candidates:", len(candidates))
print()

for i, url in enumerate(candidates, 1):

    low = url.lower()

    # Skip obvious site-wide assets
    if any(x in low for x in [
        "/gnb/",
        "logo",
        "icon",
        "favicon",
        "sprite",
        "placeholder",
        "banner"
    ]):
        continue

    print(f"[{i}] {url}")

print()
print("S22+ PRODUCT IMAGE EXTRACTION COMPLETE")
