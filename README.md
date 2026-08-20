# Atandra Bharati — Portfolio

> Personal portfolio site — live at **[atandra2000.github.io/mycv](https://atandra2000.github.io/mycv)**

A clean, monospace-first portfolio for a deep learning research engineer. Seventeen from-scratch ML projects
across LLMs, latent diffusion, multimodal AI, agentic research, long-context attention, and state-space models.

## Design

Inspired by the [opencode.ai](https://opencode.ai) aesthetic:

- **IBM Plex Mono everywhere** — body, headings, nav, buttons, tags, code
- **Mono-hue palette** — warm off-whites / near-blacks with one yellow accent for selection
- **Hairline border dividers** between sections (no underlines under headings)
- **No shadows, no gradients** — flat surface with hairline borders
- **Section title** is just bold mono text + softer subtitle — no underline
- **Tag chips** as small mono labels with hairline borders

## Highlights

- **HyMo** (434M active / 1.13B stored) — Flagship hybrid LLM: 3:1 Gated Delta Net / MLA, Asymmetric MoE, MTP, custom Triton GDN kernel, FSDP-2; pre-trained from scratch on 30B tokens
- **Autonomous ML Research Engineer** — 15-phase multi-agent platform; paper → plan → patch → train → evaluate → iterate → report
- **DeepSeek-v3-Lite** (422M) — Faithful from-scratch DeepSeek-V3 with MLA, aux-loss-free MoE, MTP — Chinchilla-optimal on a single A100 80GB
- **GPT-OSS-Lite** (502M / 247M active) — Sliding-window/full attention alternation, learned attention-sink bias, YaRN 128K; **2× KV-cache cut at 128K**, 130 tests
- **Mamba-3-Lite** (404M) — Complex64 SSD (N=64), MIMO head mixing, zero causal conv — pure PyTorch, no custom CUDA
- **LLaMA-3-Lite** (515M) — From-scratch LLaMA-3 architecture; 78% peak-memory reduction via chunked CE + gradient checkpointing
- **Stable Diffusion 1.x** (860M UNet) — Trained from scratch on 2× RTX 5090; best loss **0.0947** at epoch 16; epoch-42 checkpoint on HuggingFace
- **Vision Language Model** (PaliGemma-inspired) — Trained end-to-end on COCO 2014 captions, zero pre-trained weights
- Plus FaceAgingCycleGAN · FaceGenerationVAE · DCGAN · TranslationLM · GPT-From-Scratch · ActionRecognition · detect-objects · upscale-sr · news-agent

## Stack

Pure HTML5 + CSS3 + vanilla JavaScript — no frameworks, no bundler, no dependencies.

- IBM Plex Mono (300, 400, 450, 500, 600, 700) via Google Fonts
- Light & dark theme with `prefers-color-scheme` detection and a manual toggle
- Fully responsive (mobile / tablet / desktop)
- Accessible (ARIA labels, focus styles, `prefers-reduced-motion`)
- Interactive project filter chips
- Tabbed "at a glance" / "stack" / "contact" hero

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