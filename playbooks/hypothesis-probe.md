# Playbook: hypothesis probe

**Applies when** the paper states a structural conjecture "every solution has property X" that is
decidable exactly on each solution, and has only anecdotal evidence for it.

**Inputs.** An exhaustive enumerator of solutions at bounded height (here the paper's own sweep,
re-instrumented to record all solutions instead of only the interesting ones); an exact decision
procedure for X that is *complete*, not exponent-bounded (here: the Gaussian-prime kernel test).

**Steps.**
1. Reuse the paper's enumerator; change only what it records. Keep its three branches.
2. Implement the complete test; cross-check it against a bounded brute force on a sample, and
   re-derive each recorded solution with independent arithmetic.
3. Classify every solution (here: all-torsion / on a torsion coset / off every coset; plus the
   degeneracy that makes it uninteresting for the main conjecture).
4. Look for a *sharper* statement in the data (here: exponent rank never exceeds 2) and record it
   as a new conjecture candidate in the ledger.
5. Report the caveat on evidence strength honestly (which primes the grid can see at this height).

**Acceptance.** Zero exceptions and the cross-checks agree, or an exception re-verified by
independent exact arithmetic (which is then PROVED and the headline).

**Best tag.** SEARCH-EVIDENCE; a counterexample is PROVED.

**Next increment.** The next height, with the overflow guard re-checked; then try to prove the
sharpened statement symbolically on the identically-degenerate loci.
