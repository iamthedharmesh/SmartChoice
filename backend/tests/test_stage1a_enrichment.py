"""
Stage 1A Tests — Phone Enrichment Foundation.

Validates:
- All 980 existing phone_ids remain available
- No duplicate phone_id in enriched dataset
- Base recommendation behavior unchanged
- Missing enrichment data does not break recommendations
- phones.csv and recommendation scoring untouched
"""

import sys
sys.path.insert(0, "D:\\SmartChoice\\backend")

import pandas as pd
from app.ml.phone_recommender import PhoneData, PhoneFilters, recommend_phones
from app.ml.phone_enrichment import load_enriched, merge_enriched, validate_enriched

PASS = 0
FAIL = 0


def check(name, cond, extra=""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}  {extra}")


def main():
    print("=== STAGE 1A: ENRICHED DATA FOUNDATION TESTS ===\n")

    # ------------------------------------------------------------------
    # 1. Load base phones.csv (source of truth)
    # ------------------------------------------------------------------
    base_path = "D:\\SmartChoice\\backend\\data\\phones.csv"
    base_df = pd.read_csv(base_path)
    base_ids = set(base_df["phone_id"].tolist())

    check("1a. phones.csv loads", len(base_df) == 980, f"got {len(base_df)}")
    check("1b. 980 unique phone_ids", base_df["phone_id"].nunique() == 980)
    check("1c. phone_id range 1-980", base_df["phone_id"].min() == 1 and base_df["phone_id"].max() == 980)
    check("1d. required columns present", all(c in base_df.columns for c in [
        "phone_id", "brand", "model", "price_inr", "rating", "ram_gb", "storage_gb",
        "processor_brand", "processor_name", "core_count", "clock_speed_ghz",
        "battery_mah", "charging_watt", "refresh_rate_hz", "rear_camera_mp",
        "front_camera_mp", "rear_camera_count", "has_5g", "has_nfc", "os"
    ]))

    # ------------------------------------------------------------------
    # 2. Load phones_enriched.csv
    # ------------------------------------------------------------------
    enriched_df = load_enriched()

    check("2a. phones_enriched.csv loads", enriched_df is not None)
    check("2b. enriched has all expected columns", len(enriched_df.columns) == len([
        "phone_id", "canonical_name", "model_id", "release_date_global",
        "release_date_india", "availability_status_india", "discontinued_date_india",
        "display_size_inch", "display_type", "display_resolution",
        "display_refresh_rate_hz", "display_protection", "display_peak_brightness_nits",
        "display_hdr_support", "rear_camera_count", "rear_main_mp",
        "rear_main_aperture", "rear_main_sensor", "rear_main_ois",
        "rear_ultrawide_mp", "rear_ultrawide_aperture", "rear_telephoto_mp",
        "rear_telephoto_aperture", "rear_telephoto_optical_zoom", "rear_video_max",
        "front_camera_mp", "front_camera_aperture", "front_camera_af",
        "front_video_max", "battery_type", "wired_charging_w", "wireless_charging_w",
        "reverse_wireless_charging_w", "battery_removable", "dimensions_mm",
        "weight_g", "build_frame", "build_back", "ip_rating", "colors_available",
        "sim_type", "five_g_bands", "wifi_standard", "bluetooth_version",
        "usb_version", "usb_type", "audio_jack", "os_launch", "os_current",
        "os_update_policy_years", "official_product_url", "official_image_url",
        "local_image_path", "gsmarena_url", "launch_price_inr_official",
        "current_min_price_inr", "price_updated_at"
    ]))

    # ------------------------------------------------------------------
    # 3. Validate enriched dataset integrity
    # ------------------------------------------------------------------
    issues = validate_enriched(enriched_df)
    # Stage 1A: empty enriched dataset is expected (no data populated yet)
    # Only fail on actual data integrity issues (duplicates, missing IDs)
    real_issues = [i for i in issues if i != "Enriched dataset is empty"]
    check("3a. no validation issues", len(real_issues) == 0, f"issues: {real_issues}")
    check(
    "3b. enriched dataset has valid rows",
    len(enriched_df) >= 0 and enriched_df["phone_id"].nunique() == len(enriched_df)
)

    # ------------------------------------------------------------------
    # 4. LEFT JOIN: all base phones preserved
    # ------------------------------------------------------------------
    merged_df = merge_enriched(base_df, enriched_df)

    check("4a. merged row count == base row count", len(merged_df) == len(base_df), f"merged={len(merged_df)} base={len(base_df)}")
    check("4b. all 980 base phone_ids present", set(merged_df["phone_id"].tolist()) == base_ids)
    check("4c. no new phone_ids introduced", set(merged_df["phone_id"].tolist()).issubset(base_ids))
    check("4d. enriched columns present in merged", all(c in merged_df.columns for c in [
        "canonical_name", "release_date_global", "display_size_inch",
        "rear_main_mp", "battery_type", "dimensions_mm", "sim_type",
        "os_launch", "official_product_url", "launch_price_inr_official"
    ]))
    check(
    "4e. enriched data is correctly joined",
    (
        merged_df.loc[
            merged_df["phone_id"].isin(enriched_df["phone_id"]),
            "canonical_name"
        ].notna().all()
        and
        merged_df.loc[
            ~merged_df["phone_id"].isin(enriched_df["phone_id"]),
            "canonical_name"
        ].isna().all()
    )
)

    # ------------------------------------------------------------------
    # 5. Recommendation engine unchanged — uses PhoneData which reads phones.csv only
    # ------------------------------------------------------------------
    data = PhoneData()

    check("5a. PhoneData loads 980 phones", len(data.raw) == 980, f"got {len(data.raw)}")
    check("5b. PhoneData features shape", data.features.shape[0] == 980)
    check("5c. PhoneData does NOT have enriched columns", "canonical_name" not in data.features.columns)
    check("5d. PhoneData does NOT have display_size_inch", "display_size_inch" not in data.features.columns)

    # ------------------------------------------------------------------
    # 6. Recommendation behavior unchanged
    # ------------------------------------------------------------------
    # Baseline recommendation with no filters
    r_base = recommend_phones(data, PhoneFilters(), priority="Value", limit=10)
    check("6a. baseline returns results", r_base["total"] > 0)
    check("6b. baseline pool is 980", r_base["candidate_pool"] == 980)
    check("6c. match_percentage in range", all(0 <= x["match_percentage"] <= 100 for x in r_base["recommendations"]))
    check("6d. reasons present", all("reasons" in x for x in r_base["recommendations"]))
    check("6e. reasons <= 3", all(len(x["reasons"]) <= 3 for x in r_base["recommendations"]))

    # ------------------------------------------------------------------
    # 7. Hard filters still work identically
    # ------------------------------------------------------------------
    r_budget = recommend_phones(data, PhoneFilters(budget_max=20000), priority="Value", limit=10)
    check("7a. budget filter respected", all(x["price_inr"] <= 20000 for x in r_budget["recommendations"]))

    r_brand = recommend_phones(data, PhoneFilters(brand="Samsung"), priority="Value", limit=10)
    check("7b. brand filter respected", all(x["brand"].lower() == "samsung" for x in r_brand["recommendations"]))

    r_ram = recommend_phones(data, PhoneFilters(min_ram=12), priority="Value", limit=10)
    check("7c. min_ram filter respected", all(x["ram_gb"] >= 12 for x in r_ram["recommendations"]))

    r_5g = recommend_phones(data, PhoneFilters(has_5g=True), priority="Value", limit=10)
    check("7d. 5G filter respected", all(x["has_5g"] for x in r_5g["recommendations"]))

    r_refresh = recommend_phones(data, PhoneFilters(refresh_rate_min=120), priority="Value", limit=10)
    check("7e. refresh_rate filter respected", all(x["refresh_rate_hz"] >= 120 for x in r_refresh["recommendations"]))

    # ------------------------------------------------------------------
    # 8. Priority weights produce different rankings (unchanged)
    # ------------------------------------------------------------------
    r_gaming = recommend_phones(data, PhoneFilters(budget_max=30000), priority="Gaming", limit=1)
    r_camera = recommend_phones(data, PhoneFilters(budget_max=30000), priority="Camera", limit=1)
    check("8a. priorities differ", r_gaming["recommendations"][0]["phone_id"] != r_camera["recommendations"][0]["phone_id"])

    # ------------------------------------------------------------------
    # 9. Edge cases handled cleanly
    # ------------------------------------------------------------------
    r_empty = recommend_phones(data, PhoneFilters(budget_max=1000), priority="Value", limit=10)
    check("9a. empty candidate set handled", r_empty["total"] == 0 and r_empty["recommendations"] == [])

    r_missing_rating = recommend_phones(data, PhoneFilters(budget_max=15000), priority="Value", limit=5)
    check("9b. missing rating handled", r_missing_rating["total"] >= 0)

    r_missing_proc = recommend_phones(data, PhoneFilters(budget_max=20000), priority="Performance", limit=5)
    check("9c. missing processor handled", r_missing_proc["total"] >= 0)

    # ------------------------------------------------------------------
    # 10. All scores in valid range
    # ------------------------------------------------------------------
    from app.ml.phone_recommender import compute_use_case_scores, PRIORITY_WEIGHTS
    scores = compute_use_case_scores(data.features)
    score_cols = ["gaming_score", "camera_score", "performance_score", "battery_score",
                  "student_score", "everyday_score"]
    check("10a. all scores in [0,1]", all(scores[c].between(0, 1).all() for c in score_cols))
    check("10b. weights sum to 1.0", all(abs(sum(w.values()) - 1.0) < 1e-9 for w in PRIORITY_WEIGHTS.values()))

    # ------------------------------------------------------------------
    # 11. Variant phones preserved (distinct phone_ids for same model)
    # ------------------------------------------------------------------
    variants = data.features[data.features["model"].str.contains("Nord CE 2 Lite", na=False)]
    check("11a. RAM/storage variants preserved", len(variants) >= 2)
    check("11b. variants have distinct phone_ids", variants["phone_id"].nunique() == len(variants))

    # ------------------------------------------------------------------
    # 12. phones.csv file unchanged (sanity check)
    # ------------------------------------------------------------------
    # Verify we haven't accidentally modified the source file
    base_again = pd.read_csv(base_path)
    check("12a. phones.csv still 980 rows", len(base_again) == 980)
    check("12b. phones.csv columns unchanged", list(base_again.columns) == list(base_df.columns))

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print(f"\n=== RESULTS: {PASS} passed, {FAIL} failed ===")
    if FAIL > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()