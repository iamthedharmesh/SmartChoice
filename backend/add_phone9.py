import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/phones_enriched.csv")

phone9 = {
    "phone_id": 9,
    "canonical_name": "Nothing Phone (1)",
    "model_id": "A063",

    "release_date_global": "2022-07-12",
    "release_date_india": "2022-07-12",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.55,
    "display_type": "Flexible AMOLED",
    "display_resolution": "2400 x 1080",
    "display_refresh_rate_hz": 120,
    "display_protection": "Corning Gorilla Glass",
    "display_peak_brightness_nits": 1200,
    "display_hdr_support": "HDR10+",

    "rear_camera_count": 2,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.88",
    "rear_main_sensor": "Sony IMX766",
    "rear_main_ois": "Yes",
    "rear_ultrawide_mp": 50,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": pd.NA,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,
    "rear_video_max": "4K@30fps",

    "front_camera_mp": 16,
    "front_camera_aperture": "f/2.45",
    "front_camera_af": pd.NA,
    "front_video_max": "1080p@30fps",

    "battery_type": pd.NA,
    "wired_charging_w": 33,
    "wireless_charging_w": 15,
    "reverse_wireless_charging_w": 5,
    "battery_removable": "No",

    "dimensions_mm": "159.2 x 75.8 x 8.3",
    "weight_g": 193.5,
    "build_frame": "Aluminum",
    "build_back": "Glass",
    "ip_rating": "IP53",
    "colors_available": "Black, White",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1, n3, n5, n7, n8, n20, n28, n38, n40, n41, n77, n78",
    "wifi_standard": "Wi-Fi 6",
    "bluetooth_version": "5.2",
    "usb_version": pd.NA,
    "usb_type": "Type-C",
    "audio_jack": "No",

    "os_launch": "Android 12, Nothing OS 1.0",
    "os_current": pd.NA,
    "os_update_policy_years": "3 Years of Android Updates & 4 Years of Security Patches",

    "official_product_url": "https://in.nothing.tech/pages/phone-1",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/nothing_phone_(1)-11636.php",

    "launch_price_inr_official": 32999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
}

df = pd.read_csv(DATA_PATH)

# Remove existing Phone 9 row if this script is accidentally run again.
df = df[df["phone_id"] != 9].copy()

new_row = pd.DataFrame([phone9])
new_row = new_row[df.columns]

df = pd.concat([df, new_row], ignore_index=True)
df.to_csv(DATA_PATH, index=False)

print("Phone 9 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

row = df[df["phone_id"] == 9].iloc[0]

print("\nPhone 9 verification:")
print("canonical_name:", row["canonical_name"])
print("model_id:", row["model_id"])
print("release_date_global:", row["release_date_global"])
print("release_date_india:", row["release_date_india"])
print("battery_type:", row["battery_type"])
print("wired_charging_w:", row["wired_charging_w"])
print("wireless_charging_w:", row["wireless_charging_w"])
print("reverse_wireless_charging_w:", row["reverse_wireless_charging_w"])
print("five_g_bands:", row["five_g_bands"])
print("os_current:", row["os_current"])
print("os_update_policy_years:", row["os_update_policy_years"])
print("current_min_price_inr:", row["current_min_price_inr"])