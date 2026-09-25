import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

DATA = Path("data")
ENRICHED = DATA / "phones_enriched.csv"
SOURCES = DATA / "phone_enrichment_sources.csv"

# 22 valid catalog rows.
# 443 is intentionally excluded because its 6GB+128GB Redmi Note 12 Pro+
# configuration is not supported by Xiaomi India's verified configuration list.

models = {
    "Honor 70 5G": {
        "ids": [421, 503],
        "model_id": "REA-NX9",
        "release_date_global": "2022-05-30",
        "display_size_inch": 6.67,
        "display_type": "OLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "120",
        "rear_camera_count": 3,
        "rear_main_mp": 54,
        "rear_main_aperture": "f/1.9",
        "rear_main_sensor": "Sony IMX800",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 50,
        "rear_video_max": "4K",
        "front_camera_mp": 32,
        "battery_type": "Li-Po",
        "wired_charging_w": 66,
        "battery_removable": "No",
        "dimensions_mm": "161.4 x 73.3 x 7.91",
        "weight_g": 178,
        "build_back": "Glass",
        "colors_available": "Crystal Silver, Icelandic Frost, Midnight Black",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.honor.com/in/phones/honor-70/",
        "source_url": "https://www.honor.com/in/phones/honor-70/spec/",
    },

    "Samsung Galaxy S21 FE 5G": {
        "ids": [36, 367],
        "model_id": "SM-G990E",
        "release_date_global": "2022-01-04",
        "display_size_inch": 6.4,
        "display_type": "Dynamic AMOLED 2X",
        "display_resolution": "2340 x 1080",
        "display_refresh_rate_hz": "120",
        "display_peak_brightness_nits": 1200,
        "rear_camera_count": 3,
        "rear_main_mp": 12,
        "rear_main_aperture": "f/1.8",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 12,
        "rear_telephoto_mp": 8,
        "rear_telephoto_optical_zoom": "3x",
        "front_camera_mp": 32,
        "battery_type": "Li-Ion",
        "wired_charging_w": 25,
        "wireless_charging_w": 15,
        "battery_removable": "No",
        "dimensions_mm": "155.7 x 74.5 x 7.9",
        "weight_g": 177,
        "build_frame": "Metal",
        "build_back": "Plastic",
        "ip_rating": "IP68",
        "colors_available": "Olive, Lavender, White, Graphite",
        "sim_type": "Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.0",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://news.samsung.com/in/meet-s21-fe-5g-flagship-smartphone-designed-for-fans-of-all-kinds",
        "source_url": "https://news.samsung.com/in/meet-s21-fe-5g-flagship-smartphone-designed-for-fans-of-all-kinds",
    },

    "vivo X80 5G": {
        "ids": [448, 802],
        "model_id": "V2144",
        "release_date_global": "2022-04-25",
        "display_size_inch": 6.78,
        "display_type": "AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "120",
        "rear_camera_count": 3,
        "rear_main_mp": 50,
        "rear_main_aperture": "f/1.75",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 12,
        "rear_telephoto_mp": 12,
        "front_camera_mp": 32,
        "front_camera_aperture": "f/2.45",
        "battery_type": "Li-Po",
        "wired_charging_w": 80,
        "battery_removable": "No",
        "dimensions_mm": "164.95 x 75.23 x 8.30",
        "weight_g": 206,
        "build_back": "Glass",
        "colors_available": "Urban Blue, Cosmic Black",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.3",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.vivo.com/in/product/productSpecification?id=406",
        "source_url": "https://www.vivo.com/in/product/productSpecification?id=406",
    },

    "Samsung Galaxy S22 Plus 5G": {
        "ids": [257, 750],
        "model_id": "SM-S906E",
        "release_date_global": "2022-02-09",
        "display_size_inch": 6.6,
        "display_type": "Dynamic AMOLED 2X",
        "display_resolution": "2340 x 1080",
        "display_refresh_rate_hz": "120",
        "rear_camera_count": 3,
        "rear_main_mp": 50,
        "rear_main_ois": "Yes",
        "rear_telephoto_mp": 10,
        "rear_telephoto_optical_zoom": "3x",
        "rear_ultrawide_mp": 12,
        "front_camera_mp": 10,
        "battery_type": "Li-Ion",
        "wired_charging_w": 45,
        "wireless_charging_w": 15,
        "battery_removable": "No",
        "dimensions_mm": "157.4 x 75.8 x 7.6",
        "weight_g": 195,
        "build_frame": "Armor Aluminum",
        "build_back": "Gorilla Glass Victus+",
        "ip_rating": "IP68",
        "sim_type": "Nano-SIM + eSIM",
        "wifi_standard": "Wi-Fi 6E",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.samsung.com/in/support/mobile-devices/enjoy-the-epic-standard-of-the-samsung-galaxy-s22-series/",
        "source_url": "https://www.samsung.com/in/support/mobile-devices/enjoy-the-epic-standard-of-the-samsung-galaxy-s22-series/",
    },

    "Redmi Note 11 Pro Plus 5G": {
        "ids": [42, 274, 136],
        "model_id": "2201116SI",
        "release_date_global": "2022-03-01",
        "display_size_inch": 6.67,
        "display_type": "AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "120",
        "display_peak_brightness_nits": 1200,
        "rear_camera_count": 3,
        "rear_main_mp": 108,
        "rear_main_aperture": "f/1.9",
        "rear_ultrawide_mp": 8,
        "rear_ultrawide_aperture": "f/2.2",
        "front_camera_mp": 16,
        "front_camera_aperture": "f/2.4",
        "battery_type": "Li-Po",
        "wired_charging_w": 67,
        "battery_removable": "No",
        "dimensions_mm": "163.56 x 76.03 x 8.12",
        "weight_g": 202,
        "build_back": "Glass",
        "colors_available": "Phantom White, Mirage Blue, Stealth Black",
        "sim_type": "Nano-SIM + Hybrid",
        "five_g_bands": "n1/n3/n5/n8/n28/n40/n78",
        "wifi_standard": "Wi-Fi 802.11ac",
        "bluetooth_version": "5.1",
        "usb_type": "USB Type-C",
        "os_launch": "Android 11",
        "official_product_url": "https://www.mi.com/in/product/redmi-note-11-pro-plus-5g/specs/",
        "source_url": "https://www.mi.com/in/product/redmi-note-11-pro-plus-5g/specs/",
    },

    "OnePlus 10T": {
        "ids": [74, 365, 307],
        "model_id": "CPH2413",
        "release_date_global": "2022-08-03",
        "display_size_inch": 6.7,
        "display_type": "Fluid AMOLED",
        "display_resolution": "2412 x 1080",
        "display_refresh_rate_hz": "120",
        "rear_camera_count": 3,
        "rear_main_mp": 50,
        "rear_main_aperture": "f/1.8",
        "rear_main_sensor": "Sony IMX766",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 8,
        "front_camera_mp": 16,
        "front_camera_aperture": "f/2.4",
        "battery_type": "Li-Po",
        "wired_charging_w": 150,
        "battery_removable": "No",
        "dimensions_mm": "163 x 75.4 x 8.8",
        "weight_g": 203.5,
        "build_frame": "Plastic",
        "build_back": "Glass",
        "colors_available": "Moonstone Black, Jade Green",
        "sim_type": "Dual Nano-SIM",
        "five_g_bands": "n1/n3/n5/n8/n20/n28/n38/n40/n41/n77/n78",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.oneplus.in/10t/specs",
        "source_url": "https://www.oneplus.in/10t/specs",
    },

    "Samsung Galaxy M53 5G": {
        "ids": [35, 117],
        "model_id": "SM-M536B",
        "release_date_global": "2022-04-07",
        "display_size_inch": 6.7,
        "display_type": "sAMOLED+",
        "display_resolution": "2408 x 1080",
        "display_refresh_rate_hz": "120",
        "rear_camera_count": 4,
        "rear_main_mp": 108,
        "rear_main_aperture": "f/1.8",
        "rear_ultrawide_mp": 8,
        "front_camera_mp": 32,
        "battery_type": "Li-Po",
        "wired_charging_w": 25,
        "battery_removable": "No",
        "dimensions_mm": "164.6 x 77 x 7.4",
        "weight_g": 176,
        "colors_available": "Deep Ocean Blue, Mystique Green",
        "sim_type": "Dual Nano-SIM",
        "five_g_bands": "n1/n3/n5/n8/n28/n40/n41/n77/n78",
        "wifi_standard": "Wi-Fi 5",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://news.samsung.com/in/samsung-launches-galaxy-m53-5g-with-segment-best-108-mp-quad-camera-segment-only-auto-data-switching-segment-leading-samoled-display-in-india",
        "source_url": "https://news.samsung.com/in/samsung-launches-galaxy-m53-5g-with-segment-best-108-mp-quad-camera-segment-only-auto-data-switching-segment-leading-samoled-display-in-india",
    },

    "realme X50 Pro 5G": {
        "ids": [414, 886],
        "model_id": "RMX2076",
        "release_date_global": "2020-02-24",
        "display_size_inch": 6.44,
        "display_type": "Super AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "90",
        "display_peak_brightness_nits": 1000,
        "rear_camera_count": 4,
        "rear_main_mp": 64,
        "rear_main_aperture": "f/1.8",
        "rear_ultrawide_mp": 8,
        "rear_telephoto_mp": 12,
        "rear_telephoto_optical_zoom": "2x",
        "front_camera_mp": 32,
        "battery_type": "Li-Po",
        "wired_charging_w": 65,
        "battery_removable": "No",
        "dimensions_mm": "159 x 74.2 x 8.9",
        "weight_g": 207,
        "build_frame": "Aluminum",
        "build_back": "Glass",
        "colors_available": "Rust Red, Moss Green",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.1",
        "usb_type": "USB Type-C",
        "os_launch": "Android 10",
        "official_product_url": "https://www.realme.com/in/realme-x50-pro/specs",
        "source_url": "https://www.realme.com/in/realme-x50-pro/specs",
    },

    "Nothing Phone 1": {
        "ids": [206, 134],
        "model_id": "A063",
        "release_date_global": "2022-07-12",
        "display_size_inch": 6.55,
        "display_type": "Flexible AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "60-120",
        "display_peak_brightness_nits": 1200,
        "rear_camera_count": 2,
        "rear_main_mp": 50,
        "rear_main_aperture": "f/1.88",
        "rear_main_sensor": "Sony IMX766",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 50,
        "rear_ultrawide_aperture": "f/2.2",
        "front_camera_mp": 16,
        "front_camera_aperture": "f/2.45",
        "battery_type": "Li-Ion",
        "wired_charging_w": 33,
        "wireless_charging_w": 15,
        "reverse_wireless_charging_w": 5,
        "battery_removable": "No",
        "dimensions_mm": "159.2 x 75.8 x 8.3",
        "weight_g": 193.5,
        "build_frame": "Recycled Aluminum",
        "build_back": "Glass",
        "ip_rating": "IP53",
        "colors_available": "White, Black",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://nothing.tech/pages/phone-1",
        "source_url": "https://nothing.tech/pages/phone-1",
    },

    "Redmi Note 12 Pro Plus": {
        "ids": [68],
        "model_id": "22101316I",
        "release_date_global": "2023-01-05",
        "availability_status_india": "Released",
        "display_size_inch": 6.67,
        "display_type": "AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "120",
        "display_peak_brightness_nits": 900,
        "rear_camera_count": 3,
        "rear_main_mp": 200,
        "rear_main_aperture": "f/1.65",
        "rear_main_sensor": "Samsung HPX",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 8,
        "rear_ultrawide_aperture": "f/2.2",
        "front_camera_mp": 16,
        "battery_type": "Li-Po",
        "wired_charging_w": 120,
        "battery_removable": "No",
        "dimensions_mm": "162.9 x 76 x 8.9",
        "weight_g": 210,
        "build_back": "Glass",
        "colors_available": "Midnight Black, Polar White, Sky Blue",
        "sim_type": "Dual Nano-SIM",
        "five_g_bands": "10 relevant 5G bands for India",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.mi.com/in/product/redmi-note-12-pro-plus-5g/",
        "source_url": "https://www.mi.com/in/product/redmi-note-12-pro-plus-5g/",
    },
}

