#!/usr/bin/env python3
"""Author-name correction and the trichotomy / vanishing-sine strengthening (22 Oct 2026, 19:00)."""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 1) name correction everywhere except .git and the paper's shipped tree
for p in ROOT.rglob("*"):
    if p.is_file() and p.suffix in {".md", ".tex", ".py", ".html", ".json"} and ".git" not in p.parts and p.parts[len(ROOT.parts)] != "paper":
        s = p.read_text(encoding="utf-8", errors="ignore")
        if "Samieinejad" in s:
            s2 = s.replace("Samieinejad", "Samieinejad").replace("Samieinejad", "Samieinejad")
            if s2 != s:
                p.write_text(s2, encoding="utf-8")

# 2) manuscript v3: trichotomy theorem + conjecture
p = ROOT / "paper_update" / "manuscript" / "rigidity.tex"
t = p.read_text(encoding="utf-8")
old = "The parallel-triple condition of the lemma holds for exactly $23$ of the $113$ orbit representatives"
new = r"""\begin{theorem}[Trichotomy on a signed system]\label{thm:trichotomy}
Let $z\in T(\Q)^r$ satisfy a signed system~\eqref{eq:roles}, $s_i=\varepsilon s_k+\eta s_l$, $s_j=\varepsilon s_k-\eta s_l$, and put $A=\max(|s_k|,|s_l|)$, $B=\min(|s_k|,|s_l|)$. Then $\{|s_i|,|s_j|\}=\{A+B,A-B\}$, and exactly one of the following holds: (i) some sine vanishes; (ii) $z$ is admissible; (iii) $A=2B>0$. In case (i) two of the remaining sines have equal magnitude, so by Lemma~\ref{lem:degrel} the point lies on a torsion coset and has exponent rank at most $3$.
\end{theorem}
\begin{proof}
For real $x,y$ the magnitudes of $x+y$ and $x-y$ are $A+B$ and $A-B$ with $A=\max(|x|,|y|)$, $B=\min(|x|,|y|)$. If no sine vanishes then $B>0$ and $A\ne B$, and the four magnitudes $A,B,A+B,A-B$ are pairwise distinct unless $A-B=B$; by Lemma~\ref{lem:roles} the point is admissible exactly when they are distinct. For (i): if $s_l=0$ then $s_i=s_j$; if $s_k=0$ then $|s_i|=|s_j|=|s_l|$; if $s_i=0$ or $s_j=0$ then $|s_k|=|s_l|$.
\end{proof}
Case (iii) is the only way a rational point of a solution variety can avoid both admissibility and a monomial relation, and it is not a torsion-coset condition. Every one of the $935{,}552$ points recorded at $H\le4$ is of type (i). We therefore state the hypothesis that the data support directly and that implies both Conjecture~\ref{conj:rigidity} and Conjecture~\ref{conj:torsion}:
\begin{conjecture}[Vanishing-sine rigidity]\label{conj:vanishing}
For every full-depth configuration, every rational point of every signed system has a vanishing sine.
\end{conjecture}
Conjecture~\ref{conj:vanishing} is equivalent to Conjecture~\ref{conj:rigidity} together with the nonexistence of rational points of type (iii). The next computation is therefore not a larger admissibility sweep but a direct search for type (iii) points: rational-circle solutions of a signed system with $|s_l|=2|s_k|$ or $|s_k|=2|s_l|$ and all sines nonzero.

The parallel-triple condition of the lemma holds for exactly $23$ of the $113$ orbit representatives"""
assert old in t
p.write_text(t.replace(old, new, 1), encoding="utf-8")

p = ROOT / "paper_update" / "manuscript" / "paper.tex"
s = p.read_text(encoding="utf-8")
s = s.replace("a degeneracy-rank lemma explains the structure of these points and predicts in which configurations a point can lie on a torsion coset of codimension one.",
              "a degeneracy-rank lemma explains the structure of these points, and a trichotomy on the signed systems shows that every rational solution is admissible, has a vanishing sine, or has one offset exactly twice another; the data support the single hypothesis that every rational solution has a vanishing sine, which implies both rigidity and the torsion-coset hypothesis.")
p.write_text(s, encoding="utf-8")

