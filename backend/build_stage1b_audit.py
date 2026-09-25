import pandas as pd

AUDIT_PATH = "data/phone_enrichment_sources.csv"

records = [
    # phone_id, canonical_name, source_type, source_url, confidence, notes

    (1, "OnePlus 11 5G", "Official OnePlus product page",
     "https://www.oneplus.in/11", 1.00,
     "Source URL recorded in the Phone 1 enrichment script; used as the primary official product source."),

    (1, "OnePlus 11 5G", "GSMArena",
     "https://www.gsmarena.com/oneplus_11-11893.php", 0.90,
     "Secondary source URL recorded in the Phone 1 enrichment script."),

    (2, "OnePlus Nord CE 2 Lite 5G", "Official OnePlus specifications",
     "https://www.oneplus.in/nord-ce-2-lite-5g/specs", 1.00,
     "Official specification URL recorded in the Phone 2 enrichment script."),

    (2, "OnePlus Nord CE 2 Lite 5G", "GSMArena",
     "https://www.gsmarena.com/oneplus_nord_ce_2_lite_5g-11409.php", 0.90,
     "Secondary specification URL recorded in the Phone 2 enrichment script."),

    (3, "Samsung Galaxy A14 5G", "Official Samsung India",
     "https://www.samsung.com/in/smartphones/galaxy-a/galaxy-a14-5g-black-128gb-sm-a146bzkdins/",
     1.00,
     "Official Samsung India source URL recorded in the Phone 3 enrichment script."),

    (3, "Samsung Galaxy A14 5G", "GSMArena",
     "https://www.gsmarena.com/samsung_galaxy_a14_5g-12074.php", 0.90,
     "Secondary source URL recorded in the Phone 3 enrichment script."),

    (4, "Motorola Moto G62 5G", "Official Motorola India",
     "https://www.motorola.in/smartphones-moto-g-62-5g/p",
     1.00,
     "Official Motorola source URL recorded in the Phone 4 enrichment script."),

    (4, "Motorola Moto G62 5G", "GSMArena",
     "https://www.gsmarena.com/motorola_moto_g62_5g-11631.php", 0.90,
     "Secondary source URL recorded in the Phone 4 enrichment script."),

    (5, "Realme 10 Pro+ 5G", "Official realme India",
     "https://www.realme.com/in/realme-10-pro-plus", 1.00,
     "Official realme source URL recorded in the Phone 5 enrichment script."),

    (5, "Realme 10 Pro+ 5G", "GSMArena",
     "https://www.gsmarena.com/realme_10_pro+-12054.php", 0.90,
     "Secondary source URL recorded in the Phone 5 enrichment script."),

    (6, "Samsung Galaxy F23 5G", "Official Samsung India",
     "https://www.samsung.com/in/", 0.80,
     "Official Samsung India URL recorded in the Phone 6 enrichment script. This is the Samsung India site rather than a product-specific page."),

    (6, "Samsung Galaxy F23 5G", "GSMArena",
     "https://www.gsmarena.com/samsung_galaxy_f23-11398.php", 0.90,
     "Secondary source URL recorded in the Phone 6 enrichment script."),

    (9, "Nothing Phone (1)", "Official Nothing India",
     "https://in.nothing.tech/pages/phone-1", 1.00,
     "Official Nothing source URL recorded in the Phone 9 enrichment script."),

    (9, "Nothing Phone (1)", "GSMArena",
     "https://www.gsmarena.com/nothing_phone_(1)-11636.php", 0.90,
     "Secondary source URL recorded in the Phone 9 enrichment script."),

    (10, "OnePlus Nord 2T 5G", "Official OnePlus specifications",
     "https://www.oneplus.in/nord-2t-5g/specs", 1.00,
     "Official specification URL recorded in the Phone 10 enrichment script."),

    (11, "Realme 10 Pro 5G", "Official realme India",
     "https://www.realme.com/in/realme-10-pro/specs", 1.00,
     "Official specification URL recorded in the Phone 11 enrichment script."),

    (11, "Realme 10 Pro 5G", "GSMArena",
     "https://www.gsmarena.com/realme_10_pro-11954.php", 0.90,
     "Secondary source URL recorded in the Phone 11 enrichment script."),

    (12, "OPPO A78", "Official OPPO India",
     "https://www.oppo.com/in/smartphones/series-a/a78/specs/", 1.00,
     "Official specification URL recorded in the Phone 12 enrichment script."),

    (12, "OPPO A78", "GSMArena",
     "https://www.gsmarena.com/oppo_a78-12466.php", 0.90,
     "Secondary source URL recorded in the Phone 12 enrichment script."),

    (14, "vivo T1 5G", "Official vivo India",
     "https://www.vivo.com/in/products/t1-5g", 1.00,
     "Official vivo product URL recorded in the Phone 14 enrichment script."),

    (16, "Apple iPhone 13", "Official Apple India",
     "https://www.apple.com/in/iphone-13/", 1.00,
     "Official Apple India product URL recorded in the Phone 16 enrichment script."),

    (17, "vivo Y16", "Official vivo India",
     "https://www.vivo.com/in/products/y16", 1.00,
     "Official vivo product URL recorded in the Phone 17 enrichment script."),

    (19, "OnePlus 10R 5G", "Official OnePlus specifications",
     "https://www.oneplus.in/10r/specs", 1.00,
     "Official specification URL recorded in the Phone 19 enrichment script."),

    (20, "vivo Y22", "Official vivo India",
     "https://www.vivo.com/in/products/y22", 1.00,
     "Official vivo product URL recorded in the Phone 20 enrichment script."),

    (21, "OnePlus 11R", "Official OnePlus India",
     "https://www.oneplus.in/11r", 1.00,
     "Official OnePlus product URL recorded in the Phone 21 enrichment script."),

    (22, "vivo V25 Pro 5G", "Official vivo India",
     "https://www.vivo.com/in/products/v25-pro", 1.00,
     "Official vivo product URL recorded in the Phone 22 enrichment script."),

    (26, "Samsung Galaxy S20 FE 5G", "Official Samsung India support",
     "https://www.samsung.com/in/support/model/SM-G781BZBDEUC/",
     1.00,
     "Official Samsung India support URL recorded in the Phone 26 enrichment script."),

    (27, "OnePlus Nord CE 2 Lite 5G (8GB RAM + 128GB)", "Official OnePlus specifications",
     "https://www.oneplus.in/nord-ce-2-lite-5g/specs", 1.00,
     "Official OnePlus specification URL recorded in the Phone 27 enrichment script."),

    (28, "Apple iPhone 14 Pro Max", "Official Apple India",
     "https://www.apple.com/in/iphone-14-pro/", 1.00,
     "Official Apple India product URL recorded in the Phone 28 enrichment script."),

    (29, "vivo V25 5G", "Official vivo India",
     "https://www.vivo.com/in/products/v25", 1.00,
     "Official vivo product URL recorded in the Phone 29 enrichment script."),

    (186, "OnePlus Nord 3 5G", "Official OnePlus India",
     "https://www.oneplus.in/nord-3-5g", 1.00,
     "Official OnePlus product URL recorded in the Phone 186 enrichment script."),

    (186, "OnePlus Nord 3 5G", "GSMArena",
     "https://www.gsmarena.com/oneplus_nord_3-12368.php", 0.90,
     "Secondary source URL recorded in the Phone 186 enrichment script."),

    (347, "vivo X90 Pro 5G", "Official vivo India",
     "https://www.vivo.com/in/products/x90-pro", 1.00,
     "Official vivo product URL recorded in the Phone 347 enrichment script."),

    (347, "vivo X90 Pro 5G", "GSMArena",
     "https://www.gsmarena.com/vivo_x90_pro-12103.php", 0.90,
     "Secondary source URL recorded in the Phone 347 enrichment script."),

    (194, "Motorola Edge 30 Fusion 5G", "Official Motorola India support",
     "https://en-in.support.motorola.com/app/answers/detail/",
     0.80,
     "Official Motorola support URL recorded in the Phone 194 enrichment script; product-specific URL was truncated in the original terminal output.")
]

columns = [
    "phone_id",
    "canonical_name",
    "source_type",
    "source_url",
    "match_confidence",
    "notes"
]

existing = pd.read_csv(AUDIT_PATH)

new_df = pd.DataFrame(records, columns=columns)

# Avoid duplicates if this script is run more than once.
keys = ["phone_id", "source_url"]
existing_keys = set(zip(existing["phone_id"], existing["source_url"]))

new_df = new_df[
    ~new_df.apply(
        lambda r: (r["phone_id"], r["source_url"]) in existing_keys,
        axis=1
    )
]

combined = pd.concat([existing, new_df], ignore_index=True)

combined.to_csv(AUDIT_PATH, index=False)

print("Stage 1B audit update complete.")
print("Added audit rows:", len(new_df))
print("Total audit rows:", len(combined))
print("Unique audited phone IDs:", combined["phone_id"].nunique())

print("\nAudit coverage:")
print(
    combined.groupby("phone_id")
    .size()
    .sort_index()
    .to_string()
)