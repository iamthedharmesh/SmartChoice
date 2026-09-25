from PIL import Image, ImageOps, ImageDraw
from pathlib import Path
import math

root = Path(r".\data\image-check\batch5")

files = []

for folder in sorted(root.iterdir()):
    if not folder.is_dir():
        continue

    for path in sorted(folder.glob("*.png")):
        if path.name in {
            "edge30_1.png",
            "edge30_2.png",
            "edge30_3.png",
            "fusion_1.png",
            "fusion_2.png"
        }:
            files.append((folder.name, path))

thumb_w = 400
thumb_h = 400
label_h = 70
cols = 3
rows = math.ceil(len(files) / cols)

sheet = Image.new(
    "RGB",
    (cols * thumb_w, rows * (thumb_h + label_h)),
    "white"
)

draw = ImageDraw.Draw(sheet)

for i, (folder, path) in enumerate(files):

    img = Image.open(path).convert("RGB")
    img.thumbnail((thumb_w - 30, thumb_h - 30))

    x = (i % cols) * thumb_w
    y = (i // cols) * (thumb_h + label_h)

    px = x + (thumb_w - img.width) // 2
    py = y + (thumb_h - img.height) // 2

    sheet.paste(img, (px, py))

    label = f"{folder}\n{path.name}"

    draw.multiline_text(
        (x + 10, y + thumb_h + 8),
        label,
        fill="black",
        spacing=4
    )

output = root / "motorola_contact_sheet.jpg"
sheet.save(output, quality=95)

print("Created:", output)
