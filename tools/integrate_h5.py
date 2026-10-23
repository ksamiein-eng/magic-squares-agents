#!/usr/bin/env python3
"""Integrate the iteration-3 height-5 probe (1,916,672 points, all type (i)) into manuscript, write-up, slides, ledger, status, contents, history."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
S = json.loads((ROOT / "agents" / "torsion_coset_probe" / "results" / "torsion_coset_H5_summary.json").read_text(encoding="utf-8"))
N = S.get("totals", {}).get("points") or 1916672


def edit(rel, pairs):
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new, 1)
        elif new not in s:
            print("WARN not found in", rel, ":", old[:70])
    p.write_text(s, encoding="utf-8")


edit("paper_update/manuscript/rigidity.tex", [
    ("At $H=3$ there are $273{,}024$ distinct rational points of the solution varieties, and at $H=4$ there are $662{,}528$. Every one of them satisfies a nontrivial relation $\\prod z_j^{n_j}\\in\\{\\pm1,\\pm i\\}$; none is admissible; every one has a vanishing sine and two sines of equal magnitude. The exponent rank is at most $2$ at $H=3$; at $H=4$ it equals $3$ for $13{,}824$ points, all in two orbits.",
     "At $H=3$ there are $273{,}024$ distinct rational points of the solution varieties, at $H=4$ there are $662{,}528$, and at $H=5$ there are $1{,}916{,}672$ (each grid contains the previous one). Every one of them satisfies a nontrivial relation $\\prod z_j^{n_j}\\in\\{\\pm1,\\pm i\\}$; none is admissible; every one has a vanishing sine and two sines of equal magnitude. The exponent rank is at most $2$ at $H=3$; at $H=4$ it equals $3$ for $13{,}824$ points and at $H=5$ for $156{,}672$ points, in the same two orbits."),
    ("Every one of the $662{,}528$ points recorded at $H\\le4$ (the height-$3$ grid is contained in the height-$4$ grid, so the two sweeps are not added) is of type (i).",
     "Every one of the $1{,}916{,}672$ points recorded at $H\\le5$ (each grid contains the previous one, so the sweeps are not added) is of type (i); a direct classification of every point found no point of type (iii)."),
    ("and the evidence for the extra exclusion is only the absence of type (iii) points at $H\\le4$, where the grid carries the split primes $5$, $13$ and $17$:",
     "and the evidence for the extra exclusion is only the absence of type (iii) points at $H\\le5$, where the grid carries the split primes $5$, $13$, $17$, $29$ and $41$:"),
    ("and the two orbits that carry rank-three points at $H=4$ are among them;",
     "and the two orbits that carry rank-three points at $H=4$ and at $H=5$ are among them;"),
])
edit("paper_update/manuscript/paper.tex", [
    ("The torsion-coset hypothesis holds on all $662{,}528$ rational points of the solution varieties with three parameters of projective height at most four;",
     "The torsion-coset hypothesis holds on all $1{,}916{,}672$ rational points of the solution varieties with three parameters of projective height at most five;"),
])
edit("paper_update/CHANGES_v3.md", [
    ("all 662,528 recorded points at H ≤ 4 are of the vanishing-sine kind", "all 1,916,672 recorded points at H ≤ 5 are of the vanishing-sine kind (iteration 3 classified every point directly; 0 of type (iii))"),
    ("Torsion-coset data at H = 3 and 4 (273,024 and 662,528 points, 0 exceptions, rank-3 points at H = 4)", "Torsion-coset data at H = 3, 4 and 5 (273,024, 662,528 and 1,916,672 points, 0 exceptions, rank-3 points at H = 4 and 5 in the same two orbits)"),
])
edit("docs/RESULTS.md", [
    ("All 662,528 points recorded at height ≤ 4 (the height-3 grid is a subset, so the sweeps are not added) are of the vanishing-sine kind",
     "All 1,916,672 points recorded at height ≤ 5 (each grid contains the previous one) are of the vanishing-sine kind, by a direct classification of every point"),
    ("the evidence for the extra strength is only the absence of A = 2B points at\nheight ≤ 4, which is weak.",
     "the evidence for the extra strength is the absence of A = 2B points at\nheight ≤ 5 (split primes 5, 13, 17, 29, 41), which is early evidence."),
    ("## Infrastructure", "**Height 5 (iteration 3, planned by the planner).** 1,916,672 distinct rational solutions over all 113\norbits (40 grid values, 64,000 triples, 734 s on 6 workers; overflow handled exactly): 0 off a\ntorsion coset, 0 admissible, 0 of type (iii), every point has a vanishing sine; rank-3 points\n(156,672) occur in exactly the two orbits seen at height 4, both inside the 23 candidates\n[SEARCH-EVIDENCE, `agents/torsion_coset_probe/results/torsion_coset_H5_summary.json`].\n\n## Infrastructure"),
])
edit("docs/ONEPAGE.md", [
    ("662,528 exact solutions at height ≤ 4 (height 3 is a subset): zero exceptions.", "1,916,672 exact solutions at height ≤ 5 (each grid contains the previous): zero exceptions."),
    ("all 662,528 recorded points have a vanishing sine.", "all 1,916,672 recorded points at height ≤ 5 have a vanishing sine (0 of type A = 2B by direct classification)."),
])
edit("docs/slides.html", [
    ("<b>662,528</b> at height ≤ 4 (all 113 orbits, 48 systems)", "<b>662,528</b> at height ≤ 4 and <b>1,916,672</b> at height ≤ 5 (all 113 orbits, 48 systems)"),
    ("All 662,528 recorded points have a vanishing sine.", "All 1,916,672 recorded points at height ≤ 5 have a vanishing sine; 0 of type A = 2B."),
])
edit("README.md", [
    ("**662,528 at height ≤ 4**, all 113 orbits, 48 systems: **0 off a torsion coset**, 0 admissible.", "**662,528 at height ≤ 4** and **1,916,672 at height ≤ 5**, all 113 orbits, 48 systems: **0 off a torsion coset**, 0 admissible."),
    ("all 662,528 recorded points have a vanishing sine;", "all 1,916,672 recorded points at height ≤ 5 have a vanishing sine (0 of type A = 2B);"),
])
edit("CONTENTS.md", [
    ("Torsion-coset data at H ≤ 4 (662,528 points, 0 exceptions)", "Torsion-coset data at H ≤ 5 (1,916,672 points, 0 exceptions)"),
    ("`agents/torsion_coset_probe/results/torsion_coset_H{3,4}_summary.json`, `rank_bound_prediction.json`", "`agents/torsion_coset_probe/results/torsion_coset_H{3,4,5}_summary.json`, `rank_bound_prediction.json`"),
])
edit("HISTORY.md", [
    ("\n## Standing caveats", "| 20:50 | — | Iteration 3 height-5 probe complete: 1,916,672 points, all type (i), 0 admissible, 0 type (iii); rank-3 orbits still {0, 54} ⊂ 23 candidates | — |\n\n## Standing caveats"),
])

# ledger / status
p = ROOT / "ledger" / "attacks.json"
d = json.loads(p.read_text(encoding="utf-8"))
if not any(a["id"] == "A8" for a in d["attacks"]):
    d["attacks"].append({"id": "A8", "iteration": 3, "problem": "P7 (and P3)", "playbook": "hypothesis-probe", "agent": "torsion-coset-prober",
        "trace": "traces/09_torsion_coset_prober_H5.md", "input": {"H": 5, "orbits": 113, "systems": 48, "planned_by": "propose_next_attack(P7)"},
        "result": "1,916,672 points; type (i) 1,916,672 / (ii) 0 / (iii) 0; 0 off a torsion coset; rank-3 orbits {0,54} inside the 23 candidates; split primes 5,13,17,29,41; exact overflow handling",
        "evidence": ["agents/torsion_coset_probe/results/torsion_coset_H5_summary.json"], "tag": "SEARCH-EVIDENCE",
        "verified_by": ["self: brute-force/sympy cross-check 452/452; every type-(i) classification from exact sines"], "state_after": {"P3": "H <= 5", "P7": "H <= 5"}})
    p.write_text(json.dumps(d, indent=2), encoding="utf-8")
p = ROOT / "ledger" / "open_problems.json"
d = json.loads(p.read_text(encoding="utf-8"))
for q in d["problems"]:
    if q["id"] == "P3":
        q["state"]["iteration_3"] = "H <= 5: 1,916,672 points, 0 exceptions; rank-3 orbits still {0, 54}"
    if q["id"] == "P7":
        q["state"]["iteration_3"] = "H <= 5: all 1,916,672 points type (i); 0 type (iii); split primes 5,13,17,29,41"
        q["next"] = "H = 6 (grid primes 37, 53, 61 appear); then attempt a proof on each vanishing-sine coset by the paper's dimension reduction"
p.write_text(json.dumps(d, indent=2), encoding="utf-8")
p = ROOT / "STATUS.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["findings"]["conjecture_8_6_torsion_cosets"]["iteration_3"] = "H<=5: 1,916,672 points, 0 exceptions; every point has a vanishing sine; 0 type (iii)"
p.write_text(json.dumps(d, indent=2), encoding="utf-8")
print("H5 integrated")
