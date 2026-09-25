import requests
from pathlib import Path

urls = [
"https://cdn.opstatics.com/store/20170907/assets/images/events/2021/03/9pro/en/ksp-9pro_ksp-1-28699f.jpg.webp",
"https://cdn.opstatics.com/store/20170907/assets/images/events/2021/03/9pro/en/ksp-9pro_ksp-2-84aaf3.jpg.webp",
"https://cdn.opstatics.com/store/20170907/assets/images/events/2021/03/9pro/en/ksp-9pro_ksp-3-452f26.jpg.webp",
"https://cdn.opstatics.com/store/20170907/assets/images/events/2021/03/9pro/en/ksp-9pro_ksp-4-a783e3.jpg.webp",
"https://cdn.opstatics.com/store/20170907/assets/images/events/2021/03/9pro/en/ksp-9pro_ksp-5-545e9c.jpg.webp",
"https://cdn.opstatics.com/store/20170907/assets/images/events/2021/03/9pro/en/ksp-9pro_ksp-6-f3d6cf.jpg.webp",
"https://cdn.opstatics.com/store/20170907/assets/images/events/2021/03/9pro/en/ksp-9pro_ksp-7-13796c.jpg.webp",
"https://cdn.opstatics.com/store/20170907/assets/images/events/2021/03/9pro/en/ksp-9pro_ksp-8-04266f.jpg.webp",
"https://cdn.opstatics.com/store/20170907/assets/images/events/2021/03/9pro/en/ksp-9pro_ksp-9-17606c.jpg.webp",
"https://cdn.opstatics.com/store/20170907/assets/images/events/2021/03/9pro/en/ksp-9pro_ksp-10-0f6e3a.jpg.webp"
]

folder = Path(r".\data\image-check\batch7\OnePlus_9_Pro_5G")
folder.mkdir(parents=True, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0"}

for i, url in enumerate(urls, 1):

    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()

        path = folder / f"candidate_{i}.webp"
        path.write_bytes(r.content)

        print(f"Downloaded [{i}]: {len(r.content)} bytes")

    except Exception as e:
        print(f"ERROR [{i}]: {e}")

print()
print("ONEPLUS 9 PRO CANDIDATES DOWNLOADED")
