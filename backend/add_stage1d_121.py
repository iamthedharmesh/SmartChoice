import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

DATA = Path("data")
enriched_path = DATA / "phones_enriched.csv"
sources_path = DATA / "phone_enrichment_sources.csv"

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

shutil.copy2(
    enriched_path,
    DATA / f"phones_enriched.csv.backup_{stamp}"
)
shutil.copy2(
    sources_path,
    DATA / f"phone_enrichment_sources.csv.backup_{stamp}"
)

e = pd.read_csv(enriched_path)
s = pd.read_csv(sources_path)

if 121 in set(e["phone_id"].astype(int)):
    raise SystemExit("ABORTED: phone_id 121 already exists")

row = {col: pd.NA for col in e.columns}

row.update({
    "phone_id": 121,
    "canonical_name": "Motorola Edge 30 Pro 5G",
    "model_id": "Edge 30 Pro",
    "release_date_global": "2022-02-24",
    "release_date_india": "2022-03-05",
    "availability_status_india": "Released",

    "display_size_inch": 6.7,
    "display_type": "OLED",
    "display_resolution": "2400 x 1080 (FHD+)",
    "display_refresh_rate_hz": 144,
    "display_protection": "Corning Gorilla Glass 3",

    "rear_camera_count": 3,
    "rear_main_mp": 50,
    "rear_main_aperture": "f/1.8",
    "rear_main_ois": "Yes",
    "rear_ultrawide_mp": 50,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": pd.NA,
    "rear_video_max": "8K",
    "front_camera_mp": 60,
    "front_camera_aperture": "f/2.2",
    "front_camera_af": pd.NA,

    "wired_charging_w": 68,
    "wireless_charging_w": 15,
    "battery_removable": "No",

    "dimensions_mm": "163.6 x 75.6 x 8.5",
    "weight_g": 196,

    "build_frame": "Aluminum",
    "build_back": "Glass",
    "ip_rating": "IP52",

    "sim_type": "Dual Nano SIM",
    "wifi_standard": "Wi-Fi 6E",
    "bluetooth_version": 5.2,
    "usb_type": "USB Type-C",
    "audio_jack": "No",

    "os_launch": "Android 12",
    "os_update_policy_years": pd.NA,

    "official_product_url": pd.NA,
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,

    "gsmarena_url": "https://www.gsmarena.com/motorola_edge_30_pro-11371.php",

    "launch_price_inr_official": 44999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
})

e = pd.concat([e, pd.DataFrame([row])], ignore_index=True)

if e["phone_id"].duplicated().any():
    raise SystemExit("ABORTED: duplicate phone_id detected")

source_rows = [
    {
        "phone_id": 121,
        "canonical_name": "Motorola Edge 30 Pro 5G",
        "source_type": "official_manufacturer",
        "source_url": "https://en-in.support.motorola.com/app/answers/detail/a_id/164289",
        "match_confidence": "high",
        "notes": "Motorola India support documentation for Edge 30 Pro."
    },
    {
        "phone_id": 121,
        "canonical_name": "Motorola Edge 30 Pro 5G",
        "source_type": "gsmarena",
        "source_url": "https://www.gsmarena.com/motorola_edge_30_pro-11371.php",
        "match_confidence": "high",
        "notes": "Cross-reference for detailed hardware specifications and model identity."
    }
]

s = pd.concat([s, pd.DataFrame(source_rows)], ignore_index=True)

e.to_csv(enriched_path, index=False)
s.to_csv(sources_path, index=False)

print("SUCCESS")
print("Added phone_id: 121")
print("Enriched rows:", len(e))
print("Source audit rows:", len(s))
print("Backups created with timestamp:", stamp)
