import pandas as pd
import requests

df = pd.read_csv(r".\data\phones_enriched.csv")

ids = [9, 134, 206]

for phone_id in ids:
    row = df[df["phone_id"] == phone_id].iloc[0]
    url = row["official_image_url"]

    print("=" * 70)
    print("ID:", phone_id)
    print("Model:", row["canonical_name"])

    try:
        r = requests.head(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=20,
            allow_redirects=True
        )

        print("HTTP:", r.status_code)
        print("Content-Type:", r.headers.get("Content-Type"))
        print("Size:", r.headers.get("Content-Length"))

    except Exception as e:
        print("ERROR:", e)

print()
print("NOTHING PHONE 1 URL VERIFICATION COMPLETE")
