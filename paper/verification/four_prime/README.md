# Four-parameter rational-circle search (r = 4, squarefree full-depth configurations)

Question: does any full-depth four-row configuration in {0,±1}^4 (each coordinate nonzero in ≥3 rows — exactly the
configurations forced by Lemma 2.5 for a squarefree four-prime center) admit an admissible point of T(Q)^4?

Method (r4search.py): the 11,862 configurations form 113 orbits under signed coordinate permutations (order 384).
For each orbit representative, each choice of a "solved" coordinate j, and each triple of the other parameters
t_i = tan(chi_i/2) over all rationals of height ≤ H, every row's sine is linear in (cos chi_j, sin chi_j); each of the 48
signed systems is solved exactly (Cramer when det≠0; line∩circle with an integer square-root test when det=0) and the
unit-circle condition is tested exactly. Any admissible solution with three parameters of height ≤ H is found.
Validation: row construction vs direct sines 400/400; planted-point recovery 400/400; admissibility and singular branch unit-tested.

Results (all 113 orbits, all 4 solved coordinates, all 48 systems):
  H=3: 14 values,  2,744 triples per sweep — 0 solutions   (complete)
  H=4: 22 values, 10,648 triples          — 0 solutions   (complete)
  H=5: 38 values, 54,872 triples          — 0 solutions   (complete; ~1.19e9 system evaluations)
  H=6: in progress (resume: python3 r4search.py 6 START END; checkpoints every 10 orbits in r4_H6_progress.json)

Interpretation: contrary to the dimension heuristic (the solution set is a surface for r=4), no admissible four-parameter
rational-circle point exists at small height. This is evidence for the strong form of the rational-circle rigidity conjecture.
