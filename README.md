# Atandra Bharati — ML Engineer Portfolio

> Personal resume and project portfolio site — live at **[atandra2000.github.io/mycv](https://atandra2000.github.io/mycv)**

A clean, responsive, single-page portfolio showcasing ML engineering work across LLMs, diffusion models, GANs, and vision-language systems — all built from scratch.

## Highlights

- **DeepSeek-V3-Lite** — Full reimplementation of the DeepSeek-V3 architecture: MLA, MoE (64 routed + 2 shared experts), FP8 Triton kernels, Multi-Token Prediction, FSDP across 8× RTX 5090
- **Stable Diffusion** — Custom UNet (~860M params), DDPM/DDIM schedulers, LAION-2B data pipeline, dual-GPU VAE encoding on RunPod
- **Vision Language Model** — PaliGemma-inspired VLM: SigLIP encoder, GQA + RoPE decoder, linear projector
- **Face Aging CycleGAN** — AdaIN style normalization, multi-scale discriminator, VGG perceptual loss
- **GPT / TranslationLM / VAE / DCGAN** — Foundational architectures implemented end-to-end

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
