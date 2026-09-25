import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://blog.google/products-and-platforms/devices/pixel/meet-pixel-6-pixel-6-pro/"

headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

print("Searching official Google page for Pixel 6 Pro-specific assets...")
print()

found = []

for tag in soup.find_all(["img", "source"]):
    for attr in ["src", "srcset", "data-src", "data-srcset"]:
        value = tag.get(attr)
        if not value:
            continue

        if "pixel" in value.lower() or "pxl" in value.lower():
            for item in value.split(","):
                item = item.strip().split(" ")[0]
                if item.startswith("http"):
                    if item not in found:
                        found.append(item)

for i, item in enumerate(found, 1):
    print(f"[{i}] {item}")

print()
print(f"Found {len(found)} Pixel-related assets.")
