# Playbook: formalize in Lean

**Applies when** a result is tagged PROVED with a short written proof, or MACHINE-VERIFIED through a checker
whose acceptance predicate is small enough to re-implement.

**Steps.**
1. Write the statement in `lean/formalization.yaml` first, with its Mathlib dependencies and difficulty.
   An entry with `status: candidate` is a promise of nothing; only `status: formalized` with a file path and
   a passing `lake build` counts.
2. For an elementary statement (real arithmetic, products on the unit circle), formalize the statement
   directly and let `norm_num`, `ring_nf`, `nlinarith` and `decide` carry the computations.
3. For a certificate theorem, formalize the *checker*: the acceptance predicate over the certificate data,
   then run it on the shipped certificate inside Lean (or via a verified extraction). Never formalize the
   producer.
4. The referee tag of a formalized result becomes FORMALIZED, a sixth tag that `tools/tag_lint.py` must
   learn to accept only when the Lean file and build log exist.

**Acceptance.** `lake build` passes on a pinned Mathlib; the formal statement is checked by a fresh agent
against the paper's informal statement (statement drift is the usual failure).

**Best tag.** FORMALIZED.

**Failure modes.** Formalizing a weaker statement than the paper's; trusting `sorry`; a certificate too large
for the kernel without a verified checker.
