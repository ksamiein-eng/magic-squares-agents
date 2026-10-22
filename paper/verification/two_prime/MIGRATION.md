# Version 3 to version 4

The input attachments have not been overwritten. The version-3 PDF/source and
release hashes are preserved separately; the baseline was reverified before
new calculations.

## New verified mathematics

The exact checks now exclude every necessary full-depth two-prime configuration
for exponent pairs `(5,1)`, `(4,2)`, `(3,3)`. The current central-root bound is
`k+l >= 7`. The reduced-frequency denominator obstruction is correspondingly
strengthened from a sum of at least six to a sum of at least seven.

All 672 new signed systems and the preceding 528 pass both checking
implementations. The combined catalog has 665 polynomials, of which 662 have
modular no-rational-root witnesses. No shared component other than separately
checked common powers of t is removed.

For `(5,1)` and `(3,3)`, all finite rational fibers allowed by the resultants are
`t = 0, 1, -1`. At `t = 1,-1` the proof uses equality of the first two sine
values, not a zero fourth sine. For `(4,2)`, only `t=0` remains. Both projective
boundary lines and their intersection are checked in every representative.

## Source and package changes

Section 8 adds the new proofs and complete per-representative table. The old
sum-five lower bound and gcd corollary are relabeled as intermediate results;
they are not silently rewritten. The abstract, current status, reproduction
instructions, and next-stage plan now describe version 4. The two elliptic
quotient discussion remains an algebraic identification, not a completed
rational-point computation.

New scripts: `build_degree6_certificate.py`, `verify_degree6_stdlib.py`,
`crosscheck_degree6_sympy.py`, `test_degree6_verifier.py`, `plan_sum7.py`, and
`build_manuscript_v4.py`. All are included, with exact data and logs. The
standard-library verifier does not depend on any historical script.

## Unchanged limitations

The original claimed exponent-sum-seven range still has one verification stage
remaining. None of the old three-prime rank, saturation, Chabauty, or height
claims is reinstated. No new claim of historical novelty or formal proof-assistant
certification is made.
