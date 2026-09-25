import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://news.samsung.com/in/new-samsung-galaxy-s22-and-s22-deliver-revolutionary-camera-experiences-day-and-night"

headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

found = []

for img in soup.find_all("img"):
    for attr in ["src", "data-src", "data-lazy-src"]:
        value = img.get(attr)

        if not value:
            continue

        if value.startswith("//"):
            value = "https:" + value
        elif value.startswith("/"):
            value = urljoin(url, value)

        if value.startswith("http") and value not in found:
            found.append(value)

print("Samsung Newsroom image assets:", len(found))
print()

for i, image in enumerate(found, 1):
    print(f"[{i}] {image}")
