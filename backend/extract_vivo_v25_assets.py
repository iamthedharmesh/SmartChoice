import requests
import re
from urllib.parse import unquote

url = "https://www.vivo.com/in/products/v25"

headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

found = []

for item in re.findall(r'https?://[^"\'<>\s]+', r.text):
    item = unquote(item).replace("\\/", "/").rstrip('",\'')

    low = item.lower()

    if (
        any(x in low for x in ["vivo.com", "vivofs"])
        and any(x in low for x in [
            ".jpg", ".jpeg", ".png", ".webp"
        ])
    ):
        if item not in found:
            found.append(item)

print("Vivo image assets:", len(found))
print()

for i, item in enumerate(found[:100], 1):
    print(f"[{i}] {item}")
