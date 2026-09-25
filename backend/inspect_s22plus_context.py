from pathlib import Path
import re
from urllib.parse import unquote

page = Path(
    r".\data\image-check\batch6\Samsung_Galaxy_S22_Plus_5G\s22_plus_product_page.html"
)

html = unquote(page.read_text(encoding="utf-8")).replace("\\/", "/")

# Find occurrences of S22-related text and print nearby HTML.
patterns = [
    "Galaxy S22+",
    "Galaxy S22 Plus",
    "SM-S906",
    "S22 Plus",
    "S22+"
]

for pattern in patterns:

    print()
    print("=" * 80)
    print("SEARCH:", pattern)

    matches = list(re.finditer(re.escape(pattern), html, flags=re.I))

    print("Occurrences:", len(matches))

    for i, match in enumerate(matches[:10], 1):

        start = max(0, match.start() - 1500)
        end = min(len(html), match.end() + 2500)

        snippet = html[start:end]

        # Extract image URLs from this local section
        urls = re.findall(
            r'https?://[^"\'\s<>]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]*)?',
            snippet,
            flags=re.I
        )

        print()
        print(f"Occurrence {i}:")
        print("Image URLs found:", len(urls))

        seen = set()

        for url in urls:
            url = url.replace("&amp;", "&")

            if url in seen:
                continue

            seen.add(url)

            low = url.lower()

            if any(x in low for x in [
                "logo",
                "icon",
                "gnb",
                "menu",
                "banner"
            ]):
                continue

            print(" ", url)

print()
print("S22+ CONTEXT SEARCH COMPLETE")
