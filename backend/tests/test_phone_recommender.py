import sys
sys.path.insert(0, "D:\\SmartChoice\\backend")
from app.ml.phone_recommender import (
    PhoneData, PhoneFilters, recommend_phones, PRIORITY_WEIGHTS,
    compute_use_case_scores,
)

data = PhoneData()
PASS = 0
FAIL = 0

def check(name, cond):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  PASS  {name}")
    else:
        FAIL += 1
        print(f"  FAIL  {name}")

print("=== PHONE RECOMMENDER TESTS ===")

# A. No filters + Gaming
r = recommend_phones(data, PhoneFilters(), priority="Gaming", limit=5)
check("A. no-filter returns results", r["total"] > 0)
check("A. pool is full", r["candidate_pool"] == 980)
check("A. limit respected", r["total"] <= 5)

# B. Budget filter
rB = recommend_phones(data, PhoneFilters(budget_max=20000), priority="Value", limit=10)
check("B. budget respected", all(x["price_inr"] <= 20000 for x in rB["recommendations"]))
check("B. budget returns results", rB["total"] > 0)

# C. Brand filter
rC = recommend_phones(data, PhoneFilters(brand="Samsung"), priority="Value", limit=10)
check("C. brand respected", all(x["brand"].lower() == "samsung" for x in rC["recommendations"]))
check("C. brand returns results", rC["total"] > 0)

# D. Minimum RAM
rD = recommend_phones(data, PhoneFilters(min_ram=12), priority="Value", limit=10)
check("D. min_ram respected", all(x["ram_gb"] >= 12 for x in rD["recommendations"]))

# E. Minimum storage
rE = recommend_phones(data, PhoneFilters(min_storage=256), priority="Value", limit=10)
check("E. min_storage respected", all(x["storage_gb"] >= 256 for x in rE["recommendations"]))

# F. 5G requirement
rF = recommend_phones(data, PhoneFilters(has_5g=True), priority="Value", limit=10)
check("F. 5G respected", all(x["has_5g"] is True for x in rF["recommendations"]))
check("F. no has_5g=false returned", all(x["has_5g"] for x in rF["recommendations"]))

# G. Minimum refresh rate
rG = recommend_phones(data, PhoneFilters(refresh_rate_min=120), priority="Value", limit=10)
check("G. refresh respected", all(x["refresh_rate_hz"] >= 120 for x in rG["recommendations"]))

# H. Multiple hard filters together
rH = recommend_phones(
    data,
    PhoneFilters(budget_max=25000, brand="Samsung", min_ram=6, min_storage=128, has_5g=True, refresh_rate_min=90),
    priority="Value", limit=10,
)
check("H. combined filters respected", all(
    x["price_inr"] <= 25000 and x["brand"].lower() == "samsung"
    and x["ram_gb"] >= 6 and x["storage_gb"] >= 128
    and x["has_5g"] and x["refresh_rate_hz"] >= 90
    for x in rH["recommendations"]))

# I. Different priorities produce different rankings
rGaming = recommend_phones(data, PhoneFilters(budget_max=30000), priority="Gaming", limit=1)
rCamera = recommend_phones(data, PhoneFilters(budget_max=30000), priority="Camera", limit=1)
check("I. priorities differ", rGaming["recommendations"][0]["phone_id"] != rCamera["recommendations"][0]["phone_id"])

# J. Missing rating does not crash
rJ = recommend_phones(data, PhoneFilters(budget_max=15000), priority="Value", limit=5)
check("J. missing-rating phones handled", rJ["total"] >= 0)

# K. Missing charging wattage is not zero
feat = data.features
missing_chg = feat[feat["charging_watt"].isna()]
check("K. missing charging preserved as null", len(missing_chg) > 0)
check("K. no false zero charging", all(x["charging_watt"] != 0 or x["charging_watt"] is None for x in rJ["recommendations"]))

# L. Missing processor does not crash
rL = recommend_phones(data, PhoneFilters(budget_max=20000), priority="Performance", limit=5)
check("L. missing-processor handled", rL["total"] >= 0)

# M. All normalized scores in [0,1]
sc = compute_use_case_scores(data.features)
okM = all(sc[c].between(0, 1).all() for c in sc.columns)
check("M. scores in [0,1]", okM)

# N. All priority weights sum to 1.0
okN = all(abs(sum(w.values()) - 1.0) < 1e-9 for w in PRIORITY_WEIGHTS.values())
check("N. weights sum to 1.0", okN)

# O. Match percentage in 0-100
okO = all(0 <= x["match_percentage"] <= 100 for r in [r, rB, rC, rD, rE, rF, rG, rH, rGaming, rCamera, rJ, rL] for x in r["recommendations"])
check("O. match_percentage in [0,100]", okO)

# P. Different RAM/storage variants remain separate
variants = data.features[data.features["model"].str.contains("Nord CE 2 Lite", na=False)]
check("P. variants preserved", len(variants) >= 2)
check("P. distinct phone_ids", variants["phone_id"].nunique() == len(variants))

# Q. Empty candidate set handled cleanly
rQ = recommend_phones(data, PhoneFilters(budget_max=1000), priority="Value", limit=10)
check("Q. empty set handled", rQ["total"] == 0 and rQ["recommendations"] == [])

# Extra: over-budget phone can never appear
over = data.features[data.features["price_inr"] > 20000]
over_ids = set(over["phone_id"].tolist())
returned_ids = set(x["phone_id"] for x in rB["recommendations"])
check("EXTRA. no over-budget phone", len(over_ids & returned_ids) == 0)

# Extra: 5G requirement never returns has_5g=false
check("EXTRA. 5G only true", all(x["has_5g"] for x in rF["recommendations"]))

# Extra: reasons limited to 3
check("EXTRA. reasons <= 3", all(len(x["reasons"]) <= 3 for x in r["recommendations"]))

print(f"\n=== RESULTS: {PASS} passed, {FAIL} failed ===")
sys.exit(1 if FAIL else 0)