import pandas as pd
from pathlib import Path

path = Path(r".\data\phones_enriched.csv")

df = pd.read_csv(path)

image_url = "https://cdn.shopify.com/s/files/1/0586/3270/0077/products/phone1black1600x2160.png?v=1658472623"

ids = [9, 206, 134]

for phone_id in ids:
    mask = df["phone_id"] == phone_id

    if not mask.any():
        print(f"ERROR: phone_id {phone_id} not found")
        continue

    df.loc[mask, "official_image_url"] = image_url
    print(f"Updated: {phone_id}")

df.to_csv(path, index=False)

print()
print("VERIFY:")
print(
    df.loc[
        df["phone_id"].isin(ids),
        ["phone_id", "canonical_name", "model_id", "official_image_url"]
    ].to_string(index=False)
)

print()
print("NOTHING PHONE 1 IMAGE UPDATE COMPLETE")
