import pandas as pd

df = pd.read_csv(r".\data\phones_enriched.csv")

missing = df[
    df["official_image_url"].isna() |
    (df["official_image_url"].astype(str).str.strip() == "")
]

print("Missing official images:", len(missing))
print()

print(
    missing.groupby("canonical_name")
    .size()
    .reset_index(name="Count")
    .to_string(index=False)
)
