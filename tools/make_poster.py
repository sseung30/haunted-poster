"""Generate a bright, busy, asymmetric Halloween poster that MindAR can track.

Rule from the track guide: spooky in content, not in palette.
Every decoration below is randomised (size, colour, rotation) so nothing repeats.

Run:  uv run --with pillow python tools/make_poster.py
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1240, 1754  # A4 portrait at ~150 dpi
OUT = Path(__file__).resolve().parent.parent / "candidates" / "haunted-house.png"
rng = random.Random(1031)

PALETTE = [
    "#ff5e1a", "#ffd23f", "#3bceac", "#0ead69", "#ee4266", "#540d6e",
    "#00a6fb", "#f15bb5", "#9b5de5", "#fee440", "#00f5d4", "#ff8fab",
    "#ffffff", "#1b1b1b", "#7cff4f", "#ff3d00",
]
FONT_DIR = Path("/System/Library/Fonts/Supplemental")


def font(name, size):
    try:
        return ImageFont.truetype(str(FONT_DIR / name), size)
    except OSError:
        return ImageFont.load_default(size)


def col(exclude=()):
    return rng.choice([c for c in PALETTE if c not in exclude])


def poly_rot(cx, cy, pts, ang):
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cy + x * s + y * c) for x, y in pts]


img = Image.new("RGB", (W, H), "#8e44ff")
d = ImageDraw.Draw(img)

# --- background: irregular colour patches (no smooth gradient, no flat area)
for _ in range(520):
    x, y = rng.randint(-60, W), rng.randint(-60, H)
    r = rng.randint(20, 90)
    pts = [
        (x + r * math.cos(a) * rng.uniform(0.5, 1.2), y + r * math.sin(a) * rng.uniform(0.5, 1.2))
        for a in [i * 2 * math.pi / 7 for i in range(7)]
    ]
    d.polygon(pts, fill=col(("#1b1b1b",)))

# --- checker floor strip, uneven tile sizes, bottom only (breaks symmetry)
y = H - 330
x = 0
while x < W:
    tw = rng.randint(40, 110)
    for row in range(4):
        th = rng.randint(55, 95)
        if (row + x // 50) % 2:
            d.rectangle([x, y + row * 80, x + tw, y + row * 80 + th], fill=col())
    x += tw

# --- moon, top-right, with craters
mx, my, mr = 980, 230, 150
d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill="#fff3b0", outline="#1b1b1b", width=8)
for _ in range(9):
    cr = rng.randint(10, 38)
    cx, cy = mx + rng.randint(-100, 100), my + rng.randint(-100, 100)
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill="#e9c46a", outline="#1b1b1b", width=3)

# --- haunted house, left of centre, crooked
hx, hy = 120, 560
d.polygon([(hx, hy + 120), (hx + 520, hy + 90), (hx + 560, hy + 900), (hx - 20, hy + 920)],
          fill="#2ec4b6", outline="#1b1b1b")
d.polygon([(hx - 60, hy + 140), (hx + 250, hy - 160), (hx + 600, hy + 100)], fill="#ee4266", outline="#1b1b1b")
d.polygon([(hx + 330, hy - 60), (hx + 420, hy - 330), (hx + 500, hy + 20)], fill="#ffd23f", outline="#1b1b1b")
for _ in range(40):  # roof shingles and wall planks, irregular
    sx, sy = hx + rng.randint(0, 540), hy + rng.randint(-120, 880)
    ln = rng.randint(20, 70)
    d.line([sx, sy, sx + ln, sy + rng.randint(-6, 6)], fill=col(), width=rng.randint(4, 9))
d.rectangle([hx + 360, hy - 40, hx + 450, hy + 120], fill="#9b5de5", outline="#1b1b1b", width=6)
for i in range(14):  # windows: all different sizes/colours
    wx = hx + 30 + (i % 4) * 125 + rng.randint(-15, 15)
    wy = hy + 200 + (i // 4) * 170 + rng.randint(-20, 20)
    ww, wh = rng.randint(55, 95), rng.randint(60, 110)
    d.rectangle([wx, wy, wx + ww, wy + wh], fill=col(), outline="#1b1b1b", width=6)
    d.line([wx + ww // 2, wy, wx + ww // 2 + rng.randint(-8, 8), wy + wh], fill="#1b1b1b", width=4)
    d.line([wx, wy + wh // 2, wx + ww, wy + wh // 2 + rng.randint(-8, 8)], fill="#1b1b1b", width=4)
d.rounded_rectangle([hx + 210, hy + 700, hx + 340, hy + 905], radius=50, fill="#ff5e1a", outline="#1b1b1b", width=8)
for _ in range(25):  # cracks on the walls
    sx, sy = hx + rng.randint(0, 520), hy + rng.randint(150, 880)
    pts = [(sx, sy)]
    for _ in range(rng.randint(3, 6)):
        sx += rng.randint(-25, 25)
        sy += rng.randint(5, 30)
        pts.append((sx, sy))
    d.line(pts, fill="#1b1b1b", width=3)

# --- dead tree, right side
tx, ty = 900, H - 330


def branch(x, y, ang, length, w, depth):
    if depth == 0 or length < 12:
        return
    x2, y2 = x + length * math.cos(ang), y - length * math.sin(ang)
    d.line([x, y, x2, y2], fill="#3d1f0b", width=max(2, int(w)))
    for _ in range(rng.randint(2, 3)):
        branch(x2, y2, ang + rng.uniform(-0.8, 0.8), length * rng.uniform(0.55, 0.8), w * 0.65, depth - 1)


branch(tx, ty, math.pi / 2 + 0.08, 230, 34, 7)

# --- tombstones, each unique
labels = ["RIP", "BOO", "R.I.P.\n1666", "OOPS", "BYE", "IOU\n$3", "BRB"]
for i, lab in enumerate(labels):
    gx = 60 + i * 170 + rng.randint(-30, 30)
    gy = H - 300 + rng.randint(-40, 60)
    gw, gh = rng.randint(90, 140), rng.randint(120, 190)
    ang = rng.uniform(-0.25, 0.25)
    shape = [(-gw / 2, gh / 2), (-gw / 2, -gh / 3), (0, -gh / 2 - rng.randint(0, 30)), (gw / 2, -gh / 3), (gw / 2, gh / 2)]
    d.polygon(poly_rot(gx, gy, shape, ang), fill=col(("#1b1b1b",)), outline="#1b1b1b")
    d.multiline_text((gx - gw / 3, gy - 20), lab, fill="#1b1b1b", font=font("Arial Black.ttf", rng.randint(22, 30)))

# --- pumpkins: different sizes, colours, faces
for _ in range(8):
    px, py = rng.randint(40, W - 40), rng.randint(H - 520, H - 60)
    pr = rng.randint(30, 75)
    pc = rng.choice(["#ff7f11", "#ffb703", "#fb5607", "#7cff4f", "#00f5d4", "#ff006e"])
    for k in range(-2, 3):
        d.ellipse([px + k * pr * 0.35 - pr * 0.6, py - pr * 0.8, px + k * pr * 0.35 + pr * 0.6, py + pr * 0.8],
                  fill=pc, outline="#1b1b1b", width=3)
    d.rectangle([px - 6, py - pr - 18, px + 6, py - pr * 0.7], fill="#0ead69")
    eye = rng.choice(["tri", "dot", "x"])
    for sx in (-1, 1):
        ex, ey = px + sx * pr * 0.35, py - pr * 0.2
        if eye == "tri":
            d.polygon([(ex - 10, ey + 8), (ex + 10, ey + 8), (ex, ey - 12)], fill="#1b1b1b")
        elif eye == "dot":
            d.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill="#1b1b1b")
        else:
            d.line([ex - 9, ey - 9, ex + 9, ey + 9], fill="#1b1b1b", width=5)
            d.line([ex - 9, ey + 9, ex + 9, ey - 9], fill="#1b1b1b", width=5)
    teeth = [(px - pr * 0.5 + j * pr * 0.2, py + pr * 0.25 + (8 if j % 2 else -4)) for j in range(6)]
    d.line(teeth, fill="#1b1b1b", width=6)

# --- bats: every one a different size/angle/colour
for _ in range(16):
    bx, by = rng.randint(30, W - 30), rng.randint(30, 700)
    s = rng.uniform(0.5, 1.8)
    wing = [(0, 0), (-20, -15), (-45, -10), (-60, 5), (-48, 2), (-38, 14), (-25, 6), (-12, 16), (0, 8),
            (12, 16), (25, 6), (38, 14), (48, 2), (60, 5), (45, -10), (20, -15)]
    wing = [(x * s, y * s) for x, y in wing]
    d.polygon(poly_rot(bx, by, wing, rng.uniform(-0.6, 0.6)), fill=rng.choice(["#1b1b1b", "#540d6e", "#3a0ca3"]))

# --- stars and specks everywhere (the "freckles"), including corners
for _ in range(380):
    x, y = rng.randint(0, W), rng.randint(0, H)
    r = rng.randint(4, 16)
    kind = rng.random()
    c = col()
    if kind < 0.4:
        pts = []
        for k in range(10):
            rr = r if k % 2 == 0 else r * 0.45
            a = k * math.pi / 5 + rng.random() * 0.2
            pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
        d.polygon(pts, fill=c, outline="#1b1b1b")
    elif kind < 0.7:
        d.ellipse([x - r / 2, y - r / 2, x + r / 2, y + r / 2], fill=c, outline="#1b1b1b")
    else:
        d.line([x, y, x + rng.randint(-25, 25), y + rng.randint(-25, 25)], fill=c, width=rng.randint(3, 6))

# --- candy corn scattered in corners
for cx, cy in [(50, 60), (W - 60, H - 50), (70, H - 80), (W - 300, 60), (W // 2 + 90, 900)]:
    a = rng.uniform(0, 2 * math.pi)
    tri = [(0, -40), (-28, 30), (28, 30)]
    d.polygon(poly_rot(cx, cy, tri, a), fill="#ffffff", outline="#1b1b1b")
    d.polygon(poly_rot(cx, cy, [(0, -40), (-18, 5), (18, 5)], a), fill="#ff7f11")
    d.polygon(poly_rot(cx, cy, [(0, -40), (-8, -18), (8, -18)], a), fill="#ffd23f")

# --- title, tilted, off-centre (not "mostly text")
title = Image.new("RGBA", (900, 200), (0, 0, 0, 0))
td = ImageDraw.Draw(title)
tf = font("Chalkduster.ttf", 104)
td.text((14, 14), "HAUNTED!", font=tf, fill="#1b1b1b")
td.text((0, 0), "HAUNTED!", font=tf, fill="#fee440")
title = title.rotate(7, expand=True, resample=Image.BICUBIC)
img.paste(title, (40, 40), title)

sub = font("Arial Black.ttf", 40)
d.text((640, 1230), "scan me\nif you dare", font=sub, fill="#1b1b1b", stroke_width=4, stroke_fill="#ffffff")

# thick asymmetric border: different colour per side
for side, c in zip(range(4), ["#ff006e", "#00f5d4", "#fee440", "#3a86ff"]):
    bw = 14 + side * 6
    box = [[0, 0, W, bw], [W - bw, 0, W, H], [0, H - bw, W, H], [0, 0, bw, H]][side]
    d.rectangle(box, fill=c)

img.save(OUT)
print("wrote", OUT)
