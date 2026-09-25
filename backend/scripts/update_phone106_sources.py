from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES = BASE_DIR / "data" / "phone_enrichment_sources.csv"

PHONE_ID = 106

new_sources = [
    {
        "phone_id": 106,
        "canonical_name": "Xiaomi 13 Pro 5G",
        "source_type": "Official Xiaomi India specifications",
        "source_url": "https://www.mi.com/in/product/xiaomi-13-pro-5g/",
        "match_confidence": 1.0,
        "notes": "Primary source for India specifications including display, cameras, charging, physical specifications, connectivity, OS launch, colors and product identity."
    },
    {
        "phone_id": 106,
        "canonical_name": "Xiaomi 13 Pro 5G",
        "source_type": "Official Xiaomi UK specifications",
        "source_url": "https://www.mi.com/uk/product/xiaomi-13-pro/specs/",
        "match_confidence": 0.95,
        "notes": "Used for model/connectivity cross-check including SIM configuration, 5G bands and USB specification."
    },
    {
        "phone_id": 106,
        "canonical_name": "Xiaomi 13 Pro 5G",
        "source_type": "GSMArena",
        "source_url": "https://www.gsmarena.com/xiaomi_13_pro-11962.php",
        "match_confidence": 0.95,
        "notes": "Secondary source for global release date, model identifiers, battery chemistry, removable battery and audio jack."
    },
    {
        "phone_id": 106,
        "canonical_name": "Xiaomi 13 Pro 5G",
        "source_type": "Gadgets360",
        "source_url": "https://www.gadgets360.com/mobiles/news/xiaomi-13-pro-price-in-india-rs-79999-sale-date-march-6-10-3821337",
        "match_confidence": 1.0,
        "notes": "India launch information, general sale date and official launch price."
    },
    {
        "phone_id": 106,
        "canonical_name": "Xiaomi 13 Pro 5G",
        "source_type": "Xiaomi firmware tracker",
        "source_url": "https://ximitime.com/hyperos/nuwa/",
        "match_confidence": 0.95,
        "notes": "Used to cross-check current India firmware: HyperOS 3.1 / Android 16."
    },
    {
        "phone_id": 106,
        "canonical_name": "Xiaomi 13 Pro 5G",
        "source_type": "Xiaomi firmware tracker",
        "source_url": "https://miuidownloader.com/hyperos/nuwa",
        "match_confidence": 0.95,
        "notes": "Secondary firmware cross-check for HyperOS 3.1 / Android 16."
    },
    {
        "phone_id": 106,
        "canonical_name": "Xiaomi 13 Pro 5G",
        "source_type": "91mobiles",
        "source_url": "https://www.91mobiles.com/xiaomi-13-pro-price-in-india",
        "match_confidence": 0.85,
        "notes": "Secondary reference for India pricing history and update-policy research. Current price observation was not used as current verified price."
    },
]

df = pd.read_csv(SOURCES, dtype=str)

existing_keys = set(
    zip(
        df["phone_id"].astype(str),
        df["source_url"].astype(str)
    )
)

rows_to_add = []

for source in new_sources:
    key = (str(source["phone_id"]), str(source["source_url"]))

    if key not in existing_keys:
        rows_to_add.append(source)

if rows_to_add:
    df = pd.concat(
        [df, pd.DataFrame(rows_to_add)],
        ignore_index=True
    )

df.to_csv(SOURCES, index=False)

phone = df[df["phone_id"].astype(str) == str(PHONE_ID)]

print("Phone 106 source audit updated successfully.")
print(f"Source count: {len(phone)}")
print()

print(
    phone[
        [
            "phone_id",
            "canonical_name",
            "source_type",
            "source_url",
            "match_confidence"
        ]
    ].to_string(index=False)
)