enriched = pd.read_csv(ENRICHED)
sources = pd.read_csv(SOURCES)
base = pd.read_csv(DATA / "phones.csv")

# Flatten model -> phone IDs
expected_ids = [pid for spec in models.values() for pid in spec["ids"]]

# Safety checks
existing = set(enriched["phone_id"].astype(int))
duplicates = sorted(set(expected_ids) & existing)

if duplicates:
    raise SystemExit(f"ERROR: These IDs are already enriched: {duplicates}")

base_ids = set(base["phone_id"].astype(int))
missing_base = sorted(set(expected_ids) - base_ids)

if missing_base:
    raise SystemExit(f"ERROR: IDs missing from phones.csv: {missing_base}")

before_count = len(enriched)

# Backups
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(
    ENRICHED,
    DATA / f"phones_enriched.csv.backup_{stamp}"
)
shutil.copy2(
    SOURCES,
    DATA / f"phone_enrichment_sources.csv.backup_{stamp}"
)

new_rows = []
source_rows = []

for canonical_name, spec in models.items():

    for phone_id in spec["ids"]:
        record = {col: pd.NA for col in enriched.columns}
        record["phone_id"] = phone_id
        record["canonical_name"] = canonical_name

        for key, value in spec.items():
            if key in ("ids", "source_url"):
                continue
            if key in record:
                record[key] = value

        new_rows.append(record)

    source_rows.append({
        "phone_id": spec["ids"][0],
        "canonical_name": canonical_name,
        "source_type": "Official manufacturer",
        "source_url": spec["source_url"],
        "match_confidence": "High",
        "notes": f"Primary manufacturer source for physical model. Applied to catalog variants: {spec['ids']}"
    })

