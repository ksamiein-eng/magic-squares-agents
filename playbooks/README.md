# Attack playbooks (paper-agnostic)

A playbook is a reusable strategy an agent follows to move one entry of the open-problem
ledger. Each playbook states when it applies, its inputs, its steps, the acceptance criterion
that must hold before anything is reported, the strongest evidence tag it can ever produce,
and its known failure modes. Playbooks are what make the loop repeatable on a new paper:
the ledger names the problem type, the type names the playbook, the playbook names the agent.

| Playbook | Problem type | Best tag attainable | Used here by |
|---|---|---|---|
| [certificate-extension](certificate-extension.md) | a theorem proved by exact computer certificate up to a parameter N | MACHINE-VERIFIED | certificate-extender (N: 7 → 8 → 9) |
| [bounded-search-with-sieve](bounded-search-with-sieve.md) | "no object of height ≤ B" statements | SEARCH-EVIDENCE | point-hunter (B: 1,500 → 10⁶) |
| [automorphism-quotient-analysis](automorphism-quotient-analysis.md) | completeness of a rational-point list on a curve | PROVED (obstruction or closure) | coordinator in the quotient-geometer role |
| [hypothesis-probe](hypothesis-probe.md) | a structural "every solution has property X" conjecture | SEARCH-EVIDENCE, or PROVED by counterexample | torsion-coset-prober (H: 0 → 3 → 4) |
| [adversarial-referee](adversarial-referee.md) | every claim produced by any playbook | assigns the tag | skeptic |
| [absorb-into-verification-tree](absorb-into-verification-tree.md) | every accepted result | keeps the paper's suite the single source of truth | coordinator (`verify_paper_plus.py`) |

The loop: **convert** (Paper2MCP) → **ledger** (extract open problems with types) → **attack**
(one agent per playbook, in parallel) → **referee** (tags) → **absorb** (new stages in the paper's
own verification suite, ledger updated) → **iterate** (each playbook's `next` is a concrete command).

The requirements the loop must leave behind are in `STANDARD.md`; `tools/standard_check.py` verifies them.
