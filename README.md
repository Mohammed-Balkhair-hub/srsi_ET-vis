# SRSI Emerging Technologies Track — Visualizations (`srsi_ET-vis`)

KAUST Academy **SRSI Emerging Technologies Track** hub: animated Manim lessons in the browser, hosted on **GitHub Pages**.

Live site (after Pages is enabled):

`https://<your-username>.github.io/srsi_ET-vis/`

---

## What’s included

| Topic | Status |
|-------|--------|
| Convolutional Neural Networks | Available — 5 sections with in-page video + ZIP download |

---

## Quick start (site)

1. Create a GitHub repo named **`srsi_ET-vis`** and push this project.
2. **Settings → Pages → Build and deployment**
   - Source: **Deploy from a branch**
   - Branch: `main`, folder: **/docs**
3. Open `https://<your-username>.github.io/srsi_ET-vis/`

No build step — `docs/` is the site root. Paths are relative so they work under `/srsi_ET-vis/`.

---

## Develop / re-render videos

```bash
cd srsi_ET-vis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

chmod +x scripts/*.sh
./scripts/render_all.sh          # 1080p → exports/1080p/
./scripts/sync_site_videos.sh    # → docs/videos/cnn/ + docs/downloads/cnn-videos.zip
```

One scene:

```bash
manim -pqh topics/cnn/theory/pooling.py Pooling
```

---

## Layout

```
srsi_ET-vis/
├── docs/                     # GitHub Pages (github.io)
│   ├── index.html            # Topic hub
│   ├── topics/cnn.html       # Sectioned CNN watch page
│   ├── videos/cnn/           # Streamed MP4s
│   ├── downloads/cnn-videos.zip
│   ├── css/  js/  img/
├── topics/cnn/               # Manim sources
│   ├── branding.py
│   └── theory/
├── assets/                   # Master logo + Day 9 PDF
├── scripts/
│   ├── render_all.sh
│   └── sync_site_videos.sh
└── README.md
```

---

## Adding a future topic (e.g. Attention)

1. Add an entry to `docs/js/topics-data.js` (`status: "available"`, `sections`, `zip`, `videoDir`).
2. Add `docs/topics/attention.html` (mirror `cnn.html`).
3. Put MP4s in `docs/videos/attention/` and zip under `docs/downloads/`.
4. Optional: Manim under `topics/attention/`.

---

## Notes

- Branding: KAUST Academy logo + **SRSI Emerging Technologies Track**.
- Theme: dark blue / blue / white / orange.
- Run Manim from the **repo root** so `assets/` resolves.
