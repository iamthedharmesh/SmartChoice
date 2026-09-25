import pandas as pd
from pathlib import Path

DATA_PATH = Path("data/phones_enriched.csv")

phone194 = {
    "phone_id": 194,
    "canonical_name": "Motorola Edge 30 Fusion 5G",
    "model_id": "XT2243-1",

    "release_date_global": "2022-09-08",
    "release_date_india": "2022-09-22",
    "availability_status_india": pd.NA,
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.55,
    "display_type": "pOLED",
    "display_resolution": "2400 x 1080",
    "display_refresh_rate_hz": 144,
    "display_protection": "Corning Gorilla Glass 5",
    "display_peak_brightness_nits": 1100,
    "display_hdr_support": "HDR10+",

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": "OmniVision",
    "rear_main_ois": "Yes",
    "rear_ultrawide_mp": 13,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": pd.NA,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,
    "rear_video_max": "4K@30fps",

    "front_camera_mp": 32,
    "front_camera_aperture": "f/2.45",
    "front_camera_af": "Yes",
    "front_video_max": "4K@30fps",

    "battery_type": "Li-Polymer",
    "wired_charging_w": 68,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "158.48 x 71.99 x 7.45",
    "weight_g": 175,
    "build_frame": "Metal",
    "build_back": "3D Corning Gorilla Glass 5",
    "ip_rating": "IP52",
    "colors_available": "Cosmic Grey, Solar Gold, Viva Magenta",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1, n3, n5, n7, n8, n20, n28, n38, n40, n41, n66, n77, n78",
    "wifi_standard": "Wi-Fi 6E",
    "bluetooth_version": "5.2",
    "usb_version": "3.1",
    "usb_type": "Type-C",
    "audio_jack": "No",

    "os_launch": "Android 12, My UX",
    "os_current": pd.NA,
    "os_update_policy_years": "2 Years of Android Updates & 3 Years of Security Updates",

    "official_product_url": "https://en-in.support.motorola.com/app/answers/detail/a_id/172567/~/specifications--motorola-edge-30-fusion",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": pd.NA,

    "launch_price_inr_official": 42999,
    "current_min_price_inr": 29990,
    "price_updated_at": "2026-09-16",
}

df = pd.read_csv(DATA_PATH)

# Remove an existing row for this phone if the script is accidentally run again.
df = df[df["phone_id"] != 194].copy()

new_row = pd.DataFrame([phone194])

# Keep exact existing column order.
new_row = new_row[df.columns]

df = pd.concat([df, new_row], ignore_index=True)

df.to_csv(DATA_PATH, index=False)

print("Phone 194 written successfully.")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

row = df[df["phone_id"] == 194].iloc[0]

print("\nPhone 194 verification:")
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