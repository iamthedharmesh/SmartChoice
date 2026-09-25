import requests

url = "https://www.oppo.com/content/dam/oppo/common/mkt/v2-2/reno9-pro-plus-cn/listpage/reno9-pro-plus-list-gold.png"

try:
    r = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    print("HTTP status:", r.status_code)
    print("Content-Type:", r.headers.get("Content-Type"))
    print("Size:", len(r.content), "bytes")

    if r.status_code == 200 and r.headers.get("Content-Type", "").lower().startswith("image/"):
        print("VALID OFFICIAL IMAGE: YES")
    else:
        print("VALID OFFICIAL IMAGE: NO")

except Exception as e:
    print("ERROR:", e)
