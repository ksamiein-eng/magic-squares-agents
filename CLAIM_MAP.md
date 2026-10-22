# Claim map

Every claim this project makes, the agent that produced it, the trace that shows how, the
command that re-checks it, and the evidence tag assigned by the skeptic agent. Mirrors
`paper/editorial/CLAIM_MAP.md`. Tags: PROVED (written argument + exact computation),
MACHINE-VERIFIED (independent checker rerun here), DATABASE-QUOTED (LMFDB), SEARCH-EVIDENCE
(bounded height), CONJECTURAL.

| # | Claim | Producer | Trace (how it was done) | Re-check | Evidence file | Tag |
|---|---|---|---|---|---|---|
| F1 | The paper's 16-stage verification tree passes unchanged on this machine | coordinator | `traces/00_coordinator.md`, turn 51 (`verify_paper.py --skip-four-prime`) | `python paper/verify_paper.py --skip-four-prime` | `results/verify_paper_run.log` | MACHINE-VERIFIED |
| F2 | The paper is a working MCP server: 14 tools bound to its code, 5 resources, 3 prompts, all exercised | coordinator | `traces/00_coordinator.md`, turns 64–75 | `python paper_mcp/test_mcp.py` | `paper_mcp/test_mcp.py` output | MACHINE-VERIFIED |
| F3 | C: Y²=P(h) has involutions h→−h, h→1/h; P/h⁶ = g(h²+h⁻²); genus-2 quotient D is bielliptic with E± : v²=(w±2)g(w); E₀ : v²=g(s) | coordinator (quotient-geometer role) | `traces/00_coordinator.md`, turns 22–49: failed PARI/WSL attempt (22), sympy derivation of D, E±, E₀ (33), LMFDB lookups by j-invariant (37), failed SageMathCell attempt (40), c₄/c₆ matching bug and fix (41–45), E₀ non-torsion test (49) | `genus5_quotient_structure` tool; `verify_findings.py` stage 6 | `results/genus5_quotient_structure.json` | PROVED (identities verified in SymPy) |
| F4 | Each of E₀, E₊, E₋ has a rational point of infinite order (so rank ≥ 1) | coordinator | same turns; Nagell–Lutz on integral models: 3·(2,72) on E₀ has x = 11042/289 | `verify_findings.py` stage 6 | `results/genus5_quotient_structure.json` → `infinite_order` | PROVED |
| F5 | E₀ ≅ 123.a1, E₊ ≅ 492.b1, E₋ ≅ 1968.j1 (c₄, c₆ scaling u = 4, 8, 12); each has rank exactly 1 | coordinator + LMFDB | same turns | `verify_findings.py` stage 6 (isomorphism); LMFDB pages for rank | `results/genus5_quotient_structure.json` → `lmfdb` | isomorphism MACHINE-VERIFIED; rank DATABASE-QUOTED |
| F6 | rank Jac(C) ≥ 3; rank Jac(D) = 2 = g(D); the paper's rank-zero descent cannot prove Conjecture 7.3 and classical Chabauty on D fails | coordinator; checked by skeptic | `traces/04_skeptic.md` (independence argument: distinct j-invariants and conductors ⇒ non-isogenous ⇒ ranks add) | — | `results/skeptic_verdict.md` row 4 | ≥3 PROVED; = 2 DATABASE-QUOTED |
| F7 | Theorem 1.1 holds for k+ℓ ≤ 8: 32 new representatives, 1,536 new systems, 3,600 total; independent stdlib checker PASS | certificate-extender | `traces/01_certificate_extender.md` (plan → producer in 5 parallel parts → merge → strict check) | `python agents/certificate_extender/verify_degree8_stdlib.py`; `verify_findings.py` stage 3 | `agents/certificate_extender/results/verification_degree8_stdlib.json`, `certificate_degree8.json` | MACHINE-VERIFIED |
| F8 | The SymPy cross-check and mutation tests for the sum-8 certificate did not complete | certificate-extender; flagged by skeptic | `traces/01_certificate_extender.md` end; `traces/04_skeptic.md` issue 2 | rerun `crosscheck_degree8_sympy.py`, `test_degree8_verifier.py` | `agents/certificate_extender/results/crosscheck_degree8_sympy.log` | reported gap |
| F9 | Conjecture 8.6 holds on all 71,168 (H=2) and 273,024 (H=3) exact rational solutions of all 48 signed systems, all 113 orbits; 0 admissible; every point degenerate; exponent rank ≤ 2 | torsion-coset-prober | `traces/02_torsion_coset_prober.md` (design of the complete Gaussian-prime kernel test, cross-checks, runs) | `python agents/torsion_coset_probe/torsion_coset_probe.py 3`; `verify_findings.py` stage 5 (first ten orbits at H=2) | `agents/torsion_coset_probe/results/torsion_coset_H3_summary.json`, `REPORT.md` | SEARCH-EVIDENCE |
| F10 | No rational point on C with height ≤ 1,000,000 outside the eight known; none on D to 300,000; 12 small points on E₀, none lifting | point-hunter | `traces/03_point_hunter.md` (sieve design, moduli selection, selftest, runs) | `python agents/point_hunter/hunt.py --selftest`; `--curve C --H 300000` | `agents/point_hunter/results/search_results.json`, `e0_lift_check.json` | SEARCH-EVIDENCE |
| F11 | All of the above reviewed: four findings confirmed, two sentences downgraded, two reporting defects found and fixed | skeptic | `traces/04_skeptic.md` | — | `results/skeptic_verdict.md` | referee record |
| F12 | Conjecture 7.3 and Conjecture 8.1 are unchanged; nothing here solves the magic-square problem | — | — | — | — | CONJECTURAL |

## Not claimed

No whole-orbit closure beyond the paper's five; no rank computation of our own (ranks are LMFDB);
no Chabauty computation; no statement about k+ℓ ≥ 9 for r = 2; no statement about points of
height above the searched bounds.
