# 🔮 Haunted Tarot

타로카드에 폰 카메라를 비추면 카드 그림이 살아 움직이고 점괘를 알려주는 웹 AR (MindAR + A-Frame + GitHub Pages).

## 파일

| 파일 | 역할 |
|---|---|
| `poster.png` | 트래킹 대상 타로카드 (인쇄할 것, 579×1000) |
| `card.mp4` | 카드 위에 겹쳐 재생되는 움직이는 카드 영상 (Dreamina/Seedance 생성, 워터마크 제거·압축) |
| `targets.mind` | `poster.png`를 MindAR로 컴파일한 결과 (폰이 찾을 특징점) |
| `index.html` | 최종 AR 페이지 |
| `sample.html` | 파이프라인 테스트용 (MindAR 샘플카드에 주황 사각형) |
| `candidates/` | 백업 타깃 (코드로 생성한 유령의 집 포스터 + 컴파일본) |
| `tools/` | 포스터·영상 생성, 특징점 확인 스크립트 |

## 남은 단계

1. **분석기 확인**: [pictarize.com/image-analyzer](https://pictarize.com/image-analyzer/)에 `poster.png` 업로드 → 점수 확인
2. **배포**: GitHub Pages (main / root)
3. **테스트**: 폰에서 `https://<user>.github.io/haunted-poster/sample.html` (샘플카드) → 되면 `/` (내 포스터)
4. **인쇄**: `poster.png`를 **실제 타로카드 크기(약 7×12cm ~ 10×17cm)**로. 해상도가 낮아서 A4로 키우면 흐려져요.

> ⚠️ 포스터를 수정하면 반드시 다시 컴파일하세요.

## 위치/크기 조정 (`index.html`)

포스터 가로 = `1`, 중심 = `0 0 0`. 이 카드는 세로가 약 `1.727`라서 y 범위는 대략 `-0.86 ~ 0.86`.
16:9 영상은 `height = width × 0.5625`.

## 로컬 테스트 (노트북 웹캠)

`localhost`는 https 없이도 카메라가 허용돼서 커밋-대기 없이 빠르게 확인 가능:

```sh
python3 -m http.server 8000   # → http://localhost:8000
```

포스터를 폰 화면에 띄우고 노트북 웹캠에 비춰보면 됩니다.

## 다시 생성하기

```sh
uv run --with opencv-python-headless python tools/check_features.py poster.png

# 카드 영상 다듬기 (Dreamina 원본 → 워터마크 제거, 30fps, 무음, 압축)
ffmpeg -i dreamina.mp4 -vf "delogo=x=12:y=11:w=40:h=32,delogo=x=510:y=1194:w=188:h=46,fps=30" \
  -an -c:v libx264 -pix_fmt yuv420p -crf 26 -preset slow -movflags +faststart card.mp4

# 포스터를 바꿨으면 반드시 재컴파일 (처음 한 번: cd tools/compile && npm i)
node tools/compile/compile.mjs targets.mind poster.png
```

## 크레딧

카드 일러스트: [Happy Halloween Tarot](https://playingcarddecks.com/products/happy-halloween-tarot) — Soni Graves. 출처를 밝히고 사용.
