from PIL import Image, ImageDraw
from pathlib import Path

folder = Path(r".\data\image-check\batch7\OnePlus_9_Pro_5G")

files = [folder / f"candidate_{i}.webp" for i in range(1, 11)]

thumb_w = 300
thumb_h = 400
cell_w = 320
cell_h = 440

sheet = Image.new("RGB", (cell_w * 5, cell_h * 2), "white")

for i, file in enumerate(files):
    img = Image.open(file).convert("RGB")
    img.thumbnail((thumb_w, thumb_h))

    x = (i % 5) * cell_w
    y = (i // 5) * cell_h

    sheet.paste(
        img,
        (
            x + (cell_w - img.width) // 2,
            y + 35
        )
    )

    draw = ImageDraw.Draw(sheet)
    draw.text(
        (x + 10, y + 10),
        f"Candidate {i + 1}",
        fill="black"
    )

output = folder / "contact_sheet.png"
sheet.save(output)

print(f"Created: {output}")
