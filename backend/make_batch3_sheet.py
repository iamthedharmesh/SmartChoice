from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

ROOT = Path(r".\data\image-check\batch3")
OUTPUT = ROOT / "BATCH3_CONTACT_SHEET.jpg"

files = []

for folder in sorted(ROOT.iterdir()):
    if not folder.is_dir():
        continue

    for image in sorted(folder.iterdir()):
        if image.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]:
            files.append((folder.name, image))

print("Images found:", len(files))

if not files:
    print("No images found.")
    raise SystemExit

thumb_w = 300
thumb_h = 260
cols = 4
rows = math.ceil(len(files) / cols)

sheet = Image.new("RGB", (cols * thumb_w, rows * thumb_h), "white")
draw = ImageDraw.Draw(sheet)

for i, (folder, image_path) in enumerate(files):

    try:
        img = Image.open(image_path).convert("RGB")
        img.thumbnail((280, 210))

        x = (i % cols) * thumb_w
        y = (i // cols) * thumb_h

        img_x = x + (thumb_w - img.width) // 2
        img_y = y + 5

        sheet.paste(img, (img_x, img_y))

        label = f"{folder}\n{image_path.name}"

        draw.text(
            (x + 8, y + 220),
            label,
            fill="black"
        )

    except Exception as e:
        print("Failed:", image_path, e)

sheet.save(OUTPUT, quality=95)

print()
print("CONTACT SHEET CREATED:")
print(OUTPUT)
