# Atandra Bharati — ML Engineer Portfolio

> Personal resume and project portfolio site — live at **[atandra2000.github.io/mycv](https://atandra2000.github.io/mycv)**

A clean, responsive, single-page portfolio showcasing ML engineering work across LLMs, diffusion models, GANs, and vision-language systems — all built from scratch.

## Highlights

- **DeepSeek-V3-Lite** — Faithful from-scratch reimplementation of DeepSeek-V3 (MLA, MoE with 20 routed + 2 shared experts, Multi-Token Prediction) scaled for a single A100 80GB; training pipeline complete, pre-training run not yet started.
- **Stable Diffusion** — Custom UNet (~860M params), DDPM/DDIM schedulers, LAION data pipeline, DDP training on 2× RTX 5090; checkpoint released at epoch 42.
- **Vision Language Model** — PaliGemma-inspired VLM: SigLIP-style vision encoder, GQA + RoPE decoder, linear projector, trained end-to-end from scratch on COCO captions.
- **Face Aging CycleGAN** — AdaIN-conditioned CycleGAN, multi-scale discriminator, VGG perceptual loss; architecture and training pipeline complete.
- **GPT / TranslationLM / VAE / DCGAN / ActionRecognition** — Foundational architectures implemented end-to-end.

## Stack

Pure HTML5 + CSS3 — no frameworks, no bundler, no dependencies.
Responsive · Dark navbar on scroll · Scroll-reveal animations · Mobile-friendly hamburger menu

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

*Open to Machine Learning Engineer roles. Kolkata, India.*
