# Version 2 to version 3

## Newly completed

The six representatives proposed in v2 are certified:
(4,1;1,0), (4,1;3,0), (3,2;1,1), (3,2;1,-1), (3,2;2,1), (3,2;2,-1).
They add 288 signed systems. The combined 528-system certificate retains the
five old case records and the old factor catalog prefix exactly.

The current primitive two-prime central-root bound is k+l >= 6, replacing
k+l >= 5. The central entry is (p^k q^l)^2.

All new resultants are nonzero after removing only common powers of t.
All remaining possible rational t values are 0,1,-1. In the (4,1) cases the
fourth offset vanishes at those values. In the (3,2) cases the first two
offsets have equal magnitude. Both projective boundary lines are excluded.

There are 271 distinct nonlinear factors in the combined catalog, with 141
new ones beyond v2. The no-root witness primes are 3,5,7,11,13. Acceptance
uses exact determinant/factor identities and finite-field evaluations; it
does not assume that the factors are irreducible.

The symbolic cross-check now separately verifies every finite fiber and
projective boundary, and all 40 normal forms through coordinate gcd reduction.
The standard-library checker independently uses explicit power-map routes.

Corollary 7.5 states a compact consequence for arbitrary two-prime normal forms:
k/gcd(k,abs(m)) + l/gcd(l,abs(n)) >= 6 is necessary for a nondegenerate
rational-circle solution. This is an inheritance corollary, not a general
nonexistence theorem for all two-prime central roots.

## Still not reinstated

The original paper's larger two-prime range and remaining three-prime,
genus, rank, saturation, rational-point completeness, and height claims are
outside this certification. Historical priority is not asserted.

## Next stage: not yet computed

Exponent sum six consists of (5,1), (4,2), and (3,3). Gcd-based inheritance
excludes 23 of the 55 raw normal forms. The remaining 32 form fourteen
representative classes, requiring 672 new signed systems. Only this coverage
plan, not their elimination, is supplied in v3.
