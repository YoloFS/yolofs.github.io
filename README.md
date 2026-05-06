# yolofs.github.io

Project page for **YoloFS** — *Don't let AI agents YOLO your files: shifting
information and control to filesystems for agent safety and autonomy.*

- **Rendered site:** <https://yolofs.github.io>
- **Main repo:** <https://github.com/YoloFS/YoloFS>
- **Paper (PDF):** <https://yolofs.github.io/paper.pdf>
- **arXiv:** <https://arxiv.org/abs/2604.13536>

## Layout

| File             | Purpose                                                    |
| ---------------- | ---------------------------------------------------------- |
| `index.html`     | Home — hero, problem, gaps, YoloFS overview, results       |
| `study.html`     | Full breakdown of the 290-report misuse study              |
| `design.html`    | Design and implementation of YoloFS                        |
| `bench.html`     | Agent-benchmark methodology and results                    |
| `perf.html`      | Performance evaluation                                     |
| `nav.js`         | Single-source top-nav, auto-active by URL                  |
| `styles.css`     | Shared theme                                               |
| `favicon.svg`    | Browser tab icon                                           |
| `og.png`         | Social-share card (1200×630)                               |
| `og-template.html` | Source HTML used to render `og.png` via headless Chrome  |
| `paper.pdf`      | Latest paper PDF (auto-synced from the paper submodule)    |

## Regenerating the OG image

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --hide-scrollbars \
  --window-size=1200,630 \
  --screenshot=og.png \
  file://$PWD/og-template.html
```
