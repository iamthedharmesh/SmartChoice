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
    "phone_id": 28,
    "canonical_name": "Apple iPhone 14 Pro Max",
    "model_id": "A2893",

    "release_date_global": "2022-09-16",
    "release_date_india": "2022-09-16",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.7,
    "display_type": "LTPO Super Retina XDR OLED",
    "display_resolution": "2796x1290",
    "display_refresh_rate_hz": 120,
    "display_protection": "Ceramic Shield",
    "display_peak_brightness_nits": 2000,
    "display_hdr_support": True,

    "rear_camera_count": 3,
    "rear_main_mp": 48,
    "rear_main_aperture": "f/1.78",
    "rear_main_sensor": "Sony",
    "rear_main_ois": True,

    "rear_ultrawide_mp": 12,
    "rear_ultrawide_aperture": "f/2.2",

    "rear_telephoto_mp": 12,
    "rear_telephoto_aperture": "f/2.8",
    "rear_telephoto_optical_zoom": "3x",

    "rear_video_max": "4K@60fps",

    "front_camera_mp": 12,
    "front_camera_aperture": "f/1.9",
    "front_camera_af": True,
    "front_video_max": "4K@60fps",

    "battery_type": "Li-Ion",
    "wired_charging_w": pd.NA,
    "wireless_charging_w": 15,
    "reverse_wireless_charging_w": 0,
    "battery_removable": False,

    "dimensions_mm": "160.7 x 77.6 x 7.85",
    "weight_g": 240,

    "build_frame": "Stainless Steel",
    "build_back": "Glass",
    "ip_rating": "IP68",
    "colors_available": "Space Black; Silver; Gold; Deep Purple",

    "sim_type": "Nano-SIM + eSIM",
    "five_g_bands": pd.NA,
    "wifi_standard": "Wi-Fi 6",
    "bluetooth_version": "5.3",
    "usb_version": pd.NA,
    "usb_type": "Lightning",
    "audio_jack": False,

    "os_launch": "iOS 16",
    "os_current": pd.NA,
    "os_update_policy_years": pd.NA,

    "official_product_url": "https://www.apple.com/in/iphone-14-pro/",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": pd.NA,

    "launch_price_inr_official": 139900,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA
}

df = pd.read_csv(CSV_PATH)

df = df[df["phone_id"] != 28]

new_row = pd.DataFrame([row], columns=COLUMNS)
df = pd.concat([df, new_row], ignore_index=True)

df.to_csv(CSV_PATH, index=False)

print("Phone 28 added successfully.")
print(df[df["phone_id"] == 28].T)