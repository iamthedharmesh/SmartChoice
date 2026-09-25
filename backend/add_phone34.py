import pandas as pd

CSV_PATH = "data/phones_enriched.csv"

COLUMNS = [
    "phone_id", "canonical_name", "model_id",
    "release_date_global", "release_date_india",
    "availability_status_india", "discontinued_date_india",
    "display_size_inch", "display_type", "display_resolution",
    "display_refresh_rate_hz", "display_protection",
    "display_peak_brightness_nits", "display_hdr_support",
    "rear_camera_count", "rear_main_mp", "rear_main_aperture",
    "rear_main_sensor", "rear_main_ois",
    "rear_ultrawide_mp", "rear_ultrawide_aperture",
    "rear_telephoto_mp", "rear_telephoto_aperture",
    "rear_telephoto_optical_zoom", "rear_video_max",
    "front_camera_mp", "front_camera_aperture", "front_camera_af",
    "front_video_max", "battery_type", "wired_charging_w",
    "wireless_charging_w", "reverse_wireless_charging_w",
    "battery_removable", "dimensions_mm", "weight_g",
    "build_frame", "build_back", "ip_rating", "colors_available",
    "sim_type", "five_g_bands", "wifi_standard",
    "bluetooth_version", "usb_version", "usb_type",
    "audio_jack", "os_launch", "os_current",
    "os_update_policy_years", "official_product_url",
    "official_image_url", "local_image_path", "gsmarena_url",
    "launch_price_inr_official", "current_min_price_inr",
    "price_updated_at"
]

row = {
    "phone_id": 34,
    "canonical_name": "Apple iPhone 11 (4GB RAM + 64GB)",
    "model_id": "A2221",

    "release_date_global": "2019-09-20",
    "release_date_india": "2019-09-27",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.1,
    "display_type": "Liquid Retina IPS LCD",
    "display_resolution": "1792x828",
    "display_refresh_rate_hz": 60,
    "display_protection": "Ion-strengthened glass",
    "display_peak_brightness_nits": 625,
    "display_hdr_support": "HDR10; Dolby Vision",

    "rear_camera_count": 2,
    "rear_main_mp": 12,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": pd.NA,
    "rear_main_ois": True,

    "rear_ultrawide_mp": 12,
    "rear_ultrawide_aperture": "f/2.4",

    "rear_telephoto_mp": pd.NA,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,

    "rear_video_max": "4K@60fps",

    "front_camera_mp": 12,
    "front_camera_aperture": "f/2.2",
    "front_camera_af": False,
    "front_video_max": "4K@60fps",

    "battery_type": "Li-Ion",
    "wired_charging_w": pd.NA,
    "wireless_charging_w": 7.5,
    "reverse_wireless_charging_w": 0,
    "battery_removable": False,

    "dimensions_mm": "150.9 x 75.7 x 8.3",
    "weight_g": 194,

    "build_frame": "Aluminum",
    "build_back": "Glass",
    "ip_rating": "IP68",
    "colors_available": "Black; Green; Yellow; Purple; Red; White",

    "sim_type": "Nano-SIM + eSIM",
    "five_g_bands": pd.NA,
    "wifi_standard": "Wi-Fi 6",
    "bluetooth_version": "5.0",
    "usb_version": pd.NA,
    "usb_type": "Lightning",
    "audio_jack": False,

    "os_launch": "iOS 13",
    "os_current": pd.NA,
    "os_update_policy_years": pd.NA,

    "official_product_url": pd.NA,
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": pd.NA,

    "launch_price_inr_official": 64900,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA
}

df = pd.read_csv(CSV_PATH)

df = df[df["phone_id"] != 34]

new_row = pd.DataFrame([row], columns=COLUMNS)
df = pd.concat([df, new_row], ignore_index=True)

df.to_csv(CSV_PATH, index=False)

print("Phone 34 added successfully.")
print(df[df["phone_id"] == 34].T)