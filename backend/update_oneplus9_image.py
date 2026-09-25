import pandas as pd

path = r".\data\phones_enriched.csv"

df = pd.read_csv(path)

image_url = "https://image01-in.oneplus.net/shop/202104/27/1-M00-24-8B-rB8bwmCICVmAN0CwAAVb_9VyE6w579.png"

mask = df["phone_id"].astype(str) == "338"

if mask.sum() != 1:
    raise RuntimeError(f"Expected exactly 1 phone_id=338, found {mask.sum()}")

df.loc[mask, "official_image_url"] = image_url

df.to_csv(path, index=False)

print("Updated phone_id 338:")
print(df.loc[mask, ["phone_id", "canonical_name", "official_image_url"]].to_string(index=False))
