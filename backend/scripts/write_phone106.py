from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
ENRICHED = BASE_DIR / "data" / "phones_enriched.csv"

PHONE_ID = 106

row = {
    "phone_id": 106,
    "canonical_name": "Xiaomi 13 Pro 5G",
    "model_id": "2210132G (Global), 2210132C (China)",

    "release_date_global": "2022-12-14",
    "release_date_india": "2023-03-10",
    "availability_status_india": "",
    "discontinued_date_india": "",

    "display_size_inch": 6.73,
    "display_type": "LTPO AMOLED, 120Hz, Dolby Vision, HDR10+, 1B colors",
    "display_resolution": "3200 x 1440 (WQHD+)",
    "display_refresh_rate_hz": 120,
    "display_protection": "Corning Gorilla Glass Victus",
    "display_peak_brightness_nits": 1900,
    "display_hdr_support": "Dolby Vision, HDR10+",

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.9",
    "rear_main_sensor": "Sony IMX989, 1-inch, 3.2µm 4-in-1 pixel size",
    "rear_main_ois": "Yes (HyperOIS)",
    "rear_ultrawide_mp": 50,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": 50,
    "rear_telephoto_aperture": "f/2.0",
    "rear_telephoto_optical_zoom": "3.2x (75mm floating telephoto)",
    "rear_video_max": "8K@24fps, 4K@30/60fps, 1080p@30/60fps, Dolby Vision HDR",

    "front_camera_mp": 32,
    "front_camera_aperture": "f/2.0",
    "front_camera_af": "",
    "front_video_max": "",

    "battery_type": "Li-Po",
    "wired_charging_w": 120,
    "wireless_charging_w": 50,
    "reverse_wireless_charging_w": 10,
    "battery_removable": "No",

    "dimensions_mm": "162.9 x 74.6 x 8.38",
    "weight_g": 229,
    "build_frame": "Aluminum",
    "build_back": "Ceramic back (3D bio-ceramic)",
    "ip_rating": "IP68",
    "colors_available": "Ceramic Black, Ceramic White",

    "sim_type": "Dual SIM (Nano + Nano or Nano + eSIM)",
    "five_g_bands": "n1, n3, n5, n7, n8, n20, n28, n38, n40, n41, n66, n71, n75, n77, n78, n79 (SA/NSA)",
    "wifi_standard": "Wi-Fi 7 (802.11 a/b/g/n/ac/ax/be)",
    "bluetooth_version": "5.3",
    "usb_version": "2.0 (480 Mbps)",
    "usb_type": "USB Type-C",
    "audio_jack": "No",

    "os_launch": "Android 13, MIUI 14",
    "os_current": "HyperOS 3.1 (Android 16)",
    "os_update_policy_years": "3 Years of Android Updates / 5 Years of Security Updates",

    "official_product_url": "https://www.mi.com/in/product/xiaomi-13-pro-5g/",
    "official_image_url": "",
    "local_image_path": "",
    "gsmarena_url": "https://www.gsmarena.com/xiaomi_13_pro-11962.php",

    "launch_price_inr_official": 79999,
    "current_min_price_inr": "",
    "price_updated_at": "",
}

df = pd.read_csv(ENRICHED, dtype=str)

# Remove the previously written Phone 106 row.
df = df[df["phone_id"].astype(str) != str(PHONE_ID)].copy()

# Make sure every CSV column exists in the row.
for col in df.columns:
    if col not in row:
        row[col] = ""

# Add Phone 106 using the EXACT existing 57-column schema.
new_row = pd.DataFrame(
    [[row[col] for col in df.columns]],
    columns=df.columns
)

df = pd.concat([df, new_row], ignore_index=True)

# Keep phone IDs numeric and sorted.
df["phone_id"] = pd.to_numeric(df["phone_id"], errors="coerce")
df = df.sort_values("phone_id").reset_index(drop=True)

df.to_csv(ENRICHED, index=False)

print("Phone 106 written successfully.")
print(f"Total enriched rows: {len(df)}")
print()

phone = df[df["phone_id"] == PHONE_ID]

print(
    phone[
        [
            "phone_id",
            "canonical_name",
            "model_id",
            "display_size_inch",
            "rear_main_sensor",
            "rear_telephoto_mp",
            "rear_telephoto_optical_zoom",
            "wired_charging_w",
            "wireless_charging_w",
            "os_current",
            "os_update_policy_years",
            "launch_price_inr_official",
            "current_min_price_inr",
        ]
    ].to_string(index=False)
)