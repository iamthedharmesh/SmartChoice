import pandas as pd

path = r".\data\phones_enriched.csv"
df = pd.read_csv(path)

image_url = "https://cdn.shopify.com/s/files/1/0510/4556/4565/files/A40Ultra.png?v=1662723370"

mask = df["phone_id"] == 533
df.loc[mask, "official_image_url"] = image_url

df.to_csv(path, index=False)

row = df.loc[mask, ["phone_id", "canonical_name", "official_image_url"]]
print(row.to_string(index=False))
