#!/usr/bin/env python3
"""Repair docs/slides.html: rebuild slide 7 with all five finding boxes, inline the SVG figure, tighten sizes, add a counter."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "docs" / "slides.html"
s = p.read_text(encoding="utf-8")
svg = (ROOT / "docs" / "figure.svg").read_text(encoding="utf-8")
svg = re.sub(r"<svg ", '<svg class="fig" style="width:100%;height:auto;max-height:72vh" ', svg, count=1)

# 1) inline the figure
s = re.sub(r'<img class="fig" src="figure.svg" alt="architecture">', lambda m: svg, s)

# 2) rebuild slide 7 completely
start = s.find('<section class="slide">\n  <h2>Findings 2')
end = s.find("</section>", start) + len("</section>")
assert start > 0 and end > start
slide7 = """<section class="slide">
  <h2>Findings 2–5 — pushing the certified region, and learning from a failure</h2>
  <div class="box"><p><b>Certificate extender.</b> Theorem 1.1 extended from exponent sum 7 to <b>8</b> (iteration 1: 3,600 systems, checker PASS 133 s, SymPy cross-check 75/75) and to <b>9</b> (iteration 2, by the planner's command: 5,520 systems, 553,392 exact determinants, checker PASS 305 s). <span class="tag MV">MACHINE-VERIFIED</span></p></div>
  <div class="box"><p><b>Torsion prober.</b> Conjecture 8.6 tested on <b>273,024</b> exact rational solutions at height ≤ 3 and <b>662,528</b> at height ≤ 4 (all 113 orbits, 48 systems): 0 off a torsion coset, 0 admissible. Iteration 1 proposed a sharper form (rank ≤ 2); iteration 2 refuted it (rank-3 points in two orbits). The loop corrected itself. <span class="tag SE">SEARCH-EVIDENCE</span></p></div>
  <div class="box"><p><b>From the failure, a lemma.</b> A zero sine on row r is the relation A<sub>r</sub>; equal magnitudes on rows i, j give A<sub>i</sub> ± A<sub>j</sub>. So degenerate points lie on torsion cosets, rank ≤ 3, and rank 3 needs A<sub>i</sub> ± A<sub>j</sub> ∥ A<sub>r</sub>. Criterion true in 23/113 orbits, including the two that showed rank 3; all rank-3 points explained. <span class="tag PROVED">PROVED</span> <span class="tag MV">MACHINE-VERIFIED</span></p></div>
  <div class="box"><p><b>Trichotomy.</b> On a signed system the magnitudes are forced to be {A, B, A+B, A−B}, so a rational solution is admissible, has a vanishing sine, or has A = 2B. All 935,552 recorded points have a vanishing sine. One hypothesis, <b>vanishing-sine rigidity</b>, now implies both conjectures and names the next search: A = 2B points. <span class="tag PROVED">PROVED</span> <span class="tag SE">SEARCH-EVIDENCE</span> <span class="tag CONJ">CONJECTURAL</span></p></div>
  <div class="box"><p><b>Point hunter.</b> Sieved exact search: no new point on C to height <b>1,000,000</b> (500 billion pairs, 6 min), none on the genus-2 quotient to 300,000; 12 small points on E₀, none lifting. <span class="tag SE">SEARCH-EVIDENCE</span></p></div>
</section>"""
s = s[:start] + slide7 + s[end:]

# 3) sizes and counter
s = s.replace("  .slide { display:none; box-sizing:border-box; width:100vw; height:100vh; padding:56px 80px; }",
              "  .slide { display:none; box-sizing:border-box; width:100vw; height:100vh; padding:44px 72px; overflow:hidden; }")
s = s.replace("  h1 { font-size:46px; margin:0 0 12px; color:var(--accent); }\n  h2 { font-size:34px; margin:0 0 18px; color:var(--accent); }\n  p, li { font-size:22px; line-height:1.4; }",
              "  h1 { font-size:44px; margin:0 0 12px; color:var(--accent); }\n  h2 { font-size:30px; margin:0 0 14px; color:var(--accent); }\n  p, li { font-size:19px; line-height:1.38; }\n  .counter { position:fixed; right:18px; bottom:12px; color:#999; font-size:14px; }")
s = s.replace("  .box { background:var(--box); border-radius:12px; padding:16px 22px; margin:8px 0; }",
              "  .box { background:var(--box); border-radius:12px; padding:12px 18px; margin:7px 0; }")
s = s.replace("  table { border-collapse:collapse; font-size:19px; }", "  table { border-collapse:collapse; font-size:17px; }")
if '<div class="counter"' not in s:
    s = s.replace("<script>", '<div class="counter" id="counter">1 / 10</div>\n<script>')
    s = s.replace("function show(n){ slides[i].classList.remove('active'); i=(n+slides.length)%slides.length; slides[i].classList.add('active'); }",
                  "function show(n){ slides[i].classList.remove('active'); i=(n+slides.length)%slides.length; slides[i].classList.add('active'); document.getElementById('counter').textContent=(i+1)+' / '+slides.length; }")
p.write_text(s, encoding="utf-8")
print("slides fixed; boxes on slide 7:", slide7.count('class="box"'), "; inline svg:", "<svg" in s and 'src="figure.svg"' not in s)
