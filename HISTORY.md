# History

Versioned record of what this repository claimed, when, and every correction. Earlier states remain
in git history; corrections are recorded here rather than silently overwritten (the convention of
`openai/math`'s history file, applied to a much smaller collection).

| Time (EDT, 22 Oct 2026) | Commit | What was added | Corrections recorded |
|---|---|---|---|
| 17:08 | `f2adb7b` | Paper MCP server (14 tools), agent team, `/rigidity-attack` skill, SDK runner | — |
| 17:23 | `0508ee2` | Iteration 1 results: sum-8 certificate, torsion probe H ≤ 3, point hunt to 10⁶, quotient structure; write-up, slides | — |
| 17:24 | `0508ee2` | Skeptic verdict applied | "rank = 1" and "rank Jac(D) = 2" downgraded to DATABASE-QUOTED; independence argument for rank Jac(C) ≥ 3 written; two unfinished reports (placeholders, empty section) fixed |
| 17:35 | `0b95b0c` | Audit trail: verbatim traces, claim map, status, `verify_findings.py`, provenance tooling | — |
| 17:40 | `7430a5b` | Reproduction run (6 stages pass); sum-8 SymPy cross-check (75/75) and mutation tests completed | known gap "secondary checks did not finish" closed |
| 18:19 | `26fcf44` | Paper2Attack loop: ledger, playbooks, planner tool, tag linter, overlay verifier; iteration 2 torsion probe H = 4 | **Iteration 1's candidate sharpening "exponent rank ≤ 2" refuted** (13,824 rank-3 points in orbits 0 and 54); int64 overflow guard valid at H ≤ 3 found invalid at H = 4 and replaced |
| 18:27 | `01e0985` | Iteration 2 sum-9 certificate (strict checker PASS); degeneracy-rank lemma explaining the rank-3 points; prediction (23 orbits) | — |
| 18:38 | `ae046dc` | Overlay suite with six agent stages, all passing; lint passing | tag linter refused the lemma's MACHINE-VERIFIED tag until its stage had run in a full overlay pass |
| 18:52 | `ffe9bcd` | Manuscript v3 (both authors, additions), generalisation document | — |
| 18:57 | `2851d44` | Author name corrected (Samiein → Samieinejad); trichotomy theorem and vanishing-sine rigidity conjecture | name correction |
| 19:04 | `47f5dbb` | MiKTeX installed; `paper_update/paper_v3.pdf` compiled (33 pages) | a wide display reflowed |
| 19:27 | `e4c8070` | Licenses (MIT code, CC BY-NC-ND paper), CITATION.cff | — |
| 20:17 | `a520d89` | HTML fixes: slide 7 rebuilt (two finding boxes had been lost by a failed edit), figure inlined, one-page write-up | lost slide content restored |
| 20:18 | `07adb58` | Slide 7 in two columns | — |
| 20:3x | — | Iteration 3 launched: second skeptic pass over iteration 2, type-(iii) search at H = 5, sum-10 certificate; `openai/math`-style history, contents map, formalization catalogue | (recorded below when results land) |

## Standing caveats

- Elliptic-curve ranks equal to 1 are quoted from the LMFDB, never re-proved here.
- Every height-bounded statement is evidence, not proof.
- Sum-9 secondary checks (SymPy cross-check, mutation tests) were not run at the time of the hackathon submission; sum-8's were and passed.
- No result in this repository is formalized in Lean (see `lean/formalization.yaml` for the candidates).
