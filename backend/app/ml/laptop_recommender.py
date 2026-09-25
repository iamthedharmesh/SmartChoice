"""
SmartChoice - Laptop Hardware Persona Recommendation Engine
Evaluates laptop specifications against user priorities:
- Coding / Software Engineering (RAM, multi-core CPU, NVMe SSD speed, display density)
- Gaming & 3D Rendering (Dedicated RTX GPU tier, high refresh rate, cooling headroom)
- Student & Portability (Sub-1.5kg weight, battery capacity in Whr, affordability)
- Productivity & Everyday (Balanced 16GB RAM, modern CPU, display comfort, reliability)
- Value for Money (Maximum hardware per rupee spent)
"""

import os
from typing import Any, Dict, List, Optional
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "laptops.csv")

def _calc_coding_score(row: pd.Series) -> float:
    # RAM Weight (40%)
    ram = row.get("ram_gb", 8) or 8
    if ram >= 32:
        ram_score = 100.0
    elif ram >= 18:
        ram_score = 94.0
    elif ram >= 16:
        ram_score = 88.0
    elif ram >= 12:
        ram_score = 75.0
    else:
        ram_score = 55.0

    # CPU Cores & Tier (35%)
    cores = row.get("cpu_cores", 6) or 6
    if cores >= 16:
        cpu_score = 100.0
    elif cores >= 12:
        cpu_score = 92.0
    elif cores >= 10:
        cpu_score = 86.0
    elif cores >= 8:
        cpu_score = 80.0
    elif cores >= 6:
        cpu_score = 70.0
    else:
        cpu_score = 52.0

    # Storage (15%)
    storage = row.get("storage_gb", 512) or 512
    storage_score = 100.0 if storage >= 1024 else (85.0 if storage >= 512 else 60.0)

    # Display Resolution / Real Estate (10%)
    res = str(row.get("resolution", "")).lower()
    if any(k in res for k in ["retina", "2.8k", "3k", "3.2k", "wqxga", "qhd"]):
        disp_score = 95.0
    elif "wuxga" in res or "fhd+" in res:
        disp_score = 85.0
    else:
        disp_score = 72.0

    return round(ram_score * 0.40 + cpu_score * 0.35 + storage_score * 0.15 + disp_score * 0.10, 1)


def _calc_gaming_score(row: pd.Series) -> float:
    gpu_type = str(row.get("gpu_type", "Integrated")).lower()
    gpu_model = str(row.get("gpu_model", "")).lower()
    refresh = row.get("refresh_rate_hz", 60) or 60

    # GPU Power Tier (60%)
    if "rtx 4080" in gpu_model:
        gpu_score = 100.0
    elif "rtx 4070" in gpu_model:
        gpu_score = 93.0
    elif "rtx 4060" in gpu_model:
        gpu_score = 86.0
    elif "rtx 4050" in gpu_model:
        gpu_score = 78.0
    elif "rtx 3050" in gpu_model or "a1000" in gpu_model:
        gpu_score = 68.0
    elif "rtx 2050" in gpu_model or "rx 6500m" in gpu_model:
        gpu_score = 58.0
    elif "m3 max" in str(row.get("processor_model", "")).lower():
        gpu_score = 82.0
    elif "m3 pro" in str(row.get("processor_model", "")).lower():
        gpu_score = 74.0
    elif "arc" in gpu_model or "radeon 780m" in gpu_model:
        gpu_score = 54.0
    else:
        gpu_score = 30.0

    # Refresh Rate (25%)
    if refresh >= 240:
        refresh_score = 100.0
    elif refresh >= 165:
        refresh_score = 92.0
    elif refresh >= 144:
        refresh_score = 85.0
    elif refresh >= 120:
        refresh_score = 75.0
    else:
        refresh_score = 45.0

    # RAM Capacity (15%)
    ram = row.get("ram_gb", 8) or 8
    ram_score = 100.0 if ram >= 32 else (88.0 if ram >= 16 else 55.0)

    return round(gpu_score * 0.60 + refresh_score * 0.25 + ram_score * 0.15, 1)