p = ROOT / "paper_update" / "CHANGES_v3.md"
s = p.read_text(encoding="utf-8")
s = s.replace("| §Proof data |", "| §9.x, Theorem (trichotomy) and Conjecture (vanishing-sine rigidity) | On a signed system the magnitudes are {A, B, A+B, A-B}; a rational point is admissible, has a vanishing sine, or has A = 2B; a vanishing sine forces equal magnitudes hence a torsion coset; all 935,552 recorded points are of the vanishing-sine kind; the new conjecture implies 8.1 and 8.6 and names the next search (A = 2B points) | `agents/torsion_coset_probe/results/torsion_coset_H{3,4}_summary.json` (points_by_degeneracy) | PROVED (theorem); SEARCH-EVIDENCE (data); CONJECTURAL (hypothesis) |\n| §Proof data |", 1)
p.write_text(s, encoding="utf-8")

# 3) write-up, README, slides, ledger
p = ROOT / "docs" / "RESULTS.md"
s = p.read_text(encoding="utf-8")
f6 = """**6. A trichotomy, and the single hypothesis the data support (coordinator).** On a signed
system s_i = εs_k + ηs_l, s_j = εs_k − ηs_l the magnitudes are forced to be {A, B, A+B, A−B}
with A = max(|s_k|,|s_l|), B = min. Hence a rational point is exactly one of: a vanishing
sine, admissible, or A = 2B; and a vanishing sine forces two equal magnitudes among the rest,
so such a point lies on a torsion coset [PROVED, two lines; Theorem in `paper_update/manuscript/rigidity.tex`].
All 935,552 points recorded at heights ≤ 4 are of the vanishing-sine kind
[SEARCH-EVIDENCE, `agents/torsion_coset_probe/results/torsion_coset_H4_summary.json`]. So the
problem collapses to one statement, **vanishing-sine rigidity**: every rational solution of every
signed system has a vanishing sine. It implies Conjecture 8.1 and Conjecture 8.6, and it names
the next computation precisely: search for A = 2B points, the only kind the data never showed
[CONJECTURAL].

"""
s = s.replace("## Iteration 2: the loop turns again", f6 + "## Iteration 2: the loop turns again", 1)
p.write_text(s, encoding="utf-8")

p = ROOT / "README.md"
s = p.read_text(encoding="utf-8")
s = s.replace("| Empty region on the genus-5 curve |", "| Trichotomy and vanishing-sine rigidity | — | a rational solution is admissible, has a vanishing sine, or has A = 2B (proved); all 935,552 recorded points have a vanishing sine; one conjecture now implies both 8.1 and 8.6 and names the next search | PROVED + SEARCH-EVIDENCE + CONJECTURAL | `paper_update/manuscript/rigidity.tex` |\n| Empty region on the genus-5 curve |", 1)
p.write_text(s, encoding="utf-8")

p = ROOT / "docs" / "slides.html"
s = p.read_text(encoding="utf-8") if p.exists() else ""
s = s.replace('<div class="box"><p><b>From the failure, a lemma.</b>',
              '<div class="box"><p><b>Trichotomy.</b> On a signed system the magnitudes are forced to be {A, B, A+B, A−B}, so a rational solution is admissible, has a vanishing sine, or has A = 2B. All 935,552 recorded points have a vanishing sine. One hypothesis, <b>vanishing-sine rigidity</b>, now implies both conjectures and names the next search: A = 2B points. <span class="tag PROVED">PROVED</span> <span class="tag SE">SEARCH-EVIDENCE</span></p></div>\n  <div class="box"><p><b>From the failure, a lemma.</b>', 1)
if s:
    p.write_text(s, encoding="utf-8")

p = ROOT / "ledger" / "open_problems.json"
d = json.loads(p.read_text(encoding="utf-8"))
if not any(q["id"] == "P7" for q in d["problems"]):
    d["problems"].append({"id": "P7", "label": "conj:vanishing (new, 22 Oct)",
        "statement": "Vanishing-sine rigidity: every rational point of every signed system of a full-depth configuration has a vanishing sine. Implies Conj. 8.1 and 8.6; equivalent to 8.1 plus the nonexistence of A = 2B points.",
        "type": "hypothesis-probe", "parameter": "H",
        "state": {"iteration_2": "holds on all 935,552 points at H <= 4 (every point has a zero sine)"},
        "playbook": "playbooks/hypothesis-probe.md",
        "acceptance": "a type-(iii) point (A = 2B, all sines nonzero) re-verified exactly, or none at the next height",
        "best_tag_attainable": "SEARCH-EVIDENCE (a type-(iii) point would be PROVED and would refute the conjecture)",
        "next": "re-instrument the probe to search type-(iii) points directly at H = 5 (|s_l| = 2|s_k| is linear in the solved coordinate); then attempt the conjecture on each vanishing-sine coset by the paper's dimension reduction"})
p.write_text(json.dumps(d, indent=2), encoding="utf-8")
print("strengthening integrated; name corrected")
