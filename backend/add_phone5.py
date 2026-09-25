import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/phones_enriched.csv")

phone5 = {
    "phone_id": 5,
    "canonical_name": "Realme 10 Pro+ 5G",
    "model_id": "RMX3686",

    "release_date_global": "2022-11-17",
    "release_date_india": "2022-12-08",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.7,
    "display_type": "AMOLED",
    "display_resolution": "2412 x 1080",
    "display_refresh_rate_hz": 120,
    "display_protection": "0.65mm Double-Reinforced Glass",
    "display_peak_brightness_nits": 950,
    "display_hdr_support": "HDR10+",

    "rear_camera_count": 3,
    "rear_main_mp": 108,
    "rear_main_aperture": "f/1.75",
    "rear_main_sensor": pd.NA,
    "rear_main_ois": "No",
    "rear_ultrawide_mp": 8,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": 2,
    "rear_telephoto_aperture": "f/2.4",
    "rear_telephoto_optical_zoom": "No",
    "rear_video_max": "4K@30fps",

    "front_camera_mp": 16,
    "front_camera_aperture": "f/2.45",
    "front_camera_af": pd.NA,
    "front_video_max": "1080p@30fps",

    "battery_type": pd.NA,
    "wired_charging_w": 67,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "161.5 x 73.9 x 7.78",
    "weight_g": 172.5,
    "build_frame": pd.NA,
    "build_back": "Glass",
    "ip_rating": pd.NA,
    "colors_available": "Hyperspace Gold, Dark Matter, Nebula Blue",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n40, n41, n78, n1, n3, n5, n8, n28A (SA); n1, n3, n41, n77, n78 (NSA)",
    "wifi_standard": "Wi-Fi 6",
    "bluetooth_version": "5.2",
    "usb_version": pd.NA,
    "usb_type": "Type-C",
    "audio_jack": "No",

    "os_launch": "Android 13, realme UI 4.0",
    "os_current": pd.NA,
    "os_update_policy_years": pd.NA,

    "official_product_url": "https://www.realme.com/in/realme-10-pro-plus",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/realme_10_pro+-12054.php",

    "launch_price_inr_official": 24999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
}

df = pd.read_csv(DATA_PATH)

# Remove existing Phone 5 row if the script is accidentally run again.
df = df[df["phone_id"] != 5].copy()

new_row = pd.DataFrame([phone5])
new_row = new_row[df.columns]

df = pd.concat([df, new_row], ignore_index=True)
df.to_csv(DATA_PATH, index=False)

print("Phone 5 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

row = df[df["phone_id"] == 5].iloc[0]

print("\nPhone 5 verification:")
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