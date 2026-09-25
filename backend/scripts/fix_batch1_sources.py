from pathlib import Path
import csv

BASE = Path(__file__).resolve().parents[1]
SOURCES = BASE / "data" / "phone_enrichment_sources.csv"

rows = [
    [15, "Samsung Galaxy S23 Ultra 5G", "Samsung India",
     "https://www.samsung.com/in/smartphones/galaxy-s23-ultra/", "1.0",
     "Official product page"],

    [15, "Samsung Galaxy S23 Ultra 5G", "Samsung Newsroom India",
     "https://news.samsung.com/in/samsung-galaxy-s23-ultra-launch-india", "1.0",
     "India launch information"],

    [15, "Samsung Galaxy S23 Ultra 5G", "GSMArena",
     "https://www.gsmarena.com/samsung_galaxy_s23_ultra-12254.php", "0.95",
     "Detailed hardware specifications"],

    [15, "Samsung Galaxy S23 Ultra 5G", "91mobiles",
     "https://www.91mobiles.com/index.php/samsung-galaxy-s23-ultra-5g-price-in-india", "0.85",
     "Dated 2026 market price"],

    [207, "Samsung Galaxy A54 5G", "Samsung India",
     "https://www.samsung.com/in/smartphones/galaxy-a54-5g/", "1.0",
     "Official product page"],

    [207, "Samsung Galaxy A54 5G", "Samsung Newsroom India",
     "https://news.samsung.com/in/samsung-launches-all-new-galaxy-a54-5g-and-a34-5g-with-stunning-design-and-trendy-colours", "1.0",
     "India launch information"],

    [207, "Samsung Galaxy A54 5G", "GSMArena",
     "https://www.gsmarena.com/samsung_galaxy_a54_5g-12199.php", "0.95",
     "Detailed hardware specifications"],

    [207, "Samsung Galaxy A54 5G", "Gadgets360",
     "https://www.gadgets360.com/samsung-galaxy-a54-5g-price-in-india-116239", "0.85",
     "Dated 2026 market price"],

    [153, "Apple iPhone 15 Pro Max", "Apple India",
     "https://www.apple.com/in/iphone-15-pro/specs/", "1.0",
     "Official specifications"],

    [153, "Apple iPhone 15 Pro Max", "Apple Support India",
     "https://support.apple.com/en-in/116477", "1.0",
     "Model identification"],

    [153, "Apple iPhone 15 Pro Max", "Apple Newsroom India",
     "https://www.apple.com/in/newsroom/2023/09/apple-debuts-iphone-15-pro-and-iphone-15-pro-max/", "1.0",
     "India launch information"],

    [153, "Apple iPhone 15 Pro Max", "GSMArena",
     "https://www.gsmarena.com/apple_iphone_15_pro_max-12473.php", "0.95",
     "Detailed hardware specifications"],

    [153, "Apple iPhone 15 Pro Max", "91mobiles",
     "https://www.91mobiles.com/apple-iphone-15-pro-max-price-in-india", "0.85",
     "Dated 2026 market price"],
]

with SOURCES.open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "phone_id",
        "canonical_name",
        "source_type",
        "source_url",
        "match_confidence",
        "notes",
    ])
    writer.writerows(rows)

print("Source audit fixed successfully.")
print("Rows:", len(rows))