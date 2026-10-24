"""Rough local stand-in for the Pictarize analyser: where are the feature points?

Draws FAST corners on the poster and prints a coverage grid. Empty cells are
places the phone has nothing to hold on to. Still run the real analyser
(pictarize.com/image-analyzer) before compiling.

Run:  uv run --with opencv-python-headless python tools/check_features.py [poster.png]
"""
import sys
from pathlib import Path

import cv2

root = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "poster.png"
img = cv2.imread(str(src))
# MindAR works on a downscaled greyscale copy, so analyse at a similar size
scale = 512 / max(img.shape[:2])
small = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
grey = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)

kps = cv2.FastFeatureDetector_create(threshold=30).detect(grey)
rows, cols = 8, 6
h, w = grey.shape
grid = [[0] * cols for _ in range(rows)]
for k in kps:
    x, y = k.pt
    grid[min(int(y / h * rows), rows - 1)][min(int(x / w * cols), cols - 1)] += 1

print(f"{len(kps)} feature points\n")
weak = 0
for r in grid:
    print(" ".join(f"{n:4d}" for n in r))
    weak += sum(n < 15 for n in r)
print(f"\nweak cells (<15 points): {weak}/{rows * cols}")

vis = small.copy()
for k in kps:
    cv2.circle(vis, (int(k.pt[0]), int(k.pt[1])), 2, (0, 0, 255), -1)
out = root / "tools" / "features_preview.png"
cv2.imwrite(str(out), vis)
print("preview:", out)
