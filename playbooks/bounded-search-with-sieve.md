# Playbook: bounded search with a residue sieve

**Applies when** the ledger entry is "no rational object of height ≤ B has property X" and X is an
exact arithmetic test (a square, a solution of an equation).

**Inputs.** The homogeneous form(s); the symmetries that shrink the window; known objects to
plant; a time budget.

**Steps.**
1. Measure, do not assume: for each small prime power, compute the fraction of residue pairs that
   pass. Drop moduli with pass rate near 1 (here 2, 3, 5, 7, 11 were useless for P, and the
   *reason* — P is a square modulo 2304 and a square residue at 5, 7, 11 — is a mathematical
   observation worth recording).
2. Pack the useful moduli into a few composites; AND their tables over a vectorised array per q;
   filter survivors with the remaining moduli; exact big-integer test on what is left.
3. Self-test before any run: planted known objects must survive every modulus; an always-square
   form must lose nothing; random samples must agree with direct computation.
4. Run with checkpoints; record pairs scanned, survivors per stage, exact tests, time.

**Acceptance.** Self-test passes; every reported object re-verified exactly; the bound stated as
max(|p|, q) ≤ B with the window and symmetry written out.

**Best tag.** SEARCH-EVIDENCE. A found object is PROVED (after exact re-verification) and changes
the ledger entry's type.

**Failure modes.** int64 overflow in the vectorised stage (guard it); non-primitive pairs
inflating survivor counts (gcd filter); mistaking a sieve for a proof.

**Next increment.** 10× the height costs about 10× the time at fixed sieve strength; beyond
~10⁷ the value is low for curves of genus ≥ 2 and the structural playbook should take over.
