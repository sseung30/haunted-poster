# 🔮 Haunted Tarot

Point your phone at a tarot card and watch it come alive. The illustration starts to move, and a new fortune appears below the card every time you scan it.

It's web AR, so there's no app to install. Open the link, allow the camera, and point.

**Try it:** https://sseung30.github.io/haunted-poster/

Built with [MindAR](https://hiukim.github.io/mind-ar-js-doc/) (image tracking), [A-Frame](https://aframe.io/) (rendering) and GitHub Pages (hosting).

## How it works

1. `poster.png` (the card) is compiled into `targets.mind`, a file of the card's feature points.
2. In the phone browser, MindAR looks for those points in the camera feed and keeps following the card.
3. A-Frame plays `card.mp4` directly on top of the card, sized to match it exactly.
4. GitHub Pages serves the page over `https://`, which phone browsers require before they allow camera access.

## Files

| File | Purpose |
|---|---|
| `index.html` | The AR page |
| `poster.png` | The tracking target: the tarot card (574×990, transparent rounded corners) |
| `targets.mind` | `poster.png` compiled by MindAR (the feature points the phone looks for) |
| `card.mp4` | Animated version of the card, shown on top of it (made with Seedance on Dreamina, watermark removed, compressed) |
| `sample.html` | Pipeline check: shows an orange plane on MindAR's [sample card](https://hiukim.github.io/mind-ar-js-doc/assets/images/card-06cb9111a8e32627db6bfafc7aa22a4d.png) |
| `candidates/` | Backup target: a generated haunted-house poster and its compiled `.mind` file |
| `tools/` | Scripts to generate the backup poster, check feature points and compile targets |

## Try it

1. Show `poster.png` on a screen, or print it at real tarot-card size (about 7×12 cm to 10×17 cm). The source image is small, so it gets blurry at A4.
2. Open the link above in **Chrome (Android) or Safari (iPhone)**. Apps' built-in browsers (Instagram, KakaoTalk, etc.) often block the camera.
3. Allow the camera and point it at the card from 30 to 60 cm away.
4. If the card stays still, tap the screen once. Some phones need a tap before a video can play.

Seeing an old version? Add `?v=2` (any new number) to the end of the URL.

## Adjusting position and size

Inside the target, the card's width is `1` and `0 0 0` is its centre. The card is about `1.725` tall, so y runs from about `-0.86` to `0.86`.

The video covers 96.8% of the card’s width (`width="0.968" height="1.739"`). This was measured by matching video frames against `poster.png`, because the generated clip crops a little off each side.

## Local testing

Browsers allow the camera on `localhost` without https, so you can test with a laptop webcam without waiting for a deploy:

```sh
python3 -m http.server 8000   # then open http://localhost:8000
```

Show the card on your phone screen and hold it up to the webcam.

## Rebuilding

```sh
# Check feature-point coverage (writes tools/features_preview.png)
uv run --with opencv-python-headless python tools/check_features.py poster.png

# Recompile after ANY change to poster.png (first time only: cd tools/compile && npm i)
node tools/compile/compile.mjs targets.mind poster.png

# Clean up a new Dreamina clip: remove watermarks, 30 fps, no audio, compress
ffmpeg -i dreamina.mp4 -vf "delogo=x=12:y=11:w=40:h=32,delogo=x=510:y=1194:w=188:h=46,fps=30" \
  -an -c:v libx264 -pix_fmt yuv420p -crf 26 -preset slow -movflags +faststart card.mp4
```

The `delogo` boxes match the 704×1248 clip used here. Check the watermark positions in a new clip before reusing them.

## Lessons

- **Spooky in content, not in palette.** Tracking needs busy, high-contrast, asymmetric art. Dark, minimal, foggy designs give the phone nothing to lock onto.
- **Lock the camera in the video prompt.** If the AI clip zooms or pans, it no longer lines up with the real card.
- **Muted + `playsinline`** is what lets the video autoplay on phones.

## Credits

Card art: [Happy Halloween Tarot](https://playingcarddecks.com/products/happy-halloween-tarot) by Soni Graves. Used with credit for a hackathon demo.
