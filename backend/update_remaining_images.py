import pandas as pd

path = r".\data\phones_enriched.csv"
df = pd.read_csv(path)

updates = {
    257: "https://img.global.news.samsung.com/ca/wp-content/uploads/2022/02/019_galaxys22plus_front_green-1024x683.jpg",
    750: "https://img.global.news.samsung.com/ca/wp-content/uploads/2022/02/019_galaxys22plus_front_green-1024x683.jpg",

    72: "https://asia-exstatic-vivofs.vivo.com/PSee2l50xoirPK7y/1640862857357/4947ef03091facc9b18c1b913d862b4d.png",
    126: "https://asia-exstatic-vivofs.vivo.com/PSee2l50xoirPK7y/1640862857357/4947ef03091facc9b18c1b913d862b4d.png",

    29: "https://in-exstatic-vivofs.vivo.com/gdHFRinHEMrj3yPG/1661844290896/1fb10741c2d8f0a11baf16779347f8a7.png",

    251: "https://d13pvy8xd75yde.cloudfront.net/global/phones/45c026326fdce9098edaf838b954f79b.png",
}

for phone_id, url in updates.items():
    df.loc[df["phone_id"] == phone_id, "official_image_url"] = url

df.to_csv(path, index=False)

print("Updated:", len(updates), "phone rows")
print()

for phone_id in updates:
    row = df.loc[
        df["phone_id"] == phone_id,
        ["phone_id", "canonical_name", "official_image_url"]
    ]
    print(row.to_string(index=False))
    print()
