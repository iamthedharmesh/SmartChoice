import pandas as pd
df = pd.read_csv(r'D:\SmartChoice\backend\data\phones.csv')
print('=== BRAND COUNTS ===')
print(df['brand'].value_counts().head(20))
print()
print('=== PRICE RANGES PER BRAND (top brands) ===')
for brand in df['brand'].value_counts().head(10).index:
    subset = df[df['brand'] == brand]
    print(f'{brand}: {len(subset)} phones, price range: INR {subset["price_inr"].min():,.0f} - INR {subset["price_inr"].max():,.0f}')