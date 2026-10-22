#!/usr/bin/env python3
"""Reflow the quotient-identities display in paper_update/manuscript/paper.tex onto two lines (and in the generator)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GOOD = ("\\begin{gather*}\n"
        " P(h)=f(h^2),\\qquad \\frac{P(h)}{h^6}=g\\!\\left(h^2+h^{-2}\\right),\\qquad \\frac{f(x)}{x^3}=g\\!\\left(x+\\frac1x\\right),\\\\\n"
        " f(x)=x^6+70x^5-1009x^4+7060x^3-1009x^2+70x+1.\n"
        "\\end{gather*}")
pat = re.compile(r"\\begin\{gather\*\}.*?\\end\{gather\*\}", re.S)
for f in [ROOT / "paper_update" / "manuscript" / "paper.tex", ROOT / "tools" / "patch_paper_v3.py"]:
    s = f.read_text(encoding="utf-8")
    n = len(pat.findall(s))
    s2 = pat.sub(lambda m: GOOD, s, count=1)
    f.write_text(s2, encoding="utf-8")
    print(f.name, "gather blocks found:", n, "replaced:", s2 != s)
s = (ROOT / "paper_update" / "manuscript" / "paper.tex").read_text(encoding="utf-8")
i = s.find("\\begin{gather*}")
print(repr(s[i:i + 240]))
