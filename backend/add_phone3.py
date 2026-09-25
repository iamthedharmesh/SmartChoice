import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/phones_enriched.csv")

phone3 = {
    "phone_id": 3,
    "canonical_name": "Samsung Galaxy A14 5G",
    "model_id": "SM-A146B",

    "release_date_global": "2023-01-04",
    "release_date_india": "2023-01-16",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.6,
    "display_type": "PLS LCD",
    "display_resolution": "2408 x 1080",
    "display_refresh_rate_hz": 90,
    "display_protection": pd.NA,
    "display_peak_brightness_nits": pd.NA,
    "display_hdr_support": pd.NA,

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": pd.NA,
    "rear_main_ois": "No",
    "rear_ultrawide_mp": pd.NA,
    "rear_ultrawide_aperture": pd.NA,
    "rear_telephoto_mp": pd.NA,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,
    "rear_video_max": "1080p@30fps",

    "front_camera_mp": 13,
    "front_camera_aperture": "f/2.0",
    "front_camera_af": "No",
    "front_video_max": "1080p@30fps",

    "battery_type": "Li-ion",
    "wired_charging_w": 15,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "167.7 x 78.0 x 9.1",
    "weight_g": 201,
    "build_frame": pd.NA,
    "build_back": "Plastic",
    "ip_rating": pd.NA,
    "colors_available": "Black, Light Green, Dark Red",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1, n3, n5, n7, n8, n20, n28a, n38, n40, n41, n77, n78",
    "wifi_standard": "Wi-Fi 5 (802.11 a/b/g/n/ac)",
    "bluetooth_version": "5.2",
    "usb_version": "2.0",
    "usb_type": "Type-C",
    "audio_jack": "Yes",

    "os_launch": "Android 13, One UI 5.0",
    "os_current": pd.NA,
    "os_update_policy_years": "2 Years of Android Updates & 4 Years of Security Updates",

    "official_product_url": "https://www.samsung.com/in/smartphones/galaxy-a/galaxy-a14-5g/",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/samsung_galaxy_a14_5g-12074.php",

    "launch_price_inr_official": 16499,
    "current_min_price_inr": 18499,
    "price_updated_at": "2026-09-11",
}

df = pd.read_csv(DATA_PATH)

# Remove existing Phone 3 row if the script is accidentally run again.
df = df[df["phone_id"] != 3].copy()

new_row = pd.DataFrame([phone3])
new_row = new_row[df.columns]

df = pd.concat([df, new_row], ignore_index=True)
df.to_csv(DATA_PATH, index=False)

print("Phone 3 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

row = df[df["phone_id"] == 3].iloc[0]

print("\nPhone 3 verification:")
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