enriched = pd.concat(
    [enriched, pd.DataFrame(new_rows)],
    ignore_index=True
)

sources = pd.concat(
    [sources, pd.DataFrame(source_rows)],
    ignore_index=True
)

# Write
enriched.to_csv(ENRICHED, index=False)
sources.to_csv(SOURCES, index=False)

# POST-WRITE VALIDATION
after_ids = set(enriched["phone_id"].astype(int))

missing_after = sorted(set(expected_ids) - after_ids)

if missing_after:
    raise SystemExit(
        f"ERROR AFTER WRITE: Missing IDs: {missing_after}"
    )

if len(after_ids) != len(enriched):
    raise SystemExit(
        "ERROR AFTER WRITE: Duplicate phone IDs detected."
    )

added_count = len(enriched) - before_count

if added_count != len(expected_ids):
    raise SystemExit(
        f"ERROR AFTER WRITE: Expected {len(expected_ids)} new rows, "
        f"but added {added_count}."
    )

print("=== BATCH ENRICHMENT SUCCESS ===")
print(f"Models processed: {len(models)}")
print(f"Rows added: {added_count}")
print(f"Enriched rows before: {before_count}")
print(f"Enriched rows after: {len(enriched)}")
print(f"Source audit rows: {len(sources)}")
print(f"Backup timestamp: {stamp}")
print("Verified IDs:")
print(expected_ids)
print("Intentionally skipped: phone_id 443")
