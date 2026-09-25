import requests
from pathlib import Path

urls = [
"https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Probably_the_best_one_for_the_blo.width-200.format-webp.webp",
"https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Google_Pixel_Portfolio_Shot.width-1200.format-webp.webp",
"https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Google_Pixel_Portfolio_Shot.width-500.format-webp.webp",
"https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Google_Pixel_Portfolio_Shot.width-800.format-webp.webp",
"https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Google_Pixel_Portfolio_Shot.width-1600.format-webp.webp",
"https://storage.googleapis.com/gweb-uniblog-publish-prod/images/Google_Pixel_Portfolio_Shot.width-2000.format-webp.webp",
"https://storage.googleapis.com/gweb-uniblog-publish-prod/images/UpdatedPXL_art.width-800.format-webp.webp",
"https://storage.googleapis.com/gweb-uniblog-publish-prod/images/UpdatedPXL_art.width-1600.format-webp.webp",
"https://storage.googleapis.com/gweb-uniblog-publish-prod/images/UpdatedPXL_art.width-2200.format-webp.webp"
]

folder = Path(r".\data\image-check\batch4\Google_Pixel_6_Pro")
folder.mkdir(parents=True, exist_ok=True)

for i, url in enumerate(urls, 1):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        path = folder / f"candidate_{i}.webp"
        path.write_bytes(r.content)
        print(f"[{i}] saved")
    except Exception as e:
        print(f"[{i}] FAILED:", e)

print("DONE")
