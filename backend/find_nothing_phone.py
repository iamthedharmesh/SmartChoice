import pandas as pd

df = pd.read_csv(r".\data\phones_enriched.csv")

matches = df[
    df["canonical_name"].astype(str).str.contains(
        "Nothing Phone 1|Nothing Phone \(1\)",
        case=False,
        regex=True,
        na=False
    )
]

print("Nothing Phone matches:")
print(
    matches[
        ["phone_id", "canonical_name", "model_id", "official_image_url"]
    ].to_string(index=False)
)

print()
print("Rows containing 'Nothing':")
matches2 = df[
    df.astype(str).apply(
        lambda col: col.str.contains("Nothing", case=False, na=False)
    ).any(axis=1)
]

print(
    matches2[
        ["phone_id", "canonical_name", "model_id", "official_image_url"]
    ].to_string(index=False)
)
