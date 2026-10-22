# Point hunter: bounded rational point search on the genus-5 curve C

Agent: `point-hunter`. Date: 2026-10-22. Code: `hunt.py` (this directory). Raw output:
`results/search_results.json` (merged), per-run files `results/search_results_*.json`,
logs `results/log_*.txt`, lift check `results/e0_lift_check.json`.

## Objects searched

Theorem 1.2 of the paper reduces the existence of an admissible rational-circle point for
configuration D1 to a rational point on

    C : Y^2 = P(h) = h^12 + 70h^10 - 1009h^8 + 7060h^6 - 1009h^4 + 70h^2 + 1

outside the eight known points K = {(0,+-1), (+-1,+-72), two points at infinity}
(Conjecture 7.3 = `conj:points`: C(Q) = K). P is even and palindromic, so C has the
involutions h -> -h and h -> 1/h with quotients

    D  : Y^2 = f(x) = x^6 + 70x^5 - 1009x^4 + 7060x^3 - 1009x^2 + 70x + 1   (x = h^2), genus 2
    E0 : v^2 = g(s) = s^3 + 70s^2 - 1012s + 6920   (s = h^2 + h^-2, v = Y/h^3), elliptic.

## Method (`hunt.py`)

Write h = p/q in lowest terms. Y is rational iff the homogeneous form
P_hom(p,q) = sum_i c_i p^{2(6-i)} q^{2i} is a perfect square. Symmetry: P_hom(p,q) =
P_hom(-p,q) = P_hom(q,p), so 0 <= p <= q suffices (height H = max(|p|,q) = q).
Same for D with the sextic form f_hom and -q <= p <= q (f is palindromic but not even).
For E0, g is not palindromic; q*g_hom(p,q) must be a square and the window is |p| <= H,
1 <= q <= H.

Residue sieve. For a modulus M the table T_M[q mod M][p mod M] records whether
form(p,q) mod M lies in the set of squares mod M (a necessary condition, so a true point
is never discarded). Moduli are chosen automatically per form: the pass rate of every
prime power (2^2..2^8, 3..3^4, 5..5^3, 7, 49, 11, 121, 13, 169, primes up to 149) is
measured, useless ones (rate > 0.95) are dropped, and the rest are greedily packed into
composite moduli of size <= 6000. For each q, the three strongest composites are ANDed
over a vectorised boolean array in p (numpy tiling); the survivors are filtered by the
remaining composites with fancy indexing; the final survivors are evaluated exactly with
Python big integers and tested with `math.isqrt`, after a gcd check. Every reported point
is re-verified exactly.

A structural observation worth recording: for C every power of 2, 3 and 5 and the primes
7 and 11 have pass rate exactly 1 (no sieving power). For 2^8 * 3^2 this follows from the
identity P = (1+h^2)^2(h^4+34h^2+1)^2 - (48h^2(1-h^2))^2, so P_hom is a square modulo
2304; for 5, 7, 11 it means every value of P_hom is a square residue, i.e. C has the
maximal number of F_l-points there. The effective moduli for C are the primes
13..149 (strongest: 31, 73, 29, 79, 43) and 49. Overall sieve pass rate for C is about
2.0e-9 per pair; in practice only the two trivial lines p = 0 and p = q (the
non-primitive multiples of the known points) survive, so almost no exact tests are needed.

