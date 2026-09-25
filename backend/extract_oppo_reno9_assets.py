import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.oppo.com/cn/smartphones/series-reno/reno9-pro-plus/"

headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

html = r.text
soup = BeautifulSoup(html, "html.parser")

found = []

# Extract URLs from HTML attributes
for tag in soup.find_all(True):
    for attr, value in tag.attrs.items():
        if not isinstance(value, str):
            continue

        if "image" in attr.lower() or attr.lower() in {
            "src", "srcset", "data-src", "data-srcset",
            "data-original", "data-lazy-src"
        }:
            for item in value.split(","):
                item = item.strip().split(" ")[0]

                if item.startswith("//"):
                    item = "https:" + item

                elif item.startswith("/"):
                    item = urljoin(url, item)

                if item.startswith("http"):
                    if item not in found:
                        found.append(item)

# Extract absolute URLs directly from raw HTML
for match in re.findall(r'https?://[^"\'\s<>]+', html):
    clean = match.replace("\\/", "/")

    if clean not in found:
        found.append(clean)

# Keep likely OPPO image/CDN assets
candidates = []

for item in found:
    low = item.lower()

    if any(x in low for x in [
        ".jpg", ".jpeg", ".png", ".webp", ".avif"
    ]):
        if any(x in low for x in [
            "oppo.com",
            "oppo-img",
            "oppo"
        ]):
            candidates.append(item)

print("OPPO image candidates:", len(candidates))
print()

for i, item in enumerate(candidates[:100], 1):
    print(f"[{i}] {item}")
