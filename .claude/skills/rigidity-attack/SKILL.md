---
name: rigidity-attack
description: Run one iteration of the Paper2Attack loop on the rational-circle rigidity paper: ledger -> fan-out by playbook -> referee -> absorb into the paper's verification suite -> propose the next iteration. Use with /rigidity-attack [target], where target is "all", "P1".."P6" (a ledger problem id), "audit" or "next".
---

# Paper2Attack loop (one iteration)

You are the coordinator. The paper's code is the `rational_circle` MCP server (`.mcp.json`); the
specialists are in `.claude/agents/`; the strategies are in `playbooks/`; the state is in `ledger/`.
Discipline (from Paper2Agent): every tool binds to the paper's own code; every result is tested
before it is reported; verifiers are fresh agents distinct from producers.

## Phase 0: ground truth
1. `mcp__rational_circle__ledger_board` → the open problems, their types, states and playbooks.
2. Launch **auditor** on the cheap paper stages; do not wait.

## Phase 1: plan
For each problem in scope call `mcp__rational_circle__propose_next_attack(problem_id)`; it returns the
playbook, the agent, the concrete command, the cost and the stop rule. With target "next", choose
the cheapest increment per problem type. With "P<k>", only that problem.

## Phase 2: fan-out (parallel, one agent per playbook)
Launch the named agents in the same message, each with: the playbook file, the command from the
planner, an exclusive directory `agents/<name>/`, a wall-clock budget, and the acceptance criterion.
Partial results are reported as partial. `paper/` is never written.

## Phase 3: referee
Launch **skeptic** (playbook `adversarial-referee.md`) on all reports; it reruns one computation per
specialist through the MCP tools and writes `results/skeptic_verdict.md` with tags.

## Phase 4: absorb
1. Add each accepted result as a stage in `paper_overlay/stages.json`; run `python verify_paper_plus.py --overlay-only`.
2. Append the attack to `ledger/attacks.json` and update the state in `ledger/open_problems.json`.
3. Run `python tools/tag_lint.py` (fails if any claim lacks a tag, evidence or passing stage), then `python tools/make_provenance.py`.
4. Export traces: `python tools/export_traces.py <jsonl> traces/<n>_<agent>.md`.

## Phase 5: synthesis and next
**scribe** updates `docs/RESULTS.md` (tags only from the verdict). Close with: which ledger entries
moved, by how much, and the planner's command for the next iteration.
