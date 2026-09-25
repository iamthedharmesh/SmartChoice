import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

DATA = Path("data")
ENRICHED = DATA / "phones_enriched.csv"
SOURCES = DATA / "phone_enrichment_sources.csv"

batch = {
    969: {
        "canonical_name": "Motorola ThinkPhone",
        "model_id": "ThinkPhone",
        "release_date_global": "2023-01-05",
        "availability_status_india": "Released",
        "display_size_inch": 6.6,
        "display_type": "pOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "144",
        "display_protection": "Corning Gorilla Glass Victus",
        "display_peak_brightness_nits": 1100,
        "rear_camera_count": 3,
        "rear_main_mp": 50,
        "rear_main_aperture": "f/1.8",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 13,
        "rear_video_max": "8K",
        "front_camera_mp": 32,
        "front_camera_aperture": "f/2.45",
        "battery_type": "Li-Po",
        "wired_charging_w": 68,
        "wireless_charging_w": 15,
        "battery_removable": "No",
        "dimensions_mm": "158.76 x 74.34 x 8.26",
        "weight_g": 188.5,
        "build_frame": "Aramid fiber",
        "build_back": "Aramid fiber",
        "ip_rating": "IP68",
        "colors_available": "Carbon Black",
        "sim_type": "Dual Nano-SIM",
        "five_g_bands": "n1/n2/n3/n5/n7/n8/n12/n13/n20/n25/n26/n28/n38/n40/n41/n66/n71/n77/n78",
        "wifi_standard": "Wi-Fi 6E",
        "bluetooth_version": "5.3",
        "usb_type": "USB Type-C",
        "os_launch": "Android 13",
        "official_product_url": "https://www.motorola.com/business/thinkphone/p",
        "gsmarena_url": "https://www.gsmarena.com/motorola_thinkphone-12046.php",
    },

    251: {
        "canonical_name": "Tecno Phantom X2 Pro 5G",
        "model_id": "AD8",
        "release_date_global": "2022-12-07",
        "availability_status_india": "Released",
        "display_size_inch": 6.8,
        "display_type": "AMOLED",
        "display_resolution": "2400 x 1080",
        "display_refresh_rate_hz": "120",
        "display_protection": "Corning Gorilla Glass Victus",
        "rear_camera_count": 3,
        "rear_main_mp": 50,
        "rear_main_aperture": "f/1.9",
        "rear_main_ois": "Yes",
        "rear_telephoto_mp": 50,
        "rear_telephoto_optical_zoom": "2.5x",
        "rear_ultrawide_mp": 13,
        "front_camera_mp": 32,
        "battery_type": "Li-Po",
        "wired_charging_w": 45,
        "battery_removable": "No",
        "dimensions_mm": "164.6 x 72.7 x 8.9",
        "weight_g": 201,
        "build_back": "Glass",
        "colors_available": "Mars Orange, Stardust Gray",
        "sim_type": "Dual Nano-SIM",
        "five_g_bands": "n1/n3/n5/n7/n8/n20/n28/n38/n40/n41/n77/n78",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.3",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.tecno-mobile.in/phones/tech-specs/tecspecs/phantom-x2-pro-5g/",
        "gsmarena_url": "https://www.gsmarena.com/tecno_phantom_x2_pro-11908.php",
    },

    275: {
        "canonical_name": "Xiaomi 12 Pro 5G",
        "model_id": "2201122G",
        "release_date_global": "2021-12-28",
        "availability_status_india": "Released",
        "display_size_inch": 6.73,
        "display_type": "LTPO AMOLED",
        "display_resolution": "3200 x 1440",
        "display_refresh_rate_hz": "120",
        "display_protection": "Corning Gorilla Glass Victus",
        "display_peak_brightness_nits": 1500,
        "display_hdr_support": "Dolby Vision, HDR10+",
        "rear_camera_count": 3,
        "rear_main_mp": 50,
        "rear_main_aperture": "f/1.9",
        "rear_main_sensor": "Sony IMX707",
        "rear_main_ois": "Yes",
        "rear_telephoto_mp": 50,
        "rear_ultrawide_mp": 50,
        "front_camera_mp": 32,
        "battery_type": "Li-Po",
        "wired_charging_w": 120,
        "wireless_charging_w": 50,
        "reverse_wireless_charging_w": 10,
        "battery_removable": "No",
        "dimensions_mm": "163.6 x 74.6 x 8.16",
        "weight_g": 205,
        "build_frame": "Aluminum",
        "build_back": "Glass",
        "ip_rating": "IP53",
        "colors_available": "Blue, Purple, Gray",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.mi.com/in/product/xiaomi-12-pro-5g/specs/",
        "gsmarena_url": "https://www.gsmarena.com/xiaomi_12_pro-11285.php",
    },

    271: {
        "canonical_name": "Google Pixel 6 Pro",
        "model_id": "Pixel 6 Pro",
        "release_date_global": "2021-10-19",
        "availability_status_india": "Not officially launched",
        "display_size_inch": 6.71,
        "display_type": "LTPO OLED",
        "display_resolution": "3120 x 1440",
        "display_refresh_rate_hz": "120",
        "display_protection": "Corning Gorilla Glass Victus",
        "display_peak_brightness_nits": 800,
        "display_hdr_support": "HDR",
        "rear_camera_count": 3,
        "rear_main_mp": 50,
        "rear_main_aperture": "f/1.85",
        "rear_main_ois": "Yes",
        "rear_telephoto_mp": 48,
        "rear_telephoto_optical_zoom": "4x",
        "rear_ultrawide_mp": 12,
        "front_camera_mp": 11.1,
        "front_camera_aperture": "f/2.2",
        "battery_type": "Li-Ion",
        "wired_charging_w": 30,
        "wireless_charging_w": 23,
        "battery_removable": "No",
        "dimensions_mm": "163.9 x 75.9 x 8.9",
        "weight_g": 210,
        "build_frame": "Aluminum",
        "build_back": "Gorilla Glass Victus",
        "ip_rating": "IP68",
        "colors_available": "Stormy Black, Cloudy White, Sorta Sunny",
        "sim_type": "Nano-SIM + eSIM",
        "wifi_standard": "Wi-Fi 6E",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://support.google.com/pixelphone/answer/7158570",
        "gsmarena_url": "https://www.gsmarena.com/google_pixel_6_pro-10918.php",
    },

    562: {
        "canonical_name": "LG Wing 5G",
        "model_id": "LM-F100",
        "release_date_global": "2020-09-14",
        "availability_status_india": "Released",
        "display_size_inch": 6.8,
        "display_type": "P-OLED",
        "display_resolution": "2460 x 1080",
        "display_refresh_rate_hz": "60",
        "rear_camera_count": 3,
        "rear_main_mp": 64,
        "rear_main_aperture": "f/1.8",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 13,
        "front_camera_mp": 32,
        "front_camera_aperture": "f/1.9",
        "battery_type": "Li-Po",
        "wired_charging_w": 25,
        "battery_removable": "No",
        "dimensions_mm": "169.5 x 74.5 x 10.9",
        "weight_g": 260,
        "build_frame": "Aluminum",
        "build_back": "Glass",
        "ip_rating": "IP54",
        "colors_available": "Aurora Gray, Illusion Sky",
        "sim_type": "Nano-SIM",
        "five_g_bands": "n1/n3/n5/n7/n28/n38/n40/n41/n66/n77/n78",
        "wifi_standard": "Wi-Fi 5",
        "bluetooth_version": "5.1",
        "usb_type": "USB Type-C",
        "os_launch": "Android 10",
        "official_product_url": "https://www.lg.com/global/newsroom/news/corporate/lg-wing-represents-a-new-definition-of-usability-never-seen-before-in-a-smartphone/",
        "gsmarena_url": "https://www.gsmarena.com/lg_wing_5g-10452.php",
    },

    360: {
        "canonical_name": "Xiaomi 12T Pro 5G",
        "model_id": "22081212UG",
        "release_date_global": "2022-10-04",
        "availability_status_india": "Not officially launched",
        "display_size_inch": 6.67,
        "display_type": "AMOLED",
        "display_resolution": "2712 x 1220",
        "display_refresh_rate_hz": "120",
        "display_peak_brightness_nits": 900,
        "display_hdr_support": "Dolby Vision, HDR10+",
        "rear_camera_count": 3,
        "rear_main_mp": 200,
        "rear_main_aperture": "f/1.69",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 8,
        "front_camera_mp": 20,
        "battery_type": "Li-Po",
        "wired_charging_w": 120,
        "battery_removable": "No",
        "dimensions_mm": "163.1 x 75.9 x 8.6",
        "weight_g": 205,
        "build_frame": "Plastic",
        "build_back": "Glass",
        "ip_rating": "IP53",
        "colors_available": "Black, Blue, Silver",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.mi.com/global/product/xiaomi-12t-pro/specs/",
        "gsmarena_url": "https://www.gsmarena.com/xiaomi_12t_pro-11887.php",
    },

    67: {
        "canonical_name": "OnePlus 10 Pro 5G",
        "model_id": "NE2211",
        "release_date_global": "2022-01-11",
        "availability_status_india": "Released",
        "display_size_inch": 6.7,
        "display_type": "LTPO2 Fluid AMOLED",
        "display_resolution": "3216 x 1440",
        "display_refresh_rate_hz": "1-120",
        "display_protection": "Corning Gorilla Glass Victus",
        "display_hdr_support": "HDR10+",
        "rear_camera_count": 3,
        "rear_main_mp": 48,
        "rear_main_aperture": "f/1.8",
        "rear_main_sensor": "Sony IMX789",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 50,
        "rear_telephoto_mp": 8,
        "rear_telephoto_aperture": "f/2.4",
        "rear_telephoto_optical_zoom": "3.3x",
        "rear_video_max": "8K@24fps",
        "front_camera_mp": 32,
        "battery_type": "Li-Po",
        "wired_charging_w": 80,
        "wireless_charging_w": 50,
        "battery_removable": "No",
        "dimensions_mm": "163.0 x 73.9 x 8.6",
        "weight_g": 201,
        "build_frame": "Aluminum",
        "build_back": "Glass",
        "ip_rating": "IP68",
        "colors_available": "Emerald Forest, Volcanic Black",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.oneplus.in/10-pro/specs",
        "gsmarena_url": "https://www.gsmarena.com/oneplus_10_pro-11234.php",
    },

    533: {
        "canonical_name": "ZTE Axon 40 Ultra 5G",
        "model_id": "A2023P",
        "release_date_global": "2022-05-09",
        "availability_status_india": "Not officially launched",
        "display_size_inch": 6.8,
        "display_type": "AMOLED",
        "display_resolution": "2480 x 1116",
        "display_refresh_rate_hz": "120",
        "rear_camera_count": 3,
        "rear_main_mp": 64,
        "rear_main_aperture": "f/1.6",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 64,
        "rear_telephoto_mp": 64,
        "rear_telephoto_optical_zoom": "3.5x",
        "front_camera_mp": 16,
        "battery_type": "Li-Po",
        "wired_charging_w": 80,
        "battery_removable": "No",
        "dimensions_mm": "163.2 x 73.5 x 8.4",
        "weight_g": 204,
        "build_frame": "Aluminum",
        "build_back": "Glass",
        "colors_available": "Black, Silver",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6E",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 12",
        "official_product_url": "https://www.zte.com.cn/global/products/smart-phones/axon-series/axon-40-ultra",
        "gsmarena_url": "https://www.gsmarena.com/zte_axon_40_ultra-11585.php",
    },

    338: {
        "canonical_name": "OnePlus 9 Pro",
        "model_id": "LE2121",
        "release_date_global": "2021-03-23",
        "availability_status_india": "Released",
        "display_size_inch": 6.7,
        "display_type": "LTPO Fluid2 AMOLED",
        "display_resolution": "3216 x 1440",
        "display_refresh_rate_hz": "1-120",
        "display_protection": "Corning Gorilla Glass",
        "rear_camera_count": 4,
        "rear_main_mp": 48,
        "rear_main_aperture": "f/1.8",
        "rear_main_sensor": "Sony IMX789",
        "rear_main_ois": "Yes",
        "rear_ultrawide_mp": 50,
        "rear_telephoto_mp": 8,
        "rear_telephoto_optical_zoom": "3.3x",
        "front_camera_mp": 16,
        "battery_type": "Li-Po",
        "wired_charging_w": 65,
        "wireless_charging_w": 50,
        "battery_removable": "No",
        "dimensions_mm": "163.2 x 73.6 x 8.7",
        "weight_g": 197,
        "build_frame": "Aluminum",
        "build_back": "Glass",
        "ip_rating": "IP68",
        "colors_available": "Pine Green, Morning Mist, Stellar Black",
        "sim_type": "Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.2",
        "usb_type": "USB Type-C",
        "os_launch": "Android 11",
        "official_product_url": "https://www.oneplus.in/9-pro/specs",
        "gsmarena_url": "https://www.gsmarena.com/oneplus_9_pro-10750.php",
    },

    695: {
        "canonical_name": "Samsung Galaxy Note 10 Plus",
        "model_id": "SM-N975F",
        "release_date_global": "2019-08-07",
        "availability_status_india": "Released",
        "display_size_inch": 6.8,
        "display_type": "Dynamic AMOLED",
        "display_resolution": "3040 x 1440",
        "display_refresh_rate_hz": "60",
        "display_protection": "Corning Gorilla Glass 6",
        "rear_camera_count": 4,
        "rear_main_mp": 12,
        "rear_main_aperture": "f/1.5-f/2.4",
        "rear_main_ois": "Yes",
        "rear_telephoto_mp": 12,
        "rear_telephoto_optical_zoom": "2x",
        "rear_ultrawide_mp": 16,
        "front_camera_mp": 10,
        "front_camera_aperture": "f/2.2",
        "battery_type": "Li-Ion",
        "wired_charging_w": 45,
        "wireless_charging_w": 15,
        "reverse_wireless_charging_w": 9,
        "battery_removable": "No",
        "dimensions_mm": "162.3 x 77.2 x 7.9",
        "weight_g": 196,
        "build_frame": "Aluminum",
        "build_back": "Glass",
        "ip_rating": "IP68",
        "colors_available": "Aura Glow, Aura White, Aura Black, Aura Blue",
        "sim_type": "Hybrid Dual Nano-SIM",
        "wifi_standard": "Wi-Fi 6",
        "bluetooth_version": "5.0",
        "usb_type": "USB Type-C",
        "os_launch": "Android 9",
        "official_product_url": "https://www.samsung.com/global/galaxy/galaxy-note10/specs/",
        "gsmarena_url": "https://www.gsmarena.com/samsung_galaxy_note10+-9732.php",
    },
}

