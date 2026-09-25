import pandas as pd

# Selected 10 phones for Stage 1B prototype
selected = [
    (15, "Samsung", "Samsung Galaxy S23 Ultra 5G", 114990),
    (207, "Samsung", "Samsung Galaxy A54 5G", 34999),
    (153, "Apple", "Apple iPhone 15 Pro Max", 142990),
    (7, "Apple", "Apple iPhone 14", 65999),
    (106, "Xiaomi", "Xiaomi 13 Pro 5G", 58990),
    (8, "Xiaomi", "Xiaomi Redmi Note 12 Pro Plus", 29999),
    (1, "OnePlus", "OnePlus 11 5G", 54999),
    (186, "OnePlus", "OnePlus Nord 3 5G", 27999),
    (347, "Vivo", "Vivo X90 Pro 5G", 56999),
    (194, "Motorola", "Motorola Edge 30 Fusion 5G", 39999),
]

print("=== SELECTED 10 PHONES FOR STAGE 1B ===")
for phone_id, brand, model, price in selected:
    print(f"phone_id={phone_id} | {brand} | {model} | INR {price:,.0f}")

# Verify they exist in phones.csv
df = pd.read_csv(r'D:\SmartChoice\backend\data\phones.csv')
for phone_id, brand, model, price in selected:
    match = df[df['phone_id'] == phone_id]
    if len(match) == 1:
        print(f"  VERIFIED: {match.iloc[0]['brand']} {match.iloc[0]['model']} INR {match.iloc[0]['price_inr']:,.0f}")
    else:
        print(f"  ERROR: phone_id={phone_id} not found or duplicated")