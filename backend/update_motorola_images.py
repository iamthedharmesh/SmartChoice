import pandas as pd
from pathlib import Path

path = Path(r".\data\phones_enriched.csv")

df = pd.read_csv(path)

updates = {
    86: "https://motorolain.vtexassets.com/arquivos/ids/157225/Motorola-edge-30-pdp-render-Mojito-4-31f5yjhf.png?v=637878943961030000",
    223: "https://motorolain.vtexassets.com/arquivos/ids/157225/Motorola-edge-30-pdp-render-Mojito-4-31f5yjhf.png?v=637878943961030000",
    194: "https://motorolain.vtexassets.com/arquivos/ids/157906/motorola-edge-30-fusion-pdp-ecom-render-21-barberry-5nfzuirw.png?v=638833323210500000",
}

for phone_id, image_url in updates.items():
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
        df["phone_id"].isin(updates.keys()),
        ["phone_id", "canonical_name", "official_image_url"]
    ].to_string(index=False)
)

print()
print("MOTOROLA IMAGE UPDATE COMPLETE")
