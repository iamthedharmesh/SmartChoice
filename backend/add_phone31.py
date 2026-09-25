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
    "phone_id": 31,
    "canonical_name": "Realme 10 Pro (8GB RAM + 128GB)",
    "model_id": "RMX3663",

    "release_date_global": "2022-11-17",
    "release_date_india": "2022-12-08",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.72,
    "display_type": "IPS LCD",
    "display_resolution": "2400x1080",
    "display_refresh_rate_hz": 120,
    "display_protection": pd.NA,
    "display_peak_brightness_nits": 680,
    "display_hdr_support": pd.NA,

    "rear_camera_count": 2,
    "rear_main_mp": 108,
    "rear_main_aperture": "f/1.75",
    "rear_main_sensor": "Samsung HM6",
    "rear_main_ois": False,

    "rear_ultrawide_mp": pd.NA,
    "rear_ultrawide_aperture": pd.NA,

    "rear_telephoto_mp": pd.NA,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,

    "rear_video_max": "1080p@30fps",

    "front_camera_mp": 16,
    "front_camera_aperture": "f/2.45",
    "front_camera_af": False,
    "front_video_max": "1080p@30fps",

    "battery_type": "Li-Ion",
    "wired_charging_w": 33,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": False,

    "dimensions_mm": "163.7 x 74.2 x 8.1",
    "weight_g": 190,

    "build_frame": "Plastic",
    "build_back": "Plastic",
    "ip_rating": pd.NA,
    "colors_available": "Hyperspace Gold; Dark Matter; Nebula Blue",

    "sim_type": "Dual Nano-SIM",
    "five_g_bands": "n1,n3,n5,n7,n8,n20,n28,n38,n40,n41,n77,n78",
    "wifi_standard": "Wi-Fi 5",
    "bluetooth_version": "5.1",
    "usb_version": "2.0",
    "usb_type": "USB Type-C",
    "audio_jack": True,

    "os_launch": "Android 13; realme UI 4.0",
    "os_current": pd.NA,
    "os_update_policy_years": "2 Android updates + 3 years security",

    "official_product_url": pd.NA,
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": pd.NA,

    "launch_price_inr_official": 18999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA
}

df = pd.read_csv(CSV_PATH)
df = df[df["phone_id"] != 31]

new_row = pd.DataFrame([row], columns=COLUMNS)
df = pd.concat([df, new_row], ignore_index=True)

df.to_csv(CSV_PATH, index=False)

print("Phone 31 added successfully.")
print(df[df["phone_id"] == 31].T)