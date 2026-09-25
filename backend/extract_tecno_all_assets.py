import requests
import re
from urllib.parse import unquote

url = "https://www.tecno-mobile.com/in/phones/product-detail/product/phantom-x2-pro/"

headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

html = r.text

print("Page HTTP:", r.status_code)
print("Page size:", len(html))
print()

# Find all CloudFront image URLs in the page
matches = re.findall(
    r'https?://d13pvy8xd75yde\.cloudfront\.net/[^"\'<>\s]+',
    html
)

found = []

for item in matches:
    item = unquote(item)
    item = item.replace("\\/", "/")

    # Remove common trailing HTML/JSON characters
    item = item.rstrip('",\'')

    if item not in found:
        found.append(item)

print("CloudFront assets found:", len(found))
print()

for i, item in enumerate(found, 1):
    print(f"[{i}] {item}")
