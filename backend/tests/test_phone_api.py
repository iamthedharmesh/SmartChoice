import sys
sys.path.insert(0, "D:\\SmartChoice\\backend")
from fastapi.testclient import TestClient
from app.main import app

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

print("=== PHONE API TESTS ===")

with TestClient(app) as client:
    # 1. GET /mobiles returns 200
    r = client.get("/mobiles")
    check("1. /mobiles returns 200", r.status_code == 200, r.status_code)
    data = r.json()
    check("1b. has page/limit/total/mobiles", all(k in data for k in ("page", "limit", "total", "mobiles")))
    check("1c. total is 980", data["total"] == 980, data["total"])
    check("1d. mobiles is list", isinstance(data["mobiles"], list))

    # 2. Pagination works
    r2 = client.get("/mobiles", params={"page": 2, "limit": 10})
    check("2a. page 2 returns 200", r2.status_code == 200)
    d2 = r2.json()
    check("2b. page=2", d2["page"] == 2)
    check("2c. limit=10", d2["limit"] == 10)
    check("2d. len matches limit", len(d2["mobiles"]) == 10)
    r1 = client.get("/mobiles", params={"page": 1, "limit": 10})
    check("2e. page1 != page2 ids", r1.json()["mobiles"][0]["phone_id"] != d2["mobiles"][0]["phone_id"])

    # 3. GET /mobiles/search works
    r3 = client.get("/mobiles/search", params={"q": "Samsung"})
    check("3. search returns 200", r3.status_code == 200)
    check("3b. search total > 0", r3.json()["total"] > 0)

    # 4. Search is case-insensitive
    r4l = client.get("/mobiles/search", params={"q": "samsung"})
    r4u = client.get("/mobiles/search", params={"q": "SAMSUNG"})
    check("4. case-insensitive search", r4l.json()["total"] == r4u.json()["total"])

    # 5. Search filters work
    r5 = client.get("/mobiles/search", params={"brand": "Samsung", "min_ram": 8, "has_5g": True})
    for m in r5.json()["mobiles"]:
        check("5. brand filter", m["brand"].lower() == "samsung")
        check("5. min_ram filter", m["ram_gb"] >= 8)
        check("5. 5g filter", bool(m["has_5g"]))

    # 6. GET /mobiles/{phone_id} returns a phone
    first_id = r1.json()["mobiles"][0]["phone_id"]
    r6 = client.get(f"/mobiles/{first_id}")
    check("6. detail returns 200", r6.status_code == 200)
    d6 = r6.json()
    check("6b. correct phone_id", d6["phone_id"] == first_id)
    check("6c. has model", bool(d6.get("model")))

    # 7. Unknown phone_id returns 404
    r7 = client.get("/mobiles/99999999")
    check("7. unknown returns 404", r7.status_code == 404, r7.status_code)

    # 8. POST /recommend/phone/preferences returns 200
    body = {"budget_max": 30000, "min_ram": 8, "min_storage": 128, "has_5g": True, "priority": "Gaming", "limit": 10}
    r8 = client.post("/recommend/phone/preferences", json=body)
    check("8. recommend returns 200", r8.status_code == 200, r8.status_code)
    d8 = r8.json()
    check("8b. has recommendations key", "recommendations" in d8)
    check("8c. has applied_preferences", "applied_preferences" in d8)

    # 9. Recommendation response contains match_percentage
    check("9. match_percentage present", all("match_percentage" in x for x in d8["recommendations"]))
    check("9b. match_percentage in 0-100", all(0 <= x["match_percentage"] <= 100 for x in d8["recommendations"]))

    # 10. Recommendation response contains reasons
    check("10. reasons present", all("reasons" in x for x in d8["recommendations"]))
    check("10b. reasons <= 3", all(len(x["reasons"]) <= 3 for x in d8["recommendations"]))

    # 11. Budget constraint is respected
    for x in d8["recommendations"]:
        check("11. budget respected", x["price_inr"] <= 30000, f"{x['model']} {x['price_inr']}")

    # 12. 5G requirement is respected
    check("12. 5G respected", all(x["has_5g"] for x in d8["recommendations"]))

    # 13. Minimum RAM is respected
    check("13. min_ram respected", all(x["ram_gb"] >= 8 for x in d8["recommendations"]))

    # 14. Minimum storage is respected
    check("14. min_storage respected", all(x["storage_gb"] >= 128 for x in d8["recommendations"]))

    # 15. Priority validation rejects invalid priority
    r15 = client.post("/recommend/phone/preferences", json={"priority": "Bogus"})
    check("15. invalid priority rejected", r15.status_code == 400, r15.status_code)

    # 16. Empty candidate set returns total=0 cleanly
    r16 = client.post("/recommend/phone/preferences", json={"budget_max": 1000, "priority": "Value"})
    check("16. empty set 200", r16.status_code == 200, r16.status_code)
    d16 = r16.json()
    check("16b. total == 0", d16["total"] == 0)
    check("16c. recommendations empty", d16["recommendations"] == [])

    # EXTRA: detail fields complete
    rX = client.get(f"/mobiles/{first_id}")
    check("EXTRA. detail has all fields", all(k in rX.json() for k in (
        "phone_id","brand","model","price_inr","rating","ram_gb","storage_gb",
        "processor_brand","processor_name","core_count","clock_speed_ghz",
        "battery_mah","charging_watt","refresh_rate_hz","rear_camera_mp",
        "front_camera_mp","rear_camera_count","has_5g","has_nfc","os")))

    # EXTRA: recommend has all score fields
    if d8["recommendations"]:
        x = d8["recommendations"][0]
        check("EXTRA. all score fields", all(k in x for k in (
            "gaming_score","camera_score","performance_score","battery_score",
            "value_score","student_score","everyday_score")))

    # EXTRA: limit cap
    rX2 = client.post("/recommend/phone/preferences", json={"priority": "Value", "limit": 999})
    check("EXTRA. limit capped", rX2.status_code == 400, rX2.status_code)

print(f"\n=== RESULTS: {PASS} passed, {FAIL} failed ===")
sys.exit(1 if FAIL else 0)