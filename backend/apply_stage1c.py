from pathlib import Path

path = Path("app/main.py")
text = path.read_text(encoding="utf-8")

# 1. Add enrichment import
old = """from app.ml.phone_recommender import (
    PhoneData,
    PhoneFilters,
    recommend_phones,
)
"""

new = """from app.ml.phone_recommender import (
    PhoneData,
    PhoneFilters,
    recommend_phones,
)
from app.ml.phone_enrichment import load_enriched
"""

if old not in text:
    raise RuntimeError("Could not find phone_recommender import block")

text = text.replace(old, new, 1)


# 2. Load enriched data at startup
old = """    app.state.movies_index = movies_index
    app.state.phones = _load_phones()
    yield
"""

new = """    app.state.movies_index = movies_index
    app.state.phones = _load_phones()
    app.state.phone_enriched = load_enriched()
    yield
"""

if old not in text:
    raise RuntimeError("Could not find lifespan phone loading block")

text = text.replace(old, new, 1)


# 3. Replace phone summary helper with enriched-aware helpers
old = """def _phone_summary(row: pd.Series) -> dict:
    return {k: _cell_to_json(row.get(k)) for k in PHONE_FIELDS}


def _cell_to_json(value):
"""

new = """ENRICHMENT_FIELDS = [
    "canonical_name",
    "model_id",
    "release_date_global",
    "release_date_india",
    "availability_status_india",
    "discontinued_date_india",
    "display_size_inch",
    "display_type",
    "display_resolution",
    "display_refresh_rate_hz",
    "display_protection",
    "display_peak_brightness_nits",
    "display_hdr_support",
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
    "battery_type",
    "wired_charging_w",
    "wireless_charging_w",
    "reverse_wireless_charging_w",
    "battery_removable",
    "dimensions_mm",
    "weight_g",
    "build_frame",
    "build_back",
    "ip_rating",
    "colors_available",
    "sim_type",
    "five_g_bands",
    "wifi_standard",
    "bluetooth_version",
    "usb_version",
    "usb_type",
    "audio_jack",
    "os_launch",
    "os_current",
    "os_update_policy_years",
    "official_product_url",
    "official_image_url",
    "local_image_path",
    "gsmarena_url",
    "launch_price_inr_official",
    "current_min_price_inr",
    "price_updated_at",
]


def _get_phone_enrichment(phone_id: int):
    enriched = getattr(app.state, "phone_enriched", None)

    if enriched is None or enriched.empty:
        return None

    matches = enriched[enriched["phone_id"] == phone_id]

    if matches.empty:
        return None

    row = matches.iloc[0]

    return {
        field: _cell_to_json(row.get(field))
        for field in ENRICHMENT_FIELDS
    }


def _phone_summary(row: pd.Series, include_enrichment: bool = True) -> dict:
    phone_id = int(row["phone_id"])

    result = {
        k: _cell_to_json(row.get(k))
        for k in PHONE_FIELDS
    }

    if include_enrichment:
        result["enrichment"] = _get_phone_enrichment(phone_id)

    return result


def _attach_enrichment_to_recommendations(result: dict) -> dict:
    recommendations = result.get("recommendations", [])

    for recommendation in recommendations:
        phone_id = recommendation.get("phone_id")

        if phone_id is not None:
            recommendation["enrichment"] = _get_phone_enrichment(int(phone_id))
        else:
            recommendation["enrichment"] = None

    return result


def _cell_to_json(value):
"""

if old not in text:
    raise RuntimeError("Could not find _phone_summary block")

text = text.replace(old, new, 1)


# 4. Attach enrichment to recommendation response
old = """    result = recommend_phones(
        phones,
        PhoneFilters(
            budget_max=req.budget_max,
            budget_min=req.budget_min,
            brand=req.brand,
            min_ram=req.min_ram,
            min_storage=req.min_storage,
            has_5g=req.has_5g,
            refresh_rate_min=req.refresh_rate_min,
        ),
        priority=req.priority,
        limit=req.limit,
    )
    return result
"""

new = """    result = recommend_phones(
        phones,
        PhoneFilters(
            budget_max=req.budget_max,
            budget_min=req.budget_min,
            brand=req.brand,
            min_ram=req.min_ram,
            min_storage=req.min_storage,
            has_5g=req.has_5g,
            refresh_rate_min=req.refresh_rate_min,
        ),
        priority=req.priority,
        limit=req.limit,
    )

    return _attach_enrichment_to_recommendations(result)
"""

if old not in text:
    raise RuntimeError("Could not find recommendation endpoint block")

text = text.replace(old, new, 1)


path.write_text(text, encoding="utf-8")

print("Stage 1C patch applied successfully.")
