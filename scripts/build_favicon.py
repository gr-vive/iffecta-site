"""Build favicons from the brand wordmark: the «IF» glyphs of logo-oneline-white.png
on a pink (#F52A82) rounded square. Outputs go to public/.

    python scripts/build_favicon.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "public" / "assets" / "brand" / "logo-oneline-white.png"
OUT = ROOT / "public"

PINK = (245, 42, 130, 255)
LETTERS = 2        # «IF»
MASTER = 1024      # master canvas, downscaled to every size
RADIUS = 0.22      # corner radius as a share of the side
GLYPH_H = 0.46     # monogram height as a share of the side


def letter_spans(alpha: Image.Image) -> list[tuple[int, int]]:
    """x-ranges of the glyphs, found from the alpha column projection."""
    w, h = alpha.size
    px = alpha.load()
    cols = [any(px[x, y] > 40 for y in range(h)) for x in range(w)]
    spans, start = [], None
    for x, ink in enumerate(cols + [False]):
        if ink and start is None:
            start = x
        elif not ink and start is not None:
            spans.append((start, x))
            start = None
    return spans


def main() -> None:
    logo = Image.open(LOGO).convert("RGBA")
    spans = letter_spans(logo.getchannel("A"))
    x0, x1 = spans[0][0], spans[LETTERS - 1][1]
    glyph = logo.crop((x0, 0, x1, logo.height))
    glyph = glyph.crop(glyph.getchannel("A").getbbox())

    side = MASTER
    icon = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    ImageDraw.Draw(icon).rounded_rectangle((0, 0, side - 1, side - 1), radius=int(side * RADIUS), fill=PINK)

    target_h = int(side * GLYPH_H)
    scale = target_h / glyph.height
    glyph = glyph.resize((int(glyph.width * scale), target_h), Image.LANCZOS)
    icon.alpha_composite(glyph, ((side - glyph.width) // 2, (side - glyph.height) // 2))

    def save(size: int, name: str) -> None:
        icon.resize((size, size), Image.LANCZOS).save(OUT / name)
        print(f"{name:24s} {size}x{size}")

    save(512, "icon-512.png")
    save(192, "icon-192.png")
    save(180, "apple-touch-icon.png")
    save(32, "favicon-32.png")
    icon.resize((64, 64), Image.LANCZOS).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("favicon.ico              16/32/48")


if __name__ == "__main__":
    main()
