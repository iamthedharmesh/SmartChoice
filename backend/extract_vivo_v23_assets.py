import requests
import re
from urllib.parse import urljoin, unquote

url = "https://www.vivo.com/in/products/v23"

headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

html = r.text

found = []

# Absolute URLs
for item in re.findall(r'https?://[^"\'<>\s]+', html):
    item = unquote(item)
    item = item.replace("\\/", "/").rstrip('",\'')

    if item not in found:
        found.append(item)

# Protocol-relative URLs
for item in re.findall(r'//[^"\'<>\s]+', html):
    item = unquote(item)
    item = "https:" + item
    item = item.replace("\\/", "/").rstrip('",\'')

    if item not in found:
        found.append(item)

candidates = []

for item in found:
    low = item.lower()

    if (
        any(x in low for x in [
            "vivo.com",
            "vivofs",
            "vivo"
        ])
        and any(x in low for x in [
            ".jpg", ".jpeg", ".png", ".webp"
        ])
    ):
        if item not in candidates:
            candidates.append(item)

print("vivo image assets:", len(candidates))
print()

for i, item in enumerate(candidates[:150], 1):
    print(f"[{i}] {item}")
