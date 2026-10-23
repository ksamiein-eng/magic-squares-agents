# Contents map

The collection is organised by *result family*, as in `openai/math`'s manuscript map, but with
one addition per family: its evidence tag and its formalization status.

| Family | Result | Where stated | Produced by | Evidence | Verification | Tag | Lean |
|---|---|---|---|---|---|---|---|
| R1 | Theorem 1.1 holds through exponent sum 8, 9, then 10 (8,688 signed systems; witness prime 23 first needed at sum 10) | `paper_update/manuscript/paper.tex` §4.3, Thm 4.5 | certificate-extender, iterations 1–2 | `agents/certificate_extender/results/verification_degree{8,9,10}_stdlib.json` | overlay stages `two_prime_sum{8,9,10}_stdlib`; sum-8 SymPy cross-check and mutation tests | MACHINE-VERIFIED | not formalized (candidate: checker acceptance as a `decide`-style certificate; large) |
| R2 | Quotient structure of the genus-5 curve: involutions, D, E₀ = 123.a1, E₊ = 492.b1, E₋ = 1968.j1; rank ≥ 1 each; rank Jac(C) ≥ 3 | §8, Props 8.1–8.2 | coordinator (quotient-geometer role) | `results/genus5_quotient_structure.json` | overlay stage `genus5_quotient_structure` | PROVED (identities, ranks ≥ 1, ≥ 3); DATABASE-QUOTED (rank = 1) | not formalized (candidate: the four polynomial identities and the Nagell–Lutz multiples are routine in Lean/Mathlib) |
| R3 | Torsion-coset data at H ≤ 5 (1,916,672 points, 0 exceptions); degeneracy-rank lemma; parallel-triple criterion | §9.x, Prop., Lemma | torsion-coset-prober (iterations 1–2) and coordinator | `agents/torsion_coset_probe/results/torsion_coset_H{3,4,5}_summary.json`, `rank_bound_prediction.json` | overlay stages `torsion_coset_probe_H2_orbits_0_10`, `degeneracy_rank_bound` | SEARCH-EVIDENCE (data); PROVED (lemma); MACHINE-VERIFIED (criterion) | not formalized (candidate: the lemma is a short statement about products of unit-circle elements) |
| R4 | Trichotomy on a signed system; vanishing-sine rigidity conjecture | §9.x, Thm, Conj. | coordinator | `agents/torsion_coset_probe/results/torsion_coset_H4_summary.json` (`points_by_degeneracy`) | second skeptic pass (iteration 3) | PROVED (theorem); CONJECTURAL (hypothesis) | not formalized (candidate: elementary real-analysis statement, well suited to Lean) |
| R5 | No rational point on C with height ≤ 10⁶ outside the known eight; none on D to 3·10⁵ | §8, final paragraph | point-hunter | `agents/point_hunter/results/search_results.json` | overlay stage `genus5_point_hunter_selftest` | SEARCH-EVIDENCE | not applicable |

Standard: `STANDARD.md` (ten requirements) and `tools/standard_check.py` (`results/standard_check.json`).

Supporting material: `traces/` (verbatim agent transcripts, all runs), `CLAIM_MAP.md` (claim → trace turn →
re-check command), `ledger/` (open problems and attacks), `playbooks/` (strategies), `PROVENANCE.json` and
`SHA256SUMS` (hashes), `HISTORY.md` (versions and corrections), `results/skeptic_verdict*.md` (referee passes),
`paper_update/paper_v3.pdf` (the manuscript), `docs/RESULTS.md` (the full report), `docs/GENERALIZATION.md` (the method beyond this instance).
