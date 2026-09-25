from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES = BASE_DIR / "data" / "phone_enrichment_sources.csv"

PHONE_ID = 8

new_sources = [
    {
        "phone_id": 8,
        "canonical_name": "Xiaomi Redmi Note 12 Pro Plus 5G",
        "source_type": "Official Xiaomi India specifications",
        "source_url": "https://www.mi.com/in/product/redmi-note-12-pro-plus-5g/",
        "match_confidence": 1.0,
        "notes": "Primary source for India product specifications including display, camera, charging, physical specifications, colors and product identity."
    },
    {
        "phone_id": 8,
        "canonical_name": "Xiaomi Redmi Note 12 Pro Plus 5G",
        "source_type": "Official Xiaomi India specifications",
        "source_url": "https://www.mi.com/in/product/redmi-note-12-pro-plus-5g/specs/",
        "match_confidence": 1.0,
        "notes": "Official India specification source for connectivity, India 5G bands and update policy."
    },
    {
        "phone_id": 8,
        "canonical_name": "Xiaomi Redmi Note 12 Pro Plus 5G",
        "source_type": "Official Xiaomi India FAQ",
        "source_url": "https://www.mi.com/in/product/redmi-note-12-pro-plus-5g/faq/",
        "match_confidence": 1.0,
        "notes": "Official source for Gorilla Glass 5, Super OIS, headphone jack and launch software information."
    },
    {
        "phone_id": 8,
        "canonical_name": "Xiaomi Redmi Note 12 Pro Plus 5G",
        "source_type": "Official Xiaomi UK specifications",
        "source_url": "https://www.mi.com/uk/product/redmi-note-12-pro-plus-5g/specs/",
        "match_confidence": 0.95,
        "notes": "Secondary official Xiaomi source for display, camera, connectivity, dimensions, weight and video specifications."
    },
    {
        "phone_id": 8,
        "canonical_name": "Xiaomi Redmi Note 12 Pro Plus 5G",
        "source_type": "GSMArena",
        "source_url": "https://www.gsmarena.com/xiaomi_redmi_note_12_pro+-11954.php",
        "match_confidence": 0.9,
        "notes": "Secondary source for global release date, model identifiers, battery chemistry and non-removable battery."
    },
    {
        "phone_id": 8,
        "canonical_name": "Xiaomi Redmi Note 12 Pro Plus 5G",
        "source_type": "Indian Express",
        "source_url": "https://indianexpress.com/article/technology/tech-news-technology/xiaomi-redmi-note-12-redmi-note-12-pro-5g-launch-live-updates-8362228/",
        "match_confidence": 1.0,
        "notes": "India launch date and historical launch pricing."
    },
    {
        "phone_id": 8,
        "canonical_name": "Xiaomi Redmi Note 12 Pro Plus 5G",
        "source_type": "Firmware tracker",
        "source_url": "https://xmfirmwareupdater.com/archive/hyperos/ruby/",
        "match_confidence": 0.9,
        "notes": "Used to cross-check India firmware and current HyperOS 2 / Android 14 status."
    },
    {
        "phone_id": 8,
        "canonical_name": "Xiaomi Redmi Note 12 Pro Plus 5G",
        "source_type": "91mobiles",
        "source_url": "https://www.91mobiles.com/xiaomi-redmi-note-12-pro-plus-5g-price-in-india",
        "match_confidence": 0.8,
        "notes": "Secondary reference for historical pricing and software-update information. Current price was not stored as verified."
    },
    {
        "phone_id": 8,
        "canonical_name": "Xiaomi Redmi Note 12 Pro Plus 5G",
        "source_type": "Gadgets360",
        "source_url": "https://www.gadgets360.com/redmi-note-12-pro-plus-price-in-india-107931",
        "match_confidence": 0.85,
        "notes": "Secondary reference for historical price and charging details. Historical price was not stored as current."
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

print("Phone 8 source audit updated successfully.")
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