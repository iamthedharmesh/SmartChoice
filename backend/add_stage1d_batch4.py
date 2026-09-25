import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

DATA = Path("data")
ENRICHED = DATA / "phones_enriched.csv"
SOURCES = DATA / "phone_enrichment_sources.csv"

models = {
    "Apple iPhone 13 Pro Max": {
        "ids": [162, 683, 757],
        "model_id": "A2643",
        "release_date_global": "2021-09-14",
        "availability_status_india": "Released",
        "display_size_inch": 6.7,
        "display_type": "Super Retina XDR OLED",
        "display_resolution": "2778 x 1284",
        "display_refresh_rate_hz": "60",
        "display_protection": "Ceramic Shield",
        "display_hdr_support": "HDR10, Dolby Vision",
        "rear_camera_count": 3,
        "rear_main_mp": 12,
        "rear_main_aperture": "f/1.5",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 12,
        "rear_telephoto_mp": 12,
        "rear_telephoto_optical_zoom": "3x",
        "rear_video_max": "4K@60fps",
        "front_camera_mp": 12,
        "front_camera_aperture": "f/2.2",
        "front_camera_af": "Yes",
        "front_video_max": "4K@60fps",
        "battery_type": "Li-Ion",
        "wired_charging_w": 20,
        "wireless_charging_w": 15,
        "battery_removable": "No",
        "dimensions_mm": "160.8 x 78.1 x 7.65",
        "weight_g": 240,
        "build_frame": "Stainless steel",
        "build_back": "Glass",
        "ip_rating": "IP68",
        "colors_available": "Graphite, Gold, Silver, Sierra Blue, Alpine Green",
        "sim_type": "Nano-SIM + eSIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.0",
        "usb_type": "Lightning",
        "os_launch": "iOS 15",
        "official_product_url": "https://www.apple.com/in/iphone-13-pro/specs/",
        "source_url": "https://www.apple.com/in/iphone-13-pro/specs/"
    },

    "Motorola Edge 30 5G": {
        "ids": [86, 223],
        "model_id": "XT2203-1",
        "release_date_global": "2022-04-07",
        "availability_status_india": "Released",
        "display_size_inch": 6.5,
        "display_type": "OLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "144",
        "display_hdr_support": "HDR10+",
        "rear_camera_count": 3,
        "rear_main_mp": 50,
        "rear_main_aperture": "f/1.8",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 50,
        "front_camera_mp": 32,
        "front_camera_aperture": "f/2.25",
        "battery_type": "Li-Po",
        "wired_charging_w": 33,
        "battery_removable": "No",
        "dimensions_mm": "159.38 x 74.236 x 6.79",
        "weight_g": 155,
        "build_frame": "Plastic",
        "build_back": "Plastic",
        "colors_available": "Meteor Grey, Aurora White, Supermoon Silver",
        "sim_type": "Dual Nano-SIM",
        "five_g_bands": "n1/n3/n5/n7/n8/n20/n28/n38/n40/n41/n66/n77/n78",
        "wifi_standard": "Wi-Fi 6E",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.motorola.in/smartphones-motorola-edge-30/p",
        "source_url": "https://www.motorola.in/smartphones-motorola-edge-30/p"
    },

    "POCO X4 GT 5G": {
        "ids": [492, 978],
        "model_id": "22041216G",
        "release_date_global": "2022-06-23",
        "availability_status_india": "Not officially launched",
        "display_size_inch": 6.6,
        "display_type": "LCD",
        "display_resolution": "2460 x 1080",
        "display_refresh_rate_hz": "144",
        "display_peak_brightness_nits": 650,
        "display_protection": "Corning Gorilla Glass 5",
        "rear_camera_count": 3,
        "rear_main_mp": 64,
        "rear_main_aperture": "f/1.89",
        "rear_ultrawide_mp": 8,
        "front_camera_mp": 20,
        "battery_type": "Li-Po",
        "wired_charging_w": 67,
        "battery_removable": "No",
        "dimensions_mm": "163.6 x 74.3 x 8.9",
        "weight_g": 200,
        "build_back": "Glass",
        "colors_available": "Black, Blue, Silver",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.3",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.po.co/global/poco-x4-gt/specs",
        "source_url": "https://www.po.co/global/poco-x4-gt/specs"
    },

    "Samsung Galaxy A52": {
        "ids": [564, 437],
        "model_id": "SM-A525F",
        "release_date_global": "2021-03-17",
        "availability_status_india": "Released",
        "display_size_inch": 6.5,
        "display_type": "Super AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "90",
        "display_peak_brightness_nits": 800,
        "display_protection": "Corning Gorilla Glass 5",
        "rear_camera_count": 4,
        "rear_main_mp": 64,
        "rear_main_aperture": "f/1.8",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 12,
        "rear_telephoto_mp": 5,
        "front_camera_mp": 32,
        "front_camera_aperture": "f/2.2",
        "battery_type": "Li-Po",
        "wired_charging_w": 25,
        "battery_removable": "No",
        "dimensions_mm": "159.9 x 75.1 x 8.4",
        "weight_g": 189,
        "build_back": "Plastic",
        "ip_rating": "IP67",
        "colors_available": "Awesome Black, Awesome White, Awesome Violet, Awesome Blue",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 5",
        "bluetooth_version": "5.0",
        "usb_type": "USB Type-C",
        "os_launch": "Android 11",
        "official_product_url": "https://news.samsung.com/in/samsung-launches-galaxy-a52-and-galaxy-a72-in-india-makes-exciting-innovations-accessible-to-all",
        "source_url": "https://news.samsung.com/in/samsung-launches-galaxy-a52-and-galaxy-a72-in-india-makes-exciting-innovations-accessible-to-all"
    },

    "Samsung Galaxy S22 5G": {
        "ids": [108, 537],
        "model_id": "SM-S901E",
        "release_date_global": "2022-02-09",
        "availability_status_india": "Released",
        "display_size_inch": 6.1,
        "display_type": "Dynamic AMOLED 2X",
        "display_resolution": "2340 x 1080",
        "display_refresh_rate_hz": "120",
        "display_peak_brightness_nits": 1300,
        "rear_camera_count": 3,
        "rear_main_mp": 50,
        "rear_main_aperture": "f/1.8",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 12,
        "rear_telephoto_mp": 10,
        "rear_telephoto_optical_zoom": "3x",
        "front_camera_mp": 10,
        "front_camera_aperture": "f/2.2",
        "battery_type": "Li-Ion",
        "wired_charging_w": 25,
        "wireless_charging_w": 15,
        "battery_removable": "No",
        "dimensions_mm": "146.0 x 70.6 x 7.6",
        "weight_g": 168,
        "build_frame": "Armor Aluminum",
        "build_back": "Gorilla Glass Victus+",
        "ip_rating": "IP68",
        "colors_available": "Phantom Black, White, Green, Pink Gold",
        "sim_type": "Nano-SIM + eSIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.samsung.com/in/support/mobile-devices/enjoy-the-epic-standard-of-smartphone-experiences-with-the-galaxy-s22-series/",
        "source_url": "https://www.samsung.com/in/support/mobile-devices/enjoy-the-epic-standard-of-smartphone-experiences-with-the-galaxy-s22-series/"
    },

    "vivo V23 5G": {
        "ids": [126, 72],
        "model_id": "V2130",
        "release_date_global": "2022-01-05",
        "availability_status_india": "Released",
        "display_size_inch": 6.44,
        "display_type": "AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "90",
        "rear_camera_count": 3,
        "rear_main_mp": 64,
        "rear_main_aperture": "f/1.89",
        "rear_ultrawide_mp": 8,
        "front_camera_mp": 50,
        "front_camera_aperture": "f/2.0",
        "battery_type": "Li-Po",
        "wired_charging_w": 44,
        "battery_removable": "No",
        "dimensions_mm": "157.2 x 72.42 x 7.39",
        "weight_g": 179,
        "build_back": "Glass",
        "colors_available": "Sunshine Gold, Stardust Black",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 5",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.vivo.com/in/products/param/v235g",
        "source_url": "https://www.vivo.com/in/products/param/v235g"
    },

    "vivo V23 Pro 5G": {
        "ids": [218, 423],
        "model_id": "V2132",
        "release_date_global": "2022-01-05",
        "availability_status_india": "Released",
        "display_size_inch": 6.56,
        "display_type": "AMOLED",
        "display_resolution": "2376 x 1080",
        "display_refresh_rate_hz": "90",
        "rear_camera_count": 3,
        "rear_main_mp": 108,
        "rear_main_aperture": "f/1.88",
        "rear_ultrawide_mp": 8,
        "front_camera_mp": 50,
        "front_camera_aperture": "f/2.0",
        "battery_type": "Li-Po",
        "wired_charging_w": 44,
        "battery_removable": "No",
        "dimensions_mm": "159.46 x 73.27 x 7.39",
        "weight_g": 171,
        "build_back": "Glass",
        "colors_available": "Sailing Blue, Sunshine Gold",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 5",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.vivo.com/in/products/param/v23pro",
        "source_url": "https://www.vivo.com/in/products/param/v23pro"
    },

    "Xiaomi 11i HyperCharge 5G": {
        "ids": [581, 922],
        "model_id": "21091116I",
        "release_date_global": "2022-01-06",
        "availability_status_india": "Released",
        "display_size_inch": 6.67,
        "display_type": "AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "120",
        "display_peak_brightness_nits": 1200,
        "rear_camera_count": 3,
        "rear_main_mp": 108,
        "rear_main_aperture": "f/1.9",
        "rear_ultrawide_mp": 8,
        "front_camera_mp": 16,
        "battery_type": "Li-Po",
        "wired_charging_w": 120,
        "battery_removable": "No",
        "dimensions_mm": "163.65 x 76.15 x 8.12",
        "weight_g": 207,
        "build_back": "Glass",
        "colors_available": "Pacific Pearl, Stealth Black, Purple Mist, Camo Green",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 802.11ac",
        "bluetooth_version": "5.1",
        "usb_type": "USB Type-C",
        "os_launch": "Android 11",
        "official_product_url": "https://www.mi.com/in/product/xiaomi-11i-hypercharge-5g/specs/",
        "source_url": "https://www.mi.com/in/product/xiaomi-11i-hypercharge-5g/specs/"
    },

    "Xiaomi Mi 11 Lite NE 5G": {
        "ids": [304, 467],
        "model_id": "2109119DI",
        "release_date_global": "2021-09-15",
        "availability_status_india": "Released",
        "display_size_inch": 6.55,
        "display_type": "AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "90",
        "display_peak_brightness_nits": 800,
        "rear_camera_count": 3,
        "rear_main_mp": 64,
        "rear_main_aperture": "f/1.79",
        "rear_ultrawide_mp": 8,
        "front_camera_mp": 20,
        "battery_type": "Li-Po",
        "wired_charging_w": 33,
        "battery_removable": "No",
        "dimensions_mm": "160.53 x 75.73 x 6.81",
        "weight_g": 158,
        "build_back": "Glass",
        "colors_available": "Diamond Dazzle, Tuscany Coral, Vinyl Black",
        "sim_type": "Hybrid Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 5",
        "bluetooth_version": "5.1",
        "usb_type": "USB Type-C",
        "os_launch": "Android 11",
        "official_product_url": "https://www.mi.com/in/product/xiaomi-11-lite-ne-5g/specs/",
        "source_url": "https://www.mi.com/in/product/xiaomi-11-lite-ne-5g/specs/"
    },

    "iQOO 7": {
        "ids": [147, 546],
        "model_id": "I2012",
        "release_date_global": "2021-01-11",
        "availability_status_india": "Released",
        "display_size_inch": 6.62,
        "display_type": "AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "120",
        "rear_camera_count": 3,
        "rear_main_mp": 48,
        "rear_main_aperture": "f/1.79",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 13,
        "rear_telephoto_mp": 2,
        "front_camera_mp": 16,
        "battery_type": "Li-Po",
        "wired_charging_w": 66,
        "battery_removable": "No",
        "dimensions_mm": "162.2 x 75.8 x 8.7",
        "weight_g": 196,
        "build_back": "Glass",
        "colors_available": "Solid Ice Blue, Storm Black",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 11",
        "official_product_url": "https://www.iqoo.com/in/products/param/iqoo7",
        "source_url": "https://www.iqoo.com/in/products/param/iqoo7"
    }
}

