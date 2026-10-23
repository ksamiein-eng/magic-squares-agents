#!/usr/bin/env python3
"""Apply the second skeptic pass (results/skeptic_verdict_iteration2.md): fix the double-counted total,
qualify the sum-9 checking protocol, and soften the vanishing-sine wording. Idempotent."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
edits = {
    "paper_update/manuscript/rigidity.tex": [
        ("Every one of the $935{,}552$ points recorded at $H\\le4$ is of type (i).",
         "Every one of the $662{,}528$ points recorded at $H\\le4$ (the height-$3$ grid is contained in the height-$4$ grid, so the two sweeps are not added) is of type (i)."),
        ("We therefore state the hypothesis that the data support directly and that implies both Conjecture~\\ref{conj:rigidity} and Conjecture~\\ref{conj:torsion}:",
         "We therefore state the hypothesis that the data are consistent with and that implies both Conjecture~\\ref{conj:rigidity} and Conjecture~\\ref{conj:torsion}; it is strictly stronger than Conjecture~\\ref{conj:rigidity}, since it also excludes type (iii), and the evidence for the extra exclusion is only the absence of type (iii) points at $H\\le4$, where the grid carries the split primes $5$, $13$ and $17$:"),
        ("The remaining $21$ orbits are a prediction for larger heights.",
         "The remaining $21$ orbits are candidates for larger heights; the criterion is necessary, not sufficient."),
    ],
    "paper_update/manuscript/paper.tex": [
        ("The two-parameter certificate is extended through exponent sum nine ($5{,}520$ signed systems, independently re-checked).",
         "The two-parameter certificate is extended through exponent sum nine ($5{,}520$ signed systems; the standard-library checker accepts the whole certificate, and the sum-eight part is additionally cross-checked symbolically)."),
        ("the data support the single hypothesis that every rational solution has a vanishing sine, which implies both rigidity and the torsion-coset hypothesis.",
         "the data are consistent with the hypothesis that every rational solution has a vanishing sine, which implies both rigidity and the torsion-coset hypothesis and is strictly stronger than the former."),
        ("while the symbolic cross-check and mutation tests of the sum-nine part had not been run at the time of writing.",
         "while the symbolic cross-check and mutation tests of the sum-nine part had not been run at the time of writing; the sum-nine checker differs from the sum-eight checker, which passed its mutation tests, only in constants (expected case list, schema name, coverage range)."),
    ],
    "paper_update/CHANGES_v3.md": [
        ("all 935,552 recorded points are of the vanishing-sine kind", "all 662,528 recorded points at H ≤ 4 are of the vanishing-sine kind"),
    ],
    "docs/RESULTS.md": [
        ("All 935,552 points recorded at heights ≤ 4 are of the vanishing-sine kind", "All 662,528 points recorded at height ≤ 4 (the height-3 grid is a subset, so the sweeps are not added) are of the vanishing-sine kind"),
        ("So the\nproblem collapses to one statement, **vanishing-sine rigidity**: every rational solution of every\nsigned system has a vanishing sine. It implies Conjecture 8.1 and Conjecture 8.6, and it names\nthe next computation precisely: search for A = 2B points, the only kind the data never showed\n[CONJECTURAL].",
         "So the\nproblem reduces to one hypothesis, **vanishing-sine rigidity**: every rational solution of every\nsigned system has a vanishing sine. It implies Conjecture 8.1 and Conjecture 8.6 and is strictly\nstronger than 8.1; the evidence for the extra strength is only the absence of A = 2B points at\nheight ≤ 4, which is weak. It names the next computation precisely: search for A = 2B points\n[CONJECTURAL]."),
        ("The other\n21 orbits are a prediction for height 5.", "The other\n21 orbits are candidates for height 5 (the criterion is necessary, not sufficient)."),
    ],
    "docs/ONEPAGE.md": [
        ("all recorded points have a vanishing sine. **Vanishing-sine rigidity** implies Conj. 8.1 and 8.6 and names the next search (A = 2B points)",
         "all 662,528 recorded points have a vanishing sine. **Vanishing-sine rigidity** implies Conj. 8.1 and 8.6, is strictly stronger than 8.1, and names the next search (A = 2B points; their absence so far is weak evidence)"),
    ],
    "docs/slides.html": [
        ("All 935,552 recorded points have a vanishing sine. One hypothesis, <b>vanishing-sine rigidity</b>, now implies both conjectures and names the next search: A = 2B points.",
         "All 662,528 recorded points have a vanishing sine. One hypothesis, <b>vanishing-sine rigidity</b>, implies both conjectures (it is strictly stronger than 8.1) and names the next search: A = 2B points."),
    ],
    "README.md": [
        ("all 935,552 recorded points have a vanishing sine; one conjecture now implies both 8.1 and 8.6 and names the next search",
         "all 662,528 recorded points have a vanishing sine; one conjecture, strictly stronger than 8.1, implies both 8.1 and 8.6 and names the next search"),
    ],
    "CONTENTS.md": [
        ("Torsion-coset data at H ≤ 4 (935,552 points, 0 exceptions)", "Torsion-coset data at H ≤ 4 (662,528 points, 0 exceptions)"),
    ],
    "docs/VIDEO_SCRIPT.md": [
        ("One conjecture now implies both of the paper's.", "One conjecture, strictly stronger than the paper's, now implies both of them."),
    ],
}
for rel, pairs in edits.items():
    p = ROOT / rel
    if not p.exists():
        return
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if new in s:
            continue
        if old in s:
            s = s.replace(old, new)
        else:
            print("WARN not found in", rel, ":", old[:60].encode("ascii","replace").decode())
    p.write_text(s, encoding="utf-8")

# ledger
p = ROOT / "ledger" / "open_problems.json"
d = json.loads(p.read_text(encoding="utf-8"))
for q in d["problems"]:
    if q["id"] == "P7":
        q["state"]["iteration_2"] = "holds on all 662,528 points at H <= 4 (every point has a zero sine); strictly stronger than 8.1; evidence for the extra strength is weak (grid primes 5, 13, 17)"
p.write_text(json.dumps(d, indent=2), encoding="utf-8")

# history
p = ROOT / "HISTORY.md"
s = p.read_text(encoding="utf-8")
row = "| 20:40 | — | Second skeptic pass applied | **Corrections:** the total \"935,552 points at H ≤ 4\" double-counted (height-3 grid ⊂ height-4 grid) and is now 662,528; the abstract's \"independently re-checked\" for sum 9 qualified (standard-library checker only; sum-8 part symbolically cross-checked; checkers differ only in constants); vanishing-sine rigidity stated as strictly stronger than 8.1 with weak evidence for the extra strength; \"prediction\" for the 21 orbits changed to \"candidates\" (criterion necessary, not sufficient) |\n\n## Standing caveats"
if "Second skeptic pass applied" not in s:
    s = s.replace("\n## Standing caveats", "\n" + row, 1)
p.write_text(s, encoding="utf-8")
print("skeptic-2 corrections applied")
