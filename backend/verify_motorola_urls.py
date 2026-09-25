import pandas as pd
import requests

df = pd.read_csv(r".\data\phones_enriched.csv")

ids = [86, 223, 194]

for phone_id in ids:
    row = df[df["phone_id"] == phone_id].iloc[0]
    url = row["official_image_url"]

    print("=" * 70)
    print("ID:", phone_id)
    print("Model:", row["canonical_name"])
    print("URL:", url)

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
        print("HEAD failed:", e)

        try:
            r = requests.get(
                url,
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=20,
                stream=True
            )
            print("GET HTTP:", r.status_code)
            print("Content-Type:", r.headers.get("Content-Type"))
        except Exception as e2:
            print("GET failed:", e2)

print()
print("MOTOROLA IMAGE URL VERIFICATION COMPLETE")
