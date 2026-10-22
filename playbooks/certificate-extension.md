# Playbook: certificate extension

**Applies when** a paper proves a statement for all parameters up to N by an exact, machine-checked
certificate produced by a *producer* and accepted by an *independent checker* (different code,
no shared import, ideally standard library only).

**Inputs.** The producer and checker scripts; the shipped certificate for N; the coverage rule
that lets smaller cases be inherited (here: column-gcd reduction); a wall-clock budget.

**Steps.**
1. Plan: enumerate all raw cases at N+1, mark the ones inherited from ≤ N by the paper's own
   reduction lemma, group the rest into orbits under the paper's symmetry group, choose
   representatives, and *assert* exact coverage (disjoint orbits, union equals the remainder).
2. Produce: run the producer on the representatives in parallel, one process per signature,
   checkpointing per case. A degenerate case (vanishing resultant, factor without a witness)
   is recorded as UNRESOLVED and never dropped.
3. Merge into the baseline certificate with a new schema version and new catalog ids.
4. Verify: adapt the independent checker only in its expectations (case list, schema, coverage
   range); run it strictly. Secondary checks (symbolic cross-check, mutation tests) run after.
5. Report the theorem exactly as strong as what the strict checker accepted.

**Acceptance.** Strict checker status PASS on the merged certificate; coverage re-derived by the
checker, not copied from the plan.

**Best tag.** MACHINE-VERIFIED. Never PROVED by this playbook alone: the checker and Python are
inside the trust boundary; say so.

**Failure modes.** Resultant degrees grow fast (here 54 → 126 → ~170); factoring dominates.
A missing witness prime below the bound is a real finding, not a bug. Do not "allow partial"
silently; a partial certificate must be labelled PARTIAL in the file and the report.

**Next increment.** N+1 with the same scripts; the plan step tells you the cost before you start.
