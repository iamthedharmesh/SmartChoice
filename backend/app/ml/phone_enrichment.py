"""
Phone Enrichment Loader — LEFT JOIN helper for phones_enriched.csv.

This module provides utilities to load enriched phone data and merge it with
the base phones.csv using phone_id as the join key. Missing enrichment data
never breaks the base recommendation engine.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


ENRICHED_COLUMNS = [
    # Identity
    "phone_id",
    "canonical_name",
    "model_id",
    # Timeline
    "release_date_global",
    "release_date_india",
    "availability_status_india",
    "discontinued_date_india",
    # Display
    "display_size_inch",
    "display_type",
    "display_resolution",
    "display_refresh_rate_hz",
    "display_protection",
    "display_peak_brightness_nits",
    "display_hdr_support",
    # Camera
    "rear_camera_count",
    "rear_main_mp",
    "rear_main_aperture",
    "rear_main_sensor",
    "rear_main_ois",
    "rear_ultrawide_mp",
    "rear_ultrawide_aperture",
    "rear_telephoto_mp",
    "rear_telephoto_aperture",
    "rear_telephoto_optical_zoom",
    "rear_video_max",
    "front_camera_mp",
    "front_camera_aperture",
    "front_camera_af",
    "front_video_max",
    # Battery
    "battery_type",
    "wired_charging_w",
    "wireless_charging_w",
    "reverse_wireless_charging_w",
    "battery_removable",
    # Physical
    "dimensions_mm",
    "weight_g",
    "build_frame",
    "build_back",
    "ip_rating",
    "colors_available",
    # Connectivity
    "sim_type",
    "five_g_bands",
    "wifi_standard",
    "bluetooth_version",
    "usb_version",
    "usb_type",
    "audio_jack",
    # Software
    "os_launch",
    "os_current",
    "os_update_policy_years",
    # Media/Links
    "official_product_url",
    "official_image_url",
    "local_image_path",
    "gsmarena_url",
    # Pricing
    "launch_price_inr_official",
    "current_min_price_inr",
    "price_updated_at",
]


def load_enriched(csv_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load the enriched phone data from phones_enriched.csv.

    Returns an empty DataFrame with the expected columns if the file doesn't exist
    or is empty, ensuring graceful degradation.
    """
    if csv_path is None:
        csv_path = str(Path(__file__).resolve().parent.parent.parent / "data" / "phones_enriched.csv")

    path = Path(csv_path)
    if not path.exists():
        return pd.DataFrame(columns=ENRICHED_COLUMNS)

    try:
        df = pd.read_csv(csv_path)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=ENRICHED_COLUMNS)

    # Ensure all expected columns exist (backward compatibility if schema evolves)
    for col in ENRICHED_COLUMNS:
        if col not in df.columns:
            df[col] = pd.NA

    # Ensure phone_id is int for reliable joins
    if "phone_id" in df.columns:
        df["phone_id"] = pd.to_numeric(df["phone_id"], errors="coerce").astype("Int64")

    return df[ENRICHED_COLUMNS]


def merge_enriched(
    base_df: pd.DataFrame,
    enriched_df: Optional[pd.DataFrame] = None,
    csv_path: Optional[str] = None,
) -> pd.DataFrame:
    """
    LEFT JOIN enriched data onto base phone DataFrame using phone_id.

    Args:
        base_df: DataFrame from phones.csv (must have phone_id column)
        enriched_df: Pre-loaded enriched DataFrame (optional)
        csv_path: Path to phones_enriched.csv (used if enriched_df not provided)

    Returns:
        DataFrame with all base columns + all enriched columns.
        Base rows are preserved exactly; enriched columns are NaN where no match.
    """
    if enriched_df is None:
        enriched_df = load_enriched(csv_path)

    if enriched_df.empty:
        # No enrichment data — return base with empty enriched columns
        result = base_df.copy()
        for col in ENRICHED_COLUMNS:
            if col not in result.columns:
                result[col] = pd.NA
        return result

    # Ensure join keys are compatible
    base_df = base_df.copy()
    base_df["phone_id"] = pd.to_numeric(base_df["phone_id"], errors="coerce").astype("Int64")
    enriched_df = enriched_df.copy()
    enriched_df["phone_id"] = pd.to_numeric(enriched_df["phone_id"], errors="coerce").astype("Int64")

    # LEFT JOIN — base phones are never dropped
    merged = base_df.merge(enriched_df, on="phone_id", how="left", validate="many_to_one")

    return merged


def validate_enriched(enriched_df: pd.DataFrame) -> list[str]:
    """
    Validate the enriched dataset for common issues.

    Returns list of warning/error messages (empty = clean).
    """
    issues = []

    if enriched_df.empty:
        issues.append("Enriched dataset is empty")
        return issues

    # Duplicate phone_id check
    dup_count = enriched_df["phone_id"].duplicated().sum()
    if dup_count > 0:
        issues.append(f"Found {dup_count} duplicate phone_id(s) in enriched data")

    # Missing phone_id check
    missing_id = enriched_df["phone_id"].isna().sum()
    if missing_id > 0:
        issues.append(f"Found {missing_id} row(s) with missing phone_id")

    return issues


def get_enriched_for_phone(enriched_df: pd.DataFrame, phone_id: int) -> Optional[dict]:
    """
    Get enriched data for a single phone_id as a dict.

    Returns None if phone_id not found in enriched data.
    """
    matches = enriched_df[enriched_df["phone_id"] == phone_id]
    if matches.empty:
        return None
    return matches.iloc[0].to_dict()


# Convenience: load and validate at import time for scripts
if __name__ == "__main__":
    enriched = load_enriched()
    print(f"Enriched dataset: {len(enriched)} rows, {len(enriched.columns)} columns")
    issues = validate_enriched(enriched)
    if issues:
        print("Validation issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("Validation: OK")