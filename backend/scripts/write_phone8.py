from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
ENRICHED = BASE_DIR / "data" / "phones_enriched.csv"

PHONE_ID = 8

row = {
    "phone_id": 8,
    "canonical_name": "Xiaomi Redmi Note 12 Pro Plus 5G",
    "model_id": "22101316UP (India), 22101316UG (Global), 22101316UCP (China)",

    "release_date_global": "2022-11-01",
    "release_date_india": "2023-01-11",
    "availability_status_india": "",
    "discontinued_date_india": "",

    "display_size_inch": 6.67,
    "display_type": "Flow AMOLED, 120Hz, HDR10+, Dolby Vision, 10-bit (1B colors)",
    "display_resolution": "2400 x 1080 (FHD+)",
    "display_refresh_rate_hz": 120,
    "display_protection": "Corning Gorilla Glass 5",
    "display_peak_brightness_nits": 900,
    "display_hdr_support": "HDR10+, Dolby Vision",

    "rear_camera_count": 3,
    "rear_main_mp": 200,
    "rear_main_aperture": "f/1.65",
    "rear_main_sensor": "Samsung HPX, 1/1.4\", 16-in-1 binning to 2.24µm",
    "rear_main_ois": "Yes (Super OIS)",
    "rear_ultrawide_mp": 8,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": "",
    "rear_telephoto_aperture": "",
    "rear_telephoto_optical_zoom": "",
    "rear_video_max": "4K@30fps, 1080p@30/60fps, 720p@30/120/240/960fps",

    "front_camera_mp": 16,
    "front_camera_aperture": "f/2.0",
    "front_camera_af": "",
    "front_video_max": "",

    "battery_type": "Li-Po",
    "wired_charging_w": 120,
    "wireless_charging_w": 0,
    "reverse_wireless_charging_w": 0,
    "battery_removable": "No",

    "dimensions_mm": "162.9 x 76.0 x 8.98",
    "weight_g": 208,
    "build_frame": "Plastic",
    "build_back": "Glass",
    "ip_rating": "IP53",
    "colors_available": "Arctic White, Iceberg Blue, Obsidian Black",

    "sim_type": "Dual SIM (Nano + Nano, hybrid slot with microSD)",
    "five_g_bands": "n1, n3, n5, n8, n28a, n38, n40, n41, n77, n78 (SA/NSA)",
    "wifi_standard": "Wi-Fi 6 (802.11 a/b/g/n/ac/ax)",
    "bluetooth_version": "5.2",
    "usb_version": "2.0",
    "usb_type": "USB Type-C",
    "audio_jack": "Yes, 3.5mm",

    "os_launch": "Android 12, MIUI 13",
    "os_current": "HyperOS 2.0 (Android 14)",
    "os_update_policy_years": "2 Years of Software Updates / 4 Years of Security Updates",

    "official_product_url": "https://www.mi.com/in/product/redmi-note-12-pro-plus-5g/",
    "official_image_url": "",
    "local_image_path": "",
    "gsmarena_url": "https://www.gsmarena.com/xiaomi_redmi_note_12_pro+-11954.php",

    "launch_price_inr_official": 29999,
    "current_min_price_inr": "",
    "price_updated_at": "",
}

df = pd.read_csv(ENRICHED, dtype=str)

# Remove existing Phone 8 if the script was previously run.
df = df[df["phone_id"].astype(str) != str(PHONE_ID)].copy()

# Preserve the exact existing 57-column schema.
for col in df.columns:
    if col not in row:
        row[col] = ""

new_row = pd.DataFrame(
    [[row[col] for col in df.columns]],
    columns=df.columns
)

df = pd.concat([df, new_row], ignore_index=True)

df["phone_id"] = pd.to_numeric(df["phone_id"], errors="coerce")
df = df.sort_values("phone_id").reset_index(drop=True)

df.to_csv(ENRICHED, index=False)

print("Phone 8 written successfully.")
print(f"Total enriched rows: {len(df)}")
print()

phone = df[df["phone_id"] == PHONE_ID]

print(
    phone[
        [
            "phone_id",
            "canonical_name",
            "model_id",
            "release_date_global",
            "release_date_india",
            "display_size_inch",
            "rear_main_mp",
            "rear_main_sensor",
            "rear_telephoto_mp",
            "wired_charging_w",
            "wireless_charging_w",
            "os_current",
            "os_update_policy_years",
            "launch_price_inr_official",
            "current_min_price_inr",
        ]
    ].to_string(index=False)
)