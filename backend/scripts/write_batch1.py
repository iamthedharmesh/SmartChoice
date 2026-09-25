from pathlib import Path
import csv

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data"

ENRICHED = DATA / "phones_enriched.csv"
SOURCES = DATA / "phone_enrichment_sources.csv"

# Read existing enrichment CSV
with ENRICHED.open("r", encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    existing = {int(row["phone_id"]): row for row in reader if row.get("phone_id")}

required = {
    15, 207, 153
}

missing = required - set(existing)
print("Existing enrichment rows:", len(existing))
print("Batch 1 IDs:", sorted(required))

def row(phone_id, **values):
    result = {field: "" for field in fieldnames}
    result["phone_id"] = str(phone_id)
    for key, value in values.items():
        if key not in result:
            raise ValueError(f"Unknown column: {key}")
        result[key] = str(value)
    return result


rows = [
    row(
        15,
        canonical_name="Samsung Galaxy S23 Ultra 5G",
        model_id="SM-S918B",
        release_date_global="2023-02-01",
        release_date_india="2023-02-17",
        availability_status_india="Listed in India; stock/availability varies",
        discontinued_date_india="",
        display_size_inch="6.8",
        display_type="Dynamic AMOLED 2X, 120Hz, HDR10+",
        display_resolution="3088 x 1440 (QHD+)",
        display_refresh_rate_hz="120",
        display_protection="Gorilla Glass Victus 2",
        display_peak_brightness_nits="1750",
        display_hdr_support="HDR10+",
        rear_camera_count="4",
        rear_main_mp="200",
        rear_main_aperture="f/1.7",
        rear_main_sensor='Samsung HP2, 1/1.3"',
        rear_main_ois="Yes",
        rear_ultrawide_mp="12",
        rear_ultrawide_aperture="f/2.2",
        rear_telephoto_mp="10 (3x) + 10 (10x)",
        rear_telephoto_aperture="f/2.4 (3x), f/4.9 (10x)",
        rear_telephoto_optical_zoom="3x, 10x",
        rear_video_max="8K@24/30fps, 4K@30/60fps",
        front_camera_mp="12",
        front_camera_aperture="f/2.2",
        front_camera_af="Yes (PDAF)",
        front_video_max="4K@30/60fps",
        battery_type="Li-Ion 5000 mAh",
        wired_charging_w="45",
        wireless_charging_w="15",
        reverse_wireless_charging_w="4.5",
        battery_removable="No",
        dimensions_mm="163.4 x 78.1 x 8.9",
        weight_g="234",
        build_frame="Aluminum",
        build_back="Glass (Gorilla Glass Victus 2)",
        ip_rating="IP68",
        colors_available="Phantom Black, Cream, Green, Lavender, Graphite, Sky Blue, Lime, Red",
        sim_type="Nano-SIM + Nano-SIM / eSIM",
        five_g_bands="n1, n2, n3, n5, n7, n8, n12, n20, n25, n28, n38, n40, n41, n66, n77, n78",
        wifi_standard="Wi-Fi 6E (802.11 a/b/g/n/ac/ax)",
        bluetooth_version="5.3",
        usb_version="USB 3.2 Gen 1",
        usb_type="Type-C",
        audio_jack="No",
        os_launch="Android 13, One UI 5.1",
        os_current="Android 16, One UI 8.5",
        os_update_policy_years="4 OS / 5 Security",
        official_product_url="https://www.samsung.com/in/smartphones/galaxy-s23-ultra/",
        official_image_url="https://images.samsung.com/is/image/samsung/p6pim/in/sm-s918bzgains/gallery/in-galaxy-s23-ultra-s918-sm-s918bzgains-538662647",
        local_image_path="",
        gsmarena_url="https://www.gsmarena.com/samsung_galaxy_s23_ultra-12254.php",
        launch_price_inr_official="124999",
        current_min_price_inr="81999",
        price_updated_at="2026-08-01",
    ),

    row(
        207,
        canonical_name="Samsung Galaxy A54 5G",
        model_id="SM-A546B",
        release_date_global="2023-03-16",
        release_date_india="2023-03-28",
        availability_status_india="Available via third-party retailers",
        discontinued_date_india="",
        display_size_inch="6.4",
        display_type="Super AMOLED, 120Hz, HDR10+",
        display_resolution="2340 x 1080 (FHD+)",
        display_refresh_rate_hz="120",
        display_protection="Gorilla Glass 5",
        display_peak_brightness_nits="1000",
        display_hdr_support="HDR10+",
        rear_camera_count="3",
        rear_main_mp="50",
        rear_main_aperture="f/1.8",
        rear_main_sensor="",
        rear_main_ois="Yes",
        rear_ultrawide_mp="12",
        rear_ultrawide_aperture="f/2.2",
        rear_telephoto_mp="",
        rear_telephoto_aperture="",
        rear_telephoto_optical_zoom="",
        rear_video_max="4K@30fps, 1080p@30/60fps",
        front_camera_mp="32",
        front_camera_aperture="f/2.2",
        front_camera_af="",
        front_video_max="4K@30fps",
        battery_type="Li-Ion 5000 mAh",
        wired_charging_w="25",
        wireless_charging_w="No",
        reverse_wireless_charging_w="No",
        battery_removable="No",
        dimensions_mm="158.2 x 76.7 x 8.2",
        weight_g="202",
        build_frame="Plastic",
        build_back="Glass (Gorilla Glass 5)",
        ip_rating="IP67",
        colors_available="Awesome Graphite, Awesome Violet, Awesome Lime, Awesome Silver",
        sim_type="Nano-SIM + Nano-SIM",
        five_g_bands="n1, n3, n5, n7, n8, n20, n28, n38, n40, n41, n77, n78",
        wifi_standard="Wi-Fi 6 (802.11 a/b/g/n/ac/ax)",
        bluetooth_version="5.3",
        usb_version="USB 2.0",
        usb_type="Type-C",
        audio_jack="No",
        os_launch="Android 13, One UI 5.1",
        os_current="Android 16, One UI 8.5",
        os_update_policy_years="4 OS / 5 Security",
        official_product_url="https://www.samsung.com/in/smartphones/galaxy-a54-5g/",
        official_image_url="https://images.samsung.com/is/image/samsung/p6pim/in/sm-a546blvgins/gallery/in-galaxy-a54-5g-a546-sm-a546blvgins-537812594",
        local_image_path="",
        gsmarena_url="https://www.gsmarena.com/samsung_galaxy_a54_5g-12199.php",
        launch_price_inr_official="38999",
        current_min_price_inr="25999",
        price_updated_at="2026-07-21",
    ),

    row(
        153,
        canonical_name="Apple iPhone 15 Pro Max",
        model_id="A3106 (India)",
        release_date_global="2023-09-22",
        release_date_india="2023-09-22",
        availability_status_india="Available via third-party retailers",
        discontinued_date_india="",
        display_size_inch="6.7",
        display_type="LTPO Super Retina XDR OLED, 120Hz (ProMotion), HDR",
        display_resolution="2796 x 1290 (460 ppi)",
        display_refresh_rate_hz="120",
        display_protection="Ceramic Shield front",
        display_peak_brightness_nits="2000 (outdoor), 1600 (HDR)",
        display_hdr_support="HDR, Dolby Vision, HDR10",
        rear_camera_count="3",
        rear_main_mp="48",
        rear_main_aperture="f/1.78",
        rear_main_sensor='1/1.28", 1.22µm, dual pixel PDAF, sensor-shift OIS',
        rear_main_ois="Yes (sensor-shift)",
        rear_ultrawide_mp="12",
        rear_ultrawide_aperture="f/2.2",
        rear_telephoto_mp="12",
        rear_telephoto_aperture="f/2.8",
        rear_telephoto_optical_zoom="5x (120mm equivalent), 3x (77mm) via crop",
        rear_video_max="4K@24/25/30/60fps, ProRes 4K@30fps (external), 1080p@25/30/60fps",
        front_camera_mp="12",
        front_camera_aperture="f/1.9",
        front_camera_af="Yes (PDAF)",
        front_video_max="4K@24/25/30/60fps",
        battery_type="Li-Ion",
        wired_charging_w="27",
        wireless_charging_w="15 (MagSafe), 7.5 (Qi)",
        reverse_wireless_charging_w="No",
        battery_removable="No",
        dimensions_mm="159.9 x 76.7 x 8.25",
        weight_g="221",
        build_frame="Titanium (Grade 5)",
        build_back="Glass (textured matte)",
        ip_rating="IP68 (6m for 30 min)",
        colors_available="Natural Titanium, Blue Titanium, White Titanium, Black Titanium",
        sim_type="Nano-SIM + eSIM",
        five_g_bands="n1, n2, n3, n5, n7, n8, n12, n20, n25, n26, n28, n29, n30, n38, n40, n41, n48, n66, n70, n71, n77, n78, n79",
        wifi_standard="Wi-Fi 6E (802.11 a/b/g/n/ac/ax)",
        bluetooth_version="5.3",
        usb_version="USB 3.2 Gen 2 (up to 10 Gbps)",
        usb_type="Type-C",
        audio_jack="No",
        os_launch="iOS 17",
        os_current="iOS 26.6.2",
        os_update_policy_years="5-6 major iOS updates (historical)",
        official_product_url="https://www.apple.com/in/iphone-15-pro/specs/",
        official_image_url="https://www.apple.com/v/iphone-15-pro/f/images/overview/hero/iphone_15_pro_hero__c9e5v0z4z22y_large.jpg",
        local_image_path="",
        gsmarena_url="https://www.gsmarena.com/apple_iphone_15_pro_max-12473.php",
        launch_price_inr_official="159900",
        current_min_price_inr="134899",
        price_updated_at="2026-06-12",
    ),
]


# Merge approved rows into existing data.
for r in rows:
    existing[int(r["phone_id"])] = r

# Write enriched CSV with original header/order.
with ENRICHED.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for phone_id in sorted(existing):
        writer.writerow(existing[phone_id])


# Create source audit.
source_rows = [
    [15, "Samsung Galaxy S23 Ultra 5G", "Samsung India", "https://www.samsung.com/in/smartphones/galaxy-s23-ultra/", "1.0", "Official product page"],
    [15, "Samsung Galaxy S23 Ultra 5G", "Samsung Newsroom India", "https://news.samsung.com/in/samsung-galaxy-s23-ultra-launch-india", "1.0", "India launch information"],
    [15, "Samsung Galaxy S23 Ultra 5G", "GSMArena", "https://www.gsmarena.com/samsung_galaxy_s23_ultra-12254.php", "0.95", "Detailed hardware specifications"],
    [15, "Samsung Galaxy S23 Ultra 5G", "91mobiles", "https://www.91mobiles.com/index.php/samsung-galaxy-s23-ultra-5g-price-in-india", "0.85", "Dated 2026 market price"],

    [207, "Samsung Galaxy A54 5G", "Samsung India", "https://www.samsung.com/in/smartphones/galaxy-a54-5g/", "1.0", "Official product page"],
    [207, "Samsung Galaxy A54 5G", "Samsung Newsroom India", "https://news.samsung.com/in/samsung-launches-all-new-galaxy-a54-5g-and-a34-5g-with-stunning-design-and-trendy-colours", "1.0", "India launch information"],
    [207, "Samsung Galaxy A54 5G", "GSMArena", "https://www.gsmarena.com/samsung_galaxy_a54_5g-12199.php", "0.95", "Detailed hardware specifications"],
    [207, "Samsung Galaxy A54 5G", "Gadgets360", "https://www.gadgets360.com/samsung-galaxy-a54-5g-price-in-india-116239", "0.85", "Dated 2026 market price"],

    [153, "Apple iPhone 15 Pro Max", "Apple India", "https://www.apple.com/in/iphone-15-pro/specs/", "1.0", "Official specifications"],
    [153, "Apple Support India", "https://support.apple.com/en-in/116477", "1.0", "Model identification"],
    [153, "Apple Newsroom India", "https://www.apple.com/in/newsroom/2023/09/apple-debuts-iphone-15-pro-and-iphone-15-pro-max/", "1.0", "India launch information"],
    [153, "GSMArena", "https://www.gsmarena.com/apple_iphone_15_pro_max-12473.php", "0.95", "Detailed hardware specifications"],
    [153, "91mobiles", "https://www.91mobiles.com/apple-iphone-15-pro-max-price-in-india", "0.85", "Dated 2026 market price"],
]

with SOURCES.open("w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "phone_id",
        "canonical_name",
        "source_type",
        "source_url",
        "match_confidence",
        "notes",
    ])
    writer.writerows(source_rows)

print("Batch 1 written successfully.")
print("Enriched phone IDs:", sorted(existing))
print("Source audit:", SOURCES)