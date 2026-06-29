"""Atandra Bharati — Resume PDF generator.

One-page US Letter, sans-serif body (Helvetica) + monospace accents (Menlo)
for repo paths and code-like tokens. Designed for ML/AI engineering roles.

Output: <repo>/atandra_bharati_resume.pdf
"""

from pathlib import Path
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Fonts ────────────────────────────────────────────────────────────────────
# HelveticaNeue (macOS system font) avoids a cmap collision in Helvetica.ttc
# when both regular and bold are registered in the same PDF.
pdfmetrics.registerFont(TTFont('Sans',     '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=0))
pdfmetrics.registerFont(TTFont('SansBold', '/System/Library/Fonts/HelveticaNeue.ttc', subfontIndex=1))
pdfmetrics.registerFont(TTFont('Mono',     '/System/Library/Fonts/Menlo.ttc',         subfontIndex=0))
pdfmetrics.registerFont(TTFont('MonoBold', '/System/Library/Fonts/Menlo.ttc',         subfontIndex=2))

# ── Layout constants ─────────────────────────────────────────────────────────
PAGE_W, PAGE_H = LETTER                        # 612 × 792 pt
MARGIN_X       = 0.5 * inch                    # 36 pt
MARGIN_TOP     = 0.45 * inch
MARGIN_BOTTOM  = 0.4 * inch
USABLE_W       = PAGE_W - 2 * MARGIN_X         # 540 pt

# Type scale (points) — bumped for better readability
SZ_NAME     = 24
SZ_ROLE     = 10.5
SZ_CONTACT  = 9.0
SZ_H2       = 11.0
SZ_BODY     = 9.4
SZ_BULLET   = 9.4
SZ_META     = 8.4
SZ_TINY     = 8.0

# Character spacing (added to text after a font is set; reportlab accepts a
# `charSpace` arg in `drawString` / `text` calls — we expose it via the Doc API)
DEFAULT_CHARSPACE = 0.2

# Colors
INK         = '#111111'
INK_SOFT    = '#2a2a2a'
INK_MID     = '#555555'
INK_FAINT   = '#888888'
INK_RULE    = '#cfcfcf'
INK_ACCENT  = '#0a5cff'

# Leading (line height) multipliers — slightly looser to match larger type
LEAD_BODY   = 1.36
LEAD_BULLET = 1.34
LEAD_META   = 1.28


# ── Renderer ─────────────────────────────────────────────────────────────────
class Doc:
    def __init__(self, c):
        self.c = c
        self.y = PAGE_H - MARGIN_TOP          # current baseline (top-down)
        self.bottom = MARGIN_BOTTOM           # stop drawing above this

    def space_left(self):
        return self.y - self.bottom

    def need(self, h):
        """If remaining space < h, auto-page-break and return False."""
        if self.space_left() < h:
            self.page_break()
            return False
        return True

    def page_break(self):
        self.c.showPage()
        self.y = PAGE_H - MARGIN_TOP

    def ensure(self, h):
        """Auto-break if there isn't room for h more points."""
        if self.space_left() < h:
            self.page_break()

    def text(self, s, font='Sans', size=SZ_BODY, color=INK, x=None, dy=0,
             charSpace=DEFAULT_CHARSPACE):
        """Draw at current y, advance y by size."""
        x = MARGIN_X if x is None else x
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        self.c.drawString(x, self.y - size, s, charSpace=charSpace)
        self.y -= size + dy

    def measure(self, s, font, size, charSpace=DEFAULT_CHARSPACE):
        # stringWidth doesn't natively add charSpace; reportlab's drawString adds
        # it as an extra per-character offset, so we approximate by including it.
        return pdfmetrics.stringWidth(s, font, size) + charSpace * max(0, len(s) - 1)

    def wrap(self, s, font, size, max_w):
        words, lines, cur = s.split(), [], ''
        for w in words:
            trial = (cur + ' ' + w).strip()
            if self.measure(trial, font, size) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur); cur = w
        if cur: lines.append(cur)
        return lines

    def para(self, s, font='Sans', size=SZ_BODY, color=INK,
             leading=LEAD_BODY, max_w=None, indent_first=0):
        """Word-wrap and draw a paragraph. y advances by full block height."""
        if max_w is None: max_w = USABLE_W - indent_first
        lines = self.wrap(s, font, size, max_w)
        block_h = size * leading * len(lines)
        self.ensure(block_h + 2)
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        x0 = MARGIN_X + indent_first
        for i, line in enumerate(lines):
            self.c.drawString(x0, self.y - size - i * size * leading, line)
        self.y -= block_h

    def bullet(self, label_bold, rest, font='Sans', size=SZ_BULLET,
               color=INK_SOFT, leading=LEAD_BULLET, label_color=INK):
        """Render a '• LABEL: rest' style bullet. label_bold drawn bold."""
        x = MARGIN_X + 8
        # Pre-compute wrapped lines for height estimation
        lw = self.measure(label_bold + ' ', 'SansBold', size)
        avail = USABLE_W - 8 - lw
        words, lines, cur = rest.split(), [], ''
        first = True
        for w in words:
            trial = (cur + ' ' + w).strip()
            if self.measure(trial, 'Sans', size) <= (avail if first else USABLE_W - 8) or not cur:
                cur = trial
            else:
                lines.append(cur)
                first = False
                cur = w
        if cur: lines.append(cur)
        block_h = size * leading * len(lines)
        self.ensure(block_h + 4)
        # Bullet glyph
        self.c.setFont('SansBold', size)
        self.c.setFillColor(label_color)
        self.c.drawString(MARGIN_X, self.y - size, '•')
        # Bold lead-in
        self.c.setFont('SansBold', size)
        self.c.setFillColor(INK)
        self.c.drawString(x, self.y - size, label_bold)
        # Wrapped rest
        self.c.setFont('Sans', size)
        self.c.setFillColor(color)
        first = True
        for i, line in enumerate(lines):
            x_l = (MARGIN_X + 8 + lw) if i == 0 else (MARGIN_X + 8)
            self.c.drawString(x_l, self.y - size - i * size * leading, line)
            first = False
        self.y -= block_h

    def tags(self, items, col_w, font='Mono', size=SZ_TINY, color=INK_MID):
        """Render a flat comma-separated tag line (wraps if needed)."""
        s = '  ·  '.join(items)
        lines = self.wrap(s, font, size, USABLE_W)
        self.c.setFont(font, size)
        self.c.setFillColor(color)
        for i, line in enumerate(lines):
            self.c.drawString(MARGIN_X, self.y - size - i * size * 1.25, line)
        self.y -= size * 1.25 * len(lines)

    def h2(self, label, sub=None):
        """Section heading: small caps + horizontal rule underneath."""
        # Reserve space — push to next page if fewer than 30pt remain
        if self.space_left() < 30:
            self.page_break()
        self.y -= 4
        self.c.setFont('SansBold', SZ_H2)
        self.c.setFillColor(INK)
        self.c.drawString(MARGIN_X, self.y - SZ_H2, label.upper())
        lw = self.measure(label.upper(), 'SansBold', SZ_H2)
        if sub:
            self.c.setFont('Sans', SZ_META)
            self.c.setFillColor(INK_FAINT)
            self.c.drawString(MARGIN_X + lw + 8, self.y - SZ_META + 1.5, sub)
        self.y -= SZ_H2 + 2
        # hairline rule
        self.c.setStrokeColor(INK_RULE)
        self.c.setLineWidth(0.4)
        self.c.line(MARGIN_X, self.y, PAGE_W - MARGIN_X, self.y)
        self.y -= 4

    def spacer(self, h):
        self.y -= h


# ── Header ───────────────────────────────────────────────────────────────────
def draw_header(d):
    # Name
    d.c.setFont('SansBold', SZ_NAME)
    d.c.setFillColor(INK)
    d.c.drawString(MARGIN_X, d.y - SZ_NAME, 'Atandra Bharati')
    d.y -= SZ_NAME + 2

    # Role line
    d.c.setFont('Sans', SZ_ROLE)
    d.c.setFillColor(INK_SOFT)
    role = 'Deep Learning Research Engineer  ·  From-scratch PyTorch implementations of frontier AI architectures'
    lines = d.wrap(role, 'Sans', SZ_ROLE, USABLE_W)
    d.c.drawString(MARGIN_X, d.y - SZ_ROLE, lines[0])
    d.y -= SZ_ROLE + 6

    # Contact line — 2 columns × 2 rows, monospace for visual rhythm
    d.c.setFont('Mono', SZ_CONTACT)
    d.c.setFillColor(INK_MID)
    contacts = [
        'atandrabharati@gmail.com',
        'github.com/atandra2000',
        'linkedin.com/in/atandrabharati',
        'atandra2000.github.io/mycv',
    ]
    line_w = USABLE_W / 2
    for i in range(0, 4, 2):
        for j, txt in enumerate(contacts[i:i+2]):
            d.c.drawString(MARGIN_X + j * line_w, d.y - SZ_CONTACT, txt)
        d.y -= SZ_CONTACT + 3
    # Location strip
    d.c.setFont('Sans', SZ_CONTACT)
    d.c.setFillColor(INK_FAINT)
    d.c.drawString(MARGIN_X, d.y - SZ_CONTACT,
                   'Kolkata, India   ·   Remote-friendly   ·   Open to global remote roles')
    d.y -= SZ_CONTACT + 8


# ── Anchor metric strip ──────────────────────────────────────────────────────
# ── Sections ─────────────────────────────────────────────────────────────────
def draw_summary(d):
    d.h2('Summary')
    d.para(
        'Self-taught deep learning research engineer (B.Tech Civil Engineering, 2024) with '
        '14 from-scratch PyTorch projects spanning LLMs, latent diffusion, multimodal AI, '
        'agentic research, long-context attention, and state-space models. Headline results: '
        '78% peak-memory cut on LLaMA-3 pretraining (92 GB → 20 GB on a single A100 80GB); '
        '0.0947 training loss on Stable Diffusion 1.x from scratch (860M UNet, 2× RTX 5090); '
        '2× KV-cache reduction at 128K in a GPT-OSS-style long-context MoE; 15-phase '
        'multi-agent ML research platform with 878 passing tests.',
        size=SZ_BODY, leading=LEAD_BODY, color=INK_SOFT,
    )
    d.spacer(3)


def draw_skills(d):
    d.h2('Technical Skills')
    groups = [
        ('LLM',           'LLaMA-3 · DeepSeek-V3 · GPT-OSS · Mamba-3 · MLA · GQA · MoE · MTP · '
                          'Gated Delta Net · complex64 SSD · sliding/full attention · '
                          'learned sinks · YaRN · μP · WSD · NorMuon · CautiousAdamW'),
        ('Generative Vision', 'Stable Diffusion 1.x · latent diffusion · UNet · DDPM/DDIM · '
                              'Min-SNR · CFG · EMA · VAE · GAN · DCGAN · PatchGAN · β-VAE · '
                              'CycleGAN · AdaIN'),
        ('Multimodal & Video', 'ViT · SigLIP · PaliGemma-style fusion · HRNet pose · ST-GCN · '
                               'CTR-GCN · NTU RGB+D 120'),
        ('Core',          'Python 3.12 · PyTorch 2.x · torch.compile · SDPA · Flash-Attn 2 · '
                          'BF16 · chunked CE · gradient checkpointing · DDP · safetensors · '
                          'HuggingFace · Diffusers · W&B · Comet'),
        ('Agentic & Infra', 'Multi-agent orchestration · provider-agnostic LLM routing · vector + '
                          'graph memory · Pydantic v2 · pytest · Ruff · A100 80GB · RTX 5090 · '
                          'RTX 6000 Ada · RTX 3090 · P100 · 2× T4'),
    ]
    for label, items in groups:
        d.c.setFont('SansBold', SZ_BODY)
        d.c.setFillColor(INK)
        d.c.drawString(MARGIN_X, d.y - SZ_BODY, label)
        lw = d.measure(label, 'SansBold', SZ_BODY)
        d.c.setFont('Sans', SZ_BODY)
        d.c.setFillColor(INK_SOFT)
        avail = USABLE_W - lw - 8
        lines = d.wrap(items, 'Sans', SZ_BODY, avail)
        first = True
        for i, line in enumerate(lines):
            x = (MARGIN_X + lw + 8) if first else MARGIN_X
            d.c.drawString(x, d.y - SZ_BODY - i * SZ_BODY * LEAD_BODY, line)
            first = False
        d.y -= SZ_BODY * LEAD_BODY * len(lines) + 1
    d.spacer(2)


def draw_experience(d):
    d.h2('Experience')
    # Role header
    d.c.setFont('SansBold', SZ_BODY + 0.6)
    d.c.setFillColor(INK)
    d.c.drawString(MARGIN_X, d.y - SZ_BODY - 0.6, 'ML Engineering Portfolio')
    d.c.setFont('Mono', SZ_META)
    d.c.setFillColor(INK_FAINT)
    period = 'Nov 2022 – Present  ·  Self-directed  ·  github.com/atandra2000'
    pw = d.measure(period, 'Mono', SZ_META)
    d.c.drawString(PAGE_W - MARGIN_X - pw, d.y - SZ_BODY - 0.6, period)
    d.y -= SZ_BODY + 4

    d.bullet(
        '14 from-scratch PyTorch systems',
        'across LLMs, latent diffusion, multimodal AI, generative vision, video '
        'understanding, and agentic ML — no HF Trainer, no Lightning, every layer '
        'written by hand.',
    )
    d.bullet(
        'Memory engineering flagship: LLaMA-3-Lite',
        '515M-param LLaMA-3-style transformer cut peak training memory 92 GB → 20 GB '
        '(78%) on a single A100 80GB via gradient checkpointing, chunked cross-entropy '
        '(logits 50 GB → 0.3 GB), disk-backed token caching (RAM 112 GB → 1 MB), BF16, '
        'FA2, channels_last, and fused AdamW.',
    )
    d.bullet(
        'Frontier reproductions',
        'faithful DeepSeek-V3 (MLA + AuxLossFreeGate MoE + MTP, with the absorption '
        'trick), GPT-OSS (sliding/full attention alt + learned sinks + YaRN 128K, 2× '
        'KV-cache cut at 128K), and Mamba-3 (complex64 SSD with 50% smaller state, MIMO '
        'head mixing, zero causal conv).',
    )
    d.bullet(
        'Diffusion flagship: Stable Diffusion 1.x',
        '860M-param UNet trained from random init on 2× RTX 5090 across a 7-phase '
        'curriculum (LAION-Aesthetic → DiffusionDB/JourneyDB → VGGFace2 → COCO → '
        'consolidation); best loss 0.0947 at epoch 16; epoch-42 checkpoint released '
        'on HuggingFace.',
    )
    d.bullet(
        'Agentic flagship: Autonomous ML Research Engineer',
        '15-phase multi-agent platform (23 agents, 61 tools, 186 models, 878 tests) '
        'that turns an arXiv paper into evaluated experiments end-to-end with '
        'provider-agnostic LLM routing and self-repair.',
    )
    d.spacer(2)


def draw_projects(d):
    d.h2('Selected Projects')
    projects = [
        ('Stable Diffusion 1.x — from random init on 2× RTX 5090',
         'StableDiffusion',
         '860M-param UNet across a 7-phase curriculum on 1.3M+ images (LAION-Aesthetic → '
         'DiffusionDB/JourneyDB → VGGFace2 → COCO → consolidation). DDPM/DDIM, Min-SNR, '
         'EMA, channels_last on Blackwell, DDP/NCCL. Best loss 0.0947 at epoch 16; '
         'epoch-42 checkpoint released on HuggingFace.'),
        ('Autonomous ML Research Engineer — 15-phase multi-agent platform',
         'AutonomousResearcher',
         'Paper-to-experiment end-to-end: paper analysis, repo analysis, experiment '
         'planning, code patches, training runs, statistical evaluation, autonomous '
         'looping, research reports. 23 agents, 61 tools, 186 models, 878 tests. '
         'Provider-agnostic LLM layer with self-repair.'),
        ('DeepSeek-v3-Lite — faithful V3 reproduction',
         'DeepSeek-v3-Lite',
         '422M params · MLA with absorption-trick inference · AuxLossFreeGate MoE · '
         'Multi-Token Prediction · MTP-as-draft speculative decoding. Companion '
         '643-line MLA deep-dive.'),
        ('FusionLLM — hybrid MLA + Gated Delta Net + MoE + MTP',
         'FusionLLM',
         '415.6M active / 868.6M stored params, 24 layers, single A100 80GB. '
         'Dual-optimizer (NorMuon + CautiousAdamW), WSD + μP scheduler, 8.31B-token '
         'Chinchilla recipe.'),
        ('Face Aging CycleGAN — per-layer AdaIN conditioning',
         'FaceAgingCycleGAN',
         '256×256 IMDB-WIKI, 31/50 epochs on RTX 6000 Ada. Bidirectional young ↔ old '
         'with AdaIN style normalization, 3-scale PatchGAN discriminator, LSGAN + '
         'VGG-19 perceptual + L1 identity losses.'),
        ('Vision-Language Model — PaliGemma-inspired, zero pretrained weights',
         'VisionLanguageModel',
         '140M params · SigLIP ViT encoder + linear projector + Gemma-style GQA decoder '
         'with RoPE & GeGLU. Image patches injected at [IMG] tokens; trained end-to-end '
         'on COCO 2014 on a single P100.'),
    ]
    for title, repo, desc in projects:
        d.ensure((SZ_BODY + 0.4) * 1.15 * 2 + SZ_BODY * 4)  # room for title + desc
        # Project title row (title left, repo path right)
        d.c.setFont('SansBold', SZ_BODY + 0.4)
        d.c.setFillColor(INK)
        d.c.setFont('Mono', SZ_META)
        d.c.setFillColor(INK_ACCENT)
        repo_url = f'github.com/atandra2000/{repo}'
        rw = d.measure(repo_url, 'Mono', SZ_META)
        title_max_w = USABLE_W - rw - 12
        # Wrap title if needed
        title_lines = d.wrap(title, 'SansBold', SZ_BODY + 0.4, title_max_w)
        d.c.setFont('SansBold', SZ_BODY + 0.4)
        d.c.setFillColor(INK)
        for i, line in enumerate(title_lines):
            d.c.drawString(MARGIN_X, d.y - SZ_BODY - 0.4 - i * (SZ_BODY + 0.4) * 1.15, line)
        # Repo URL on first line, vertically centered to title block
        d.c.setFont('Mono', SZ_META)
        d.c.setFillColor(INK_ACCENT)
        d.c.drawString(PAGE_W - MARGIN_X - rw, d.y - SZ_BODY - 0.4, repo_url)
        d.y -= (SZ_BODY + 0.4) * 1.15 * len(title_lines) + 3
        # Description — indented
        d.para(desc, font='Sans', size=SZ_BODY - 0.4,
               color=INK_SOFT, leading=LEAD_BODY, indent_first=10)
        d.y -= 2
    d.spacer(0)


def draw_education(d):
    d.h2('Education')
    d.c.setFont('SansBold', SZ_BODY)
    d.c.setFillColor(INK)
    d.c.drawString(MARGIN_X, d.y - SZ_BODY, 'B.Tech, Civil Engineering')
    d.c.setFont('Mono', SZ_META)
    d.c.setFillColor(INK_FAINT)
    period = '2020 – 2024'
    pw = d.measure(period, 'Mono', SZ_META)
    d.c.drawString(PAGE_W - MARGIN_X - pw, d.y - SZ_BODY + 1.5, period)
    d.y -= SZ_BODY + 1

    d.c.setFont('Sans', SZ_META)
    d.c.setFillColor(INK_MID)
    d.c.drawString(MARGIN_X, d.y - SZ_META, 'Heritage Institute of Technology, Kolkata · heritageit.edu')
    d.y -= SZ_META + 3

    d.para(
        'Civil Engineering for the math, structures, and optimization; deep learning self-taught '
        'in parallel, from raw PyTorch up to frontier LLM, diffusion, multimodal, and '
        'agentic architectures.',
        font='Sans', size=SZ_BODY - 0.4, color=INK_SOFT, leading=LEAD_BODY,
    )


# ── Build ────────────────────────────────────────────────────────────────────
def build():
    out = Path('/tmp/resume.pdf')
    c = Canvas(str(out), pagesize=LETTER)
    c.setTitle('Atandra Bharati — Deep Learning Research Engineer · Résumé')
    c.setAuthor('Atandra Bharati')
    c.setSubject('Résumé')
    c.setCreator('Atandra Bharati · Resume PDF Generator')

    # Wrap drawString so every text gets a small charSpace by default
    # (already-tight typography reads better with a touch of tracking).
    _orig_drawString = c.drawString
    _cs = DEFAULT_CHARSPACE
    def _drawString(x, y, s, charSpace=_cs):
        _orig_drawString(x, y, s, charSpace=charSpace)
    c.drawString = _drawString

    d = Doc(c)
    draw_header(d)
    draw_summary(d)
    draw_skills(d)
    draw_experience(d)
    draw_projects(d)
    draw_education(d)

    c.save()
    sz = (Path(out).stat().st_size)
    print(f'Wrote {out}  ({sz} bytes)')


if __name__ == '__main__':
    build()