import requests
import re

queries = [
    "site:news.samsung.com/in SM-S906E Galaxy S22+",
    "site:news.samsung.com/in Galaxy S22 Plus SM-S906",
    "site:samsung.com SM-S906E Galaxy S22 Plus"
]

headers = {"User-Agent": "Mozilla/5.0"}

for query in queries:
    print("=" * 80)
    print("QUERY:", query)
    print()

    # Bing HTML search
    search_url = "https://www.google.com/search?q=" + requests.utils.quote(query)

    try:
        r = requests.get(search_url, headers=headers, timeout=30)
        print("Search HTTP:", r.status_code)

        urls = re.findall(
            r'https?://[^"\'<>\s]+',
            r.text
        )

        seen = set()

        for url in urls:
            url = url.replace("\\/", "/")

            if (
                "samsung.com" in url.lower()
                and url not in seen
            ):
                seen.add(url)
                print(url)

    except Exception as e:
        print("ERROR:", e)

    print()