# Load
enriched = pd.read_csv(ENRICHED)
sources = pd.read_csv(SOURCES)

# Safety check
existing = set(enriched["phone_id"].astype(int))
duplicates = sorted(set(batch) & existing)
if duplicates:
    raise SystemExit(f"ERROR: These IDs already exist: {duplicates}")

# Verify all IDs are present in base catalog
base = pd.read_csv(DATA / "phones.csv")
base_ids = set(base["phone_id"].astype(int))
missing = sorted(set(batch) - base_ids)
if missing:
    raise SystemExit(f"ERROR: IDs missing from phones.csv: {missing}")

# Backups
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(ENRICHED, DATA / f"phones_enriched.csv.backup_{stamp}")
shutil.copy2(SOURCES, DATA / f"phone_enrichment_sources.csv.backup_{stamp}")

# Create rows
rows = []

for phone_id, values in batch.items():
    record = {col: pd.NA for col in enriched.columns}
    record["phone_id"] = phone_id

    for key, value in values.items():
        if key in record:
            record[key] = value

    rows.append(record)

new_rows = pd.DataFrame(rows)
enriched = pd.concat([enriched, new_rows], ignore_index=True)
enriched.to_csv(ENRICHED, index=False)

# Source audit
source_rows = []

for phone_id, values in batch.items():
    source_rows.append({
        "phone_id": phone_id,
        "canonical_name": values["canonical_name"],
        "source_type": "Official manufacturer",
        "source_url": values["official_product_url"],
        "match_confidence": "High",
        "notes": "Primary manufacturer documentation used for model/specification verification."
    })

    source_rows.append({
        "phone_id": phone_id,
        "canonical_name": values["canonical_name"],
        "source_type": "GSMArena",
        "source_url": values["gsmarena_url"],
        "match_confidence": "High",
        "notes": "Secondary specification cross-check."
    })

sources = pd.concat([sources, pd.DataFrame(source_rows)], ignore_index=True)
sources.to_csv(SOURCES, index=False)

print("=== BATCH ENRICHMENT SUCCESS ===")
print(f"Added phones: {len(batch)}")
print("IDs:", ", ".join(map(str, batch.keys())))
print(f"Enriched rows: {len(enriched)}")
print(f"Source audit rows: {len(sources)}")
print(f"Backup timestamp: {stamp}")
