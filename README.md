# Rigidity Lab: a validated loop for AI on hard open problems in mathematics

**Instance one: magic squares of squares.** A research paper becomes an agent; a team of agents
attacks its open conjectures by fixed playbooks; a referee agent reruns and tags every claim;
accepted results are absorbed into the paper's own verification suite; a planner emits the next
iteration. Three iterations ran in 48 hours: the paper's main theorem was extended three times,
the obstruction to its central conjecture was located, a never-tested hypothesis was checked on
1.9 million exact solutions, and the loop refuted its own first sharpening and turned the failure
into a proved lemma. Nothing here solves the magic-square problem; every claim says exactly how
far it goes.

Authors: Kimia Samieinejad, Jonathan Wolinski. Built with Paper2Agent (Miao, Davis, Zhang, Pritchard, Zou, *Nature* 2026).

## The standard

[`STANDARD.md`](STANDARD.md) states, as ten checkable requirements, what this repository does so that
a reader can trust an AI-assisted result without trusting the author or the model: tagged claims
with a fixed vocabulary, producer/checker separation, a fresh referee that reruns, one-command
reproduction, the paper's own suite as the source of truth, verbatim traces with hashes, a claim
map, a history with every correction, formalization status per result, and disclosure with licences
and citation. `python tools/standard_check.py` verifies a repository against it and writes
`results/standard_check.json`; this repository passes 10/10, after the checker itself caught one
violation (a run report inside the shipped paper package had been overwritten; restored, recorded
in `HISTORY.md`). The standard is meant to be reused: the checker reads only file shapes and hashes.

## Results

| Target in the paper | Before | After | Evidence tag | Where |
|---|---|---|---|---|
| Theorem 1.1, rigidity for r = 2 | exponent sum ≤ 7 (2,064 systems) | **exponent sum ≤ 8** in iteration 1 (3,600 systems, checker PASS 133 s, SymPy cross-check 75/75) **≤ 9** in iteration 2 (5,520 systems) and **≤ 10** in iteration 3 (8,688 systems, 66 new representatives, checker PASS 1,309 s, witness prime 23 first needed; sum-10 secondary checks pending, sum-8 and sum-9 PASS) | MACHINE-VERIFIED | `agents/certificate_extender/` |
| Conjecture 7.3, eight-point list on the genus-5 curve | "needs quadratic Chabauty" | curve splits: quotients E₀ = 123.a1, E₊ = 492.b1, E₋ = 1968.j1, all rank 1 (exact non-torsion witnesses; ranks database-quoted) ⇒ rank-zero descent cannot close it; it is a quadratic-Chabauty problem on a bielliptic genus-2 curve of rank 2 | MACHINE-VERIFIED + DATABASE-QUOTED | `results/genus5_quotient_structure.json` |
| Conjecture 8.6, torsion-coset hypothesis | untested | 273,024 exact rational solutions at height ≤ 3, **662,528 at height ≤ 4** and **1,916,672 at height ≤ 5**, all 113 orbits, 48 systems: **0 off a torsion coset**, 0 admissible. Iteration 1's candidate sharpening (exponent rank ≤ 2) was refuted by iteration 2 (rank-3 points in two orbits) | SEARCH-EVIDENCE | `agents/torsion_coset_probe/` |
| Degeneracy-rank lemma (from the height-4 failure) | — | degenerate points lie on torsion cosets; rank ≤ 3, rank 3 only if A_i ± A_j ∥ A_r; criterion holds in 23/113 orbits and contains both orbits that showed rank 3; still exactly those two at height 5 | PROVED + MACHINE-VERIFIED | `agents/torsion_coset_probe/rank_bound.py` |
| Trichotomy and vanishing-sine rigidity | — | a rational solution is admissible, has a vanishing sine, or has A = 2B (proved); all 1,916,672 recorded points at height ≤ 5 have a vanishing sine (0 of type A = 2B); one conjecture, strictly stronger than 8.1, implies both 8.1 and 8.6 and names the next search | PROVED + SEARCH-EVIDENCE + CONJECTURAL | `paper_update/manuscript/rigidity.tex` |
| Empty region on the genus-5 curve | height 1,500 | **height 1,000,000** on C (500 billion pairs, 6 min), 300,000 on the genus-2 quotient | SEARCH-EVIDENCE | `agents/point_hunter/` |

