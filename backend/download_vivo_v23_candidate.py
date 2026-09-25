import requests
from pathlib import Path

url = "https://in-exstatic-vivofs.vivo.com/gdHFRinHEMrj3yPG/1718260966763/91b877c9485e5a0f0caeaee9e5519e91.png"

folder = Path(r".\data\image-check\vivo_v23")
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
else:
    print("VALID IMAGE: NO")
