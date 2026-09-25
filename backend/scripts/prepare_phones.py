"""
Stage A: prepare backend/data/phones.csv from smartphones_cleaned_v6.csv.

Rules:
- No imputation of price: exclude records with missing/invalid price.
- Missing rating kept as null (NaN) - documented neutral fallback not applied here.
- Missing charging_watt kept as null (NaN), NOT converted to 0.
- Missing refresh_rate_hz kept as null (NaN), NOT converted to 0.
- Preserve distinct RAM/storage variants as separate phones.
- Remove only true full-row duplicates.
- Camera MP already numeric in source (primary_camera_rear/front); kept as-is.
- No release_year added (not trustworthy in source).

Source: kaggle nikhil1998saxena17/smartphones-data (smartphones_cleaned_v6.csv)
"""
import pandas as pd

SRC = r"C:\Users\Admin\.cache\kagglehub\datasets\nikhil1998saxena17\smartphones-data\versions\1\smartphones_cleaned_v6.csv"
DST = r"D:\SmartChoice\backend\data\phones.csv"

df = pd.read_csv(SRC)
original_rows = len(df)

# --- 1. brand / model normalization ---
df["brand"] = df["brand_name"].astype(str).str.strip().str.title()
_BRAND_FIX = {"Oneplus": "OnePlus", "Iqoo": "iQOO", "Poco": "POCO"}
df["brand"] = df["brand"].replace(_BRAND_FIX)
df["model"] = df["model"].astype(str).str.strip()

# --- 2. boolean -> int (0/1) ---
for col in ["has_5g", "has_nfc"]:
    df[col] = df[col].astype(bool).astype(int)

# --- 3. numeric coercion ---
df["price_inr"] = pd.to_numeric(df["price"], errors="coerce")
df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
df["ram_gb"] = pd.to_numeric(df["ram_capacity"], errors="coerce")
df["storage_gb"] = pd.to_numeric(df["internal_memory"], errors="coerce")
df["processor_brand"] = df["processor_brand"].astype(str).str.strip().str.lower()
df["processor_name"] = df["processor_brand"]  # source has no separate processor_name column
df["core_count"] = pd.to_numeric(df["num_cores"], errors="coerce")
df["clock_speed_ghz"] = pd.to_numeric(df["processor_speed"], errors="coerce")
df["battery_mah"] = pd.to_numeric(df["battery_capacity"], errors="coerce")
df["charging_watt"] = pd.to_numeric(df["fast_charging"], errors="coerce")   # kept null if missing
df["refresh_rate_hz"] = pd.to_numeric(df["refresh_rate"], errors="coerce")  # kept null if missing
df["rear_camera_mp"] = pd.to_numeric(df["primary_camera_rear"], errors="coerce")
df["front_camera_mp"] = pd.to_numeric(df["primary_camera_front"], errors="coerce")
df["rear_camera_count"] = pd.to_numeric(df["num_rear_cameras"], errors="coerce")
df["os"] = df["os"].astype(str).str.strip().str.lower()

# --- 4. exclude records with missing/invalid price ---
before_price_filter = len(df)
df = df[df["price_inr"].notna() & (df["price_inr"] > 0)]
rows_removed_missing_price = before_price_filter - len(df)

# --- 5. remove only true full-row duplicates on the relevant spec set ---
spec_cols = ["brand", "model", "price_inr", "rating", "ram_gb", "storage_gb",
             "processor_brand", "core_count", "clock_speed_ghz", "battery_mah",
             "charging_watt", "refresh_rate_hz", "rear_camera_mp", "front_camera_mp",
             "has_5g", "has_nfc", "os"]
before_dedup = len(df)
df = df.drop_duplicates(subset=spec_cols, keep="first")
rows_removed_duplicates = before_dedup - len(df)

# --- 6. final column selection ---
final_cols = [
    "brand", "model", "price_inr", "rating", "ram_gb", "storage_gb",
    "processor_brand", "processor_name", "core_count", "clock_speed_ghz",
    "battery_mah", "charging_watt", "refresh_rate_hz", "rear_camera_mp",
    "front_camera_mp", "rear_camera_count", "has_5g", "has_nfc", "os",
]
df = df[final_cols].reset_index(drop=True)
df.insert(0, "phone_id", range(1, len(df) + 1))

df.to_csv(DST, index=False)

# ---------------- validation report ----------------
print("=== STAGE A VALIDATION ===")
print("A. Original row count:", original_rows)
print("B. Final cleaned row count:", len(df))
print("C. Columns created:", list(df.columns))
print("D. Rows removed:")
print("   - missing/invalid price:", rows_removed_missing_price)
print("   - true duplicate spec sets:", rows_removed_duplicates)
print("E. Missing-value treatment:")
print("   - rating: kept as null (NaN), not imputed")
print("   - charging_watt: kept as null (NaN), NOT set to 0")
print("   - refresh_rate_hz: kept as null (NaN), NOT set to 0")
print("   - processor_brand/core_count/clock_speed/battery: kept as null where source missing")
print("F. Camera parsing:")
print("   - source already provides numeric primary_camera_rear/front; no string parsing needed")
print("   - rear_camera_count carried from num_rear_cameras")
print("G. Duplicate handling: dedup on full relevant spec set only; RAM/storage variants preserved")
print()
print("Missing per target column:")
for c in final_cols:
    print(f"   {c}: {int(df[c].isna().sum())}")
print()
print("price_inr  min/max:", int(df["price_inr"].min()), "/", int(df["price_inr"].max()))
print("rating     min/max:", df["rating"].min(), "/", df["rating"].max())
print("ram_gb distribution:")
print(df["ram_gb"].value_counts().sort_index().to_string())
print("storage_gb distribution:")
print(df["storage_gb"].value_counts().sort_index().to_string())
print("has_5g counts:", df["has_5g"].value_counts().to_dict())
print("brand counts (top 15):")
print(df["brand"].value_counts().head(15).to_string())
print("processor_brand counts:")
print(df["processor_brand"].value_counts().to_string())
print("rear_camera_mp distribution (top):")
print(df["rear_camera_mp"].value_counts().head(12).sort_index().to_string())
print("Wrote:", DST)