Full report with every finding and its evidence: [`docs/RESULTS.md`](docs/RESULTS.md). Referee passes:
[`results/skeptic_verdict.md`](results/skeptic_verdict.md), [`results/skeptic_verdict_iteration2.md`](results/skeptic_verdict_iteration2.md).
Result families with formalization status: [`CONTENTS.md`](CONTENTS.md). Versions and every correction: [`HISTORY.md`](HISTORY.md).

## The paper

`paper/` is the paper under attack, *Rational-circle rigidity for magic squares of squares: certified
exclusions, a genus-five reduction, and surfaces of general type* (version 2, 13 October 2026), with its
251-file verification tree and 16-stage suite, byte-identical and never modified by the agents.
`paper_update/` is version 3 (22 October 2026, both authors), compiled to
[`paper_update/paper_v3.pdf`](paper_update/paper_v3.pdf), with the additions as numbered results:
Theorem 4.5 (certified exclusion through exponent sum ten), Section 8 (quotients of the genus-five curve),
and in Section 9 the torsion-coset data, the degeneracy-relations lemma, the trichotomy theorem and the
vanishing-sine rigidity conjecture. Each addition is tied to its evidence in
[`paper_update/CHANGES_v3.md`](paper_update/CHANGES_v3.md).

## The problem, in one paragraph

Write the central entry of a magic square of squares as `y²`. Each of the four lines through the
centre gives a Pythagorean triangle on hypotenuse `y`, hence a point of the rational unit circle
`T(Q)`. The magic conditions become: four sines of integer combinations of the angles have
magnitudes `{a, b, a+b, a−b}`. **Rigidity** says that for every "full-depth" integer frequency
matrix this never happens on `T(Q)^r`. The paper proves it for `r = 2` up to exponent sum 7
(2,064 exact certificates), reduces the three-parameter case D1 to whether the genus-5 curve
`Y² = h¹² + 70h¹⁰ − 1009h⁸ + 7060h⁶ − 1009h⁴ + 70h² + 1` has a rational point beyond eight known
ones (Conjecture 7.3), finds nothing in an exhaustive four-parameter sweep at projective height ≤ 4,
and proves the Hadamard solution surfaces are of general type.

## Architecture

```
 convert ──► ledger ──► attack ──► referee ──► absorb ──► iterate
 Paper2MCP   open       one agent   skeptic     new stages  planner emits
 14 tools    problems   per         reruns,     in the      the next command
 bound to    typed by   playbook,   tags every  paper's own (sum 8 → 9 → 10,
 the paper's kind,      parallel,   claim       suite;      H 3 → 4 → 5, …)
 own code    with next  exclusive              ledger +
             increment  dirs                   lint + hashes
```

