import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/phones_enriched.csv")

phone6 = {
    "phone_id": 6,
    "canonical_name": "Samsung Galaxy F23 5G",
    "model_id": "SM-E236BIDH",

    "release_date_global": "2022-03-08",
    "release_date_india": "2022-03-08",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.6,
    "display_type": "LCD",
    "display_resolution": "2408 x 1080",
    "display_refresh_rate_hz": 120,
    "display_protection": "Corning Gorilla Glass 5",
    "display_peak_brightness_nits": pd.NA,
    "display_hdr_support": pd.NA,

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": pd.NA,
    "rear_main_ois": "No",
    "rear_ultrawide_mp": 8,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": 2,
    "rear_telephoto_aperture": "f/2.4",
    "rear_telephoto_optical_zoom": pd.NA,
    "rear_video_max": "4K@30fps",

    "front_camera_mp": 8,
    "front_camera_aperture": "f/2.2",
    "front_camera_af": pd.NA,
    "front_video_max": "1080p@30fps",

    "battery_type": "Li-ion",
    "wired_charging_w": 25,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "165.5 x 77.0 x 8.4",
    "weight_g": 198,
    "build_frame": pd.NA,
    "build_back": "Plastic",
    "ip_rating": pd.NA,
    "colors_available": "Aqua Blue, Forest Green",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1, n3, n5, n7, n8, n20, n28, n66, n38, n40, n41, n78",
    "wifi_standard": "Wi-Fi 5 (802.11 a/b/g/n/ac)",
    "bluetooth_version": "5.0",
    "usb_version": "2.0",
    "usb_type": "Type-C",
    "audio_jack": "Yes",

    "os_launch": "Android 12, One UI 4.1",
    "os_current": pd.NA,
    "os_update_policy_years": "2 Years of Android Updates & 4 Years of Security Updates",

    "official_product_url": "https://www.samsung.com/in/",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/samsung_galaxy_f23-11398.php",

    "launch_price_inr_official": 18499,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
}

df = pd.read_csv(DATA_PATH)

# Remove existing Phone 6 row if the script is accidentally run again.
df = df[df["phone_id"] != 6].copy()

new_row = pd.DataFrame([phone6])
new_row = new_row[df.columns]

df = pd.concat([df, new_row], ignore_index=True)
df.to_csv(DATA_PATH, index=False)

print("Phone 6 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

row = df[df["phone_id"] == 6].iloc[0]

print("\nPhone 6 verification:")
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