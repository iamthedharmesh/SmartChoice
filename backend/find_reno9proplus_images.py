import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urls = [
    "https://www.oppo.com/cn/smartphones/series-reno/reno9-pro-plus/",
    "https://www.oppo.com/cn/smartphones/series-reno/reno9-pro-plus-5g/"
]

headers = {"User-Agent": "Mozilla/5.0"}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=30)
        print(f"{r.status_code}  {url}")

        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")

            candidates = []

            for tag in soup.find_all(["img", "source"]):
                for attr in ["src", "srcset", "data-src", "data-srcset"]:
                    value = tag.get(attr)
                    if not value:
                        continue

                    for item in value.split(","):
                        item = item.strip().split(" ")[0]
                        if item.startswith("http") and item not in candidates:
                            if "reno9" in item.lower() or "reno-9" in item.lower():
                                candidates.append(item)

            print(f"Reno9-specific candidates: {len(candidates)}")
            for i, candidate in enumerate(candidates[:30], 1):
                print(f"[{i}] {candidate}")

            break

    except Exception as e:
        print("ERROR:", e)
