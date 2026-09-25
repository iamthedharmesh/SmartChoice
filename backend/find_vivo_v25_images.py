import requests
import re
from urllib.parse import unquote

url = "https://www.vivo.com/in/products/v25"

headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers, timeout=30)

print("HTTP:", r.status_code)
print("Page size:", len(r.text))

if r.status_code == 200:
    found = []

    for item in re.findall(r'https?://[^"\'<>\s]+', r.text):
        item = unquote(item).replace("\\/", "/").rstrip('",\'')

        low = item.lower()

        if (
            any(x in low for x in ["vivo.com", "vivofs"])
            and any(x in low for x in [
                "v25", "v25-5g", "v25_5g"
            ])
            and any(x in low for x in [
                ".jpg", ".jpeg", ".png", ".webp"
            ])
        ):
            if item not in found:
                found.append(item)

    print("V25-specific image candidates:", len(found))

    for i, item in enumerate(found, 1):
        print(f"[{i}] {item}")
