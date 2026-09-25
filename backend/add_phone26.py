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
    "phone_id": 26,
    "canonical_name": "Samsung Galaxy S20 FE 5G",
    "model_id": "SM-G781B",

    "release_date_global": "2021-01-29",
    "release_date_india": "2021-03-30",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.5,
    "display_type": "Super AMOLED",
    "display_resolution": "2400x1080",
    "display_refresh_rate_hz": 120,
    "display_protection": "Corning Gorilla Glass 3",
    "display_peak_brightness_nits": 1200,
    "display_hdr_support": True,

    "rear_camera_count": 3,
    "rear_main_mp": 12,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": pd.NA,
    "rear_main_ois": True,

    "rear_ultrawide_mp": 12,
    "rear_ultrawide_aperture": "f/2.2",

    "rear_telephoto_mp": 8,
    "rear_telephoto_aperture": "f/2.4",
    "rear_telephoto_optical_zoom": "3x",

    "rear_video_max": "4K@60fps",

    "front_camera_mp": 32,
    "front_camera_aperture": "f/2.2",
    "front_camera_af": False,
    "front_video_max": "4K@30fps",

    "battery_type": "Li-Ion",
    "wired_charging_w": 25,
    "wireless_charging_w": 15,
    "reverse_wireless_charging_w": 4.5,
    "battery_removable": False,

    "dimensions_mm": "159.8 x 74.5 x 8.4",
    "weight_g": 190,

    "build_frame": "Aluminum",
    "build_back": "Plastic",
    "ip_rating": "IP68",
    "colors_available": "Cloud Navy; Cloud Red; Cloud Lavender; Cloud Mint; Cloud White",

    "sim_type": "Hybrid Dual Nano-SIM",
    "five_g_bands": "n1,n3,n5,n7,n8,n20,n28,n38,n40,n41,n66,n77,n78",
    "wifi_standard": "Wi-Fi 6",
    "bluetooth_version": "5.0",
    "usb_version": "3.2",
    "usb_type": "USB Type-C",
    "audio_jack": False,

    "os_launch": "Android 11; One UI 3.1",
    "os_current": pd.NA,
    "os_update_policy_years": "3 Android updates + 4 years security",

    "official_product_url": "https://www.samsung.com/in/support/model/SM-G781BZBDEUA/",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": pd.NA,

    "launch_price_inr_official": 47999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA
}

df = pd.read_csv(CSV_PATH)

df = df[df["phone_id"] != 26]

new_row = pd.DataFrame([row], columns=COLUMNS)
df = pd.concat([df, new_row], ignore_index=True)

df.to_csv(CSV_PATH, index=False)

print("Phone 26 added successfully.")
print(df[df["phone_id"] == 26].T)