# SRSI Emerging Technologies Track — Visualizations

KAUST Academy **SRSI Emerging Technologies Track** hub: animated Manim lessons you can watch in the browser, hosted on GitHub Pages.

| | Link |
|---|---|
| **Live site** | [https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/) |
| **Repository** | [https://github.com/Mohammed-Balkhair-hub/srsi_ET-vis](https://github.com/Mohammed-Balkhair-hub/srsi_ET-vis) |
| **CNN module** | [https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/cnn.html](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/cnn.html) |
| **RNN module** | [https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/rnn.html](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/rnn.html) |
| **Attention module** | [https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/attention.html](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/attention.html) |

If the live site 404s, enable Pages once: **Settings → Pages → Deploy from a branch → `main` / `/docs`**.

---

## What’s included

| Topic | Status |
|-------|--------|
| [Convolutional Neural Networks](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/cnn.html) | Available — 5 sections, [ZIP](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/downloads/cnn-videos.zip) |
| [Recurrent Neural Networks](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/rnn.html) | Available — 4 sections, [ZIP](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/downloads/rnn-videos.zip) |
| [Attention](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/topics/attention.html) | Available — 4 sections, [ZIP](https://Mohammed-Balkhair-hub.github.io/srsi_ET-vis/downloads/attention-videos.zip) |

---

## Clone & develop

```bash
git clone https://github.com/Mohammed-Balkhair-hub/srsi_ET-vis.git
cd srsi_ET-vis
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

chmod +x scripts/*.sh
./scripts/render_all.sh attention   # or cnn | rnn | all
./scripts/sync_site_videos.sh attention
```

Single scene:

```bash
manim -pqh topics/attention/theory/scores_softmax.py ScoresSoftmax
```

---

## Layout

```
srsi_ET-vis/
├── docs/
│   ├── topics/cnn.html  rnn.html  attention.html
│   ├── videos/cnn/  rnn/  attention/
│   └── downloads/
├── exports/1080p/cnn|rnn|attention/
├── topics/cnn/  rnn/  attention/
├── assets/
└── scripts/
```

---

## Notes

- Branding: KAUST Academy logo + **SRSI Emerging Technologies Track**
- Theme: dark blue / blue / white / orange (site); white background Manim videos
- Run Manim from the **repo root** so `assets/` resolves
