#!/usr/bin/env python3
"""Draw the cover image (1600x900) and a results figure (1600x900) with Pillow, for the submission gallery and post."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"


def font(size, bold=False):
    for name in (["segoeuib.ttf", "arialbd.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def gradient_bg(w, h):
    img = Image.new("RGB", (w, h), (11, 16, 32))
    px = img.load()
    for y in range(h):
        for x in range(0, w, 2):
            t = x / w; u = y / h
            r = int(11 + 40 * (1 - u) * t); g = int(16 + 60 * u * (1 - t) + 10 * t); b = int(32 + 70 * t + 30 * u)
            px[x, y] = (min(r, 255), min(g, 255), min(b, 255))
            if x + 1 < w:
                px[x + 1, y] = px[x, y]
    return img


def grad_text(draw, xy, text, f, c1=(45, 212, 191), c2=(167, 139, 250)):
    # approximate a horizontal gradient by drawing character by character
    x, y = xy
    n = max(1, len(text) - 1)
    for k, ch in enumerate(text):
        t = k / n
        col = tuple(int(c1[j] + (c2[j] - c1[j]) * t) for j in range(3))
        draw.text((x, y), ch, font=f, fill=col)
        x += draw.textlength(ch, font=f)


def cover():
    w, h = 1600, 900
    img = gradient_bg(w, h); d = ImageDraw.Draw(img)
    d.text((80, 70), "OSI HACKATHON 2026 · PHYSICAL SCIENCES & MATHEMATICS", font=font(22, True), fill=(45, 212, 191))
    d.text((80, 120), "A paper that attacks", font=font(84, True), fill=(238, 242, 255))
    grad_text(d, (80, 215), "its own open problems", font(84, True))
    d.text((80, 330), "Rigidity Lab: a validated loop for AI on hard open problems in mathematics.", font=font(30), fill=(219, 226, 255))
    d.text((80, 372), "Instance one: magic squares of squares.", font=font(30), fill=(154, 166, 200))
    stats = [("3", "iterations of the loop\nin one afternoon"), ("5,520", "signed systems certified\n(theorem extended twice)"), ("1.9M", "rational solutions tested,\nzero exceptions"), ("0", "claims without a\nreferee tag")]
    x = 80
    for n, l in stats:
        d.rounded_rectangle((x, 470, x + 340, 700), radius=22, fill=(255, 255, 255, 14), outline=(255, 255, 255))
        d.rounded_rectangle((x, 470, x + 340, 700), radius=22, fill=(22, 30, 58), outline=(60, 70, 110))
        grad_text(d, (x + 26, 500), n, font(76, True))
        d.multiline_text((x + 26, 600), l, font=font(22), fill=(154, 166, 200), spacing=6)
        x += 365
    d.text((80, 780), "Kimia Samieinejad · Jonathan Wolinski · github.com/ksamiein-eng/magic-squares-agents", font=font(24), fill=(154, 166, 200))
    img.save(OUT / "cover.png"); print("wrote", OUT / "cover.png")


def results():
    w, h = 1600, 900
    img = gradient_bg(w, h); d = ImageDraw.Draw(img)
    d.text((80, 60), "WHAT MOVED TODAY", font=font(22, True), fill=(45, 212, 191))
    d.text((80, 100), "Three iterations, every claim tagged", font=font(56, True), fill=(238, 242, 255))
    rows = [("Theorem 1.1 (r = 2)", "sum ≤ 7", "sum ≤ 9  ·  5,520 systems, checker PASS", "MACHINE-VERIFIED", (45, 212, 191)),
            ("Conjecture 7.3 (genus-5 curve)", "needs Chabauty", "quotients 123.a1 · 492.b1 · 1968.j1, all rank 1; rank Jac(C) ≥ 3", "PROVED / DATABASE-QUOTED", (74, 222, 128)),
            ("Conjecture 8.6 (torsion cosets)", "untested", "1,916,672 solutions at height ≤ 5, zero exceptions", "SEARCH-EVIDENCE", (167, 139, 250)),
            ("New: trichotomy + lemma", "—", "a false sharpening refuted, then explained; one conjecture implies both", "PROVED / CONJECTURAL", (251, 113, 133)),
            ("Empty region on the curve", "height 1,500", "height 1,000,000", "SEARCH-EVIDENCE", (167, 139, 250))]
    y = 200
    d.text((80, y), "target", font=font(20, True), fill=(154, 166, 200)); d.text((480, y), "before", font=font(20, True), fill=(154, 166, 200)); d.text((680, y), "after", font=font(20, True), fill=(154, 166, 200)); d.text((1260, y), "tag", font=font(20, True), fill=(154, 166, 200))
    y += 44
    for t, b, a, tag, col in rows:
        d.line((80, y - 10, 1520, y - 10), fill=(50, 58, 90), width=1)
        d.text((80, y), t, font=font(26, True), fill=(238, 242, 255)); d.text((480, y), b, font=font(24), fill=(154, 166, 200)); d.text((680, y), a, font=font(24), fill=(219, 226, 255))
        d.rounded_rectangle((1260, y + 2, 1260 + 14 + d.textlength(tag, font=font(18, True)), y + 34), radius=12, outline=col, width=2)
        d.text((1267, y + 7), tag, font=font(18, True), fill=col)
        y += 96
    d.text((80, 800), "Referee passes: 2 · reproducible stages: 6/6 passing · transcripts: 9 agent runs · the problem is still open", font=font(24), fill=(154, 166, 200))
    img.save(OUT / "results.png"); print("wrote", OUT / "results.png")


cover(); results()
