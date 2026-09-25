import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

DATA = Path("data")
enriched_path = DATA / "phones_enriched.csv"
sources_path = DATA / "phone_enrichment_sources.csv"

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

shutil.copy2(enriched_path, DATA / f"phones_enriched.csv.backup_{stamp}")
shutil.copy2(sources_path, DATA / f"phone_enrichment_sources.csv.backup_{stamp}")

e = pd.read_csv(enriched_path)
s = pd.read_csv(sources_path)

if 746 in set(e["phone_id"].astype(int)):
    raise SystemExit("ABORTED: phone_id 746 already exists")

row = {col: pd.NA for col in e.columns}

row.update({
    "phone_id": 746,
    "canonical_name": "realme GT 2 Pro 5G",
    "model_id": "RMX3301",

    "release_date_global": "2022-01-04",
    "release_date_india": pd.NA,
    "availability_status_india": "Released",

    "display_size_inch": 6.7,
    "display_type": "2K QHD+ AMOLED, LTPO 2.0",
    "display_resolution": "3216 x 1440",
    "display_refresh_rate_hz": 120,
    "display_protection": "Corning Gorilla Glass Victus",
    "display_peak_brightness_nits": 1400,
    "display_hdr_support": "HDR10+",

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": "Sony IMX766",
    "rear_main_ois": "Yes",
    "rear_ultrawide_mp": 50,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": pd.NA,
    "rear_video_max": "8K",
    "front_camera_mp": 32,
    "front_camera_aperture": "f/2.4",
    "front_camera_af": pd.NA,
    "front_video_max": "1080p@30fps",

    "battery_type": pd.NA,
    "wired_charging_w": 65,
    "wireless_charging_w": pd.NA,
    "reverse_wireless_charging_w": pd.NA,
    "battery_removable": "No",

    "dimensions_mm": "163.2 x 74.7 x 8.18",
    "weight_g": "199 Steel Black; 189 Paper White/Paper Green",

    "build_frame": pd.NA,
    "build_back": "Biopolymer / AG glass depending on edition",
    "ip_rating": pd.NA,
    "colors_available": "Steel Black, Paper White, Paper Green",

    "sim_type": "Dual Nano SIM",
    "five_g_bands": "n1/n3/n5/n7/n8/n20/n28/n38/n40/n41/n66/n77/n78",
    "wifi_standard": "Wi-Fi 6",
    "bluetooth_version": 5.2,
    "usb_version": pd.NA,
    "usb_type": "USB Type-C",
    "audio_jack": "No",

    "os_launch": "Android 12, realme UI 3.0",
    "os_current": pd.NA,
    "os_update_policy_years": pd.NA,

    "official_product_url": "https://www.realme.com/in/realme-gt-2-pro",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,

    "gsmarena_url": "https://www.gsmarena.com/realme_gt_2_pro-11228.php",

    "launch_price_inr_official": pd.NA,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
})

e = pd.concat([e, pd.DataFrame([row])], ignore_index=True)

if e["phone_id"].duplicated().any():
    raise SystemExit("ABORTED: duplicate phone_id detected")

source_rows = [
    {
        "phone_id": 746,
        "canonical_name": "realme GT 2 Pro 5G",
        "source_type": "official_manufacturer",
        "source_url": "https://www.realme.com/in/realme-gt-2-pro/specs",
        "match_confidence": "high",
        "notes": "Official realme India specification page; confirms 12GB+256GB variant and technical specifications."
    },
    {
        "phone_id": 746,
        "canonical_name": "realme GT 2 Pro 5G",
        "source_type": "official_manufacturer",
        "source_url": "https://www.realme.com/in/realme-gt-2-pro",
        "match_confidence": "high",
        "notes": "Official realme India product page."
    }
]

s = pd.concat([s, pd.DataFrame(source_rows)], ignore_index=True)

e.to_csv(enriched_path, index=False)
s.to_csv(sources_path, index=False)

print("SUCCESS")
print("Added phone_id: 746")
print("Enriched rows:", len(e))
print("Source audit rows:", len(s))
print("Backup timestamp:", stamp)
