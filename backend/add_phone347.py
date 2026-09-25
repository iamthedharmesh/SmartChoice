from pathlib import Path
import pandas as pd

BASE = Path(r"D:\SmartChoice\backend")
ENRICHED = BASE / "data" / "phones_enriched.csv"

df = pd.read_csv(ENRICHED)
columns = list(df.columns)

phone347 = {
    "phone_id": 347,
    "canonical_name": "vivo X90 Pro 5G",
    "model_id": "V2219",

    "release_date_global": "2023-02-22",
    "release_date_india": "2023-04-26",
    "availability_status_india": pd.NA,
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.78,
    "display_type": "AMOLED",
    "display_resolution": "2800 x 1260",
    "display_refresh_rate_hz": 120,
    "display_protection": pd.NA,
    "display_peak_brightness_nits": pd.NA,
    "display_hdr_support": pd.NA,

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.75",
    "rear_main_sensor": "Sony IMX989",
    "rear_main_ois": "Yes",
    "rear_ultrawide_mp": 12,
    "rear_ultrawide_aperture": "f/2.0",
    "rear_telephoto_mp": 50,
    "rear_telephoto_aperture": "f/1.6",
    "rear_telephoto_optical_zoom": "2x",
    "rear_video_max": "8K@24fps",

    "front_camera_mp": 32,
    "front_camera_aperture": "f/2.45",
    "front_camera_af": pd.NA,
    "front_video_max": "4K@30fps",

    "battery_type": pd.NA,
    "wired_charging_w": 120,
    "wireless_charging_w": 50,
    "reverse_wireless_charging_w": pd.NA,
    "battery_removable": "No",

    "dimensions_mm": "164.1 x 74.5 x 9.3",
    "weight_g": 214.6,
    "build_frame": "Aluminum alloy",
    "build_back": "Vegan leather finish",
    "ip_rating": "IP68",
    "colors_available": "Legendary Black",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1, n2, n3, n5, n7, n8, n20, n28, n38, n40, n41, n66, n71, n75, n77, n78, n79",
    "wifi_standard": "Wi-Fi 6",
    "bluetooth_version": "5.3",
    "usb_version": "3.2 Gen 1",
    "usb_type": "Type-C",
    "audio_jack": "No",

    "os_launch": "Android 13, Funtouch OS 13",
    "os_current": pd.NA,
    "os_update_policy_years": "3 Years of Android Updates & 3 Years of Security Updates",

    "official_product_url": "https://www.vivo.com/in/products/x90-pro",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/vivo_x90_pro-12103.php",

    "launch_price_inr_official": 84999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
}

missing = [c for c in columns if c not in phone347]

if missing:
    raise RuntimeError(f"Missing fields: {missing}")

# Remove Phone 347 if already present
df = df[df["phone_id"] != 347].copy()

# Add Phone 347
row = {c: phone347[c] for c in columns}
df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

# Keep IDs sorted
df["phone_id"] = pd.to_numeric(df["phone_id"])
df = df.sort_values("phone_id").reset_index(drop=True)

# Save
df.to_csv(ENRICHED, index=False)

print("Phone 347 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

check = df[df["phone_id"] == 347].iloc[0]

print("\nPhone 347 verification:")
for field in [
    "canonical_name",
    "model_id",
    "release_date_global",
    "release_date_india",
    "battery_type",
    "wired_charging_w",
    "wireless_charging_w",
    "reverse_wireless_charging_w",
    "five_g_bands",
    "os_current",
    "os_update_policy_years",
    "current_min_price_inr",
]:
    print(f"{field}: {check[field]}")