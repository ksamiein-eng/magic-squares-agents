# Playbook: adversarial referee

**Applies to** every claim produced by any other playbook, before it reaches a write-up.

**Steps.**
1. For each claim, find the exact computation, file or citation behind it.
2. Rerun at least one computation per producer through the paper's tools (never trust a log).
3. Tag: PROVED / MACHINE-VERIFIED / DATABASE-QUOTED / SEARCH-EVIDENCE / CONJECTURAL / UNSUPPORTED.
4. Rewrite any sentence that is stronger than its tag. Look specifically for: rank ≥ 1 reported as
   rank = 1; a bounded search reported as a proof; a certificate counted before the independent
   checker accepted it; one-way transport maps used as equivalences; a relaxed-problem statement
   conflated with the original problem; unfilled placeholders and empty sections in reports.
5. Write the verdict table first, then the three most serious issues, then "what moved".

**Acceptance.** The verdict file exists and every claim in the write-up cites a tag from it;
`tools/tag_lint.py` enforces this mechanically.

**Rule.** The referee is a fresh agent, never the producer (Paper2Agent's verifier discipline).