enriched = pd.read_csv(ENRICHED)
sources = pd.read_csv(SOURCES)
base = pd.read_csv(DATA / "phones.csv")

expected_ids = [pid for spec in models.values() for pid in spec["ids"]]

existing = set(enriched["phone_id"].astype(int))

duplicates = sorted(set(expected_ids) & existing)
if duplicates:
    raise SystemExit(f"ERROR: Already enriched: {duplicates}")

base_ids = set(base["phone_id"].astype(int))
missing_base = sorted(set(expected_ids) - base_ids)

if missing_base:
    raise SystemExit(f"ERROR: Missing from phones.csv: {missing_base}")

before_count = len(enriched)

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
        "notes": f"Primary manufacturer source. Applied to catalog variants: {spec['ids']}"
    })

enriched = pd.concat(
    [enriched, pd.DataFrame(new_rows)],
    ignore_index=True
)

sources = pd.concat(
    [sources, pd.DataFrame(source_rows)],
    ignore_index=True
)

enriched.to_csv(ENRICHED, index=False)
sources.to_csv(SOURCES, index=False)

# Hard post-write checks
after_ids = set(enriched["phone_id"].astype(int))

missing_after = sorted(set(expected_ids) - after_ids)

if missing_after:
    raise SystemExit(f"ERROR AFTER WRITE: {missing_after}")

if len(after_ids) != len(enriched):
    raise SystemExit("ERROR AFTER WRITE: Duplicate phone IDs detected.")

added_count = len(enriched) - before_count

if added_count != len(expected_ids):
    raise SystemExit(
        f"ERROR AFTER WRITE: expected {len(expected_ids)}, "
        f"added {added_count}"
    )

print("=== BATCH ENRICHMENT SUCCESS ===")
print(f"Models processed: {len(models)}")
print(f"Rows added: {added_count}")
print(f"Enriched rows before: {before_count}")
print(f"Enriched rows after: {len(enriched)}")
print(f"Source audit rows: {len(sources)}")
print(f"Backup timestamp: {stamp}")
print("Verified IDs:", sorted(expected_ids))
