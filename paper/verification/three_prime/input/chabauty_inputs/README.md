# Quadratic Chabauty inputs for the magic-square-of-squares three-prime bounded orbits

Proposition 7.3 of the paper: each rank-1 sieve curve E: y^2 = f(s) (f cubic) yields,
via the square condition s = w^2, a bielliptic genus-2 curve

        C : Y^2 = f(w^2),

whose Jacobian is isogenous to E x E' with E': y^2 = s f(s). For all eight curves here
BOTH E and E' have rank 1, so rank J(C) = 2 = genus and classical Chabauty-Coleman fails,
but the curves are exactly in the scope of QUADRATIC CHABAUTY FOR BIELLIPTIC GENUS-2 CURVES
(Balakrishnan-Dogra; Bianchi, "Quadratic Chabauty for (bi)elliptic curves...").

## Files
- chabauty_inputs.json     : per-curve data (sextic model of C, both elliptic quotients with
                             minimal models / conductors / ranks / generators, good primes).
- run_qc.sage              : Sage driver — builds C, lists small rational points, records QC inputs.
- run_qc.magma             : Magma driver (QCMod).
- chabauty_inputs_magma.m  : Magma data file (sextic coefficients).

## What a run must establish
For each C, that C(Q) consists only of the points with w in {0, infinity} and the
Weierstrass points — all of which are DEGENERATE (an area vanishes or two coincide).
Combined with the Mordell-Weil sieve residue classes in ../certs/sieves_cubic.json
(which already pin any extra point to a single nontrivial class of height > 10^10 on E_A/E2
and the d=2 twist), a successful QC run closes orbits B1, B2, C, D1, D3, E2:
  => for three distinct primes, a magic square of squares can only occur in D2, D4, F+1, F+2.

## The eight curves (quotient conductors)
- E_A: C genus 2; quotients 1968 & 123 (both rank 1); good primes [5, 7, 11, 13, 17, 19]
- E_B: C genus 2; quotients 352 & 352 (both rank 1); good primes [3, 5, 7, 13, 17, 19]
- E_C: C genus 2; quotients 352 & 352 (both rank 1); good primes [3, 5, 7, 13, 17, 19]
- E_D: C genus 2; quotients 1840 & 184 (both rank 1); good primes [3, 7, 11, 13, 17, 19]
- E_D_tw2: C genus 2; quotients 7360 & 1472 (both rank 1); good primes [3, 7, 11, 13, 17, 19]
- E_D_twm2: C genus 2; quotients 7360 & 1472 (both rank 1); good primes [3, 7, 11, 13, 17, 19]
- E_D_tw5: C genus 2; quotients 9200 & 4600 (both rank 1); good primes [3, 7, 11, 13, 17, 19]
- E_A_cubic_E2: C genus 2; quotients 1968 & 492 (both rank 1); good primes [5, 7, 11, 13, 17, 19]
