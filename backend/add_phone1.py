from pathlib import Path
import pandas as pd

BASE = Path(r"D:\SmartChoice\backend")
ENRICHED = BASE / "data" / "phones_enriched.csv"

df = pd.read_csv(ENRICHED)

# Preserve the existing exact 57-column schema
columns = list(df.columns)

phone1 = {
    "phone_id": 1,
    "canonical_name": "OnePlus 11 5G",
    "model_id": "CPH2447",
    "release_date_global": "2023-02-07",
    "release_date_india": "2023-02-14",
    "availability_status_india": pd.NA,
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.7,
    "display_type": "Super Fluid AMOLED, LTPO 3.0, 1-120Hz dynamic, Dolby Vision, HDR10+, 10-bit",
    "display_resolution": "3216 x 1440 (QHD+), 525 ppi",
    "display_refresh_rate_hz": 120,
    "display_protection": "Corning Gorilla Glass Victus",
    "display_peak_brightness_nits": 1300,
    "display_hdr_support": "Dolby Vision, HDR10+",

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": 'Sony IMX890, 1/1.56", 1.0µm, 6P lens',
    "rear_main_ois": "Yes",
    "rear_ultrawide_mp": 48,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": 32,
    "rear_telephoto_aperture": "f/2.0",
    "rear_telephoto_optical_zoom": "2x",
    "rear_video_max": "8K@24fps, 4K@30/60fps, 1080p@30/60fps, 720p@240/480fps",

    "front_camera_mp": 16,
    "front_camera_aperture": "f/2.45",
    "front_camera_af": pd.NA,
    "front_video_max": "4K@30fps, 1080p@30/60fps, 720p@30fps",

    "battery_type": pd.NA,
    "wired_charging_w": 100,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "163.1 x 74.1 x 8.53 (Eternal Green/Titan Black), 8.56 (Marble Odyssey)",
    "weight_g": "205 (Eternal Green/Titan Black), 203 (Marble Odyssey)",
    "build_frame": "Aluminum",
    "build_back": "Glass",
    "ip_rating": "IP54",
    "colors_available": "Eternal Green, Titan Black, Marble Odyssey",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1, n3, n5, n7, n8, n20, n28A, n38, n40, n41, n66, n77, n78 (SA/NSA)",
    "wifi_standard": "Wi-Fi 7",
    "bluetooth_version": "5.3",
    "usb_version": "2.0",
    "usb_type": "Type-C",
    "audio_jack": "No",

    "os_launch": "Android 13, OxygenOS 13",
    "os_current": "OxygenOS 16 (Android 16)",
    "os_update_policy_years": "4 Years of Android Updates & 5 Years of Security Updates",

    "official_product_url": "https://www.oneplus.in/11",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/oneplus_11-11893.php",

    "launch_price_inr_official": 56999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
}

# Ensure all columns exist
missing = [c for c in columns if c not in phone1]
if missing:
    raise RuntimeError(f"Missing fields in Phone 1 data: {missing}")

# Remove existing Phone 1 if present, then insert corrected version
df = df[df["phone_id"] != 1].copy()

row = {c: phone1[c] for c in columns}
df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

# Preserve numeric ordering
df["phone_id"] = pd.to_numeric(df["phone_id"])
df = df.sort_values("phone_id").reset_index(drop=True)

# Save
df.to_csv(ENRICHED, index=False)

print("Phone 1 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

check = df[df["phone_id"] == 1].iloc[0]

print("\nPhone 1 verification:")
for field in [
    "canonical_name",
    "release_date_global",
    "release_date_india",
    "battery_type",
    "wireless_charging_w",
    "reverse_wireless_charging_w",
    "five_g_bands",
    "os_current",
    "os_update_policy_years",
    "current_min_price_inr",
]:
    print(f"{field}: {check[field]}")