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
    "phone_id": 25,
    "canonical_name": "vivo V26 Pro",
    "model_id": pd.NA,

    "release_date_global": pd.NA,
    "release_date_india": pd.NA,
    "availability_status_india": "Not officially launched",
    "discontinued_date_india": pd.NA,

    "display_size_inch": pd.NA,
    "display_type": pd.NA,
    "display_resolution": pd.NA,
    "display_refresh_rate_hz": pd.NA,
    "display_protection": pd.NA,
    "display_peak_brightness_nits": pd.NA,
    "display_hdr_support": pd.NA,

    "rear_camera_count": pd.NA,
    "rear_main_mp": pd.NA,
    "rear_main_aperture": pd.NA,
    "rear_main_sensor": pd.NA,
    "rear_main_ois": pd.NA,

    "rear_ultrawide_mp": pd.NA,
    "rear_ultrawide_aperture": pd.NA,

    "rear_telephoto_mp": pd.NA,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,

    "rear_video_max": pd.NA,

    "front_camera_mp": pd.NA,
    "front_camera_aperture": pd.NA,
    "front_camera_af": pd.NA,
    "front_video_max": pd.NA,

    "battery_type": pd.NA,
    "wired_charging_w": pd.NA,
    "wireless_charging_w": pd.NA,
    "reverse_wireless_charging_w": pd.NA,
    "battery_removable": pd.NA,

    "dimensions_mm": pd.NA,
    "weight_g": pd.NA,

    "build_frame": pd.NA,
    "build_back": pd.NA,
    "ip_rating": pd.NA,
    "colors_available": pd.NA,

    "sim_type": pd.NA,
    "five_g_bands": pd.NA,
    "wifi_standard": pd.NA,
    "bluetooth_version": pd.NA,
    "usb_version": pd.NA,
    "usb_type": pd.NA,
    "audio_jack": pd.NA,

    "os_launch": pd.NA,
    "os_current": pd.NA,
    "os_update_policy_years": pd.NA,

    "official_product_url": pd.NA,
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": pd.NA,

    "launch_price_inr_official": pd.NA,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA
}

df = pd.read_csv(CSV_PATH)

df = df[df["phone_id"] != 25]

new_row = pd.DataFrame([row], columns=COLUMNS)
df = pd.concat([df, new_row], ignore_index=True)

df.to_csv(CSV_PATH, index=False)

print("Phone 25 added successfully.")
print(df[df["phone_id"] == 25].T)