# Rigidity Lab: a validated loop for AI on hard open problems in mathematics

**Instance one: magic squares of squares · OSI Hackathon 2026 · Kimia Samieinejad, Jonathan Wolinski · 22 October 2026**
Code and full report: https://github.com/ksamiein-eng/magic-squares-agents

**The loop.** A research paper and its 251-file proof tree become an MCP server (Paper2Agent-style, 14 tools bound to the paper's own code). An open-problem *ledger* types each target; a *playbook* per type names the agent and its acceptance criterion; specialists attack in parallel; a *skeptic* reruns one computation per specialist and tags every claim (PROVED, MACHINE-VERIFIED, DATABASE-QUOTED, SEARCH-EVIDENCE, CONJECTURAL); accepted results are *absorbed* as new stages of the paper's own verification suite without touching the paper; a *planner* emits the next iteration's commands. A linter refuses any claim without a tag, an evidence file, a verifier and a passing stage. Verbatim agent transcripts, a claim map and hash-backed provenance make every step auditable. The loop ran twice today.

**The problem.** Nine distinct squares in a 3×3 magic square is open. The paper replaces the Gaussian-prime arithmetic by rational points on the unit circle; the obstruction survives (*rational-circle rigidity*, Conj. 8.1). Proved for two parameters through exponent sum 7; the first three-parameter case is reduced to whether a genus-5 curve has only eight rational points (Conj. 7.3); a torsion-coset hypothesis (Conj. 8.6) was untested.

**What moved today**

| Target | Before | After | Tag |
|---|---|---|---|
| Theorem 1.1 (r = 2) | exponent sum ≤ 7 | **≤ 8**, then **≤ 9** (5,520 systems; independent checker PASS; sum-8 also SymPy-cross-checked) | MACHINE-VERIFIED |
| Conjecture 7.3 | "needs quadratic Chabauty" | curve has involutions h→−h, h→1/h; elliptic quotients 123.a1, 492.b1, 1968.j1 with exact infinite-order witnesses; rank Jac(C) ≥ 3 proved; rank-zero descent and classical Chabauty ruled out; it is a quadratic-Chabauty problem on a bielliptic genus-2 curve of rank 2 | PROVED / DATABASE-QUOTED |
| Conjecture 8.6 | untested | 1,916,672 exact solutions at height ≤ 5 (each grid contains the previous): zero exceptions. Iteration 1's sharpening (rank ≤ 2) refuted by iteration 2; the failure became a lemma: degenerate points lie on torsion cosets, rank ≤ 3, rank 3 only if A_i ± A_j ∥ A_r (criterion holds in 23/113 orbits, including both observed) | SEARCH-EVIDENCE / PROVED |
| New: trichotomy | — | on a signed system a rational solution is admissible, has a vanishing sine, or has A = 2B; all 1,916,672 recorded points at height ≤ 5 have a vanishing sine (0 of type A = 2B by direct classification). **Vanishing-sine rigidity** implies Conj. 8.1 and 8.6, is strictly stronger than 8.1, and names the next search (A = 2B points; their absence so far is weak evidence) | PROVED / CONJECTURAL |
| Empty region on the curve | height 1,500 | height 1,000,000 (500 billion pairs) | SEARCH-EVIDENCE |

**What it did not do.** Close a conjecture, or run on a second paper. Ranks "= 1" are database-quoted; all height bounds are evidence. The referee's table and two reporting defects it caught are in the repository.

**Why now.** `openai/math` (Oct 2026) released 719 AI manuscripts with ~42% Lean-formalized and three withdrawn within a day: candidate theorems are cheap, verified status is not. Here every claim carries a referee tag, everything reproduces from one command, all transcripts are verbatim, and the unformalized status is stated per result (`lean/formalization.yaml`) rather than left implicit.

**Why it generalises.** Nothing depends on magic squares except the tool bindings and the ledger. Any paper proved "for N ≤ N₀ by certificate", any curve with a conjecturally complete point list, and any "every solution has property X" hypothesis is a direct instance of an existing playbook. The manuscript is updated to version 3 with the new theorem, propositions, lemma and conjecture (`paper_update/paper_v3.pdf`).
