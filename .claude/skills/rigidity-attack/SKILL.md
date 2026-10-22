---
name: rigidity-attack
description: Orchestrate the multi-agent attack on the rational-circle rigidity conjecture for magic squares of squares. Runs the Paper2Agent-style paper MCP server, fans out the specialist agents (auditor, point-hunter, quotient-geometer, certificate-extender, torsion-prober), then the skeptic, then the scribe. Use with /rigidity-attack [target], where target is "all", "D1", "sum8", "torsion", "r4" or "audit".
---

# Rigidity attack: orchestration

You are the coordinator. The paper's code is available as the `rational_circle` MCP server (`.mcp.json`); the specialist agents are in `.claude/agents/`. Follow Paper2Agent's discipline: every tool call binds to the paper's own code, every result is tested before it is reported, verifiers are fresh agents distinct from producers.

## Phase 0: ground truth
1. Call `mcp__rational_circle__paper_overview` and read `paper://claim-map`.
2. Launch **auditor** to rerun the cheap stages (`D1_*`, `torus_rowspace_crosscheck`, `article_identities_and_tables`) and classify the main theorems. Do not wait; continue.

## Phase 1: fan-out (parallel, one agent per angle)
Launch in the same message, each with a narrow brief and an exclusive output directory under `agents/<name>/`:
- **point-hunter**: genus-five curve to the largest height feasible; report bound, survivors, points.
- **quotient-geometer**: the Chabauty-readiness memo for C (quotients, ranks with provenance, method that could close Conjecture 7.3).
- **certificate-extender**: certify exponent sum 8 (and 9 if time) by the paper's own method; stdlib checker must accept.
- **torsion-prober**: test Conjecture 8.6 on all exact solutions at height <= 3.
If the target argument names one angle, launch only that specialist plus the auditor.

## Phase 2: adversarial review
When all specialists have reported, launch **skeptic** with the concatenated reports. It must rerun at least one computation per specialist through the MCP tools and return the verdict table.

## Phase 3: synthesis
Launch **scribe** with the verdict table and the reports; it writes `docs/RESULTS.md` (one page) with evidence tags, then the README "Findings" section.

## Invariants
- Nothing enters `docs/RESULTS.md` without a Skeptic tag.
- Never modify `paper/` (the shipped proof records); all agent work lives in `agents/` and `docs/`.
- Report partial results as partial. A specialist that ran out of time reports what was verified.
- Close with: which conjecture moved, by how much, and what the next computation is.
