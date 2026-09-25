import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urls = [
    "https://www.samsung.com/in/smartphones/galaxy-s22/",
    "https://www.samsung.com/in/smartphones/galaxy-s/galaxy-s22-plus/"
]

headers = {"User-Agent": "Mozilla/5.0"}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=30)
        print(f"{r.status_code}  {url}")

        if r.status_code != 200:
            continue

        html = r.text
        soup = BeautifulSoup(html, "html.parser")

        found = []

        # Search all HTML for SM-S906 / S22+ references
        matches = re.findall(
            r'https?://[^"\'\s<>]+',
            html
        )

        for item in matches:
            item = item.replace("\\/", "/")

            low = item.lower()

            if (
                "sm-s906" in low
                or "s22-plus" in low
                or "s22_plus" in low
                or "s22plus" in low
            ):
                if item not in found:
                    found.append(item)

        print(f"Model-specific URL candidates: {len(found)}")

        for i, item in enumerate(found[:100], 1):
            print(f"[{i}] {item}")

        print()

    except Exception as e:
        print("ERROR:", e)
