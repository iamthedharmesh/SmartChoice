import requests
import re
from urllib.parse import unquote, urljoin

urls = [
    "https://www.ztedevices.com/en/products/smartphones/axon-40-ultra/",
    "https://www.zte.com.cn/global/products/handsets/axon40-ultra"
]

headers = {"User-Agent": "Mozilla/5.0"}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=30)

        print("=" * 80)
        print("HTTP:", r.status_code, url)
        print("Page size:", len(r.text))

        if r.status_code != 200:
            continue

        found = []

        for item in re.findall(r'https?://[^"\'<>\s]+', r.text):
            item = unquote(item).replace("\\/", "/").rstrip('",\'')

            low = item.lower()

            if (
                any(x in low for x in [
                    ".jpg", ".jpeg", ".png", ".webp"
                ])
                and any(x in low for x in [
                    "axon", "40ultra", "40-ultra", "zte"
                ])
            ):
                if item not in found:
                    found.append(item)

        print("Potential Axon 40 Ultra assets:", len(found))

        for i, item in enumerate(found[:100], 1):
            print(f"[{i}] {item}")

        if found:
            break

    except Exception as e:
        print("ERROR:", e)
