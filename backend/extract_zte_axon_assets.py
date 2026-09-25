import requests
import re
from html import unescape

url = "https://www.ztedevices.com/en/products/smartphones/axon-40-ultra/"

headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

html = unescape(r.text)

# Decode common escaped slashes/quotes
html = html.replace("\\/", "/").replace('\\"', '"')

# Find ZTE official DAM assets
patterns = [
    r'https?://[^"\'<>\s]+/content/dam/zte-devices/[^"\'<>\s]+',
    r'/content/dam/zte-devices/[^"\'<>\s]+'
]

found = []

for pattern in patterns:
    for item in re.findall(pattern, html, flags=re.I):
        item = item.rstrip('",\'')
        
        if item.startswith("/"):
            item = "https://www.ztedevices.com" + item

        if item not in found:
            found.append(item)

# Keep image assets associated with Axon 40
candidates = []

for item in found:
    low = item.lower()

    if any(ext in low for ext in [
        ".jpg", ".jpeg", ".png", ".webp"
    ]):
        if any(x in low for x in [
            "axon-40",
            "axon40",
            "axon_40",
            "axon"
        ]):
            candidates.append(item)

print("ZTE Axon-related image assets:", len(candidates))
print()

for i, item in enumerate(candidates[:100], 1):
    print(f"[{i}] {item}")
