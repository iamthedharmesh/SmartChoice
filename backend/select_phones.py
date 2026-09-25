import pandas as pd
df = pd.read_csv(r'D:\SmartChoice\backend\data\phones.csv')

# Select representative phones across brands and price tiers
candidates = [
    # Samsung - flagship
    ("Samsung", "Galaxy S23 Ultra 5G"),
    # Samsung - mid-range
    ("Samsung", "Galaxy A54 5G"),
    # Apple - flagship
    ("Apple", "iPhone 15 Pro Max"),
    # Apple - mid-range
    ("Apple", "iPhone 14"),
    # Xiaomi - flagship
    ("Xiaomi", "13 Pro 5G"),
    # Xiaomi - budget/mid
    ("Xiaomi", "Redmi Note 12 Pro Plus"),
    # OnePlus - flagship
    ("OnePlus", "11 5G"),
    # OnePlus - mid-range
    ("OnePlus", "Nord 3 5G"),
    # Vivo - flagship
    ("Vivo", "X90 Pro 5G"),
    # Motorola - mid-range
    ("Motorola", "Edge 30 Fusion 5G"),
    # Realme - mid-range
    ("Realme", "11 Pro Plus"),
    # POCO - budget performance
    ("POCO", "F5"),
    # Google - Pixel
    ("Google", "Pixel 7 Pro 5G"),
    # Nothing
    ("Nothing", "Phone 2"),
    # iQOO
    ("iQOO", "11 5G"),
]

print("=== CANDIDATE MATCHES ===")
for brand, model in candidates:
    matches = df[(df['brand'].str.lower() == brand.lower()) & (df['model'].str.contains(model, case=False, na=False))]
    if len(matches) > 0:
        for _, row in matches.iterrows():
            print(f"phone_id={row['phone_id']} | {row['brand']} | {row['model']} | INR {row['price_inr']:,.0f} | rating={row['rating']}")
    else:
        print(f"NOT FOUND: {brand} {model}")