def _calc_student_score(row: pd.Series) -> float:
    # Portability / Weight (45%)
    weight = float(row.get("weight_kg", 1.8) or 1.8)
    if weight <= 1.25:
        weight_score = 100.0
    elif weight <= 1.45:
        weight_score = 92.0
    elif weight <= 1.65:
        weight_score = 82.0
    elif weight <= 1.85:
        weight_score = 70.0
    elif weight <= 2.10:
        weight_score = 55.0
    else:
        weight_score = 40.0

    # Battery Life Whr (35%)
    whr = float(row.get("battery_whr", 50) or 50)
    if whr >= 80:
        bat_score = 100.0
    elif whr >= 70:
        bat_score = 92.0
    elif whr >= 54:
        bat_score = 82.0
    elif whr >= 42:
        bat_score = 70.0
    else:
        bat_score = 50.0

    # General Rating & Value (20%)
    rating = float(row.get("rating", 80) or 80)
    return round(weight_score * 0.45 + bat_score * 0.35 + rating * 0.20, 1)


def _calc_productivity_score(row: pd.Series) -> float:
    coding = _calc_coding_score(row)
    student = _calc_student_score(row)
    rating = float(row.get("rating", 80) or 80)
    return round(coding * 0.45 + student * 0.35 + rating * 0.20, 1)


def _calc_value_score(row: pd.Series) -> float:
    price = float(row.get("price_inr", 60000) or 60000)
    rating = float(row.get("rating", 80) or 80)
    ram = float(row.get("ram_gb", 8) or 8)

    # Benchmark capability points relative to expenditure
    capability = rating + (ram >= 16) * 6
    if price < 40000:
        value = min(98.0, capability * 1.15)
    elif price < 65000:
        value = min(95.0, capability * 1.05)
    elif price < 100000:
        value = min(90.0, capability * 0.95)
    else:
        value = min(85.0, capability * 0.85)

    return round(value, 1)


def _generate_reasons(row: pd.Series, priority: str) -> List[str]:
    reasons = []
    gpu_type = str(row.get("gpu_type", "")).lower()
    gpu_model = str(row.get("gpu_model", ""))
    refresh = row.get("refresh_rate_hz", 60) or 60
    ram = row.get("ram_gb", 8) or 8
    storage = row.get("storage_gb", 512) or 512
    weight = float(row.get("weight_kg", 1.8) or 1.8)
    whr = float(row.get("battery_whr", 50) or 50)
    res = str(row.get("resolution", ""))
    cores = row.get("cpu_cores", 6) or 6

    if priority == "Gaming":
        if "dedicated" in gpu_type:
            reasons.append(f"{gpu_model} dedicated GPU handles modern AAA gaming & rendering")
        if refresh >= 120:
            reasons.append(f"Ultra-smooth {refresh}Hz high refresh display")
        if ram >= 16:
            reasons.append(f"{ram} GB RAM ensures zero stutter in heavy scenes")
    elif priority == "Coding":
        reasons.append(f"{ram} GB RAM supports Docker, VMs, and multiple IDEs")
        reasons.append(f"{cores}-core CPU accelerates compilation and background processes")
        if "retina" in res.lower() or "oled" in res.lower() or "2.8k" in res.lower():
            reasons.append(f"High-density {res} panel reduces eye fatigue")
    elif priority == "Student":
        if weight <= 1.5:
            reasons.append(f"Ultra-lightweight {weight} kg chassis is effortless for campus travel")
        if whr >= 50:
            reasons.append(f"{int(whr)} Whr high-capacity battery powers full days of classes")
        reasons.append("Reliable ergonomics and build for long study sessions")
    elif priority == "Value":
        reasons.append(f"Class-leading hardware specifications in the {int(row.get('price_inr', 0)):,} INR tier")
        if ram >= 16:
            reasons.append(f"Generous {ram} GB RAM and {storage} GB fast SSD")
    else:  # Productivity / Everyday
        reasons.append(f"Balanced performance with {ram} GB memory and {row.get('processor_model')}")
        if whr >= 50:
            reasons.append(f"{int(whr)} Whr battery for all-day unplugged productivity")
        if weight <= 1.6:
            reasons.append(f"Sleek {weight} kg portable form factor")

    if not reasons:
        reasons.append(f"Solid all-rounder with {ram} GB RAM and {storage} GB NVMe storage")
    return reasons[:3]


