from pathlib import Path
import pandas as pd

BASE = Path(r"D:\SmartChoice\backend")
ENRICHED = BASE / "data" / "phones_enriched.csv"

df = pd.read_csv(ENRICHED)
columns = list(df.columns)

phone186 = {
    "phone_id": 186,
    "canonical_name": "OnePlus Nord 3 5G",
    "model_id": "CPH2493",

    "release_date_global": "2023-07-05",
    "release_date_india": "2023-07-15",
    "availability_status_india": pd.NA,
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.74,
    "display_type": "Super Fluid AMOLED",
    "display_resolution": "2772 x 1240",
    "display_refresh_rate_hz": 120,
    "display_protection": "Corning Gorilla Glass 5",
    "display_peak_brightness_nits": 1450,
    "display_hdr_support": "HDR10+",

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": "Sony IMX890",
    "rear_main_ois": "Yes",
    "rear_ultrawide_mp": 8,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": pd.NA,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,
    "rear_video_max": "4K@60fps",

    "front_camera_mp": 16,
    "front_camera_aperture": "f/2.4",
    "front_camera_af": pd.NA,
    "front_video_max": "1080p@30fps",

    "battery_type": pd.NA,
    "wired_charging_w": 80,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "162.6 x 75.1 x 8.1",
    "weight_g": 193,
    "build_frame": "Plastic",
    "build_back": "Glass, Gorilla Glass 5",
    "ip_rating": "IP54",
    "colors_available": "Tempest Gray, Misty Green",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1, n3, n5, n8, n28A, n40, n41, n78",
    "wifi_standard": "Wi-Fi 6",
    "bluetooth_version": "5.3",
    "usb_version": "2.0",
    "usb_type": "Type-C",
    "audio_jack": "No",

    "os_launch": "Android 13, OxygenOS 13.1",
    "os_current": "OxygenOS 16 (Android 16)",
    "os_update_policy_years": "3 Years of Android Updates & 4 Years of Security Updates",

    "official_product_url": "https://www.oneplus.in/nord-3-5g",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/oneplus_nord_3-12368.php",

    "launch_price_inr_official": 33999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
}

# Check that our schema matches the existing 57-column schema
missing = [c for c in columns if c not in phone186]

if missing:
    raise RuntimeError(f"Missing fields: {missing}")

# Remove Phone 186 if it already exists
df = df[df["phone_id"] != 186].copy()

# Add corrected Phone 186
row = {c: phone186[c] for c in columns}
df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

# Keep phone IDs sorted
df["phone_id"] = pd.to_numeric(df["phone_id"])
df = df.sort_values("phone_id").reset_index(drop=True)

# Save
df.to_csv(ENRICHED, index=False)

print("Phone 186 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

check = df[df["phone_id"] == 186].iloc[0]

print("\nPhone 186 verification:")
for field in [
    "canonical_name",
    "model_id",
    "release_date_global",
    "release_date_india",
    "battery_type",
    "wired_charging_w",
    "wireless_charging_w",
    "five_g_bands",
    "os_current",
    "os_update_policy_years",
    "current_min_price_inr",
]:
    print(f"{field}: {check[field]}")