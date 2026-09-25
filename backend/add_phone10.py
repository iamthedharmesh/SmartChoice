import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/phones_enriched.csv")

phone10 = {
    "phone_id": 10,
    "canonical_name": "OnePlus Nord 2T 5G",
    "model_id": "CPH2401",

    "release_date_global": "2022-05-19",
    "release_date_india": "2022-07-05",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.43,
    "display_type": "AMOLED",
    "display_resolution": "2400 x 1080",
    "display_refresh_rate_hz": 90,
    "display_protection": "Corning Gorilla Glass 5",
    "display_peak_brightness_nits": pd.NA,
    "display_hdr_support": "HDR10+",

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": "Sony IMX766",
    "rear_main_ois": "Yes",
    "rear_ultrawide_mp": 8,
    "rear_ultrawide_aperture": pd.NA,
    "rear_telephoto_mp": 2,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,
    "rear_video_max": "4K@30fps",

    "front_camera_mp": 32,
    "front_camera_aperture": pd.NA,
    "front_camera_af": pd.NA,
    "front_video_max": "1080p@30fps",

    "battery_type": pd.NA,
    "wired_charging_w": 80,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "159.1 x 73.2 x 8.2",
    "weight_g": 190,
    "build_frame": pd.NA,
    "build_back": pd.NA,
    "ip_rating": pd.NA,
    "colors_available": "Jade Fog, Gray Shadow",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1, n3, n5, n8, n28, n40, n41, n78",
    "wifi_standard": "Wi-Fi 6",
    "bluetooth_version": "5.2",
    "usb_version": "2.0",
    "usb_type": "Type-C",
    "audio_jack": "No",

    "os_launch": "Android 12, OxygenOS 12.1",
    "os_current": pd.NA,
    "os_update_policy_years": "2 Years of Android Updates & 3 Years of Security Updates",

    "official_product_url": "https://www.oneplus.in/nord-2t-5g/specs",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": pd.NA,

    "launch_price_inr_official": 28999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
}

df = pd.read_csv(DATA_PATH)

# Remove existing Phone 10 row if the script is accidentally run again.
df = df[df["phone_id"] != 10].copy()

new_row = pd.DataFrame([phone10])
new_row = new_row[df.columns]

df = pd.concat([df, new_row], ignore_index=True)
df.to_csv(DATA_PATH, index=False)

print("Phone 10 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

row = df[df["phone_id"] == 10].iloc[0]

print("\nPhone 10 verification:")
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