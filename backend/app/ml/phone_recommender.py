"""
SmartChoice Mobile Recommendation Engine.

Explainable hybrid phone recommendation: hard user filters + priority-weighted
use-case scores. No TF-IDF dominance; no invented specifications.

Data source: backend/data/phones.csv (Stage A output, 980 cleaned variants).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Processor brand tiers (HEURISTIC, not benchmark data)
# ---------------------------------------------------------------------------
PROCESSOR_TIERS = {
    "bionic": 1.00,
    "snapdragon": 0.90,
    "dimensity": 0.88,
    "exynos": 0.75,
    "helio": 0.65,
    "unisoc": 0.55,
    "tiger": 0.50,
    "google": 0.70,
    "kirin": 0.72,
    "mediatek": 0.80,
    "spreadtrum": 0.45,
    "sc9863a": 0.45,
    "fusion": 0.60,
}
PROCESSOR_NEUTRAL_FALLBACK = 0.60  # unknown/missing brand -> neutral, not 0


@dataclass
class PhoneFilters:
    budget_max: Optional[int] = None
    budget_min: Optional[int] = None
    brand: Optional[str] = None
    min_ram: Optional[int] = None
    min_storage: Optional[int] = None
    has_5g: Optional[bool] = None
    refresh_rate_min: Optional[int] = None


PRIORITY_WEIGHTS = {
    "Gaming": {
        "gaming": 0.35, "performance": 0.25, "battery": 0.10,
        "value": 0.10, "camera": 0.05, "rating": 0.05, "overall": 0.10,
    },
    "Camera": {
        "camera": 0.40, "rating": 0.15, "value": 0.15, "performance": 0.10,
        "battery": 0.10, "gaming": 0.05, "overall": 0.05,
    },
    "Performance": {
        "performance": 0.40, "gaming": 0.20, "value": 0.15, "battery": 0.10,
        "rating": 0.10, "camera": 0.05,
    },
    "Battery": {
        "battery": 0.40, "value": 0.20, "performance": 0.15, "rating": 0.10,
        "camera": 0.10, "gaming": 0.05,
    },
    "Value": {
        "value": 0.40, "rating": 0.20, "performance": 0.15, "battery": 0.10,
        "camera": 0.10, "gaming": 0.05,
    },
    "Student": {
        "student": 0.35, "value": 0.20, "battery": 0.15, "performance": 0.10,
        "rating": 0.10, "camera": 0.05, "gaming": 0.05,
    },
    "Everyday": {
        "everyday": 0.35, "value": 0.20, "performance": 0.15, "battery": 0.10,
        "camera": 0.10, "rating": 0.10,
    },
}

REQUIRED_COLUMNS = [
    "phone_id", "brand", "model", "price_inr", "rating", "ram_gb", "storage_gb",
    "processor_brand", "processor_name", "core_count", "clock_speed_ghz",
    "battery_mah", "charging_watt", "refresh_rate_hz", "rear_camera_mp",
    "front_camera_mp", "rear_camera_count", "has_5g", "has_nfc", "os",
]

NUMERIC_FEATURES = [
    "price_inr", "rating", "ram_gb", "storage_gb", "core_count",
    "clock_speed_ghz", "battery_mah", "charging_watt", "refresh_rate_hz",
    "rear_camera_mp", "front_camera_mp",
]

# Percentile clipping bounds used before min-max normalization.
CLIP_BOUNDS = {
    "price_inr": (1, 99),
    "rating": (1, 99),
    "ram_gb": (1, 99),
    "storage_gb": (1, 99),
    "core_count": (1, 99),
    "clock_speed_ghz": (1, 99),
    "battery_mah": (1, 99),
    "charging_watt": (1, 99),
    "refresh_rate_hz": (1, 99),
    "rear_camera_mp": (1, 99),
    "front_camera_mp": (1, 99),
}


# ---------------------------------------------------------------------------
# Normalization helpers
# ---------------------------------------------------------------------------
def _robust_minmax(series: pd.Series, lo_pct: float = 1.0, hi_pct: float = 99.0) -> pd.Series:
    """Percentile-clipped min-max normalization into [0, 1].

    Missing values are preserved as NaN (never coerced to 0). The clipping
    bounds are computed from the *full* dataset so a single outlier cannot
    distort the entire scale.
    """
    s = pd.to_numeric(series, errors="coerce")
    if s.notna().sum() == 0:
        return pd.Series(np.nan, index=s.index)
    lo = float(np.nanpercentile(s.dropna(), lo_pct))
    hi = float(np.nanpercentile(s.dropna(), hi_pct))
    if hi == lo:
        return pd.Series(np.where(s.notna(), 0.5, np.nan), index=s.index)
    clipped = s.clip(lower=lo, upper=hi)
    return (clipped - lo) / (hi - lo)


def _log_norm(series: pd.Series, lo_pct: float = 1.0, hi_pct: float = 99.0) -> pd.Series:
    """log1p then min-max normalize into [0, 1]. Used for price."""
    s = pd.to_numeric(series, errors="coerce")
    if s.notna().sum() == 0:
        return pd.Series(np.nan, index=s.index)
    log_s = np.log1p(s.fillna(0))
    lo = float(np.nanpercentile(log_s.dropna(), lo_pct))
    hi = float(np.nanpercentile(log_s.dropna(), hi_pct))
    if hi == lo:
        return pd.Series(np.where(s.notna(), 0.5, np.nan), index=s.index)
    clipped = log_s.clip(lower=lo, upper=hi)
    return (clipped - lo) / (hi - lo)


def _renormalize(weights: dict) -> dict:
    """Renormalize a weight dict so its values sum to 1.0."""
    total = sum(weights.values())
    if total == 0:
        return {k: 0.0 for k in weights}
    return {k: v / total for k, v in weights.items()}


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
class PhoneData:
    """Loads and caches the cleaned phones dataset with normalized features."""

    def __init__(self, csv_path: Optional[str] = None):
        if csv_path is None:
            csv_path = str(Path(__file__).resolve().parent.parent.parent / "data" / "phones.csv")
        self.csv_path = csv_path
        self.raw = self._load(csv_path)
        self.features = self._compute_features(self.raw)

    @staticmethod
    def _load(csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path)
        missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise ValueError(f"phones.csv missing required columns: {missing}")
        return df.reset_index(drop=True)

    @staticmethod
    def _compute_features(df: pd.DataFrame) -> pd.DataFrame:
        f = pd.DataFrame(index=df.index)
        f["phone_id"] = df["phone_id"]
        f["brand"] = df["brand"].astype(str).str.strip()
        f["model"] = df["model"].astype(str).str.strip()
        f["os"] = df["os"].astype(str).str.strip().str.lower()
        f["has_5g"] = df["has_5g"].astype(int)
        f["has_nfc"] = df["has_nfc"].astype(int)

        f["price_inr"] = pd.to_numeric(df["price_inr"], errors="coerce")
        f["rating"] = pd.to_numeric(df["rating"], errors="coerce")
        f["ram_gb"] = pd.to_numeric(df["ram_gb"], errors="coerce")
        f["storage_gb"] = pd.to_numeric(df["storage_gb"], errors="coerce")
        f["core_count"] = pd.to_numeric(df["core_count"], errors="coerce")
        f["clock_speed_ghz"] = pd.to_numeric(df["clock_speed_ghz"], errors="coerce")
        f["battery_mah"] = pd.to_numeric(df["battery_mah"], errors="coerce")
        f["charging_watt"] = pd.to_numeric(df["charging_watt"], errors="coerce")
        f["refresh_rate_hz"] = pd.to_numeric(df["refresh_rate_hz"], errors="coerce")
        f["rear_camera_mp"] = pd.to_numeric(df["rear_camera_mp"], errors="coerce")
        f["front_camera_mp"] = pd.to_numeric(df["front_camera_mp"], errors="coerce")
        f["rear_camera_count"] = pd.to_numeric(df["rear_camera_count"], errors="coerce")
        f["processor_brand"] = df["processor_brand"].astype(str).str.strip().str.lower()

        # Normalized [0,1] features (NaN preserved for missing).
        f["price_log_norm"] = _log_norm(f["price_inr"])
        f["rating_norm"] = _robust_minmax(f["rating"])
        f["ram_norm"] = _robust_minmax(f["ram_gb"])
        f["storage_norm"] = _robust_minmax(f["storage_gb"])
        f["core_norm"] = _robust_minmax(f["core_count"])
        f["clock_norm"] = _robust_minmax(f["clock_speed_ghz"])
        f["battery_norm"] = _robust_minmax(f["battery_mah"])
        f["charging_norm"] = _robust_minmax(f["charging_watt"])
        f["refresh_norm"] = _robust_minmax(f["refresh_rate_hz"])
        f["rear_cam_norm"] = _robust_minmax(f["rear_camera_mp"])
        f["front_cam_norm"] = _robust_minmax(f["front_camera_mp"])

        # Processor tier score (heuristic; neutral fallback for unknown/missing).
        f["processor_score"] = f["processor_brand"].map(PROCESSOR_TIERS).fillna(PROCESSOR_NEUTRAL_FALLBACK)

        # Value score: rating efficiency per log-price (NaN-safe).
        f["value_score"] = _safe_value(f)

        return f


def _safe_value(f: pd.DataFrame) -> pd.Series:
    """rating / log1p(price). NaN where rating or price is missing."""
    rating = f["rating"]
    log_price = np.log1p(f["price_inr"].fillna(0))
    raw = rating / log_price.replace(0, np.nan)
    return _robust_minmax(raw)


# ---------------------------------------------------------------------------
# Use-case scores (all in [0,1]; NaN components are skipped and weights
# renormalized so a phone is not unfairly penalized for missing data)
# ---------------------------------------------------------------------------
def _combine(weights: dict, series_map: dict) -> pd.Series:
    """Weighted sum with per-row renormalization over available components."""
    total = pd.Series(0.0, index=next(iter(series_map.values())).index)
    weight_sum = pd.Series(0.0, index=total.index)
    for key, w in weights.items():
        s = series_map[key].fillna(np.nan)
        mask = s.notna().to_numpy()
        total = total + (s.fillna(0.0) * w)
        weight_sum = weight_sum + pd.Series(np.where(mask, w, 0.0), index=total.index)
    result = total / weight_sum.replace(0, np.nan)
    return result.fillna(0.0).clip(0.0, 1.0)


def compute_use_case_scores(f: pd.DataFrame) -> pd.DataFrame:
    s = pd.DataFrame(index=f.index)

    ps = f["processor_score"].fillna(PROCESSOR_NEUTRAL_FALLBACK)
    rn = f["ram_norm"].fillna(0.5)
    rf = f["refresh_norm"].fillna(0.5)
    cn = f["core_norm"].fillna(0.5)
    clk = f["clock_norm"].fillna(0.5)
    bat = f["battery_norm"].fillna(0.5)
    chg = f["charging_norm"].fillna(np.nan)
    rc = f["rear_cam_norm"].fillna(0.5)
    fc = f["front_cam_norm"].fillna(0.5)
    rcnt = f["rear_camera_count"].fillna(0.0)
    rcnt_norm = _robust_minmax(rcnt).fillna(0.5)
    val = f["value_score"].fillna(0.5)
    rtg = f["rating_norm"].fillna(0.5)

    # Gaming: processor + RAM + refresh + clock + cores
    s["gaming_score"] = _combine(
        {"processor": 0.35, "ram": 0.20, "refresh": 0.20, "clock": 0.15, "core": 0.10},
        {"processor": ps, "ram": rn, "refresh": rf, "clock": clk, "core": cn},
    )
    # Performance: processor + clock + RAM + cores
    s["performance_score"] = _combine(
        {"processor": 0.45, "clock": 0.20, "ram": 0.20, "core": 0.15},
        {"processor": ps, "clock": clk, "ram": rn, "core": cn},
    )
    # Camera: rear + front + rear count bonus
    s["camera_score"] = _combine(
        {"rear": 0.60, "front": 0.25, "count": 0.15},
        {"rear": rc, "front": fc, "count": rcnt_norm},
    )
    # Battery: capacity + charging (charging missing -> renormalize)
    s["battery_score"] = _combine(
        {"battery": 0.65, "charging": 0.35},
        {"battery": bat, "charging": chg},
    )
    # Student: value + battery + RAM + storage
    s["student_score"] = _combine(
        {"value": 0.35, "battery": 0.25, "ram": 0.20, "storage": 0.20},
        {"value": val, "battery": bat, "ram": rn, "storage": f["storage_norm"].fillna(0.5)},
    )
    # Everyday: balanced
    s["everyday_score"] = _combine(
        {"value": 0.25, "performance": 0.25, "battery": 0.20, "camera": 0.15, "rating": 0.15},
        {"value": val, "performance": s["performance_score"], "battery": bat,
         "camera": s["camera_score"], "rating": rtg},
    )
    return s


# ---------------------------------------------------------------------------
# Hard filters
# ---------------------------------------------------------------------------
def apply_hard_filters(f: pd.DataFrame, flt: PhoneFilters) -> pd.DataFrame:
    """Apply user constraints. Filters are None -> not applied."""
    mask = pd.Series(True, index=f.index)

    if flt.budget_max is not None:
        mask &= f["price_inr"].fillna(np.inf) <= flt.budget_max
    if flt.budget_min is not None:
        mask &= f["price_inr"].fillna(-np.inf) >= flt.budget_min
    if flt.brand is not None:
        mask &= f["brand"].str.lower() == str(flt.brand).strip().lower()
    if flt.min_ram is not None:
        mask &= f["ram_gb"].fillna(-1) >= flt.min_ram
    if flt.min_storage is not None:
        mask &= f["storage_gb"].fillna(-1) >= flt.min_storage
    if flt.has_5g is True:
        mask &= f["has_5g"] == 1
    if flt.refresh_rate_min is not None:
        mask &= f["refresh_rate_hz"].fillna(-1) >= flt.refresh_rate_min

    return f[mask].copy()


# ---------------------------------------------------------------------------
# Reason generation (explainability)
# ---------------------------------------------------------------------------
def _reasons(
    row: pd.Series,
    scores: dict,
    priority: str,
    enrichment: Optional[dict] = None,
) -> list:
    """Generate concise, data-backed recommendation reasons.

    Enrichment is optional and never affects ranking.
    Only verified/non-empty enrichment values are used.
    """
    reasons = []
    enrichment = enrichment or {}

    def has_value(key: str) -> bool:
        value = enrichment.get(key)
        if value is None:
            return False
        if pd.isna(value):
            return False
        return str(value).strip().lower() not in {"", "na", "nan", "none"}

    def add(reason: str) -> None:
        if reason and reason not in reasons:
            reasons.append(reason)

    # ---------------------------------------------------------
    # Enriched display
    # ---------------------------------------------------------
    if has_value("display_type") and priority in ("Gaming", "Everyday", "Performance"):
        display_type = str(enrichment["display_type"]).strip()
        refresh = enrichment.get("display_refresh_rate_hz")

        if has_value("display_refresh_rate_hz"):
            try:
                refresh = float(refresh)
                add(f"{int(refresh)} Hz {display_type} display")
            except (TypeError, ValueError):
                add(f"{display_type} display")
        else:
            add(f"{display_type} display")

    # ---------------------------------------------------------
    # Enriched camera
    # ---------------------------------------------------------
    if priority == "Camera":
        if has_value("rear_main_mp"):
            try:
                mp = float(enrichment["rear_main_mp"])
                camera_reason = f"{int(mp) if mp.is_integer() else mp} MP main camera"

                if has_value("rear_main_ois"):
                    ois = str(enrichment["rear_main_ois"]).strip().lower()
                    if ois in {"yes", "true", "1"}:
                        camera_reason += " with OIS"

                add(camera_reason)
            except (TypeError, ValueError):
                pass

        if has_value("rear_main_sensor"):
            add(f"Main camera uses {str(enrichment['rear_main_sensor']).strip()} sensor")

        if has_value("rear_video_max"):
            add(f"Rear video up to {str(enrichment['rear_video_max']).strip()}")

    # ---------------------------------------------------------
    # Enriched battery / charging
    # ---------------------------------------------------------
    if priority == "Battery":
        if has_value("wired_charging_w"):
            try:
                watts = float(enrichment["wired_charging_w"])
                add(f"{int(watts) if watts.is_integer() else watts}W wired charging")
            except (TypeError, ValueError):
                pass

        if has_value("wireless_charging_w"):
            try:
                watts = float(enrichment["wireless_charging_w"])
                if watts > 0:
                    add(f"{int(watts) if watts.is_integer() else watts}W wireless charging")
            except (TypeError, ValueError):
                pass

    # ---------------------------------------------------------
    # Enriched build / durability
    # ---------------------------------------------------------
    if priority in ("Everyday", "Value"):
        if has_value("ip_rating"):
            add(f"{str(enrichment['ip_rating']).strip()} water/dust resistance")

        if has_value("build_back"):
            build_back = str(enrichment["build_back"]).strip()
            if build_back.lower() not in {"plastic", "na"}:
                add(f"{build_back} back")

    # ---------------------------------------------------------
    # Existing base-data reasons
    # ---------------------------------------------------------
    if priority in ("Gaming", "Performance") and pd.notna(row.get("refresh_rate_hz")):
        rr = float(row["refresh_rate_hz"])
        if rr >= 120:
            add(f"{int(rr)} Hz refresh rate is useful for gaming")

    if pd.notna(row.get("ram_gb")) and float(row["ram_gb"]) >= 8:
        add(f"{int(row['ram_gb'])} GB RAM supports demanding apps")

    if pd.notna(row.get("battery_mah")) and float(row["battery_mah"]) >= 5000:
        add(f"Large {int(row['battery_mah'])} mAh battery")

    if pd.notna(row.get("charging_watt")) and float(row["charging_watt"]) >= 30:
        add(f"Fast {int(row['charging_watt'])}W charging")

    if pd.notna(row.get("rear_camera_mp")) and float(row["rear_camera_mp"]) >= 48:
        add("Strong camera hardware")

    if pd.notna(row.get("value_score")) and float(scores.get("value_score", 0)) >= 0.7:
        add("Good value for the price")

    if priority == "Battery" and pd.notna(row.get("battery_mah")):
        if float(row["battery_mah"]) >= 5000:
            add(f"Large {int(row['battery_mah'])} mAh battery")

    if float(row.get("has_5g", 0)) == 1:
        add("Meets your 5G requirement")

    return reasons[:3]
    reasons = []

    # Performance / gaming
    if priority in ("Gaming", "Performance") and pd.notna(row.get("refresh_rate_hz")):
        rr = float(row["refresh_rate_hz"])
        if rr >= 120:
            reasons.append(f"{int(rr)} Hz refresh rate is useful for gaming")
    if pd.notna(row.get("ram_gb")) and float(row["ram_gb"]) >= 8:
        reasons.append(f"{int(row['ram_gb'])} GB RAM supports demanding apps")
    if pd.notna(row.get("battery_mah")) and float(row["battery_mah"]) >= 5000:
        reasons.append(f"Large {int(row['battery_mah'])} mAh battery")
    if pd.notna(row.get("charging_watt")) and float(row["charging_watt"]) >= 30:
        reasons.append(f"Fast {int(row['charging_watt'])}W charging")
    if pd.notna(row.get("rear_camera_mp")) and float(row["rear_camera_mp"]) >= 48:
        reasons.append("Strong camera hardware")
    if pd.notna(row.get("value_score")) and float(scores.get("value_score", 0)) >= 0.7:
        reasons.append("Good value for the price")
    if priority == "Battery" and pd.notna(row.get("battery_mah")) and float(row["battery_mah"]) >= 5000:
        if "Large" not in " ".join(reasons):
            reasons.append(f"Large {int(row['battery_mah'])} mAh battery")
    if float(row.get("has_5g", 0)) == 1:
        reasons.append("Meets your 5G requirement")

    # Deduplicate and keep strongest 3.
    seen = set()
    out = []
    for r in reasons:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out[:3]


# ---------------------------------------------------------------------------
# Main recommendation function
# ---------------------------------------------------------------------------
def recommend_phones(
    data: PhoneData,
    filters: PhoneFilters,
    priority: str = "Value",
    limit: int = 10,
) -> dict:
    """Return ranked phone recommendations for the given preferences."""
    if priority not in PRIORITY_WEIGHTS:
        raise ValueError(f"Unknown priority: {priority}. Choose from {list(PRIORITY_WEIGHTS)}")

    f = data.features.copy()
    candidates = apply_hard_filters(f, filters)

    if len(candidates) == 0:
        return {
            "applied_preferences": filters_to_dict(filters),
            "priority": priority,
            "total": 0,
            "recommendations": [],
            "candidate_pool": 0,
        }

    scores = compute_use_case_scores(candidates)
    for col in scores.columns:
        candidates[col] = scores[col].values

    weights = dict(PRIORITY_WEIGHTS[priority])
    overall_key = "overall" if "overall" in weights else None

    score_map = {
        "gaming": "gaming_score",
        "performance": "performance_score",
        "camera": "camera_score",
        "battery": "battery_score",
        "value": "value_score",
        "student": "student_score",
        "everyday": "everyday_score",
        "rating": "rating_norm",
        "overall": "value_score",
    }

    total = pd.Series(0.0, index=candidates.index)
    weight_sum = pd.Series(0.0, index=candidates.index)
    for key, w in weights.items():
        col = score_map.get(key)
        if col is None or col not in candidates.columns:
            continue
        s = pd.to_numeric(candidates[col], errors="coerce").fillna(0.0).clip(0.0, 1.0)
        total = total + s * w
        weight_sum = weight_sum + w

    final = (total / weight_sum.replace(0, np.nan)).fillna(0.0).clip(0.0, 1.0)
    candidates["final_score"] = final
    candidates["match_percentage"] = (final * 100).round(1)

    ranked = candidates.sort_values("final_score", ascending=False).head(limit)

    recs = []
    score_cols = ["gaming_score", "camera_score", "performance_score",
                  "battery_score", "value_score", "student_score",
                  "everyday_score", "rating_norm"]
    for _, row in ranked.iterrows():
        sc = {c: float(row.get(c, 0.0)) for c in score_cols if c in row.index}
        recs.append({
            "phone_id": int(row["phone_id"]),
            "brand": str(row["brand"]),
            "model": str(row["model"]),
            "price_inr": _maybe_int(row.get("price_inr")),
            "rating": _maybe_float(row.get("rating")),
            "ram_gb": _maybe_float(row.get("ram_gb")),
            "storage_gb": _maybe_float(row.get("storage_gb")),
            "processor_brand": str(row.get("processor_brand", "")),
            "battery_mah": _maybe_int(row.get("battery_mah")),
            "charging_watt": _maybe_float(row.get("charging_watt")),
            "refresh_rate_hz": _maybe_int(row.get("refresh_rate_hz")),
            "rear_camera_mp": _maybe_float(row.get("rear_camera_mp")),
            "front_camera_mp": _maybe_float(row.get("front_camera_mp")),
            "has_5g": bool(int(row.get("has_5g", 0)) == 1),
            "os": str(row.get("os", "")),
            "match_percentage": _safe_score(row["match_percentage"]),
            "gaming_score": _safe_score(row.get("gaming_score", 0.0)),
            "camera_score": _safe_score(row.get("camera_score", 0.0)),
            "performance_score": _safe_score(row.get("performance_score", 0.0)),
            "battery_score": _safe_score(row.get("battery_score", 0.0)),
            "value_score": _safe_score(row.get("value_score", 0.0)),
            "student_score": _safe_score(row.get("student_score", 0.0)),
            "everyday_score": _safe_score(row.get("everyday_score", 0.0)),
            "reasons": _reasons(row, sc, priority),
        })

    return {
        "applied_preferences": filters_to_dict(filters),
        "priority": priority,
        "total": len(recs),
        "recommendations": recs,
        "candidate_pool": int(len(candidates)),
    }


def filters_to_dict(flt: PhoneFilters) -> dict:
    return {
        "budget_max": flt.budget_max,
        "brand": flt.brand,
        "min_ram": flt.min_ram,
        "min_storage": flt.min_storage,
        "has_5g": flt.has_5g,
        "refresh_rate_min": flt.refresh_rate_min,
    }


def _maybe_int(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    return int(v)


def _maybe_float(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return None
    return float(v)


def _safe_score(v):
    """Convert a score value to a JSON-safe float.

    NaN and infinite values are mapped to 0.0 so they never reach the API
    response. Valid scores are returned unchanged.
    """
    try:
        f = float(v)
    except (TypeError, ValueError):
        return 0.0
    if math.isnan(f) or math.isinf(f):
        return 0.0
    return f