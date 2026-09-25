import requests
from pathlib import Path

url = "https://d13pvy8xd75yde.cloudfront.net/global/phones/phantom/ae/10/800/AE10%E6%B5%B7%E6%B3%A2%E8%93%8D.png"

folder = Path(r".\data\image-check\tecno_phantom_x2_pro")
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
    path = folder / "candidate_1.png"
    path.write_bytes(r.content)
    print("Downloaded:", path)
    print("VALID OFFICIAL IMAGE: YES")
else:
    print("VALID OFFICIAL IMAGE: NO")
