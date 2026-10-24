"""Render a short looping ghost clip (16:9, dark "window" background) to ghost.mp4.

Swap this for a clip you film yourself (a friend in a white sheet works great).

Run:  uv run --with pillow python tools/make_ghost_video.py
"""
import math
import random
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

W, H, FPS, SECONDS = 640, 360, 30, 6
OUT = Path(__file__).resolve().parent.parent / "ghost.mp4"
rng = random.Random(7)
stars = [(rng.randint(0, W), rng.randint(0, H // 2), rng.random()) for _ in range(60)]

ff = subprocess.Popen(
    ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
     "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "26",
     "-movflags", "+faststart", str(OUT)],
    stdin=subprocess.PIPE,
)

frames = FPS * SECONDS
for f in range(frames):
    t = f / frames  # 0..1, loops seamlessly
    img = Image.new("RGB", (W, H), "#120a24")
    d = ImageDraw.Draw(img)
    for sx, sy, ph in stars:
        b = int(120 + 120 * (0.5 + 0.5 * math.sin(2 * math.pi * (t * 3 + ph))))
        d.ellipse([sx - 1.5, sy - 1.5, sx + 1.5, sy + 1.5], fill=(b, b, min(255, b + 30)))
    d.rectangle([0, H - 60, W, H], fill="#1d0f33")
    for gx in range(20, W, 90):  # little graveyard silhouette
        d.rounded_rectangle([gx, H - 95, gx + 40, H - 50], radius=16, fill="#2b1748")

    # ghost drifts left -> right and back, bobbing
    gx = W / 2 + 200 * math.sin(2 * math.pi * t)
    gy = H / 2 - 20 + 25 * math.sin(4 * math.pi * t)
    lean = 0.25 * math.cos(2 * math.pi * t)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    body = [(gx - 55 + lean * 40, gy - 20)]
    for k in range(9):  # wavy hem
        x = gx - 55 + k * 110 / 8
        body.append((x, gy + 85 + 12 * math.sin(k * 1.6 + 10 * math.pi * t)))
    body.append((gx + 55 + lean * 40, gy - 20))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([gx - 90, gy - 110, gx + 90, gy + 120], fill=(140, 255, 230, 90))
    glow = glow.filter(ImageFilter.GaussianBlur(30))
    ld.polygon(body, fill=(245, 250, 255, 235))
    ld.ellipse([gx - 55 + lean * 40, gy - 85, gx + 55 + lean * 40, gy + 25], fill=(245, 250, 255, 235))
    ex = gx + lean * 40
    blink = abs(math.sin(2 * math.pi * t * 2)) < 0.08
    for sx in (-20, 20):
        if blink:
            ld.line([ex + sx - 9, gy - 35, ex + sx + 9, gy - 35], fill=(20, 10, 40, 255), width=4)
        else:
            ld.ellipse([ex + sx - 9, gy - 47, ex + sx + 9, gy - 23], fill=(20, 10, 40, 255))
    mo = 10 + 6 * math.sin(4 * math.pi * t)
    ld.ellipse([ex - 12, gy - 12, ex + 12, gy - 12 + mo * 2], fill=(20, 10, 40, 255))

    img = Image.alpha_composite(img.convert("RGBA"), glow)
    img = Image.alpha_composite(img, layer).convert("RGB")
    if 0.35 < t < 0.65:  # "BOO!" mid-loop
        ImageDraw.Draw(img).text((W - 170, 40), "BOO!", fill="#fee440", font_size=56, stroke_width=3, stroke_fill="#ff006e")
    ff.stdin.write(img.tobytes())

ff.stdin.close()
ff.wait()
print("wrote", OUT, f"{OUT.stat().st_size / 1e6:.1f} MB")
