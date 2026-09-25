import pandas as pd

csv_path = r".\data\phones_enriched.csv"

df = pd.read_csv(csv_path)

target = df["canonical_name"].astype(str).str.strip().eq("OnePlus 10 Pro 5G")

url = "https://oasis.opstatics.com/content/dam/oasis/page/press-photos/10pro/green/10pro-na-1.png"

print("Matching rows:", int(target.sum()))

df.loc[target, "official_image_url"] = url

df.to_csv(csv_path, index=False)

print("Updated rows:", int(target.sum()))
print("URL:", url)
