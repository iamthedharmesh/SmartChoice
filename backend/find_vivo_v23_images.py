import requests
import re
from urllib.parse import urljoin

url = "https://www.vivo.com/in/products/v23"

headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers, timeout=30)

print("HTTP:", r.status_code)
print("Page size:", len(r.text))

if r.status_code == 200:
    html = r.text

    found = []

    for item in re.findall(r'https?://[^"\'<>\s]+', html):
        item = item.replace("\\/", "/")

        low = item.lower()

        if (
            "vivo" in low
            and any(x in low for x in [
                "v23", "v23-5g", "v23_5g"
            ])
            and any(x in low for x in [
                ".jpg", ".jpeg", ".png", ".webp"
            ])
        ):
            if item not in found:
                found.append(item)

    print("V23-specific image candidates:", len(found))

    for i, item in enumerate(found[:50], 1):
        print(f"[{i}] {item}")
else:
    print("Official V23 page could not be fetched.")
