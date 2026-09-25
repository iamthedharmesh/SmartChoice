from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
ENRICHED = BASE_DIR / "data" / "phones_enriched.csv"

PHONE_ID = 7

row = {
    "phone_id": 7,
    "canonical_name": "Apple iPhone 14",
    "model_id": "A2882 (India/International), iPhone14,7",

    "release_date_global": "2022-09-16",
    "release_date_india": "2022-09-16",
    "availability_status_india": "",
    "discontinued_date_india": "",

    "display_size_in": 6.1,
    "display_type": "Super Retina XDR OLED",
    "display_resolution": "2532 x 1170",
    "refresh_rate_hz": 60,
    "display_protection": "Ceramic Shield",
    "peak_brightness_nits": 1200,
    "hdr_support": "HDR, Dolby Vision, HDR10",

    "rear_camera_count": 2,
    "rear_main_mp": 12,
    "rear_main_aperture": "f/1.5",
    "rear_main_sensor": "",
    "rear_main_ois": "Sensor-shift optical image stabilization",
    "rear_ultrawide_mp": 12,
    "rear_ultrawide_aperture": "f/2.4",
    "rear_telephoto_mp": "",
    "rear_telephoto_aperture": "",
    "rear_telephoto_optical_zoom": "",
    "front_camera_mp": 12,
    "front_camera_aperture": "f/1.9",
    "video_max": "4K 24/25/30/60 fps",

    "battery_type": "Li-Ion",
    "charging_wired_w": 20,
    "charging_wireless_w": 15,
    "reverse_wireless": False,
    "battery_removable": False,

    "dimensions_mm": "146.7 x 71.5 x 7.8",
    "weight_g": 172,
    "build_material": "Aluminum and glass",
    "ip_rating": "IP68",
    "colors": "Midnight, Purple, Starlight, Blue, (PRODUCT)RED, Yellow",

    "sim_type": "Nano-SIM + eSIM",
    "five_g_bands": "n1, n2, n3, n5, n7, n8, n12, n14, n20, n25, n26, n28, n29, n30, n38, n40, n41, n48, n53, n66, n70, n71, n77, n78, n79",
    "wifi": "Wi-Fi 6",
    "bluetooth": "Bluetooth 5.3",
    "usb": "Lightning, USB 2.0",
    "audio_jack": False,

    "os_launch": "iOS 16",
    "os_current": "iOS 27",
    "update_policy": "Apple iPhone 14 remains compatible with iOS 27",

    "official_product_url": "https://www.apple.com/in/iphone-14/",
    "official_image_url": "",
    "local_image_path": "",
    "gsmarena_url": "",

    "launch_price_inr": 79900,
    "current_min_price_inr": "",
    "price_updated_at": "",

    "notes": "Current India availability and current price were not verified as of September 2026."
}

df = pd.read_csv(ENRICHED, dtype=str)

# Remove an existing Phone 7 row if present.
df = df[df["phone_id"].astype(str) != str(PHONE_ID)]

# Ensure every existing column is present.
for col in df.columns:
    if col not in row:
        row[col] = ""

# Preserve the existing column order.
new_row = pd.DataFrame([[row.get(col, "") for col in df.columns]], columns=df.columns)

df = pd.concat([df, new_row], ignore_index=True)

# Keep phone IDs numeric/order-friendly.
df["phone_id"] = pd.to_numeric(df["phone_id"], errors="coerce")
df = df.sort_values("phone_id").reset_index(drop=True)

df.to_csv(ENRICHED, index=False)

print("Phone 7 written successfully.")
print(f"File: {ENRICHED}")
print(f"Total enriched rows: {len(df)}")
print()
print(df[df["phone_id"] == PHONE_ID][
    ["phone_id", "canonical_name", "model_id", "os_current",
     "five_g_bands", "availability_status_india",
     "current_min_price_inr", "price_updated_at"]
].to_string(index=False))