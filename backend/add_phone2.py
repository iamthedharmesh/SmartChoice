import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/phones_enriched.csv")

phone2 = {
    "phone_id": 2,
    "canonical_name": "OnePlus Nord CE 2 Lite 5G",
    "model_id": "CPH2381",

    "release_date_global": "2022-04-28",
    "release_date_india": "2022-04-28",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.59,
    "display_type": "LCD",
    "display_resolution": "2412 x 1080",
    "display_refresh_rate_hz": 120,
    "display_protection": pd.NA,
    "display_peak_brightness_nits": pd.NA,
    "display_hdr_support": pd.NA,

    "rear_camera_count": 3,
    "rear_main_mp": 64,
    "rear_main_aperture": "f/1.7",
    "rear_main_sensor": pd.NA,
    "rear_main_ois": "No",
    "rear_ultrawide_mp": pd.NA,
    "rear_ultrawide_aperture": pd.NA,
    "rear_telephoto_mp": pd.NA,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,
    "rear_video_max": "1080p@30fps",

    "front_camera_mp": 16,
    "front_camera_aperture": "f/2.0",
    "front_camera_af": pd.NA,
    "front_video_max": "1080p@30fps",

    "battery_type": pd.NA,
    "wired_charging_w": 33,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "164.3 x 75.6 x 8.5",
    "weight_g": 195,
    "build_frame": pd.NA,
    "build_back": pd.NA,
    "ip_rating": pd.NA,
    "colors_available": "Blue Tide, Black Dusk",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1, n28A, n41, n78 (SA); n41, n77, n78 (NSA)",
    "wifi_standard": "Wi-Fi 5 (802.11 a/b/g/n/ac)",
    "bluetooth_version": "5.2",
    "usb_version": "2.0",
    "usb_type": "Type-C",
    "audio_jack": "Yes",

    "os_launch": "Android 12, OxygenOS 12.1",
    "os_current": pd.NA,
    "os_update_policy_years": "2 Years of Android Updates & 3 Years of Security Updates",

    "official_product_url": "https://www.oneplus.in/nord-ce-2-lite-5g/specs",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/oneplus_nord_ce_2_lite_5g-11409.php",

    "launch_price_inr_official": 19999,
    "current_min_price_inr": 17994,
    "price_updated_at": "2026-09-11",
}

df = pd.read_csv(DATA_PATH)

# Remove existing Phone 2 row if script is accidentally run again.
df = df[df["phone_id"] != 2].copy()

new_row = pd.DataFrame([phone2])
new_row = new_row[df.columns]

df = pd.concat([df, new_row], ignore_index=True)
df.to_csv(DATA_PATH, index=False)

print("Phone 2 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

row = df[df["phone_id"] == 2].iloc[0]

print("\nPhone 2 verification:")
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