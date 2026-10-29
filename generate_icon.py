"""
Generates PickHex application icons (icon.png, icon.ico, icon.icns)
using Pillow so no external binary assets are required in git.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw


def create_pickhex_icon(size: int = 256) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Outer rounded badge background (deep slate)
    pad = int(size * 0.06)
    radius = int(size * 0.24)
    draw.rounded_rectangle(
        [pad, pad, size - pad, size - pad],
        radius=radius,
        fill=(24, 24, 32, 255),
        outline=(65, 70, 90, 255),
        width=max(2, int(size * 0.02)),
    )

    # Vibrant 6-color hex ring
    cx, cy = size * 0.5, size * 0.5
    ring_r = size * 0.28
    dot_r = size * 0.095
    palette_colors = [
        (255, 75, 92, 255),    # Coral Red
        (255, 159, 28, 255),   # Amber Orange
        (46, 196, 182, 255),   # Teal Mint
        (58, 134, 255, 255),   # Electric Blue
        (131, 56, 236, 255),   # Violet
        (255, 214, 10, 255),   # Sunny Yellow
    ]

    for i, col in enumerate(palette_colors):
        angle = (i / len(palette_colors)) * 2 * math.pi - math.pi / 2
        px = cx + math.cos(angle) * ring_r
        py = cy + math.sin(angle) * ring_r
        draw.ellipse(
            [px - dot_r, py - dot_r, px + dot_r, py + dot_r],
            fill=col,
        )

    # Center eyedropper / crosshair ring (white)
    inner_r = size * 0.14
    draw.ellipse(
        [cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
        fill=(255, 255, 255, 255),
    )
    core_r = size * 0.065
    draw.ellipse(
        [cx - core_r, cy - core_r, cx + core_r, cy + core_r],
        fill=(24, 24, 32, 255),
    )

    return img


def main():
    assets_dir = Path(__file__).parent / "assets"
    assets_dir.mkdir(exist_ok=True)

    base_img = create_pickhex_icon(256)
    png_path = assets_dir / "icon.png"
    ico_path = assets_dir / "icon.ico"
    icns_path = assets_dir / "icon.icns"

    base_img.save(png_path, format="PNG")
    base_img.save(
        ico_path,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    try:
        base_img.save(icns_path, format="ICNS")
    except Exception:
        pass
    print(f"Generated icons in {assets_dir}")


if __name__ == "__main__":
    main()
