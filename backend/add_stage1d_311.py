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

if 311 in set(e["phone_id"].astype(int)):
    raise SystemExit("ABORTED: phone_id 311 already exists in phones_enriched.csv")

row = {col: pd.NA for col in e.columns}

row.update({
    "phone_id": 311,
    "canonical_name": "Samsung Galaxy A53 5G",
    "model_id": "SM-A536E",
    "release_date_global": "2022-03-17",
    "release_date_india": "2022-03-25",
    "availability_status_india": "Released",
    "display_size_inch": 6.5,
    "display_type": "Super AMOLED Infinity-O",
    "display_resolution": "FHD+",
    "display_refresh_rate_hz": 120,
    "display_protection": "Corning Gorilla Glass 5",
    "display_peak_brightness_nits": pd.NA,
    "display_hdr_support": pd.NA,
    "rear_camera_count": 4,
    "rear_main_mp": 64,
    "rear_main_aperture": "f/1.8",
    "rear_main_sensor": pd.NA,
    "rear_main_ois": "Yes",
    "rear_ultrawide_mp": 12,
    "rear_ultrawide_aperture": "f/2.2",
    "rear_telephoto_mp": pd.NA,
    "rear_telephoto_aperture": pd.NA,
    "rear_telephoto_optical_zoom": pd.NA,
    "rear_video_max": pd.NA,
    "front_camera_mp": 32,
    "front_camera_aperture": "f/2.2",
    "front_camera_af": pd.NA,
    "front_video_max": pd.NA,
    "battery_type": pd.NA,
    "wired_charging_w": 25,
    "wireless_charging_w": pd.NA,
    "reverse_wireless_charging_w": pd.NA,
    "battery_removable": "No",
    "dimensions_mm": "159.6 x 74.8 x 8.1",
    "weight_g": 189,
    "build_frame": pd.NA,
    "build_back": pd.NA,
    "ip_rating": "IP67",
    "colors_available": "Black, White, Light Blue, Peach",
    "sim_type": pd.NA,
    "five_g_bands": pd.NA,
    "wifi_standard": pd.NA,
    "bluetooth_version": pd.NA,
    "usb_version": pd.NA,
    "usb_type": "USB Type-C",
    "audio_jack": "No",
    "os_launch": "Android 12, One UI 4.1",
    "os_current": pd.NA,
    "os_update_policy_years": "4 years OS upgrades; 5 years security updates",
    "official_product_url": "https://www.samsung.com/in/smartphones/galaxy-a/galaxy-a53-5g-awesome-black-128gb-sm-a536ezkdins/",
    "official_image_url": pd.NA,
    "local_image_path": pd.NA,
    "gsmarena_url": "https://www.gsmarena.com/samsung_galaxy_a53_5g-11268.php",
    "launch_price_inr_official": 35999,
    "current_min_price_inr": pd.NA,
    "price_updated_at": pd.NA,
})

e = pd.concat([e, pd.DataFrame([row])], ignore_index=True)

source_rows = [
    {
        "phone_id": 311,
        "canonical_name": "Samsung Galaxy A53 5G",
        "source_type": "official_manufacturer",
        "source_url": "https://news.samsung.com/in/samsung-launches-galaxy-a53-5g-with-64mp-ois-camera-and-5nm-processor-announces-exciting-pre-book-offers",
        "match_confidence": "high",
        "notes": "Samsung India launch announcement; exact 8GB+128GB variant, India availability, launch price and core specifications."
    },
    {
        "phone_id": 311,
        "canonical_name": "Samsung Galaxy A53 5G",
        "source_type": "official_manufacturer",
        "source_url": "https://www.samsung.com/in/smartphones/galaxy-a/galaxy-a53-5g-awesome-black-128gb-sm-a536ezkdins/",
        "match_confidence": "high",
        "notes": "Samsung India product page for Galaxy A53 5G."
    }
]

s = pd.concat([s, pd.DataFrame(source_rows)], ignore_index=True)

if e["phone_id"].duplicated().any():
    raise SystemExit("ABORTED: duplicate phone_id detected")

e.to_csv(enriched_path, index=False)
s.to_csv(sources_path, index=False)

print("SUCCESS")
print("Added phone_id: 311")
print("Enriched rows:", len(e))
print("Source audit rows:", len(s))
print("Backup:", f"data/phones_enriched.csv.backup_{stamp}")
print("Backup:", f"data/phone_enrichment_sources.csv.backup_{stamp}")
