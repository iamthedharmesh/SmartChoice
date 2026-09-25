import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/phones_enriched.csv")

phone11 = {
    "phone_id": 11,
    "canonical_name": "Realme 10 Pro 5G",
    "model_id": "RMX3663",

    "release_date_global": "2022-11-17",
    "release_date_india": "2022-12-08",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.72,
    "display_type": "IPS LCD",
    "display_resolution": "2400 x 1080",
    "display_refresh_rate_hz": 120,
    "display_protection": pd.NA,
    "display_peak_brightness_nits": 680,
    "display_hdr_support": pd.NA,

    "rear_camera_count": 2,
    "rear_main_mp": 108,
    "rear_main_aperture": "f/1.75",
    "rear_main_sensor": "Samsung HM6",
    "rear_main_ois": "No",
    "rear_ultrawide_mp": pd.NA,
    "rear_ultrawide_aperture": pd.NA,
    "rear_telephoto_mp": 2,
    "rear_telephoto_aperture": "f/2.4",
    "rear_telephoto_optical_zoom": pd.NA,
    "rear_video_max": "1080p@30fps",

    "front_camera_mp": 16,
    "front_camera_aperture": "f/2.45",
    "front_camera_af": pd.NA,
    "front_video_max": "1080p@30fps",

    "battery_type": "Li-ion",
    "wired_charging_w": 33,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "163.7 x 74.2 x 8.1",
    "weight_g": 190,
    "build_frame": "Plastic",
    "build_back": "Plastic",
    "ip_rating": pd.NA,
    "colors_available": "Hyperspace Gold, Dark Matter, Nebula Blue",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1, n3, n5, n7, n8, n20, n28, n38, n40, n41, n77, n78",
    "wifi_standard": "Wi-Fi 5 (802.11 a/b/g/n/ac)",
    "bluetooth_version": "5.1",
    "usb_version": "2.0",
    "usb_type": "Type-C",
    "audio_jack": "Yes",

    "os_launch": "Android 13, realme UI 4.0",
    "os_current": pd.NA,
    "os_update_policy_years": "2 Years of Android Updates & 3 Years of Security Updates",

    "official_product_url": "https://www.realme.com/in/realme-10-pro/specs",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/realme_10_pro-11954.php",

    "launch_price_inr_official": 18999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
}

df = pd.read_csv(DATA_PATH)

# Remove existing Phone 11 row if this script is accidentally run again.
df = df[df["phone_id"] != 11].copy()

new_row = pd.DataFrame([phone11])
new_row = new_row[df.columns]

df = pd.concat([df, new_row], ignore_index=True)
df.to_csv(DATA_PATH, index=False)

print("Phone 11 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

row = df[df["phone_id"] == 11].iloc[0]

print("\nPhone 11 verification:")
print("canonical_name:", row["canonical_name"])
print("model_id:", row["model_id"])
print("release_date_global:", row["release_date_global"])
print("release_date_india:", row["release_date_india"])
print("battery_type:", row["battery_type"])
print("wired_charging_w:", row["wired_charging_w"])
print("wireless_charging_w:", row["wireless_charging_w"])
print("five_g_bands:", row["five_g_bands"])
print("os_current:", row["os_current"])
print("os_update_policy_years:", row["os_update_policy_years"])
print("current_min_price_inr:", row["current_min_price_inr"])