| Piece | Path | Role |
|---|---|---|
| Paper → MCP | `paper_mcp/rational_circle_mcp.py` | Paper2Agent-style server: 17 tools bound to the paper's own code (verification stages, exact sines, orbits, curve search, quotient structure, four-parameter sweep, ledger board, next-attack planner, overlay stages), 5 resources, 3 prompts. `paper_mcp/test_mcp.py` exercises every tool in-process. |
| Agent team | `.claude/agents/*.md` | auditor, point-hunter, quotient-geometer, certificate-extender, torsion-prober, skeptic, scribe. |
| Orchestration | `.claude/skills/rigidity-attack/SKILL.md`, `orchestrator/run_attack.py` | One iteration of the loop inside Claude Code (`/rigidity-attack next`), or unattended through the Claude Agent SDK. |
| Open-problem ledger | `ledger/open_problems.json`, `ledger/attacks.json` | Every open target, typed (certificate-extension, bounded-search, hypothesis-probe, structural), with state, acceptance criterion, best attainable tag and next increment; every attack run with its evidence and verifier. |
| Playbooks | `playbooks/*.md` | Paper-agnostic strategies with acceptance criteria and failure modes; the ledger's type names the playbook, the playbook names the agent. |
| Referee contract | `tools/tag_lint.py` | Fails the build if any claim in the ledger, the report or this README lacks a tag, an existing evidence file, a verifier, or (for MACHINE-VERIFIED) a passing stage. |
| Absorb | `paper_overlay/stages.json`, `verify_paper_plus.py` | Accepted results become stages 17–23 of the paper's own suite, run by the paper's own runner in temporary copies. |
| Specialists' work | `agents/<name>/` | Code, result files and `REPORT*.md` of each computational specialist, per iteration. |
| Dashboard | `notebooks/rigidity_lab.py` | marimo notebook over the ledger, probe summaries, certificate checks and overlay suite (`python -m marimo edit notebooks/rigidity_lab.py`). |
| Audit trail | `traces/`, `CLAIM_MAP.md`, `PROVENANCE.json`, `SHA256SUMS`, `STATUS.json`, `HISTORY.md` | Verbatim transcripts of all eleven agent runs; claim → trace turn → re-check command → evidence → tag; hashes of every result file; every correction recorded. |
| Formalization | `lean/formalization.yaml` | Status of every result (none formalized yet) with exact candidate statements and difficulty. |

## Verification

```bash
pip install -r requirements.txt
python paper_mcp/test_mcp.py                      # all MCP tools, in-process (~10 s)
python paper/verify_paper.py --skip-four-prime    # the paper's own nine core stages (~4 min)
python verify_findings.py                         # six reproduction stages, all pass (~10 min)
python verify_paper_plus.py --overlay-only        # the seven agent-added stages (~40 min; sum 10 needs the regenerated certificate)
python tools/tag_lint.py                          # the referee contract
```

The sum-8 and sum-9 certificates are in `agents/certificate_extender/results/`. The sum-10 certificate
(174 MB) exceeds GitHub's file-size limit and is regenerated by
`agents/certificate_extender/build_degree10_certificate.py` (about 40 minutes on 5 cores); its strict
checker report is committed.

## Relation to `openai/math` (October 2026)

`openai/math` released 719 AI-generated manuscripts on 372 open problems, about 42% with Lean
formalizations, noting that unformalized results "could have issues"; three were withdrawn within a
day. The bottleneck in AI mathematics is no longer producing candidate theorems but making every
claim's status explicit and checkable. This repository adopts its conventions (result families,
history of versions, formalization catalogue) and tightens them: every claim carries a referee tag,
everything reproduces from one command, transcripts are verbatim, corrections are recorded including
the loop's own refuted sharpening, and the unformalized status of each result is stated rather than
left implicit.

## Beyond magic squares

Nothing in the loop depends on magic squares except the tool bindings and the ledger. What it needs
from a problem, what "validated" means here and does not, and the next instances are in
[`docs/GENERALIZATION.md`](docs/GENERALIZATION.md).

## Honesty

Nothing in this repository claims to solve the magic-square problem or to close a conjecture.
Bounded searches are evidence. Database ranks are quoted. Certificates count only after the
independent standard-library checker accepts them. The referee's tags are the contract.

## License and citation

Code: MIT (`LICENSE`), copyright 2026 Kimia Samieinejad and Jonathan Wolinski. Paper, proof records,
report and agent transcripts: CC BY-NC-ND 4.0, all rights reserved (`LICENSE-PAPER`). Please cite via
`CITATION.cff` or `paper_update/CITATION.bib`.

## Credits

Paper and verification tree: the authors. Paper2Agent: Miao, Davis, Zhang, Pritchard, Zou.
Elliptic-curve identifications: [LMFDB](https://www.lmfdb.org). Agents ran as Claude models inside Claude Code.
