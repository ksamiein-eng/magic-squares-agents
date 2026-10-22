# Playbook: absorb results into the paper's verification tree

**Why.** A result that lives only in an agent's folder decays. The paper's own verification suite
is its single source of truth, so every accepted result becomes a *stage* of that suite, in the
suite's own format, without modifying the shipped proof records.

**Steps.**
1. Keep `paper/` byte-identical (hashes in `paper/SHA256SUMS`).
2. Register each accepted result as an overlay stage in `paper_overlay/stages.json`: name, the
   agent directory, the command, and the acceptance string the log must contain.
3. `verify_paper_plus.py` runs the paper's original 16 stages through the paper's own
   `verify_paper.task` (temporary copies) and then the overlay stages, numbering them 17, 18, …,
   and writes one report in the paper's report format.
4. Update the ledger (`ledger/open_problems.json` state, `ledger/attacks.json` entry) and run
   `tools/tag_lint.py`; the lint fails if a MACHINE-VERIFIED claim has no passing stage.
5. When the paper is revised, the overlay stages are the diff the author merges.

**Acceptance.** `verify_paper_plus.py` reports every stage passed; lint passes; `PROVENANCE.json`
regenerated.
