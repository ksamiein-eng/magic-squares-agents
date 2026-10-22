# Current mathematical status - D1 normalization extension

This release adds exact exclusions and an exact residual equivalence; it does not claim that the remaining rational-point problems are solved.

## New in this release

The full 48-system D1 normal form has two independent rational-square constraints. Keeping the normalization constraint excludes 40 systems. Three rank-zero elliptic curves and their complete four-point groups are proved using elementary 2-isogeny descent, with no database rank premise.

Sixteen previously unresolved D1 factor entries close. Exact transfer maps close sixteen more entries in each of B2, C and E2: **64 new entries**, or **120 cumulative additions beyond the baseline audit**. Each of D1, B2, C and E2 now has **eight unresolved factor entries**, down from 24. **No new whole orbit is closed.**

D1 has a nondegenerate rational-circle solution if and only if

```text
Y^2 = h^12 + 70 h^10 - 1009 h^8 + 7060 h^6 - 1009 h^4 + 70 h^2 + 1
```

has a rational point beyond `(0,+/-1)`, `(1,+/-72)`, `(-1,+/-72)` and its two infinity points. The genus is five, the forward map and reconstruction are exact, and rational exceptions are checked. **The eight-point list is not proved complete.**

## Retained conclusions

All necessary two-prime rational-circle normal forms through exponent sum seven are excluded. Thus the central root `y=p^k q^l` of a primitive magic square requires `k+l >= 8`; the central entry is `y^2`.

Five of fifteen squarefree-three-prime whole orbits are closed: A, E1, E3=E4, F-1=F-3, F-2. The ten unresolved labels remain B1, B2, C, D1, D2, D3, D4, E2, F+1 and F+2. For whole-orbit nonexistence, six targets suffice by the verified torus maps: D1, D2, D3, D4, F+1 and F+2.

The previously checked nonlinear finiteness statements, complete auxiliary point lists, published full-basis matches, eight global rank-one elliptic height bounds and three rank-two minimum-height bounds are retained. A cited published basis is not described as a freshly executed saturation computation.

## Still unresolved

Completeness of the new eight-point genus-five list; the ten whole-orbit classifications; a completed quadratic-Chabauty calculation; the missing large rank-two sieve; all exceptional map chains needed for a uniform magic-square height theorem; larger two-prime signatures and historical priority.

## Reproduction

`python verify_release.py` runs all 24 stages, using SymPy 1.14.0 for the full suite. `python verify_d1_progress.py` runs just the three new stages. Each job uses a separate temporary copy. Assertions must remain enabled.

`python verification/d1_norm/verify_d1_stdlib.py` checks the new arithmetic and kernel certificate with the standard library alone. It is not a replacement for the historical-source and torus-transfer cross-check or the full baseline suite.
