# Atandra Bharati — Portfolio

> Personal portfolio site — live at **[atandra2000.github.io/mycv](https://atandra2000.github.io/mycv)**

A modern, responsive, single-page portfolio for a deep learning research engineer. Showcases twelve
from-scratch ML projects across LLMs, latent diffusion, multimodal AI, and agentic research systems.

## Highlights

- **Autonomous ML Research Engineer** — 15-phase multi-agent platform; paper → plan → patch → train → evaluate → iterate → report
- **DeepSeek-v3-Lite** (422M) — Faithful from-scratch DeepSeek-V3 with MLA, aux-loss-free MoE, MTP — Chinchilla-optimal on a single A100 80GB
- **LLaMA-3-Lite** (515M) — From-scratch LLaMA-3 architecture; 78% peak-memory reduction via chunked CE + gradient checkpointing
- **FusionLLM** (415.6M active / 868.6M stored) — MLA + Gated Delta Net + MoE + MTP in a 24-layer hybrid
- **Stable Diffusion 1.x** (860M UNet) — Trained from scratch on 2× RTX 5090; best loss **0.0947** at epoch 16
- **Vision Language Model** (PaliGemma-inspired) — Trained end-to-end on COCO 2014 captions, zero pre-trained weights
- Plus FaceAgingCycleGAN · FaceGenerationVAE · DCGAN · TranslationLM · GPT-From-Scratch · ActionRecognition

## Stack

Pure HTML5 + CSS3 + vanilla JavaScript — no frameworks, no bundler, no dependencies.

- Fully responsive (mobile / tablet / desktop)
- Light & dark theme with `prefers-color-scheme` detection and a manual toggle
- Accessible (skip link, ARIA labels, focus styles, `prefers-reduced-motion`)
- SEO-friendly (Open Graph + Twitter Card meta, semantic HTML, descriptive `alt`s)
- Interactive project filter chips
- Scroll-reveal animations
- Inline SVG favicon

## Local Development

```bash
# Just open the file
open index.html

# Or serve locally
python -m http.server 8000
```

## Deploy

Hosted via **GitHub Pages** from the `main` branch root.
Any push to `main` automatically updates the live site.

---

*Open to ML Research Engineer roles. Kolkata, India · Remote-friendly.*