import requests
from pathlib import Path

url = "https://cdn.shopify.com/s/files/1/0510/4556/4565/files/A40Ultra.png?v=1662723370"

folder = Path(r".\data\image-check\zte_axon40_ultra")
folder.mkdir(parents=True, exist_ok=True)

r = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

print("HTTP status:", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("Size:", len(r.content), "bytes")

if r.status_code == 200 and r.headers.get("Content-Type", "").lower().startswith("image/"):
    path = folder / "candidate_2.png"
    path.write_bytes(r.content)
    print("Downloaded:", path)
    print("VALID IMAGE URL: YES")
else:
    print("VALID IMAGE URL: NO")
