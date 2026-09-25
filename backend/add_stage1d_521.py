import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil

DATA = Path("data")
ENRICHED = DATA / "phones_enriched.csv"
SOURCES = DATA / "phone_enrichment_sources.csv"

PHONE_ID = 521

# Safety: verify base row exists
base = pd.read_csv(DATA / "phones.csv")
row = base[base["phone_id"] == PHONE_ID]

if row.empty:
    raise SystemExit(f"ERROR: phone_id {PHONE_ID} not found in phones.csv")

if pd.read_csv(ENRICHED)["phone_id"].eq(PHONE_ID).any():
    raise SystemExit(f"ERROR: phone_id {PHONE_ID} already exists in phones_enriched.csv")

# Backups
stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(ENRICHED, DATA / f"phones_enriched.csv.backup_{stamp}")
shutil.copy2(SOURCES, DATA / f"phone_enrichment_sources.csv.backup_{stamp}")

enriched = pd.read_csv(ENRICHED)
sources = pd.read_csv(SOURCES)

# Start with NA for every enrichment field
record = {col: pd.NA for col in enriched.columns}
record["phone_id"] = PHONE_ID
record["canonical_name"] = "realme GT 2 Pro 5G"
record["model_id"] = "RMX3301"

# Release / availability
record["release_date_global"] = "2022-01-04"
record["release_date_india"] = pd.NA
record["availability_status_india"] = "Released"
record["discontinued_date_india"] = pd.NA

# Display
record["display_size_inch"] = 6.7
record["display_type"] = "QHD+ AMOLED LTPO 2.0"
record["display_resolution"] = "3216 x 1440"
record["display_refresh_rate_hz"] = "1-120"
record["display_protection"] = "Corning Gorilla Glass Victus"
record["display_peak_brightness_nits"] = 1400
record["display_hdr_support"] = "HDR10+"

# Cameras
record["rear_camera_count"] = 3
record["rear_main_mp"] = 50
record["rear_main_aperture"] = "f/1.8"
record["rear_main_sensor"] = "Sony IMX766"
record["rear_main_ois"] = "Yes"
record["rear_ultrawide_mp"] = 50
record["rear_ultrawide_aperture"] = "f/2.2"
record["rear_telephoto_mp"] = pd.NA
record["rear_telephoto_aperture"] = pd.NA
record["rear_telephoto_optical_zoom"] = pd.NA
record["rear_video_max"] = "8K"
record["front_camera_mp"] = 32
record["front_camera_aperture"] = "f/2.4"
record["front_camera_af"] = pd.NA
record["front_video_max"] = "1080p@30fps"

# Battery / charging
record["battery_type"] = "Li-Po"
record["wired_charging_w"] = 65
record["wireless_charging_w"] = pd.NA
record["reverse_wireless_charging_w"] = pd.NA
record["battery_removable"] = "No"

# Build
record["dimensions_mm"] = "163.2 x 74.7 x 8.18"
record["weight_g"] = "189-199"
record["build_frame"] = pd.NA
record["build_back"] = "Biopolymer / AG glass depending on edition"
record["ip_rating"] = pd.NA

# Colors
record["colors_available"] = "Steel Black, Paper White, Paper Green"

# Connectivity
record["sim_type"] = "Dual Nano-SIM"
record["five_g_bands"] = "n1/n3/n5/n7/n8/n20/n28/n38/n40/n41/n66/n77/n78"
record["wifi_standard"] = "Wi-Fi 6"
record["bluetooth_version"] = "5.2"
record["usb_version"] = pd.NA
record["usb_type"] = "USB Type-C"
record["audio_jack"] = pd.NA

# Software
record["os_launch"] = "Android 12"
record["os_current"] = pd.NA
record["os_update_policy_years"] = pd.NA

# Sources / pricing
record["official_product_url"] = "https://www.realme.com/in/realme-gt-2-pro"
record["official_image_url"] = pd.NA
record["local_image_path"] = pd.NA
record["gsmarena_url"] = "https://www.gsmarena.com/realme_gt_2_pro-11230.php"
record["launch_price_inr_official"] = pd.NA
record["current_min_price_inr"] = pd.NA
record["price_updated_at"] = pd.NA

enriched = pd.concat([enriched, pd.DataFrame([record])], ignore_index=True)
enriched.to_csv(ENRICHED, index=False)

new_sources = pd.DataFrame([
    {
        "phone_id": PHONE_ID,
        "canonical_name": "realme GT 2 Pro 5G",
        "source_type": "Official manufacturer India product/specs",
        "source_url": "https://www.realme.com/in/realme-gt-2-pro/specs",
        "match_confidence": "High",
        "notes": "Official realme India specification page confirms 8GB/128GB and 12GB/256GB configurations and core specifications."
    },
    {
        "phone_id": PHONE_ID,
        "canonical_name": "realme GT 2 Pro 5G",
        "source_type": "GSMArena",
        "source_url": "https://www.gsmarena.com/realme_gt_2_pro-11230.php",
        "match_confidence": "High",
        "notes": "Secondary cross-check for model identity and specifications."
    }
])

sources = pd.concat([sources, new_sources], ignore_index=True)
sources.to_csv(SOURCES, index=False)

print("SUCCESS")
print(f"Added phone_id: {PHONE_ID}")
print(f"Enriched rows: {len(enriched)}")
print(f"Source audit rows: {len(sources)}")