class LaptopRecommender:
    def __init__(self, csv_path: str = DATA_PATH):
        self.csv_path = csv_path
        self._df: Optional[pd.DataFrame] = None
        self._load()

    def _load(self):
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"Laptops CSV not found at {self.csv_path}")
        df = pd.read_csv(self.csv_path)
        df["coding_score"] = df.apply(_calc_coding_score, axis=1)
        df["gaming_score"] = df.apply(_calc_gaming_score, axis=1)
        df["student_score"] = df.apply(_calc_student_score, axis=1)
        df["productivity_score"] = df.apply(_calc_productivity_score, axis=1)
        df["value_score"] = df.apply(_calc_value_score, axis=1)
        self._df = df

    @property
    def df(self) -> pd.DataFrame:
        if self._df is None:
            self._load()
        return self._df

    def get_all(self, page: int = 1, limit: int = 12, brand: Optional[str] = None,
                min_price: Optional[float] = None, max_price: Optional[float] = None,
                min_ram: Optional[int] = None, gpu_type: Optional[str] = None,
                search: Optional[str] = None) -> Dict[str, Any]:
        df = self.df.copy()

        if brand and brand != "Any Brand":
            df = df[df["brand"].str.lower() == brand.strip().lower()]
        if min_price is not None:
            df = df[df["price_inr"] >= min_price]
        if max_price is not None:
            df = df[df["price_inr"] <= max_price]
        if min_ram is not None:
            df = df[df["ram_gb"] >= min_ram]
        if gpu_type and gpu_type.lower() != "all":
            df = df[df["gpu_type"].str.lower() == gpu_type.strip().lower()]
        if search:
            q = search.strip().lower()
            df = df[
                df["brand"].str.lower().str.contains(q, na=False) |
                df["model"].str.lower().str.contains(q, na=False) |
                df["processor_model"].str.lower().str.contains(q, na=False) |
                df["gpu_model"].str.lower().str.contains(q, na=False)
            ]

        total = len(df)
        total_pages = max(1, (total + limit - 1) // limit)
        start = (page - 1) * limit
        end = start + limit
        items = df.iloc[start:end].to_dict(orient="records")

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "laptops": items,
        }

    def get_by_id(self, laptop_id: int) -> Optional[Dict[str, Any]]:
        matches = self.df[self.df["laptop_id"] == laptop_id]
        if matches.empty:
            return None
        return matches.iloc[0].to_dict()

    def get_brands(self) -> List[str]:
        return sorted(self.df["brand"].dropna().unique().tolist())

    def recommend(self, budget_min: Optional[float] = None, budget_max: Optional[float] = None,
                  brand: Optional[str] = None, min_ram: Optional[int] = None,
                  gpu_type: Optional[str] = None, priority: str = "Coding",
                  top_k: int = 8) -> List[Dict[str, Any]]:
        df = self.df.copy()

        # Hard constraints
        if budget_min is not None:
            df = df[df["price_inr"] >= budget_min]
        if budget_max is not None:
            df = df[df["price_inr"] <= budget_max]
        if brand and brand != "Any Brand":
            df = df[df["brand"].str.lower() == brand.strip().lower()]
        if min_ram is not None:
            df = df[df["ram_gb"] >= min_ram]
        if gpu_type and gpu_type.lower() != "all":
            df = df[df["gpu_type"].str.lower() == gpu_type.strip().lower()]

        if df.empty:
            return []

        priority_key = priority.lower()
        if "game" in priority_key:
            score_col = "gaming_score"
        elif "code" in priority_key or "soft" in priority_key or "dev" in priority_key:
            score_col = "coding_score"
        elif "student" in priority_key or "thin" in priority_key or "portable" in priority_key:
            score_col = "student_score"
        elif "value" in priority_key or "budget" in priority_key:
            score_col = "value_score"
        else:
            score_col = "productivity_score"

        # Calculate final match percentage with budget headroom bonus
        def compute_match(row):
            base = row[score_col]
            # Small bonus if comfortably within budget
            if budget_max and row["price_inr"] <= budget_max * 0.95:
                base = min(99.0, base + 2.0)
            return round(base, 1)

        df["match_percentage"] = df.apply(compute_match, axis=1)
        df["reasons"] = df.apply(lambda r: _generate_reasons(r, priority), axis=1)

        ranked = df.sort_values(by=["match_percentage", "rating"], ascending=[False, False])
        return ranked.head(top_k).to_dict(orient="records")


# Singleton instance
recommender = LaptopRecommender()