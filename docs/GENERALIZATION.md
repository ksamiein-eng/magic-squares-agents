# Beyond magic squares: the loop as a method for hard open problems

Magic squares of squares is instance one. Nothing in the loop depends on it except the six
tool bindings in `paper_mcp/` and the entries of `ledger/open_problems.json`. What the loop
needs from a problem, and what it validated on this instance:

| Loop component | Requirement on the problem | Validated here by |
|---|---|---|
| Convert (Paper2MCP) | a paper with a code or certificate tree to bind tools to | 14 tools bound to a 251-file verification tree; all paper stages pass |
| Ledger | open targets that can be *typed*: certificate-extension, bounded-search, hypothesis-probe, structural | six targets typed; three advanced, one re-positioned |
| Playbooks | a repeatable strategy per type with an acceptance criterion | each playbook ran twice (iterations 1 and 2) with the same code |
| Referee contract | claims that can be reproduced by a fresh agent | skeptic reran one computation per specialist; linter enforces tags mechanically |
| Absorb | a verification suite the results can be appended to | `verify_paper_plus.py`: 16 paper stages + 6 agent stages, all passing |
| Iterate | a planner that reads the ledger and emits the next command | iteration 2 ran from `propose_next_attack`; it refuted iteration 1's sharpening, and the failure became a lemma |

## What "validated" means here, and what it does not

Validated: the loop produced new, independently checked mathematics on a real open problem in
one afternoon (a theorem extended twice; an obstruction located; a structural lemma); it
caught its own mistakes (a false sharpening, an overflow guard, a database rank used as a
proof, two unfinished reports); and every claim is reproducible from one command with a
hash-backed provenance trail. Not validated: the loop has not closed a conjecture, has run on
one paper, and depends on the quality of the paper's own verification tree.

## Next instances (ordered by how directly the existing playbooks apply)

1. **The same paper, other targets.** Ledger entries P5 and P6 (ten unresolved three-parameter
   orbits; Kodaira dimension of the other 112 four-parameter surfaces) are typed "structural" and
   use the quotient playbook and the paper's own Gröbner scripts. The planner already emits them.
2. **Quadratic Chabauty on D** (ledger P2). Needs Magma or Sage with the Balakrishnan–Dogra code;
   inputs are in `results/genus5_quotient_structure.json`. A new playbook "external-CAS computation
   with certificate export" is the only missing piece.
3. **Other certificate-style papers.** Any result proved "for all N ≤ N₀ by exact computation"
   with a producer/checker pair (sums of squares representations, Erdős-type problems with
   computer-assisted ranges, exclusion certificates in Diophantine problems) is a direct
   instance of the certificate-extension playbook: point the ledger at the parameter, reuse the
   planner.
4. **Other rational-point problems.** The automorphism-quotient playbook and the sieved search
   apply unchanged to any hyperelliptic curve whose point list is conjectured complete.
5. **Other "every solution has property X" hypotheses.** The hypothesis-probe playbook needs only an
   exhaustive enumerator at bounded height and an exact decision procedure for X.

## How to run it on a new paper

1. Convert: write the tool bindings (`paper_mcp/<name>_mcp.py`), one tool per independently useful
   operation of the paper's code; test them in-process.
2. Ledger: list the open targets with their type, state, acceptance criterion and next increment.
3. Agents: copy `.claude/agents/`; only the specialist prompts' problem paragraphs change.
4. Run `/rigidity-attack next` (rename the skill), then `tools/tag_lint.py`, `verify_paper_plus.py`,
   `tools/make_provenance.py`, `tools/export_traces.py`.
