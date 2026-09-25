from PIL import Image, ImageDraw
from pathlib import Path

folder = Path(r".\data\image-check\batch6\Nothing_Phone_1")

files = [
    folder / "nothing_black.png",
    folder / "nothing_white.png"
]

thumb_w = 500
thumb_h = 500
label_h = 60

sheet = Image.new(
    "RGB",
    (thumb_w * 2, thumb_h + label_h),
    "white"
)

draw = ImageDraw.Draw(sheet)

for i, path in enumerate(files):

    img = Image.open(path).convert("RGBA")
    img.thumbnail((thumb_w - 30, thumb_h - 30))

    # White background for transparent PNG
    bg = Image.new("RGBA", img.size, "white")
    bg.alpha_composite(img)

    x = i * thumb_w + (thumb_w - bg.width) // 2
    y = (thumb_h - bg.height) // 2

    sheet.paste(bg.convert("RGB"), (x, y))

    draw.text(
        (i * thumb_w + 15, thumb_h + 15),
        path.name,
        fill="black"
    )

output = folder / "nothing_phone1_contact_sheet.jpg"
sheet.save(output, quality=95)

print("Created:", output)
