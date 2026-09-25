import requests

url = "https://image01-in.oneplus.net/shop/202104/27/1-M00-24-8B-rB8bwmCICVmAN0CwAAVb_9VyE6w579.png"

try:
    r = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    )

    print("HTTP status:", r.status_code)
    print("Content-Type:", r.headers.get("Content-Type"))
    print("Size:", len(r.content), "bytes")

    if r.status_code == 200 and r.headers.get("Content-Type", "").startswith("image/"):
        print("VALID OFFICIAL IMAGE: YES")
    else:
        print("VALID OFFICIAL IMAGE: NO")

except Exception as e:
    print("ERROR:", e)
