from pathlib import Path
import re
from urllib.parse import unquote

page = Path(
    r".\data\image-check\batch6\Samsung_Galaxy_S22_Plus_5G\official_page.html"
)

html = unquote(page.read_text(encoding="utf-8"))
html = html.replace("\\/", "/").replace("&amp;", "&")

# Find every image URL containing Samsung's S22/S22+ naming
urls = re.findall(
    r'https?://[^"\'\s<>]+?\.(?:jpg|jpeg|png|webp)(?:\?[^"\'\s<>]*)?',
    html,
    flags=re.I
)

unique = []

for url in urls:
    if url not in unique:
        unique.append(url)

print("=" * 80)
print("SAMSUNG NEWSROOM S22 IMAGE ASSETS")
print()

for url in unique:

    low = url.lower()

    if any(x in low for x in [
        "s22",
        "s906",
        "galaxy-s"
    ]):
        print(url)

print()
print("TOTAL S22-RELATED URLS:",
      sum(
          1 for url in unique
          if any(x in url.lower() for x in ["s22", "s906", "galaxy-s"])
      ))

print()
print("DONE")
