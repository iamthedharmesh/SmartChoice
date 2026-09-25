import pandas as pd

PATH = "data/phone_enrichment_sources.csv"

records = [
    (
        13,
        "Redmi Note 12 Pro 5G",
        "Official Xiaomi India specifications",
        "https://www.mi.com/in/product/redmi-note-12-pro-5g/specs/",
        1.00,
        "Official Xiaomi specification source for the Redmi Note 12 Pro 5G."
    ),
    (
        13,
        "Redmi Note 12 Pro 5G",
        "Official Xiaomi India product page",
        "https://www.mi.com/in/product/redmi-note-12-pro-5g/buy/",
        0.95,
        "Official Xiaomi India product page confirming the India product listing."
    ),

    (
        18,
        "OPPO Reno9 Pro+",
        "Official OPPO specifications",
        "https://www.oppo.com/cn/smartphones/series-reno/reno9-pro-plus/specs/",
        1.00,
        "Official OPPO specifications. Confirms Reno9 Pro+ model, dimensions, display, cameras, charging, connectivity and ColorOS."
    ),

    (
        23,
        "POCO X4 Pro 5G",
        "Gadgets360",
        "https://www.gadgets360.com/mobiles/news/poco-x4-pro-5g-price-in-india-rs-18999-launch-sale-date-april-5-specifications-features-flipkart-2847308/",
        0.90,
        "Secondary source for India launch, specifications and historical launch pricing."
    ),

    (
        24,
        "Xiaomi Redmi Note 12",
        "Official Xiaomi India specifications",
        "https://www.mi.com/in/product/redmi-note-12/specs/",
        1.00,
        "Official Xiaomi India specifications for display, cameras, battery, charging, dimensions, connectivity and software."
    ),
    (
        24,
        "Xiaomi Redmi Note 12",
        "Official Xiaomi India FAQ",
        "https://www.mi.com/in/product/redmi-note-12/faq/",
        1.00,
        "Official Xiaomi India FAQ confirming Gorilla Glass, 120Hz display, headphone jack, Android/MIUI version, camera setup, 33W charging and IP53."
    ),

    (
        25,
        "vivo V26 Pro",
        "Gadgets Now",
        "https://gadgetsnow.indiatimes.com/mobile-phones/vivo-v26-pro",
        0.85,
        "Source reports the Vivo V26 Pro as CANCELLED. No specifications were imported into the enriched dataset."
    ),
    (
        25,
        "vivo V26 Pro",
        "Smartprix",
        "https://www.smartprix.com/mobiles/vivo-v26-pro-ppd14x2qk2u1",
        0.85,
        "Secondary source explicitly describes the device as rumored/unverified. Used only to support the decision not to invent specifications."
    ),

    (
        31,
        "Realme 10 Pro (8GB RAM + 128GB)",
        "Official realme India newsroom",
        "https://www.realme.com/in/newsroom/realme-10-pro-series",
        1.00,
        "Official realme India launch announcement confirming realme 10 Pro 5G, 8GB+128GB variant, India availability, pricing and major specifications."
    ),

    (
        32,
        "POCO X5 Pro 5G",
        "Official POCO India",
        "https://www.youtube.com/watch?v=q4ksMdiAZXw",
        0.90,
        "Official POCO India launch video confirming POCO X5 Pro 5G and India launch context."
    ),

    (
        33,
        "vivo V27 5G (8GB RAM + 256GB)",
        "Official vivo India specifications",
        "https://www.vivo.com/in/products/param/v27",
        1.00,
        "Official vivo India parameter page confirming V27 display, cameras, battery, charging, connectivity, software and India configuration."
    ),
    (
        33,
        "vivo V27 5G (8GB RAM + 256GB)",
        "Official vivo India press release",
        "https://vivonewsroom.in/press-release/vivo-launches-the-premium-v27-series-in-india-packed-with-flagship-grade-cameras-and-3d-curved-display/",
        1.00,
        "Official vivo India launch announcement confirming India launch, V27 camera system, display, chipset and series details."
    ),
]

columns = [
    "phone_id",
    "canonical_name",
    "source_type",
    "source_url",
    "match_confidence",
    "notes"
]

existing = pd.read_csv(PATH)

new_df = pd.DataFrame(records, columns=columns)

existing_keys = set(
    zip(existing["phone_id"], existing["source_url"])
)

new_df = new_df[
    ~new_df.apply(
        lambda r: (r["phone_id"], r["source_url"]) in existing_keys,
        axis=1
    )
]

combined = pd.concat([existing, new_df], ignore_index=True)

combined.to_csv(PATH, index=False)

print("Stage 1B completion update successful.")
print("Added rows:", len(new_df))
print("Total audit rows:", len(combined))
print("Unique audited phone IDs:", combined["phone_id"].nunique())

enriched = pd.read_csv("data/phones_enriched.csv")
missing = sorted(set(enriched.phone_id) - set(combined.phone_id))

print("Missing audit phone IDs:", missing)