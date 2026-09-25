import requests
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from io import BytesIO

items = [
    (
        "s22_plus",
        "https://img.global.news.samsung.com/ca/wp-content/uploads/2022/02/019_galaxys22plus_front_green-1024x683.jpg"
    ),
    (
        "v23_gold",
        "https://asia-exstatic-vivofs.vivo.com/PSee2l50xoirPK7y/1640862857357/4947ef03091facc9b18c1b913d862b4d.png"
    ),
    (
        "v23_black",
        "https://asia-exstatic-vivofs.vivo.com/PSee2l50xoirPK7y/1640862851451/8f67c7155d8af079f5b2e4f3719044f7.png"
    ),
    (
        "v25_black",
        "https://in-exstatic-vivofs.vivo.com/gdHFRinHEMrj3yPG/1661844290896/1fb10741c2d8f0a11baf16779347f8a7.png"
    ),
    (
        "v25_blue",
        "https://in-exstatic-vivofs.vivo.com/gdHFRinHEMrj3yPG/1661844286353/e79763fef33c549db554fc6032749185.png"
    ),
    (
        "phantom_x2_pro_orange",
        "https://d13pvy8xd75yde.cloudfront.net/global/phones/45c026326fdce9098edaf838b954f79b.png"
    ),
    (
        "phantom_x2_pro_grey",
        "https://d13pvy8xd75yde.cloudfront.net/global/phones/6ac65836ee7bc0beb548fb0e470f5cdd.png"
    ),
]

folder = Path(r".\data\image-check\remaining_batch")
folder.mkdir(parents=True, exist_ok=True)

downloaded = []

for name, url in items:
    try:
        r = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=30
        )

        print(f"{name}: HTTP {r.status_code} | {r.headers.get('Content-Type')} | {len(r.content)} bytes")

        if r.status_code == 200 and r.headers.get("Content-Type", "").lower().startswith("image/"):
            path = folder / f"{name}.png"

            # Preserve JPEG if needed
            if "jpeg" in r.headers.get("Content-Type", "").lower():
                path = folder / f"{name}.jpg"

            path.write_bytes(r.content)
            downloaded.append((name, path))
            print("  SAVED:", path)
        else:
            print("  INVALID")

    except Exception as e:
        print("  ERROR:", e)

# Create contact sheet
thumb_w = 420
thumb_h = 320
label_h = 45
cols = 2
rows = (len(downloaded) + cols - 1) // cols

sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), "white")
draw = ImageDraw.Draw(sheet)

for i, (name, path) in enumerate(downloaded):
    try:
        img = Image.open(path).convert("RGB")
        img.thumbnail((thumb_w - 20, thumb_h - 20))

        x = (i % cols) * thumb_w
        y = (i // cols) * (thumb_h + label_h)

        cell = ImageOps.contain(img, (thumb_w - 20, thumb_h - 20))
        px = x + (thumb_w - cell.width) // 2
        py = y + (thumb_h - cell.height) // 2

        sheet.paste(cell, (px, py))
        draw.text((x + 10, y + thumb_h + 10), name, fill="black")

    except Exception as e:
        print("Contact sheet error:", name, e)

sheet_path = folder / "remaining_contact_sheet.jpg"
sheet.save(sheet_path, quality=95)

print()
print("CONTACT SHEET:")
print(sheet_path)
print()
print("Downloaded:", len(downloaded), "/", len(items))
