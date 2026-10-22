# Certificate extension to exponent sum eight

Agent: certificate-extender. Date: 2026-10-22. Machine: Windows 11, Python 3.11,
SymPy 1.13.1 (producer and crosscheck only; the acceptance checker is standard
library only). All files are in
`C:\Users\kimia\magic-squares-agents\agents\certificate_extender\`.
The paper directory was treated as read-only; `certificate_degree7.json` and
`verify_degree7_stdlib.py` were copied in as the baseline.

## Result in one sentence

The rational-circle exclusion of Theorem 1.1 (paper Section 4) now holds for
every two-parameter frequency matrix `A_{k,l;m,n}` with `k+l <= 8`: all 32 new
representatives of the signatures (7,1), (6,2), (5,3), (4,4) are certified, the
merged certificate `results/certificate_degree8.json` (75 cases, 3,600 signed
systems) passes the independent standard-library checker with `status: PASS`,
and there are no unresolved systems and no factor without a small witness prime.

## Method (identical to the paper's degree-7 method)

1. `plan_sum8.py` (adapted from `plan_sum7.py`): for each signature `(k,l)` with
   `k+l = 8`, `k >= l`, enumerate every raw normal form `(m,n)`, `|m|<k`, `|n|<l`
   (140 raw forms in total). A form whose reduced bounds
   `k/gcd(k,|m|) + l/gcd(l,|n|) <= 7` is inherited from the verified sum-<=7
   certificate (Lemma "integer-power inheritance"). The remaining forms are
   grouped into orbits under coordinate sign changes, signed row permutations
   and (for `k = l`) the coordinate swap, using `canonical_set/normal/orbit`
   from `verify_degree7_stdlib.py`; representatives are chosen greedily
   (smallest `|m|+|n|` first) and the script asserts that the orbits are
   disjoint and cover the remaining set exactly. Output: `results/next_sum8_plan.json`.
2. `build_degree8_certificate.py` (adapted from `build_degree7_certificate.py`,
   split into resumable parts so the four signatures ran in parallel): for each
   representative and each of the 48 signed systems, build `G1, G2`, remove the
   common `t`-power, compute `Res_u(F,G)` with SymPy, factor over `Z`, and for
   every nonlinear factor search a witness prime `p < 257` with nonzero leading
   coefficient and no root mod `p`. A zero resultant or a factor without a
   witness would be recorded as `UNRESOLVED` (never papered over); none
   occurred. `--merge` appends the parts to the degree-7 baseline, assigns
   catalog ids `P1190...`, and writes `results/certificate_degree8.json`
   (schema `magic-squares/degree8/v6`, 46 MB).
3. `verify_degree8_stdlib.py` (adapted from `verify_degree7_stdlib.py`; the diff
   is small: 32 new expected cases, new schema, 16 signatures / 308 raw forms in
   the coverage check, an optional `--allow-partial` mode that downgrades the
   claim). It does not import the producer and uses no CAS: it reconstructs the
   four sine numerators by sine addition, checks the 48 signed row spaces, the
   division identities, proves every resultant identity by exact integer
   Sylvester determinants (Bareiss) at `D+1` points with its own degree bound
   `D`, checks every factor product and constant, every modular witness, every
   finite rational fiber `t in {0, +-1}` and the three projective boundaries
   via the collision identity, and re-derives the coverage of all 308 raw
   normal forms with `k+l <= 8` by explicit routes.
4. `crosscheck_degree8_sympy.py` and `test_degree8_verifier.py` are the
   degree-7 symbolic crosscheck and mutation tests adapted to degree 8
   (status in the last section).

## Representatives (32 new; from `plan_sum8.py`)

| signature | raw forms | inherited (reduced sum <= 7) | remaining | orbit representatives (m,n) |
|---|---|---|---|---|
| (4,4) | 49 | 33 | 16 | (1,1), (1,-1), (1,3), (1,-3), (3,3), (3,-3) |
| (5,3) | 45 | 13 | 32 | (1,1), (1,-1), (1,2), (1,-2), (2,1), (2,-1), (2,2), (2,-2), (3,1), (3,-1), (3,2), (3,-2), (4,1), (4,-1), (4,2), (4,-2) |
| (6,2) | 33 | 25 | 8 | (1,1), (1,-1), (5,1), (5,-1) |
| (7,1) | 13 | 1 | 12 | (1,0), (2,0), (3,0), (4,0), (5,0), (6,0) |

Total: 140 raw forms, 72 inherited, 68 remaining, 32 representatives,
1,536 new signed systems. (The `m=n=0` forms are inherited through the reduced
bounds (1,1), i.e. the real-angle parallelogram route, as in the degree-7
plan.) The checker's own route census for the 140 sum-8 raw forms:
68 `direct_certificate`, 68 `rational_circle_power_pullback`,
4 `real_angle_parallelogram`.

## What is certified by the independent checker

`python verify_degree8_stdlib.py --output results/verification_degree8_stdlib.json`
(strict mode, no `--allow-partial`) returned `status: PASS` in 132.8 s.

- Fully certified signatures: (7,1) all 6 representatives; (6,2) all 4;
  (5,3) all 16; (4,4) all 6 -- i.e. **all four signatures, all 32
  representatives**, plus the 43 baseline cases (re-verified in the same run).
- Systems checked: 3,600 (= 2,064 baseline + 1,536 new); every one passes the
  row-space, numerator, division, Sylvester, factor-product, witness, fiber and
  boundary checks.
- Exact integer Sylvester determinants evaluated: 296,880 (132,336 baseline +
  164,544 new). Degree bounds `D` for the new cases: 128 for (4,4) (16x16
  Sylvester matrices), 120 for (5,3), 96 for (6,2), 56 for (7,1); recorded
  resultant degrees are 126, 118, 94, 54 respectively.
- Factor catalog: 2,159 polynomials, 2,156 with a modular no-root witness, 3
  linear (roots 0, 1, -1). The 32 new cases use 1,001 catalog factors, 969 of
  which first appear at sum 8. Largest new factor degree: 124.
- Witness-prime statistics for the 969 new factors: p=3: 359, p=5: 361,
  p=7: 188, p=11: 49, p=13: 8, p=17: 4. Whole catalog: 3: 908, 5: 747, 7: 347,
  11: 117, 13: 24, 17: 8, 19: 5. The largest witness prime is still 19, so the
  paper's sentence "witness prime in {3,5,7,11,13,17,19}" remains true at sum 8.
- Finite fibers: only `t in {0, 1, -1}` occur, as at degree 7 (`t=0` by
  removed-power branches in the six (7,1) cases, 6 systems each; `t = +-1` via
  linear factors). All are certified degenerate (zero offset or equal offsets)
  by the checker, as are `t = inf`, `u = inf` and both.
- Unresolved cases: **none**. No zero resultant (no common nonvertical
  component) and no factor without a witness prime below 257 appeared.

Verifier output: `results/verification_degree8_stdlib.json` (also
`results/verify_degree8_stdlib.log`). Generation summary:
`results/degree8_generation_summary.json`. Statistics and per-case table:
`results/degree8_statistics.txt`.

## Timings

Producer (SymPy, five parallel processes on an 8-core machine, started 17:01,
last part finished 17:06; about 5.5 minutes wall clock, 904 s summed per-case
CPU time). Per-case build times: (7,1) 4.6-5.5 s; (6,2) 18.5-22.3 s;
(5,3) 14.1-64.2 s; (4,4) 39.3-61.6 s (per-system resultant/factor timings are
stored in each case record under `system_timings`). Resultants took about
0.1 s each; factoring the degree-118/126 resultants dominated.
Merge: seconds. Strict stdlib verification: 132.8 s. Whole task well under one
hour of wall clock.

## Theorem statement now supported

**Theorem (exponent sum eight).** For every pair of positive integers `k, l`
with `k + l <= 8` and every `m, n` with `|m| < k`, `|n| < l`, the frequency
matrix `A_{k,l;m,n}` with rows `(k,l), (k,-l), (m,l), (k,n)` has no admissible
rational-circle point: every point of `P^1(Q) x P^1(Q)` makes one of the four
sine magnitudes vanish or two of them coincide.

**Corollary (reduced-denominator restriction).** An admissible rational-circle
point for `A_{k,l;m,n}` requires `k/gcd(k,|m|) + l/gcd(l,|n|) >= 9`.

**Arithmetic consequence (via the paper's two-prime lemma).** A primitive magic
square of nine distinct positive integer squares whose central root is
`p^k q^l` with distinct primes `p, q` requires `k + l >= 9`.

Not claimed: anything about `k + l >= 9`, anything about three or more primes;
the proof boundary is unchanged (written normal-form / real-angle lemmas plus
exactly checked algebra; Python and the checker remain in the software trust
boundary; no proof assistant).

## Files

- `plan_sum8.py`, `results/next_sum8_plan.json`
- `build_degree8_certificate.py`, `results/degree8_part_*.json`,
  `results/build_degree8_*.log`, `results/certificate_degree8.json`,
  `results/degree8_generation_summary.json`
- `verify_degree8_stdlib.py`, `results/verification_degree8_stdlib.json`,
  `results/verify_degree8_stdlib.log`
- `test_degree8_verifier.py`, `crosscheck_degree8_sympy.py`,
  `summarize_degree8.py`, `results/degree8_statistics.txt`
- copies: `verify_degree7_stdlib.py`, `results/certificate_degree7.json`

## Status of the secondary checks (not needed for the claim)

Final state (both background jobs finished):

- `crosscheck_degree8_sympy.py`: **PASS** for all 75 cases / 3,600 systems
  (direct symbolic Sylvester determinants over `Z[t]`, Chebyshev numerators,
  no resultant/factor/root calls; gcd coverage of 308 forms), 814.4 s.
  Output `results/crosscheck_degree8_sympy.json`.
- `test_degree8_verifier.py`: **PASS** on the re-run
  (`results/degree8_mutation_tests.json`): all 25 outcomes rejected or
  correctly classified -- 14 inherited mutations, 9 sum-8 mutations (dropped
  (4,4)/(7,1) cases, altered (5,3) resultant, altered (6,2) numerator, flipped
  (4,4) frequency sign, system marked unresolved, certificate carrying an
  `unresolved` list, new factor stripped of its witness), the unprovable
  finite-fiber claim, and the partial-certificate regression (reported
  PARTIAL with (5,3) not certified and (4,4) certified); plus 180 Bareiss vs
  Leibniz determinant matrices. The first run (`results/test_degree8_run1.log`)
  had rejected the same 23 mutations and then failed only on a bug in my
  partial-mode test (orphaned catalog entries, which the verifier correctly
  refuses); the test was fixed to prune the catalog as `--merge` does.

Neither secondary check affects the claim above, which is established by the
completed strict run of `verify_degree8_stdlib.py` (`status: PASS`) and is
independently confirmed by the symbolic crosscheck.

**Update (21:33 UTC).** Both secondary checks have since completed: `crosscheck_degree8_sympy.py` reports PASS on all 75 cases (814 s, SymPy 1.13.1) and `test_degree8_verifier.py` reports PASS (damaged certificates rejected; 180-matrix determinant regression). Logs: `results/crosscheck_degree8_sympy.log`, `results/test_degree8.log`.

## Iteration 2 (exponent sum nine)

The same pipeline was run one level higher on 2026-10-22, 18:06-18:30 EDT:
`plan_sum9.py` (40 representatives for (5,4), (6,3), (7,2), (8,1); exact
orbit coverage asserted), `build_degree9_certificate.py` (nine parallel
parts, 1,920 new signed systems, 0 unresolved), and `verify_degree9_stdlib.py`
in strict mode: `results/certificate_degree9.json` (115 cases, 5,520
systems) returns `status: PASS` in 305.5 s, so Theorem 1.1's rational-circle
exclusion holds for all `k+l <= 9` and the two-prime central root requires
`k+l >= 10`. Details, statistics, timings and the exact statement supported
are in `REPORT_sum9.md`.