`python hunt.py --selftest` (passes, 20 checks): sympy verification of P = F G with
F = h^6-13h^4+83h^2+1, G = h^6+83h^4-13h^2+1; P(h)/h^6 = g(h^2+h^-2);
(1+h^2)^2(h^4+34h^2+1)^2 - (48h^2(1-h^2))^2 = P(h); P = f(h^2); gcd(P,P') = 1;
P(1) = g(2) = 72^2; homogenisations match; residue tables agree with direct big-integer
computation on 3000 random samples per curve; the planted known points pass every sieve
modulus; on the always-square form (p^2+q^2)^2 all 8773 coprime pairs with q <= 120
survive the sieve (the sieve never discards a true point); and small end-to-end searches
recover the known points on C, D, E0.

## Bounds reached and timings

| curve | window | pairs scanned | stage-1 survivors | stage-2 survivors | exact tests | search time | tables |
|---|---|---|---|---|---|---|---|
| C  | 0 <= p <= q <= 300,000 | 45,000,450,000 | 57,693,372 | 600,050 | 49 | 36.5 s | 28.5 s |
| D  | -q <= p <= q <= 100,000 | 10,000,200,000 | 45,411,899 | 200,003 | 2 | 13.0 s | 31.7 s |
| E0 | abs(p) <= 2000, 1 <= q <= 2000 | 8,002,000 | 33,695 | 2,333 | 12 | 0.1 s | 16.5 s |

(The stage-2 survivor counts are dominated by the non-primitive pairs (0,q) and (q,q);
after the gcd filter essentially nothing remains.)
EXTENDED_RUNS_PLACEHOLDER

Earlier runs at C: H = 10,000, 20,000 and D: H = 5,000 gave the same result.
Machine: Windows 11, Python 3.11, numpy 1.26, single process per curve.

## Result

**No rational point on C with height max(|p|, q) <= C_BOUND other than the known eight.**
The only rational h with height <= C_BOUND for which P(h) is a rational square are
h = 0, 1, -1 (and h = infinity), i.e. exactly the points of K.

**D:** no rational x = p/q with |p|, q <= D_BOUND for which f(x) is a square other than
x = 0, 1 (and infinity), the images of K. In particular no new point on D with x a rational
square (which would lift to C).

**E0** (small points, |p|, q <= 2000): 12 rational points found, with v:

    s = 2 (v = 72, the image of h = +-1), -2 (96), 14 (96), -34 (288), -49 (327), 62 (672),
    -82 (96), 110 (1440), 1694 (71136), -194/9 (18336/81), 494/25 (92640/625),
    494/49 (167328/2401), plus the point at infinity.

So E0 has positive rank (an elliptic curve over Q has at most 16 torsion points, and
non-integral points such as 494/25 cannot be torsion by Nagell-Lutz). None of them except
s = 2 lifts to C: a lift needs s^2 - 4 to be a rational square and (s +- sqrt(s^2-4))/2 to
be a rational square; `results/e0_lift_check.json` records that s^2 - 4 is a square only
for s = +-2, and s = -2 gives h^2 = -1. This is consistent with the C search.

## What this does and does not prove

* It proves the finite statement: C(Q) contains no point of height <= C_BOUND outside K
  (and D(Q) none of height <= D_BOUND outside the images of K). Every computation is exact
  integer arithmetic; the sieve is only a filter and was tested not to discard true points.
* It does **not** prove Conjecture 7.3 (C(Q) = K). A bounded search is evidence, not a
  proof: a rational point of larger height is not excluded by any step here. Points on
  curves of genus 5 can have very large height, so absence up to C_BOUND is weak evidence by
  itself; the stronger evidence would be structural (C is a double cover of D, genus 2, and
  maps to E0, where a Chabauty or elliptic-curve-Chabauty argument could in principle
  decide the question). Because E0 has positive rank, no "E0(Q) is finite" shortcut
  exists; Chabauty on D (if rank J(D)(Q) <= 1) or elliptic-curve Chabauty over
  Q(sqrt(s^2-4)) are the natural next steps.
* Consequently Corollary 7.2 (exclusion of D1, B2, C, E2) remains conditional on
  Conjecture 7.3. Nothing here changes the logical status of any theorem in the paper.

## Reproduce

    python hunt.py --selftest
    python hunt.py --curve C  --H 300000 --out results/search_results_C.json
    python hunt.py --curve D  --H 100000 --out results/search_results_D.json
    python hunt.py --curve E0 --H 2000   --out results/search_results_E0.json
    python hunt.py --merge results/search_results_C.json results/search_results_D.json results/search_results_E0.json --out results/search_results.json
