# SRSI Emerging Technologies Track — Visualizations

KAUST Academy **SRSI Emerging Technologies Track** hub: animated Manim lessons you can watch in the browser, hosted on GitHub Pages.

| | Link |
|---|---|
| **Live site** | [https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/) |
| **Repository** | [https://github.com/Mohammed-Balkhair-hub/srsi_ET-vis](https://github.com/Mohammed-Balkhair-hub/srsi_ET-vis) |
| **CNN module** | [https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/cnn.html](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/cnn.html) |
| **RNN module** | [https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/rnn.html](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/rnn.html) |

If the live site 404s, enable Pages once: **Settings → Pages → Deploy from a branch → `main` / `/docs`**.

---

## What’s included

| Topic | Status |
|-------|--------|
| [Convolutional Neural Networks](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/cnn.html) | Available — 5 sections, in-page video players, [ZIP download](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/downloads/cnn-videos.zip) |
| [Recurrent Neural Networks](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/rnn.html) | Available — 4 sections, in-page video players, [ZIP download](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/downloads/rnn-videos.zip) |

---

## Clone & develop

```bash
git clone https://github.com/Mohammed-Balkhair-hub/srsi_ET-vis.git
cd srsi_ET-vis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

chmod +x scripts/*.sh
./scripts/render_all.sh rnn      # or cnn | all  → exports/1080p/
./scripts/sync_site_videos.sh rnn
```

Single scene:

```bash
manim -pqh topics/rnn/theory/cell_math.py RNNCellMath
```

---

## Layout

```
srsi_ET-vis/
├── docs/                     # GitHub Pages root
│   ├── index.html
│   ├── topics/cnn.html
│   ├── topics/rnn.html
│   ├── videos/cnn/  videos/rnn/
│   ├── downloads/
│   ├── css/  js/  img/
├── topics/cnn/               # Manim sources
├── topics/rnn/
├── assets/
├── scripts/
└── README.md
```

---

## Adding another topic later

1. Entry in `docs/js/topics-data.js`
2. Page under `docs/topics/<id>.html`
3. Videos in `docs/videos/<id>/` + zip in `docs/downloads/`
4. Optional Manim under `topics/<id>/`
5. Jobs in `scripts/render_all.sh` + `sync_site_videos.sh`

---

## Notes

- Branding: KAUST Academy logo + **SRSI Emerging Technologies Track**
- Theme: dark blue / blue / white / orange (site); white background Manim videos
- Run Manim from the **repo root** so `assets/` resolves
