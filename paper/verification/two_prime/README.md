# Magic squares of squares: verified core, version 4

This working release certifies the two-prime normal forms through exponent sum
six. For a primitive magic square of nine distinct positive integer squares,
if its central entry is `y^2` and `y = p^k q^l` with distinct primes, then
`k + l >= 7`. The distinction between the central root and the central entry
is important.

The new signatures are `(5,1)`, `(4,2)`, and `(3,3)`. Their 14 representatives
contribute 672 new signed systems; the complete certificate also rechecks the
528 systems from version 3. This is an exact exclusion of all rational-circle
parameters in the necessary full-depth configurations, not a finite-height
search. No historical-priority claim is made.

## Verify without third-party packages

From this directory, run:

```sh
python3 verify_degree6_stdlib.py
```

A successful run prints JSON with `status: PASS`, 1,200 checked systems,
665 catalog factors (662 with modular no-rational-root witnesses), and 95
covered raw normal forms. For a report file:

```sh
python3 verify_degree6_stdlib.py --output results/my_verification.json
```

The checker is standalone. It reconstructs sine numerators by repeated sine
addition, checks all signed assignments and exact division identities, proves
resultant identities using an independently calculated degree bound and exact
integer Sylvester determinants, checks factor products and modular witnesses,
and verifies every possible finite rational fiber and both projective boundary
lines. It rejects missing or unresolved cases. It does not import a producer,
use a CAS, solve for numerical roots, or require network access.

The 59,472 determinant evaluations (40,992 new) are exact polynomial-identity
proofs: two polynomials of degree at most D that agree at D+1 distinct points
are identical. The checker rejects a purported resultant exceeding D before
testing values. It is not a random sampling argument.

## Independent symbolic check and tests

The tested symbolic environment is Python 3.13.5 with SymPy 1.14.0. Install
`requirements.txt` in a virtual environment, then run:

```sh
python3 crosscheck_degree6_sympy.py
python3 test_degree6_verifier.py
python3 check_foundation.py
```

The symbolic implementation uses Chebyshev formulas for the inputs and direct
symbolic Sylvester determinants over ZZ[t]. It does not import the producer
or the standalone checker and does not call a resultant, factorization, or
rational-root routine to accept the certificate. It also checks finite and
projective fibers and independently verifies normal-form coverage by coordinate
gcd reduction.

The negative tests reject 13 damaged certificates and an unsupported finite-fiber
claim. An extra arithmetic regression compares fraction-free determinants with
the Leibniz formula on 180 small matrices. The elementary foundation regressions
remain bounded tests in support of the written proofs, not substitutes for them.

## Regeneration

```sh
python3 build_degree6_certificate.py
python3 verify_degree6_stdlib.py
python3 crosscheck_degree6_sympy.py
```

The producer uses SymPy factorization for discovery. If a common component or a
factor without a usable witness appears, it fails rather than declaring the
branch closed. Its intermediate `degree6_build_checkpoint.json` is explicitly
partial and unverified, not a certificate. Reproduction should not assume that
an empty search result is a proof of emptiness.

## Manuscript

`verified_core.pdf` is the 21-page working manuscript. Section 8 contains the
new proofs and the updated reduced-frequency denominator obstruction:

`k/gcd(k,abs(m)) + l/gcd(l,abs(n)) >= 7`.

The old threshold of six remains labeled as a historical intermediate result.
For manuscript regeneration (requires a LaTeX installation):

```sh
python3 build_manuscript_v4.py
pdflatex -interaction=nonstopmode -halt-on-error verified_core.tex
pdflatex -interaction=nonstopmode -halt-on-error verified_core.tex
```

The source builder reads the preserved version-3 source in `provenance/` and
`section_degree6.tex`; it requires successful verification records. It does not
rerun the checkers itself.

## Proof records

- `results/certificate_degree6.json`: every numerator, signed equation, removed
  t-power, resultant, factor product, and modular witness.
- `results/verification_degree6_stdlib.json`: standalone verification report.
- `results/crosscheck_degree6_sympy.json`: separate symbolic cross-check.
- `results/degree6_factor_catalog.md`, `results/degree6_systems.csv`: readable
  polynomial and assignment records.
- `results/normal_form_coverage_sum6.json`: every covered raw normal form and its
  direct, real-angle, or explicit circle-power proof route.
- `results/baseline_preservation_v4.json`: the eleven prior representative records
  and the 274-entry prior catalog prefix agree exactly after regeneration.
- `results/degree6_release_summary.json`: consolidated results and limitations.
- `results/baseline_v3_reverification.json`: the baseline was verified before
  extending it. `INPUT_SHA256SUMS_v4` records the input attachment hashes.
- `SHA256SUMS`: release-file integrity manifest; this is not a mathematical proof.

Old certificates and checkers remain available. Old plan files and old logs
record their own release's status; they are not the current proof boundary.

## What remains unresolved

This release does not certify exponent sum seven, other three-prime orbit
closures, claimed elliptic ranks or saturation, complete rational points on the
genus-two covers, or large canonical-height bounds. No formal proof assistant
has checked the development; Python and the checker implementations remain
part of the software trust boundary.

The next proposed stage is `(6,1)`, `(5,2)`, `(4,3)`. Run:

```sh
python3 plan_sum7.py
```

This proves coverage only: 37 of 73 raw forms inherit earlier exclusions, while
36 remaining forms have 18 representatives, requiring 864 new signed systems.
No resultant for those representatives is computed by that script. Completing
that stage would yield `k + l >= 8`, not a general solution of the problem.
