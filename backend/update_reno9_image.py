import pandas as pd

path = r".\data\phones_enriched.csv"

df = pd.read_csv(path)

image_url = "https://www.oppo.com/content/dam/oppo/common/mkt/v2-2/reno9-pro-plus-cn/listpage/reno9-pro-plus-list-gold.png"

mask = df["phone_id"].astype(str) == "18"

if mask.sum() != 1:
    raise RuntimeError(f"Expected exactly 1 phone_id=18, found {mask.sum()}")

df.loc[mask, "official_image_url"] = image_url

df.to_csv(path, index=False)

print("Updated phone_id 18:")
print(
    df.loc[
        mask,
        ["phone_id", "canonical_name", "model_id", "official_image_url"]
    ].to_string(index=False)
)
