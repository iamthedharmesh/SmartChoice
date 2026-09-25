import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/phones_enriched.csv")

phone12 = {
    "phone_id": 12,
    "canonical_name": "OPPO A78",
    "model_id": "CPH2565",

    "release_date_global": "2023-07-25",
    "release_date_india": "2023-08-01",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.43,
    "display_type": "AMOLED",
    "display_resolution": "2400 x 1080",
    "display_refresh_rate_hz": 90,
    "display_protection": "Corning Gorilla Glass 5",
    "display_peak_brightness_nits": 800,
    "display_hdr_support": pd.NA,

    "rear_camera_count": 2,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": pd.NA,
    "rear_main_ois": "No",
    "rear_ultrawide_mp": pd.NA,
    "rear_ultrawide_aperture": pd.NA,
    "rear_telephoto_mp": 2,
    "rear_telephoto_aperture": "f/2.4",
    "rear_telephoto_optical_zoom": pd.NA,
    "rear_video_max": "1080p@30fps",

    "front_camera_mp": 8,
    "front_camera_aperture": "f/2.0",
    "front_camera_af": "No",
    "front_video_max": "1080p@30fps",

    "battery_type": pd.NA,
    "wired_charging_w": 67,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "160.01 x 73.23 x 7.93",
    "weight_g": 180,
    "build_frame": pd.NA,
    "build_back": pd.NA,
    "ip_rating": "IP54",
    "colors_available": "Aqua Green, Mist Black",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": pd.NA,
    "wifi_standard": "Wi-Fi 5 (802.11ac)",
    "bluetooth_version": "5.0",
    "usb_version": pd.NA,
    "usb_type": "Type-C",
    "audio_jack": "Yes",

    "os_launch": "Android 13, ColorOS 13.1",
    "os_current": pd.NA,
    "os_update_policy_years": pd.NA,

    "official_product_url": "https://www.oppo.com/in/smartphones/series-a/a78/specs/",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/oppo_a78-12466.php",

    "launch_price_inr_official": 17499,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
}

df = pd.read_csv(DATA_PATH)

# Remove existing Phone 12 row if this script is accidentally run again.
df = df[df["phone_id"] != 12].copy()

new_row = pd.DataFrame([phone12])
new_row = new_row[df.columns]

df = pd.concat([df, new_row], ignore_index=True)
df.to_csv(DATA_PATH, index=False)

print("Phone 12 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

row = df[df["phone_id"] == 12].iloc[0]

print("\nPhone 12 verification:")
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