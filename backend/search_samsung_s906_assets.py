import requests
import re

urls = [
    "https://www.samsung.com/in/support/model/SM-S906E",
    "https://www.samsung.com/in/support/model/SM-S906EZKDINU/",
    "https://www.samsung.com/in/support/model/SM-S906ELBDINU/",
]

headers = {"User-Agent": "Mozilla/5.0"}

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=30)

        print("=" * 80)
        print(r.status_code, url)

        if r.status_code != 200:
            continue

        # Look for Samsung CDN image URLs and model references
        matches = re.findall(
            r'https?://[^"\'<>\s]+',
            r.text
        )

        found = []

        for item in matches:
            item = item.replace("\\/", "/")

            low = item.lower()

            if (
                "samsung" in low
                and (
                    "sm-s906" in low
                    or "s22" in low
                    or "s906" in low
                )
                and any(
                    ext in low
                    for ext in [".jpg", ".jpeg", ".png", ".webp"]
                )
            ):
                if item not in found:
                    found.append(item)

        print("Potential model-specific images:", len(found))

        for i, item in enumerate(found[:50], 1):
            print(f"[{i}] {item}")

    except Exception as e:
        print("ERROR:", e)
