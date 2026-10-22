# Rigidity Lab: a validated loop for AI on hard open problems in mathematics

**Instance one: magic squares of squares.** A paper becomes an agent; a team attacks its open
conjectures by fixed playbooks; a referee tags every claim; accepted results are absorbed into the
paper's own verification suite; a planner emits the next iteration. Run twice today, it extended a
theorem twice, located an obstruction, refuted its own first sharpening and turned the failure into
a lemma. See [`docs/GENERALIZATION.md`](docs/GENERALIZATION.md) for what the loop needs from a problem
and the next instances.

## Updated manuscript

`paper_update/manuscript/` is version 3 of the paper (authors Kimia Samiein and Jonathan Wolinski,
22 October 2026) with the additions as new theorems, propositions and a lemma, each tied to its
evidence in [`paper_update/CHANGES_v3.md`](paper_update/CHANGES_v3.md). Compile with pdflatex or Overleaf.
The shipped `paper/` stays byte-identical.

**OSI Hackathon 2026 (physical sciences & mathematics), October 21–22.**
A Paper2Agent-style conversion of a research paper on **magic squares of squares** into an
MCP server, plus a team of specialist agents that attack the paper's open conjectures from
different angles, with an adversarial referee between the agents and the write-up.

> The 3×3 magic square of nine distinct squares is a 30-year-old open problem (the "Parker
> square" problem). The paper under attack proves that the obstruction survives when the
> Gaussian-prime arithmetic is thrown away: it only needs the *rational circle*. It then
> conjectures that this trigonometric obstruction is universal (**rational-circle rigidity**)
> and leaves several machine-checkable targets open. This repository turns the paper into an
> agent and sends agents at those targets.

## The loop (what makes this infrastructure, not a demo)

```
 convert ──► ledger ──► attack ──► referee ──► absorb ──► iterate
 Paper2MCP   open       one agent   skeptic     new stages  planner emits
 14 tools    problems   per         reruns,     in the      the next command
 bound to    typed by   playbook,   tags every  paper's own (sum 8 → 9,
 the paper's kind,      parallel,   claim       suite;      H 3 → 4, …)
 own code    with next  exclusive              ledger +
             increment  dirs                   lint + hashes
```

| Piece | Path | Role |
|---|---|---|
| Open-problem ledger | `ledger/open_problems.json`, `ledger/attacks.json` | Every open target of the paper, typed (certificate-extension, bounded-search, hypothesis-probe, structural), with state before/after, acceptance criterion, best attainable tag, and the next increment. Every attack run with its evidence and verifier. |
| Playbooks | `playbooks/*.md` | Paper-agnostic strategies: when they apply, steps, acceptance, best tag, failure modes. The ledger's type names the playbook; the playbook names the agent. |
| Planner | MCP tool `propose_next_attack(P1)` | Returns the playbook, agent, concrete command, cost and stop rule for the next increment. |
| Referee contract | `tools/tag_lint.py` | Mechanical: every claim in the ledger, the write-up and the README table must carry a tag, an existing evidence file, a verifier, and (for MACHINE-VERIFIED) a passing stage. Fails the build otherwise. |
| Absorb | `paper_overlay/stages.json`, `verify_paper_plus.py` | Accepted results become stages 17, 18, … of the paper's own verification suite, run through the paper's own runner in temporary copies. The paper stays byte-identical; the overlay is the diff the author merges. |
| Reproduce | `verify_findings.py` | One command, six stages, all pass. |
| Audit | `traces/`, `CLAIM_MAP.md`, `PROVENANCE.json`, `SHA256SUMS`, `STATUS.json` | Verbatim agent transcripts; claim → trace turn → re-check command → evidence → tag; hashes of everything. |

Iteration 1 ran the loop once (results below). Iteration 2 was started with the planner's own
commands (exponent sum 9, torsion probe at height 4) to show the loop turning again; see
"Iteration 2" in `docs/RESULTS.md` for what it reached before the submission deadline.

## What is here

| Layer | Path | What it does |
|---|---|---|
| Paper | `paper/` | The paper, its 251-file verification tree, and the 16-stage suite `verify_paper.py` (all stages pass on this machine, log in `results/verify_paper_run.log`). Never modified by agents. |
| Paper → MCP | `paper_mcp/rational_circle_mcp.py` | Paper2Agent-style server: 14 tools bound to the paper's own code, 5 resources, 3 prompts. `paper_mcp/test_mcp.py` exercises every tool in-process. |
| Agent team | `.claude/agents/*.md` | auditor, point-hunter, quotient-geometer, certificate-extender, torsion-prober, skeptic, scribe. |
| Orchestration | `.claude/skills/rigidity-attack/SKILL.md` | `/rigidity-attack all` inside Claude Code: fan-out → referee → synthesis. |
| Unattended run | `orchestrator/run_attack.py` | Same pipeline through the Claude Agent SDK (`--target all|D1|sum8|torsion|r4|audit`). |
| Specialists' work | `agents/<name>/` | Code, results JSON and `REPORT.md` produced by each computational specialist. |
| Write-up | `docs/` | One-page write-up, figure, slide script, social post. |

## The problem, in one paragraph

Write the central entry of a magic square of squares as `y²`. Each of the four lines through
the centre gives a Pythagorean triangle on hypotenuse `y`, hence a point of the rational
unit circle `T(Q)`. The magic conditions become: four sines of integer combinations of the
angles have magnitudes `{a, b, a+b, a−b}`. **Rigidity** says that for every "full-depth"
integer frequency matrix this never happens on `T(Q)^r`. The paper proves it for `r = 2`
up to exponent sum 7 (2,064 exact certificates), reduces the three-parameter case D1 to
whether the genus-5 curve `Y² = h¹² + 70h¹⁰ − 1009h⁸ + 7060h⁶ − 1009h⁴ + 70h² + 1` has a
rational point beyond eight known ones (Conjecture 7.3), finds nothing in an exhaustive
four-parameter sweep at projective height ≤ 4, and proves the Hadamard solution surfaces are
of general type. Everything else is open.

## The attack: five angles, one referee

```
                 ┌──────────── paper_mcp (Paper2Agent-style MCP server) ────────────┐
                 │ verification stages · exact sines · orbits · curve search · ...   │
                 └───────────────┬───────────────────────────────────────────────────┘
   ┌──────────┐  ┌──────────────┴┐  ┌────────────────┐  ┌────────────────────┐  ┌──────────────┐
   │ auditor  │  │ point-hunter  │  │ quotient-      │  │ certificate-       │  │ torsion-     │
   │ rerun 16 │  │ genus-5 curve │  │ geometer       │  │ extender           │  │ prober       │
   │ stages   │  │ to height H   │  │ Jac(C) splits  │  │ Thm 1.1: sum 7→8   │  │ Conj 8.6     │
   └────┬─────┘  └──────┬────────┘  └──────┬─────────┘  └─────────┬──────────┘  └──────┬───────┘
        └───────────────┴──────────────────┴──────────────────────┴────────────────────┘
                                            │  reports
                                     ┌──────┴───────┐
                                     │   skeptic    │  reruns, tags: PROVED / MACHINE-VERIFIED /
                                     │  (referee)   │  DATABASE-QUOTED / SEARCH-EVIDENCE / CONJECTURAL
                                     └──────┬───────┘
                                     ┌──────┴───────┐
                                     │    scribe    │  docs/RESULTS.md, one page, every sentence tagged
                                     └──────────────┘
```

* **auditor** reruns the paper's certificate stages through the MCP server and classifies every claim.
* **point-hunter** searches the genus-5 curve and its quotients at large height (sieved, exact).
* **quotient-geometer** found something the paper does not use: the curve has the involutions
  `h → −h` and `h → 1/h`, so its Jacobian splits off three elliptic curves. All three have a
  rational point of infinite order (exact Nagell–Lutz witnesses from the paper's own known
  points) and are the LMFDB curves 123.a1, 492.b1 and 1968.j1, each of rank 1. Consequence:
  Conjecture 7.3 cannot be closed by the paper's rank-zero descent on any elliptic quotient;
  it is a quadratic-Chabauty problem on a bielliptic genus-2 curve of rank 2.
* **certificate-extender** reruns the paper's producer/checker pair on the next exponent sum.
* **torsion-prober** tests the torsion-coset hypothesis (Conj. 8.6) on *every* exact rational
  solution of the 48 signed systems at bounded height with a complete Gaussian-prime kernel test.
* **skeptic** reruns one computation per specialist and downgrades any sentence stronger than its evidence.

## Findings (22 October 2026, one afternoon of compute)

| Target in the paper | Before | After | Evidence tag | Where |
|---|---|---|---|---|
| Theorem 1.1, rigidity for r = 2 | exponent sum ≤ 7 (2,064 systems) | **exponent sum ≤ 8** in iteration 1 (3,600 systems, checker PASS 133 s, SymPy cross-check 75/75) and **≤ 9** in iteration 2 (5,520 systems, 40 new representatives, checker PASS 305 s; secondary checks pending) | MACHINE-VERIFIED | `agents/certificate_extender/` |
| Conjecture 7.3, eight-point list on the genus-5 curve | "needs quadratic Chabauty" | curve splits: quotients E₀ = 123.a1, E₊ = 492.b1, E₋ = 1968.j1, all rank 1 (exact non-torsion witnesses; ranks database-quoted) ⇒ rank-zero descent cannot close it; it is a quadratic-Chabauty problem on a bielliptic genus-2 curve of rank 2 | MACHINE-VERIFIED + DATABASE-QUOTED | `results/genus5_quotient_structure.json` |
| Conjecture 8.6, torsion-coset hypothesis | untested | 273,024 exact rational solutions at height ≤ 3 and **662,528 at height ≤ 4**, all 113 orbits, 48 systems: **0 off a torsion coset**, 0 admissible. Iteration 1's candidate sharpening (exponent rank ≤ 2) was refuted by iteration 2 (rank-3 points in two orbits) | SEARCH-EVIDENCE | `agents/torsion_coset_probe/` |
| Degeneracy-rank lemma (from the height-4 failure) | — | degenerate points lie on torsion cosets; rank ≤ 3, rank 3 only if A_i ± A_j ∥ A_r; criterion holds in 23/113 orbits and contains both orbits that showed rank 3; prediction for height 5 | PROVED + MACHINE-VERIFIED | `agents/torsion_coset_probe/rank_bound.py` |
| Empty region on the genus-5 curve | height 1,500 | **height 1,000,000** on C (500 billion pairs, 6 min), 300,000 on the genus-2 quotient | SEARCH-EVIDENCE | `agents/point_hunter/` |

Full one-page write-up: [`docs/RESULTS.md`](docs/RESULTS.md). Referee's verdict table:
[`results/skeptic_verdict.md`](results/skeptic_verdict.md). Specialists' own reports: `agents/*/REPORT.md`.

## Audit trail (how the agents actually did it)

The same discipline as the paper's own package: nothing is asserted without a record.

| | |
|---|---|
| `traces/` | Verbatim transcripts of every agent (reasoning, prose, tool calls, truncated results): the coordinator's quotient-curve discovery including its dead ends, each specialist's design and runs, the skeptic's reruns. Index in `traces/README.md`. |
| `CLAIM_MAP.md` | Every claim → producing agent → trace turn → re-check command → evidence file → tag. |
| `STATUS.json` | What is claimed, what is not, known gaps. |
| `PROVENANCE.json`, `SHA256SUMS` | Agent runs (ids, models, spans, turn and tool counts, transcript hashes), environment, hashes of every result file. A matching hash is evidence of byte identity, not of mathematical truth. |
| `verify_findings.py` | One command re-runs every machine-checkable finding: MCP tools, the paper's nine core stages, the sum-8 checker, the point-hunter self-test and a search, the torsion probe on ten orbits, the quotient structure. Latest report: `results/verify_findings_latest.json`. |
| `results/skeptic_verdict.md` | The referee's table. |

## Run it

```bash
pip install -r requirements.txt
python paper_mcp/test_mcp.py                 # exercises all 14 tools (~10 s)
python paper/verify_paper.py --skip-four-prime   # the paper's own 9 core stages (~4 min)
```

Inside Claude Code, opened in this folder (the `.mcp.json` registers the server and the
agents/skill are picked up automatically):

```text
/rigidity-attack all        # or: D1 | sum8 | torsion | r4 | audit
```

Unattended, through the Agent SDK:

```bash
pip install claude-agent-sdk
python orchestrator/run_attack.py --target all
```

## Paper2Agent

The conversion follows [Paper2Agent](https://github.com/jmiao24/Paper2Agent)
(Miao et al., *Nature* 2026): bind every tool to existing repository code, run the bound code
before exposing it, verify with a fresh agent, deliver resources and prompts next to the
tools. `paper_mcp/rational_circle_mcp.py` is the resulting paper MCP; `.claude/agents/` is
the agent layer. The one deliberate departure: the specialists are *researchers*, not
tutorial re-executors, so the pipeline ends in a referee rather than a test runner.

## Honesty

Nothing in this repository claims to solve the magic-square problem. Bounded searches are
evidence. Database ranks are quoted. Certificates count only after the independent
standard-library checker accepts them. The referee's tags are the contract.

## Credits

Paper and verification tree: the submitting author. Paper2Agent: Miao, Davis, Zhang, Pritchard, Zou.
Elliptic-curve identifications: [LMFDB](https://www.lmfdb.org). Agents: Claude (Fable 5.1 / Sonnet) via Claude Code.
