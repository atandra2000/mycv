"""
Atandra Bharati — Resume PDF generator
Uses ReportLab with Menlo monospace. Two-page US Letter layout.

Output: /tmp/resume.pdf
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import os, sys

# Register Menlo
pdfmetrics.registerFont(TTFont('Menlo',     '/System/Library/Fonts/Menlo.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('Menlo-Bold','/System/Library/Fonts/Menlo.ttc', subfontIndex=2))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily('Menlo', normal='Menlo', bold='Menlo-Bold')

# ── Layout constants (US Letter) ─────────────────────────────────────────────
PAGE_W, PAGE_H = LETTER                          # 612 x 792 pt
MARGIN_X = 0.6 * inch
MARGIN_TOP = 0.5 * inch
MARGIN_BOTTOM = 0.42 * inch
USABLE_W = PAGE_W - 2 * MARGIN_X                 # ~475 pt

# Type scale (in points)
SZ_NAME    = 16
SZ_ROLE    = 8.6
SZ_H2      = 8.6          # section header
SZ_H3      = 8.4          # column header
SZ_BODY    = 8.2
SZ_META    = 7.6
SZ_ANCHOR  = 13           # big anchor numbers
SZ_LBL     = 7.0          # anchor labels
SZ_TINY    = 7.4

# Colors (mono-hue)
INK         = '#111111'
INK_SOFT    = '#222222'
INK_MID     = '#444444'
INK_FAINT   = '#666666'
INK_RULE    = '#1a1a1a'
INK_RULE_W  = '#cfcfcf'
INK_BG_ANCH = '#f4f4f4'   # very faint anchor strip bg (optional)

# ── Helpers ──────────────────────────────────────────────────────────────────
class Layout:
    def __init__(self, canvas):
        self.c = canvas
        self.y = PAGE_H - MARGIN_TOP
        self.x = MARGIN_X
        self.page = 1
        self.c.setFont('Menlo', SZ_BODY)
        self.c.setFillColor(INK)

    def need(self, height):
        """If remaining height < height, push to next page (with same margins)."""
        if self.y - height < MARGIN_BOTTOM:
            self.new_page()
            return True
        return False

    def new_page(self):
        self.c.showPage()
        self.page += 1
        self.c.setFont('Menlo', SZ_BODY)
        self.c.setFillColor(INK)
        self.y = PAGE_H - MARGIN_TOP
        self.x = MARGIN_X

    def text(self, s, font='Menlo', size=SZ_BODY, color=INK, x=None, y=None):
        if x is None: x = self.x
        if y is None: y = self.y
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        self.c.drawString(x, y - size, s)   # baseline correction (ReportLab draws at baseline)
        return size

    def para(self, s, font='Menlo', size=SZ_BODY, color=INK, leading_mult=1.36,
             max_w=None, x=None, w_advance=True):
        """Wrap s into lines and render as a paragraph. Returns the height consumed."""
        if x is None: x = self.x
        leading = size * leading_mult
        if max_w is None:
            max_w = USABLE_W
        # Wrap by measuring
        words = s.split(' ')
        lines = []
        cur = ''
        for w in words:
            trial = (cur + ' ' + w).strip()
            tw = pdfmetrics.stringWidth(trial, font, size)
            if tw <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        if cur: lines.append(cur)
        # Render
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        if not self.need(leading * len(lines) + 2):
            pass  # fit
        for i, line in enumerate(lines):
            self.c.drawString(x, self.y - size - i * leading, line)
        consumed = leading * len(lines) + 2
        self.y -= consumed
        return consumed

    def spacer(self, h):
        self.y -= h

    def hrule(self, color=INK_RULE_W, weight=0.5, gap_before=4, gap_after=6):
        self.y -= gap_before
        self.c.setStrokeColor(color)
        self.c.setLineWidth(weight)
        self.c.line(MARGIN_X, self.y, PAGE_W - MARGIN_X, self.y)
        self.y -= gap_after

    def h2(self, label, meta=None):
        if self.need(SZ_H2 * 1.5 + 4):
            pass
        self.c.setFont('Menlo-Bold', SZ_H2)
        self.c.setFillColor(INK)
        self.y -= 4
        self.c.drawString(MARGIN_X, self.y - SZ_H2, label.upper())
        label_w = pdfmetrics.stringWidth(label.upper(), 'Menlo-Bold', SZ_H2)
        if meta:
            self.c.setFont('Menlo', SZ_META)
            self.c.setFillColor(INK_MID)
            self.c.drawString(MARGIN_X + label_w + 12, self.y - SZ_META, meta)
        self.y -= SZ_H2 + 4

    def h3(self, label):
        self.c.setFont('Menlo-Bold', SZ_H3)
        self.c.setFillColor(INK)
        self.y -= 4
        self.c.drawString(MARGIN_X, self.y - SZ_H3, label.upper())
        self.y -= SZ_H3 + 4


# ── Page 1 builder ────────────────────────────────────────────────────────────
def build():
    c = Canvas('/tmp/resume.pdf', pagesize=LETTER)
    c.setTitle('Atandra Bharati — Deep Learning Research Engineer · Résumé')
    c.setAuthor('Atandra Bharati')
    c.setSubject('Résumé')
    c.setCreator('Resume PDF Generator')

    L = Layout(c)

    # Name
    L.c.setFont('Menlo-Bold', SZ_NAME)
    L.c.setFillColor(INK)
    L.c.drawString(MARGIN_X, L.y - SZ_NAME, 'Atandra Bharati')
    L.y -= SZ_NAME + 4

    # Role line
    role = ('Deep Learning Research Engineer   ·   14 from-scratch PyTorch projects across LLMs, '
            'latent diffusion, multimodal, agentic ML, long-context attention, and state-space models.')
    L.c.setFont('Menlo', SZ_ROLE)
    L.c.setFillColor(INK_SOFT)
    # Wrap to 2 lines
    lines = []
    cur = ''
    for w in role.split():
        trial = (cur + ' ' + w).strip()
        if pdfmetrics.stringWidth(trial, 'Menlo', SZ_ROLE) <= USABLE_W:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    for i, line in enumerate(lines):
        L.c.drawString(MARGIN_X, L.y - SZ_ROLE - i * SZ_ROLE * 1.35, line)
    L.y -= SZ_ROLE + len(lines) * SZ_ROLE * 0.35 + 4

    # Contact grid (2 cols x 2 rows)
    contacts = [
        ('atandrabharati@gmail.com',     'github.com/atandra2000'),
        ('linkedin.com/in/atandrabharati','atandra2000.github.io/mycv'),
    ]
    col_w = USABLE_W / 2
    for row in contacts:
        for j, txt in enumerate(row):
            L.c.setFont('Menlo', 8)
            L.c.setFillColor(INK_SOFT)
            L.c.drawString(MARGIN_X + j * col_w, L.y - 8, txt)
        L.y -= 8 + 2
    L.y += 1
    L.c.setFont('Menlo', 8); L.c.setFillColor(INK_MID)
    L.c.drawString(MARGIN_X, L.y - 8, 'Kolkata, India   ·   remote-friendly   ·   open to global remote')
    L.y -= 8 + 6

    # Anchor strip — 4 cells with hairline borders
    cell_w = USABLE_W / 4
    cell_h = 30
    strip_y = L.y - cell_h
    nums   = ['14', '78%', '0.0947', '878']
    labels = [
        'From-scratch PyTorch projects',
        'Peak-memory cut — LLaMA-3 pretraining',
        'Best loss — Stable Diffusion 1.x from scratch',
        'Passing tests — Autonomous ML Research Engineer',
    ]
    for i in range(4):
        x = MARGIN_X + i * cell_w
        # border
        L.c.setStrokeColor(INK_RULE)
        L.c.setLineWidth(0.5)
        L.c.rect(x, strip_y, cell_w, cell_h)
        # vertical dividers (skip first)
        if i > 0:
            L.c.line(x, strip_y + 4, x, strip_y + cell_h - 4)
        # num
        L.c.setFont('Menlo-Bold', SZ_ANCHOR)
        L.c.setFillColor(INK)
        nw = pdfmetrics.stringWidth(nums[i], 'Menlo-Bold', SZ_ANCHOR)
        L.c.drawString(x + (cell_w - nw) / 2, strip_y + cell_h - SZ_ANCHOR - 4, nums[i])
        # label (wrapped)
        L.c.setFont('Menlo', SZ_LBL)
        L.c.setFillColor(INK_MID)
        lbl_lines = wrap(labels[i], 'Menlo', SZ_LBL, cell_w - 6)
        for li, ll in enumerate(lbl_lines):
            lw = pdfmetrics.stringWidth(ll, 'Menlo', SZ_LBL)
            L.c.drawString(x + (cell_w - lw) / 2, strip_y + 4 - li * (SZ_LBL + 1.5) + 2, ll)
    L.y = strip_y - 8

    # Rule
    L.hrule(gap_before=0, gap_after=8)

    # Summary
    L.h2('Summary')
    L.para(
        'Self-taught deep learning research engineer with 14 from-scratch PyTorch projects '
        'spanning LLMs, latent diffusion, multimodal AI, agentic research, long-context '
        'attention, and state-space models. Focused on GPU memory engineering, single-GPU '
        'feasibility, paper-faithful reproduction, and agentic orchestration of ML research.',
        size=SZ_BODY, leading_mult=1.34,
    )
    L.para(
        'Headline results: a 78% peak-memory cut on LLaMA-3 pretraining (92 GB → 20 GB); '
        'a 0.0947 training loss on Stable Diffusion 1.x trained from scratch (860M UNet, '
        '2× RTX 5090); a 2× KV-cache reduction at 128K context in GPT-OSS-Lite via '
        'sliding-window/full-attention alternation; and a 15-phase multi-agent ML research '
        'platform with 878 passing tests.',
        size=SZ_BODY, leading_mult=1.34,
    )
    L.spacer(3)

    # Experience
    L.h2('Experience')
    L.c.setFont('Menlo-Bold', 8.8); L.c.setFillColor(INK)
    L.c.drawString(MARGIN_X, L.y - 8.8, 'ML Engineering Portfolio')
    L.c.setFont('Menlo', 7.8); L.c.setFillColor(INK_MID)
    period = 'Nov 2022 – Present   ·   Kolkata, India'
    pw = pdfmetrics.stringWidth(period, 'Menlo', 7.8)
    L.c.drawString(MARGIN_X + USABLE_W - pw, L.y - 7.8, period)
    L.y -= 9
    L.c.setFont('Menlo', 7.8); L.c.setFillColor(INK_MID)
    L.c.drawString(MARGIN_X, L.y - 7.8, 'Self-directed   ·   Full-time   ·   github.com/atandra2000')
    L.y -= 9
    L.para(
        'Designed, implemented, and trained 14 end-to-end production-grade deep learning '
        'systems in raw PyTorch — no high-level wrappers, no pretrained shortcuts where the '
        'model itself is the subject. Every project engineered to fit on a single A100 80GB, '
        '2× RTX 5090, or smaller via BF16, Flash-Attn 2, gradient checkpointing, torch.compile, '
        'and chunked cross-entropy.',
        size=SZ_BODY, leading_mult=1.32,
    )
    L.para(
        'Coverage: LLM pretraining (DeepSeek-V3 reproduction, LLaMA-3, FusionLLM hybrid, '
        'GPT-OSS-Lite long-context MoE, Mamba-3 complex64 SSD); latent diffusion (Stable '
        'Diffusion 1.x from scratch on 1.3M+ images across 7 phases); multimodal '
        '(PaliGemma-style VLM on COCO with zero pretrained weights); generative vision '
        '(CycleGAN, β-VAE, DCGAN); video understanding (HRNet pose + ST-GCN); and an '
        'agentic ML research platform.',
        size=SZ_BODY, leading_mult=1.32,
    )
    L.spacer(4)

    # Selected projects header
    L.h2('Selected Projects', meta='Six flagship builds · 2022–2026')

    # Project 1: SD
    L._proj(
        'Stable Diffusion 1.x From Scratch',
        'Latent Diffusion · Generative Vision',
        'Trained a complete Stable Diffusion 1.x model from random initialization on 2× RTX 5090, '
        'releasing the 42-epoch checkpoint. 860M-param UNet across a 7-phase curriculum on '
        '1.3M+ images (LAION-Aesthetic → high-aesthetic LAION → DiffusionDB/JourneyDB → '
        'VGGFace2 → COCO → consolidation); best loss 0.0947 at epoch 16. Atomic .tmp → os.replace '
        'checkpointing, Min-SNR loss, GPU-resident EMA (0.9999), channels_last on Blackwell, '
        'DDP/NCCL with no_sync accumulation.',
        metas=['860M UNet · 7 phases · 1.3M+ images',
               '2× RTX 5090 · 42 epochs · best loss 0.0947'],
    )
    # Project 2: LLaMA-3-Lite
    L._proj(
        'LLaMA-3-Lite — 78% Memory Reduction on a Single A100',
        'LLM · Memory Engineering',
        'Built a 515M-param LLaMA-3-style transformer engineered to fit on a single A100 80GB, '
        'cutting peak training memory by 78% (92 GB → 20 GB). The cut stacks gradient '
        'checkpointing, chunked cross-entropy (logits 50 GB → 0.3 GB), and disk-backed token '
        'caching (RAM 112 GB → 1 MB) — enabling 2× batch-size headroom and ~33% throughput '
        'gain. GQA (8Q/4KV), RoPE (θ = 500K), SwiGLU, RMSNorm, Flash-Attn 2, BF16, safetensors '
        'with full RNG-state restore.',
        metas=['515M params · 8.25B-token run',
               'A100 80GB · Chunked CE · BF16 · FA2'],
    )
    # Project 3: Autonomous
    L._proj(
        'Autonomous ML Research Engineer',
        'Agentic Platform · Research Infra',
        'A 15-phase multi-agent platform that turns an arXiv paper into evaluated ML experiments '
        'end-to-end — paper analysis, repo analysis, experiment planning, code patches, training '
        'runs, statistical evaluation, autonomous looping, and research reports. Provider-agnostic '
        'LLM layer (Qwen3-Coder, GLM-5.2, Ollama Cloud) with per-agent routing, vector + graph '
        'memory, Pydantic v2, self-repair. 878 passing tests across the agent and tool surface.',
        metas=['23 agents · 61 tools · 186 models · 878 tests',
               'Qwen3-Coder · GLM-5.2 · Ollama Cloud · Pydantic v2'],
    )
    # Project 4: DeepSeek-V3-Lite
    L._proj(
        'DeepSeek-V3-Lite — Faithful V3 Reproduction',
        'LLM · Frontier Architecture',
        'Faithful from-scratch reimplementation of DeepSeek-V3 at 422M params — MLA, aux-loss-free '
        'MoE, MTP, end-to-end. MLA with KV low-rank compression, the absorption trick, decoupled '
        'RoPE; DeepSeekMoE with aux-loss-free biased-sigmoid balancing; MTP with true absorption at '
        'inference. 8.4B-token Chinchilla recipe on a single A100 80GB via SDPA Flash-Attn 2, μP '
        'LR scaling, torch.compile(max-autotune); speculative decoding up to 2× throughput via the '
        'MTP draft head. Author of the 643-line MLA deep-dive.',
        metas=['422M params · MLA · MoE · MTP',
               'A100 80GB · SDPA · torch.compile · μP · 8.4B-token recipe'],
        is_first_page=True,  # ensure fits
    )

    # ── Page 2 ────────────────────────────────────────────────────────────────
    L.new_page()

    # Project 5: GPT-OSS-Lite
    L._proj(
        'GPT-OSS-Lite — Long-Context MoE (2× KV-Cache Cut at 128K)',
        'LLM · Long-Context Attention',
        'From-scratch reimplementation of OpenAI’s GPT-OSS at 502M total / 247M active params. '
        'Twelve layers alternate sliding-window (window=128) and full attention; per-head learned '
        'attention-sink bias (clamped to [−10, 15] for BF16 SDPA stability); YaRN RoPE (θ=100K, '
        'scale=32, target=128K); pruned RoPE on global layers; top-2-of-8 routed experts + 1 shared. '
        'Verifies a 2× KV-cache reduction at 128K context (1.13 GB vs 2.25 GB pure GQA, BF16). '
        '130 tests across 10 files. Companion ATTENTION_SINKS.md walks through the sink-bias trick.',
        metas=['502M total / 247M active · SWA(128)/Full alt',
               'Learned sinks · YaRN 128K · top-2-of-8 MoE · 130 tests'],
        no_top_rule=True,
    )

    # Project 6: Mamba-3-Lite
    L._proj(
        'Mamba-3-Lite — Complex64 SSD with Zero Causal Conv',
        'LLM · State-Space Model',
        'From-scratch reproduction of Mamba-3 at 404M params, written in pure PyTorch — no '
        'mamba-ssm, no causal_conv1d, no custom CUDA, no Triton. Promotes the SSD recurrence '
        'into the complex plane (N=64, complex64) so one complex state captures both decay and '
        'rotation, halving the state dimension of Mamba-2 at parity capacity. Adds a fully-connected '
        'MIMO mixer across SSM heads and removes the causal-conv block. Companion SSD.md derives '
        'the chunkwise algorithm.',
        metas=['404M params · complex64 SSD (N=64) · MIMO head mixing',
               'A100 80GB · pure PyTorch · zero causal conv'],
    )

    # Project 7: FusionLLM
    L._proj(
        'FusionLLM — Hybrid MLA + GDN + MoE + MTP',
        'LLM · Hybrid Architecture',
        '24-layer single-GPU pre-training framework fusing four frontier mechanisms in one '
        'model: MLA, Gated Delta Net (linear-complexity attention via chunked delta-rule), '
        'DeepSeek-style MoE, and Multi-Token Prediction. 415.6M active / 868.6M stored params, '
        '64K vocab, seq_len 4096. Dual-optimizer strategy (NorMuon for 2D matrices, '
        'CautiousAdamW for embeddings and norms), WSD schedule, μP init, logit softcap ±15.0, '
        'FP32-precise GDN recurrence. 6-stage resumable data pipeline, 55 unit tests.',
        metas=['415.6M active / 868.6M stored',
               'NorMuon + CautiousAdamW · WSD + μP · 8.31B-token recipe'],
    )

    # Additional projects header
    L.h2('Additional Projects', meta='Six more · each with verified repo and build log')
    addl = [
        ('Vision-Language Model (PaliGemma-inspired).',
         'SigLIP vision encoder + linear projector + Gemma-style GQA decoder · trained end-to-end on COCO 2014 captions with zero pre-trained weights · P100.'),
        ('Face Aging CycleGAN.',
         'Per-layer AdaIN conditioning on a 101-class age embedding, 3-scale PatchGAN + mean-residue age loss, LSGAN + VGG-19 perceptual + L1 identity · 31/50 epochs on IMDB-Wiki (500k faces) · RTX 6000 Ada.'),
        ('Face Generation β-VAE.',
         '128×128 CelebA, bilinear-upsample decoder (no ConvTranspose), linear KL annealing 0 → 1 over 30 epochs · recon MSE 0.0152 · P100.'),
        ('DCGAN Face Generation.',
         'Faithful 2015 paper reproduction (Radford et al.), 50 epochs on 202k CelebA, D loss converges to ln 2 ≈ 0.693 (theoretical Nash equilibrium) · 2× T4 Kaggle.'),
        ('Neural Machine Translation (EN → IT).',
         'Encoder-decoder Transformer (6+6, d_model = 512), custom SentencePiece BPE, cross-attention visualization · loss 6.17 → 2.28 over 20 epochs on opus_books · P100.'),
        ('Action Recognition (ST-GCN).',
         'Real-time skeleton-based action recognition with from-scratch HRNet-like pose estimation + two-stream CTR-GCN · 120-class NTU RGB+D 120 pipeline ready, real-time inference targeting 30 FPS on RTX 3090.'),
    ]
    for strong, rest in addl:
        L._addl_row(strong, rest)

    # Technical skills
    L.h2('Technical Skills', meta='Built up across fourteen from-scratch projects · every keyword has shipped code behind it')
    skills = [
        ('LLM',
         'LLaMA-3, DeepSeek-V2/V3, GPT-OSS, Mamba-2/3, MLA, GQA, MQA, MoE, MTP, Gated Delta Net, complex64 SSD, sliding-window + full-attention alternation, learned attention sinks, YaRN, Chinchilla scaling, μP, WSD, NorMuon, CautiousAdamW, AdamW, speculative decoding.'),
        ('Generative Vision',
         'Stable Diffusion 1.x, latent diffusion, UNet, DDPM, DDIM, Min-SNR, classifier-free guidance, EMA, VAE, GAN, DCGAN, PatchGAN, β-VAE, CycleGAN, AdaIN, spectral normalization, VGG and LPIPS perceptual loss.'),
        ('Multimodal & Video',
         'ViT, SigLIP, PaliGemma-style fusion, HRNet pose estimation, ST-GCN, CTR-GCN, graph convolution, NTU RGB+D 120.'),
        ('Transformer Components',
         'RoPE (incl. YaRN-scaled, pruned), GQA, SwiGLU, GeGLU, RMSNorm, multi-head attention, MLA, MQA, MTP, cross-attention.'),
        ('Training & Infra',
         'BF16, FP16, FP8, mixed precision, DDP, FSDP, NCCL, torch.compile, Flash-Attn 2, SDPA, gradient checkpointing, chunked cross-entropy, disk-backed token cache, atomic checkpointing, resumable pipelines.'),
        ('Agentic ML',
         'Multi-agent orchestration, provider-agnostic LLM routing, Ollama Cloud, vector and graph memory, Pydantic v2, pytest, Ruff.'),
        ('Core',
         'Python 3.12, PyTorch 2.x, Hugging Face, Diffusers, safetensors, SentencePiece, NumPy, W&B, Comet ML, img2dataset, Git, GitHub.'),
        ('Hardware Validated',
         'A100 80GB, RTX 5090 (Blackwell), RTX 6000 Ada, RTX 3090, P100, T4 (2×), RunPod, Kaggle.'),
    ]
    L._skills(skills)

    # Two-col footer: Writing | Education
    L.spacer(4)
    L._two_col()

    c.save()
    print(f'Wrote /tmp/resume.pdf')


# ── Helpers that need Layout method extension (monkey-patched below) ─────────
def wrap(text, font, size, max_w):
    words = text.split(' ')
    lines = []
    cur = ''
    for w in words:
        trial = (cur + ' ' + w).strip()
        if pdfmetrics.stringWidth(trial, font, size) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines


def _proj(self, title, kind, body, metas, no_top_rule=False, is_first_page=False):
    if not no_top_rule:
        # hairline separator above each project (except the first in each page)
        self.y -= 2
        self.c.setStrokeColor(INK_RULE_W); self.c.setLineWidth(0.5)
        self.c.line(MARGIN_X, self.y, PAGE_W - MARGIN_X, self.y)
        self.y -= 4
    # title row
    self.c.setFont('Menlo-Bold', 8.8); self.c.setFillColor(INK)
    self.c.drawString(MARGIN_X, self.y - 8.8, title)
    self.c.setFont('Menlo', 7.6); self.c.setFillColor(INK_MID)
    kw = pdfmetrics.stringWidth(kind, 'Menlo', 7.6)
    self.c.drawString(MARGIN_X + USABLE_W - kw, self.y - 7.6, kind)
    self.y -= 9
    # body
    self.para(body, size=SZ_BODY, leading_mult=1.32)
    # meta chips row
    if metas:
        self.spacer(2)
        # Render metas left-aligned, separated by 18px
        x = MARGIN_X
        for i, m in enumerate(metas):
            self.c.setFont('Menlo', SZ_TINY); self.c.setFillColor(INK_MID)
            self.c.drawString(x, self.y - SZ_TINY, m)
            mw = pdfmetrics.stringWidth(m, 'Menlo', SZ_TINY)
            x += mw + 22 if i == 0 else mw + 22
        self.y -= SZ_TINY + 4
    self.spacer(2)


def _addl_row(self, strong, rest):
    """Additional projects arrow row with bold lead-in."""
    line = SZ_BODY * 1.32
    self.need(line * 2)
    self.c.setFont('Menlo', 8); self.c.setFillColor(INK_MID)
    self.c.drawString(MARGIN_X, self.y - 8, '→')
    # Render the strong portion then the rest
    x = MARGIN_X + 12
    self.c.setFont('Menlo-Bold', SZ_BODY); self.c.setFillColor(INK_SOFT)
    self.c.drawString(x, self.y - SZ_BODY, strong)
    sw = pdfmetrics.stringWidth(strong, 'Menlo-Bold', SZ_BODY)
    # Advance x by bold width plus a 4pt visible gap
    x += sw + 4
    # Now wrap rest
    self.c.setFont('Menlo', SZ_BODY); self.c.setFillColor(INK_SOFT)
    avail = MARGIN_X + USABLE_W - x
    words = rest.split(' ')
    cur = ''
    lines_used = 1
    for w in words:
        trial = (cur + ' ' + w).strip()
        if pdfmetrics.stringWidth(trial, 'Menlo', SZ_BODY) <= avail:
            cur = trial
        else:
            self.c.drawString(x, self.y - SZ_BODY, cur)
            self.y -= SZ_BODY * 1.32
            lines_used += 1
            x = MARGIN_X + 12
            avail = MARGIN_X + USABLE_W - x
            cur = w
    if cur:
        self.c.drawString(x, self.y - SZ_BODY, cur)
    self.y -= SZ_BODY * 1.32 + 2


def _skills(self, rows):
    label_w = 122
    row_gap = 4
    self.c.setFont('Menlo', SZ_BODY)
    line_h = SZ_BODY * 1.32
    for label, items in rows:
        # label (bold, fixed width, baseline aligned)
        # Wrap items text
        items_lines = wrap(items, 'Menlo', SZ_BODY, USABLE_W - label_w - 6)
        # Safety: if label was wider than label_w, body would overlap. Re-wrap to actual label width.
        block_h = max(line_h, line_h * len(items_lines))
        if self.need(block_h + row_gap): pass
        # label
        self.c.setFont('Menlo-Bold', SZ_BODY); self.c.setFillColor(INK_SOFT)
        self.c.drawString(MARGIN_X, self.y - SZ_BODY, label)
        # items
        x = MARGIN_X + label_w
        for i, il in enumerate(items_lines):
            self.c.setFont('Menlo', SZ_BODY); self.c.setFillColor(INK_SOFT)
            self.c.drawString(x, self.y - SZ_BODY - i * line_h, il)
        self.y -= block_h + row_gap


def _two_col(self):
    # Two columns of equal width with a 22pt gap
    col_gap = 22
    col_w = (USABLE_W - col_gap) / 2
    # Reserve current y, render both columns side-by-side, then advance y by max
    start_y = self.y
    # Left column: Writing
    self.c.setFont('Menlo-Bold', SZ_H3); self.c.setFillColor(INK)
    self.c.drawString(MARGIN_X, start_y - SZ_H3, 'WRITING')
    y1 = start_y - SZ_H3 - 4
    self.c.setFont('Menlo-Bold', 8.8); self.c.setFillColor(INK)
    title1 = 'Multi-Head Latent Attention — A Technical Deep-Dive'
    self.c.drawString(MARGIN_X, y1 - 8.8, title1)
    y1 -= 10
    body1 = ('643-line reference on KV-cache math, low-rank compression algebra, the '
             'absorption-trick derivation, and decoupled RoPE mechanics in DeepSeek-V2/V3. '
             'Companion pieces: ATTENTION_SINKS.md (600-line reference on the GPT-OSS sink '
             'bias + sliding/full attention alternation) and SSD.md (chunkwise Mamba-3 SSD '
             'derivation with naive-recurrence equivalence proof). All three live in the '
             'GitHub repos. Read on GitHub.')
    self.c.setFont('Menlo', SZ_BODY); self.c.setFillColor(INK_SOFT)
    for line in wrap(body1, 'Menlo', SZ_BODY, col_w):
        self.c.drawString(MARGIN_X, y1 - SZ_BODY, line)
        y1 -= SZ_BODY * 1.32

    # Right column: Education
    x2 = MARGIN_X + col_w + col_gap
    self.c.setFont('Menlo-Bold', SZ_H3); self.c.setFillColor(INK)
    self.c.drawString(x2, start_y - SZ_H3, 'EDUCATION')
    y2 = start_y - SZ_H3 - 4
    self.c.setFont('Menlo-Bold', 8.6); self.c.setFillColor(INK)
    self.c.drawString(x2, y2 - 8.6, 'B.Tech, Civil Engineering')
    period = '2020 – 2024'
    pw = pdfmetrics.stringWidth(period, 'Menlo', 7.6)
    self.c.setFont('Menlo', 7.6); self.c.setFillColor(INK_MID)
    self.c.drawString(x2 + col_w - pw, y2 - 7.6, period)
    y2 -= 9
    self.c.setFont('Menlo', 7.8); self.c.setFillColor(INK_MID)
    school = 'Heritage Institute of Technology, Kolkata · heritageit.edu'
    self.c.drawString(x2, y2 - 7.8, school)
    y2 -= 9
    body2 = ('Civil Engineering for the math, structures, and optimization; deep learning '
             'self-taught in parallel, from raw PyTorch up to 14 frontier architectures '
             '(DeepSeek-V3, LLaMA-3, GPT-OSS, Mamba-3, Stable Diffusion 1.x, and the 15-phase '
             'autonomous ML research platform).')
    self.c.setFont('Menlo', SZ_BODY); self.c.setFillColor(INK_SOFT)
    for line in wrap(body2, 'Menlo', SZ_BODY, col_w):
        self.c.drawString(x2, y2 - SZ_BODY, line)
        y2 -= SZ_BODY * 1.32

    self.y = min(y1, y2) - 4


# Attach methods
Layout._proj = _proj
Layout._addl_row = _addl_row
Layout._skills = _skills
Layout._two_col = _two_col

if __name__ == '__main__':
    build()
