import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

urls = [
    "https://www.tecno-mobile.com/in/phones/product-detail/product/phantom-x2-pro/",
    "https://www.tecno-mobile.com/phones/product-detail/product/phantom-x2-pro/"
]

headers = {"User-Agent": "Mozilla/5.0"}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=30)

        print("=" * 80)
        print(r.status_code, url)

        if r.status_code != 200:
            continue

        soup = BeautifulSoup(r.text, "html.parser")

        found = []

        for tag in soup.find_all(["img", "source"]):
            for attr in ["src", "srcset", "data-src", "data-srcset"]:
                value = tag.get(attr)

                if not value:
                    continue

                for item in value.split(","):
                    item = item.strip().split(" ")[0]

                    if item.startswith("//"):
                        item = "https:" + item
                    elif item.startswith("/"):
                        item = urljoin(url, item)

                    if (
                        item.startswith("http")
                        and item not in found
                        and any(x in item.lower() for x in [
                            "phantom", "x2", "pro"
                        ])
                    ):
                        found.append(item)

        print("Phantom X2 Pro candidates:", len(found))

        for i, item in enumerate(found[:50], 1):
            print(f"[{i}] {item}")

        if found:
            break

    except Exception as e:
        print("ERROR:", e)
