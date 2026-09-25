import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = "https://www.oneplus.com/us/10-pro"

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(url, headers=headers, timeout=30)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

seen = set()

for img in soup.find_all("img"):

    src = (
        img.get("src")
        or img.get("data-src")
        or img.get("data-original")
        or img.get("data-lazy-src")
    )

    if not src:
        continue

    src = urljoin(url, src)

    if src in seen:
        continue

    seen.add(src)

    low = src.lower()

    if any(x in low for x in [
        "logo",
        "icon",
        "favicon",
        "sprite",
        "placeholder"
    ]):
        continue

    if any(x in low for x in [
        "10-pro",
        "10_pro",
        "10pro"
    ]):
        print(src)
