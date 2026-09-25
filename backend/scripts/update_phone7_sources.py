from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES = BASE_DIR / "data" / "phone_enrichment_sources.csv"

PHONE_ID = 7

new_sources = [
    {
        "phone_id": 7,
        "canonical_name": "Apple iPhone 14",
        "source_type": "Official Apple specifications",
        "source_url": "https://support.apple.com/en-us/111850",
        "match_confidence": 1.0,
        "notes": "Official iPhone 14 specifications including model A2882, display, cameras, battery, connectivity and A2882 5G bands."
    },
    {
        "phone_id": 7,
        "canonical_name": "Apple iPhone 14",
        "source_type": "Official Apple launch announcement",
        "source_url": "https://www.apple.com/in/newsroom/2022/09/iphone-14-lineup-apple-watch-series-8-and-new-apple-watch-se-arrive-worldwide/",
        "match_confidence": 1.0,
        "notes": "Official Apple India launch information; iPhone 14 availability began September 16, 2022."
    },
    {
        "phone_id": 7,
        "canonical_name": "Apple iPhone 14",
        "source_type": "Official Apple iOS compatibility",
        "source_url": "https://www.apple.com/in/os/ios/",
        "match_confidence": 1.0,
        "notes": "Official Apple iOS 27 page confirms iPhone 14 compatibility with iOS 27."
    },
    {
        "phone_id": 7,
        "canonical_name": "Apple iPhone 14",
        "source_type": "GSMArena",
        "source_url": "https://www.gsmarena.com/apple_iphone_14-11861.php",
        "match_confidence": 0.95,
        "notes": "Secondary specification reference used for cross-checking model identity and specifications."
    },
    {
        "phone_id": 7,
        "canonical_name": "Apple iPhone 14",
        "source_type": "Official Apple India launch pricing",
        "source_url": "https://www.apple.com/in/newsroom/2023/03/hello-yellow-apple-introduces-new-iphone-14-and-iphone-14-plus/",
        "match_confidence": 1.0,
        "notes": "Official Apple India source confirming iPhone 14 starting price of ₹79,900."
    },
]

df = pd.read_csv(SOURCES, dtype=str)

new_df = pd.DataFrame(new_sources)

# Prevent duplicate source rows if this script is accidentally run again.
key_cols = ["phone_id", "source_url"]

existing_keys = set(
    zip(
        df["phone_id"].astype(str),
        df["source_url"].astype(str)
    )
)

rows_to_add = []

for _, row in new_df.iterrows():
    key = (str(row["phone_id"]), str(row["source_url"]))

    if key not in existing_keys:
        rows_to_add.append(row.to_dict())

if rows_to_add:
    df = pd.concat(
        [df, pd.DataFrame(rows_to_add)],
        ignore_index=True
    )

df.to_csv(SOURCES, index=False)

print("Phone 7 source audit updated successfully.")
print(f"Source file: {SOURCES}")
print()

phone7 = df[df["phone_id"].astype(str) == "7"]

print(f"Phone 7 source count: {len(phone7)}")
print()

print(
    phone7[
        [
            "phone_id",
            "canonical_name",
            "source_type",
            "source_url",
            "match_confidence"
        ]
    ].to_string(index=False)
)