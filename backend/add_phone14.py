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
    "phone_id": 14,
    "canonical_name": "vivo T1 5G",
    "model_id": "V2153",

    "release_date_global": "2022-02-09",
    "release_date_india": "2022-02-09",
    "availability_status_india": "Released",
    "discontinued_date_india": pd.NA,

    "display_size_inch": 6.58,
    "display_type": "LCD",
    "display_resolution": "2408x1080",
    "display_refresh_rate_hz": 120,
    "display_protection": pd.NA,
    "display_peak_brightness_nits": pd.NA,
    "display_hdr_support": pd.NA,

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": pd.NA,
    "rear_main_ois": False,

    "rear_ultrawide_mp": pd.NA,
    "rear_ultrawide_aperture": pd.NA,

    # The other two cameras are macro/depth rather than telephoto.
    "rear_telephoto_mp": pd.NA,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,

    "rear_video_max": "1080p@30fps",

    "front_camera_mp": 16,
    "front_camera_aperture": "f/2.0",
    "front_camera_af": False,
    "front_video_max": "1080p@30fps",

    "battery_type": pd.NA,
    "wired_charging_w": 18,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": False,

    "dimensions_mm": "164.00 x 75.60 x 8.25",
    "weight_g": 187,

    "build_frame": "Plastic",
    "build_back": "Plastic",
    "ip_rating": pd.NA,
    "colors_available": "Rainbow Fantasy; Starlight Black",

    "sim_type": "Dual Nano-SIM",
    "five_g_bands": "n1,n3,n5,n8,n28,n38,n40,n41,n77,n78",
    "wifi_standard": "Wi-Fi 5",
    "bluetooth_version": "5.1",
    "usb_version": "2.0",
    "usb_type": "USB Type-C",
    "audio_jack": True,

    "os_launch": "Android 12; Funtouch OS 12",
    "os_current": pd.NA,
    "os_update_policy_years": pd.NA,

    "official_product_url": "https://www.vivo.com/in/products/t1-5g",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": pd.NA,

    "launch_price_inr_official": 16990,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA
}

df = pd.read_csv(CSV_PATH)

# Remove existing Phone 14 if present
df = df[df["phone_id"] != 14]

new_row = pd.DataFrame([row], columns=COLUMNS)
df = pd.concat([df, new_row], ignore_index=True)

df.to_csv(CSV_PATH, index=False)

print("Phone 14 added successfully.")
print(df[df["phone_id"] == 14].T)