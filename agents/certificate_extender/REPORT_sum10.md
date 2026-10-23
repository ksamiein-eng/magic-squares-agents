# Certificate extension to exponent sum ten (iteration 3)

Agent: certificate-extender, iteration 3. Date: 2026-10-22, 20:29-21:38 EDT
(100-minute hard budget; at most 5 producer processes during the first 30
minutes because another agent's 6-process sweep shared the machine). Machine:
Windows 11, Python 3.11, SymPy 1.13.1 (producer and secondary crosscheck
only; the acceptance checker is standard library only). All files are in
`C:\Users\kimia\magic-squares-agents\agents\certificate_extender\`. The paper
directory was not touched. Baseline: `results/certificate_degree9.json`
(115 cases, 5,520 systems, strict PASS in iteration 2; see `REPORT_sum9.md`).

## Result in one sentence

The rational-circle exclusion of Theorem 1.1 now holds for every two-parameter
frequency matrix `A_{k,l;m,n}` with `k+l <= 10`: all 66 new representatives
of the signatures (9,1), (8,2), (7,3), (6,4), (5,5) are certified, the merged
certificate `results/certificate_degree10.json` (181 cases, 8,688 signed
systems, 174 MB) passes the independent standard-library checker
`verify_degree10_stdlib.py` in **strict mode** with `status: PASS` (1,309.3 s),
with no missing cases, no unresolved systems and no factor without a small
witness prime. One new fact for the paper text: the witness prime **23** is
needed for the first time (4 catalog factors, all in (6,4) cases), so the
sentence "witness prime in {3,5,7,11,13,17,19}" is false at sum 10 and must
read "{3,5,7,11,13,17,19,23}".

## Method (identical to the degree-7/8/9 pipeline)

1. `plan_sum10.py` (from `plan_sum9.py`; `SIGNATURES = [(5,5),(6,4),(7,3),(8,2),(9,1)]`,
   `INHERIT_SUM = 9`): enumerate all raw normal forms `(m,n)`, `|m|<k`, `|n|<l`
   (285 raw forms with `k+l = 10`); a form whose reduced bounds
   `k/gcd(k,|m|) + l/gcd(l,|n|)` sum to at most 9 is inherited from the
   verified sum-<=9 certificate (integer-power inheritance); the rest are
   grouped into orbits under coordinate sign changes and signed row
   permutations, and for the square signature (5,5) also the coordinate swap
   `(t,u) -> (u,t)` (`orbit` of the checker uses both coordinate permutations
   when `bounds[0]==bounds[1]`, exactly as it did for (4,4) at sum 8).
   Representatives are chosen greedily (smallest `|m|+|n|` first) and the
   script asserts that the orbits are disjoint and cover the remaining set
   exactly. Output `results/next_sum10_plan.json`.
2. `build_degree10_certificate.py` (from `build_degree9_certificate.py`): for
   each representative and each of the 48 signed systems build `G1, G2`, strip
   the common `t`-power, compute `Res_u(F,G)` with SymPy, factor over `Z`, and
   search a witness prime `p < 257` for every nonlinear factor; a zero
   resultant or a factor without a witness is recorded as `UNRESOLVED`, never
   dropped (none occurred). Resumable parts with a checkpoint after every case
   ran as background processes: `55a`, `55b`, `73a`, `73b` and `64` were
   started first (the heaviest signatures (5,5) and (6,4) at 20:29:48, five
   processes); once the (7,3) parts finished, the last two cases of each (5,5)
   part were handed to the extra parts `55c`, `55d` (the original processes
   were stopped after their eighth checkpoint, so every case lives in exactly
   one part; `--merge` asserts this), and `82` then `91` ran as one chain
   from 20:59:54. Logs: `results/build_degree10_*.log`, `results/part55a.out`
   ... `results/part91.out`. `--merge` appends the 9 parts to the degree-9
   baseline, assigns catalog ids `P3207...`, and writes
   `results/certificate_degree10.json` (schema `magic-squares/degree10/v8`);
   an absent representative would be recorded as `PARTIAL_MISSING_CASES`
   with the list (exercised by the early partial run below).
3. `verify_degree10_stdlib.py` (from `verify_degree9_stdlib.py`; diff: 66 new
   expected cases, schema `degree10/v8`, 25 signatures / 765 raw forms in the
   coverage check, arithmetic consequence `k+l >= 11`). Standard library only,
   no import of the producer, no CAS: sine numerators by sine addition, the 48
   signed row spaces, the division identities, every resultant identity by
   exact integer Sylvester determinants (Bareiss) at `D+1` points with its own
   degree bound `D`, factor products and constants, every modular witness,
   every finite rational fiber `t in {0,+-1}` and the three projective
   boundaries via the collision identity, and explicit coverage routes for all
   765 raw normal forms with `k+l <= 10`. Strict mode refuses a certificate
   with missing cases; `--allow-partial` verifies the present cases and
   reports `PARTIAL` with the list of fully certified signatures.
4. `summarize_degree10.py` collects the statistics (`results/degree10_statistics.txt`).

## Representatives (66 new; from `plan_sum10.py`, exact orbit coverage asserted)

| signature | raw forms | inherited (reduced sum <= 9) | remaining | reps | orbit representatives (m,n) |
|---|---|---|---|---|---|
| (5,5) | 81 | 17 | 64 | 20 | (1,1), (1,-1), (1,2), (1,-2), (1,3), (1,-3), (2,2), (2,-2), (1,4), (1,-4), (2,3), (2,-3), (2,4), (2,-4), (3,3), (3,-3), (3,4), (3,-4), (4,4), (4,-4) |
| (6,4) | 77 | 61 | 16 | 8 | (1,1), (1,-1), (1,3), (1,-3), (5,1), (5,-1), (5,3), (5,-3) |
| (7,3) | 65 | 17 | 48 | 24 | (1,1), (1,-1), (1,2), (1,-2), (2,1), (2,-1), (2,2), (2,-2), (3,1), (3,-1), (3,2), (3,-2), (4,1), (4,-1), (4,2), (4,-2), (5,1), (5,-1), (5,2), (5,-2), (6,1), (6,-1), (6,2), (6,-2) |
| (8,2) | 45 | 29 | 16 | 8 | (1,1), (1,-1), (3,1), (3,-1), (5,1), (5,-1), (7,1), (7,-1) |
| (9,1) | 17 | 5 | 12 | 6 | (1,0), (2,0), (4,0), (5,0), (7,0), (8,0) |

Total: 285 raw forms, 129 inherited, 156 remaining, 66 representatives,
3,168 new signed systems. For (5,5) the swap symmetry is what makes 20
representatives suffice for 64 remaining forms (orbits of size 4 instead of
2; e.g. (1,2) also covers (2,1)). Checker route census for the 285 sum-10 raw
forms: 156 `direct_certificate`, 124 `rational_circle_power_pullback`,
5 `real_angle_parallelogram` (the `m=n=0` forms). Whole census for all 765
raw forms with `k+l <= 10`: 394 direct, 346 pullback, 25 parallelogram.

## What is certified by the independent checker

`python verify_degree10_stdlib.py --output results/verification_degree10_stdlib.json`
(strict mode, no `--allow-partial`) returned `status: PASS` in 1,309.34 s
(started 21:07:44, finished 21:29:33; log `results/verify_degree10_stdlib.log`).

- Fully certified signatures: (9,1) all 6 representatives; (8,2) all 8;
  (7,3) all 24; (6,4) all 8; (5,5) all 20 -- **all five signatures, all 66
  representatives**, plus the 115 baseline cases re-verified in the same run
  (25 fully certified signatures in total, no missing cases).
- Systems checked: 8,688 (= 5,520 baseline + 3,168 new); every one passes the
  row-space, numerator, division, Sylvester, factor-product, witness, fiber
  and boundary checks.
- Exact integer Sylvester determinants: 1,085,136 (553,392 baseline + 531,744
  new). Degree bounds `D` for the new cases: 200 for (5,5) (20x20 Sylvester
  matrices, 9,648 determinants per case), 192 for (6,4), 168 for (7,3), 128
  for (8,2), 72 for (9,1); recorded resultant degrees 188-198, 184-190,
  160-166, 124-126 and 64-70 respectively.
- Factor catalog: 5,305 polynomials, 5,302 with a modular no-root witness, 3
  linear (roots 0, 1, -1). The 66 new cases use 2,154 catalog factors, 2,098
  of which first appear at sum 10. Largest new factor degree: 196 (83 such
  factors; the resultants of the (5,5) cases with even `n` are typically
  irreducible apart from a linear factor, which is also why those cases took
  the longest to factor).
- Witness primes for the 2,098 new factors: p=3: 996, p=5: 746, p=7: 247,
  p=11: 69, p=13: 24, p=17: 6, p=19: 6, **p=23: 4**. Whole catalog:
  3: 2402, 5: 1812, 7: 747, 11: 241, 13: 61, 17: 24, 19: 11, 23: 4. The four
  factors with witness 23 belong to (6,4) cases; 23 is the largest witness
  prime at sum 10 (the producer searched p < 257 and never needed more).
- Finite fibers: only `t in {0, 1, -1}` occur (`t=0` from the removed
  `t`-power in the six (9,1) cases, 6 systems each, and from a linear factor
  `t` in the other signatures; `t=+-1` via the linear factors); all certified
  degenerate (zero offset or equal offsets), as are `t = inf`, `u = inf` and
  both.
- Unresolved cases: **none** (no zero resultant, no factor without a witness
  prime below 257).

Supporting run (`--allow-partial`, `PARTIAL` as expected, all present cases
PASS): `results/verification_degree10_partial_test.json` (first 8 finished
cases merged at 20:32 as a pipeline check; 123 cases, 5,904 systems, 899 s
under full CPU contention; reported exactly the 20 sum-<=9 signatures as
fully certified and 58 missing cases). Superseded by the strict run.

## Timings

Producer (SymPy; 5 parallel processes until 20:54, then 4-6; the machine was
shared with another agent's 6-process sweep for the first 30 minutes): started
20:29:48, last part (`91`) finished 21:07:05, about 37 minutes wall clock;
10,276 s summed per-case CPU time. Per-case build times: (9,1) 7.4-13.3 s;
(8,2) 37.2-57.4 s; (7,3) 25.0-337.8 s; (6,4) 154.2-388.2 s; (5,5)
57.1-596.8 s. Within (5,5) and (7,3) the spread is structural rather than
contention: cases with odd `n` take about 60 s (resultants split into many
small factors), cases with even `n` take 250-600 s because SymPy has to
certify irreducibility of degree-190..196 factors (per-system factor times up
to 70.7 s for (5,5) and 80.5 s for (7,3); resultants themselves take 0.03-2.4 s).
Merge: about 35 s (174 MB output). Strict stdlib verification: 1,309.3 s
(it ran concurrently with the two sum-9 secondary checks). Whole iteration:
20:29-21:38, inside the 100-minute budget.

## Theorem statement supported (exactly what the strict checker accepted)

**Theorem (exponent sum ten).** For every pair of positive integers `k, l`
with `k + l <= 10` and every `m, n` with `|m| < k`, `|n| < l`, the frequency
matrix `A_{k,l;m,n}` with rows `(k,l), (k,-l), (m,l), (k,n)` has no admissible
rational-circle point: every point of `P^1(Q) x P^1(Q)` makes one of the four
sine magnitudes vanish or two of them coincide.

**Corollary (reduced-denominator restriction).** An admissible rational-circle
point for `A_{k,l;m,n}` requires `k/gcd(k,|m|) + l/gcd(l,|n|) >= 11`.

**Arithmetic consequence (via the paper's two-prime lemma).** A primitive magic
square of nine distinct positive integer squares whose central root is
`p^k q^l` with distinct primes `p, q` requires `k + l >= 11`.

Not claimed: anything about `k + l >= 11`, anything about three or more
primes; the proof boundary is unchanged (written normal-form / real-angle
lemmas plus exactly checked algebra; Python and the checker remain in the
software trust boundary; no proof assistant). The paper's witness-prime
sentence must be widened to include 23 if the sum-10 certificate is cited.

## Secondary checks for the sum-9 certificate (skipped in iteration 2)

Both scripts were created from the degree-8 versions and run on
`results/certificate_degree9.json` while the sum-10 producers were finishing.

- `test_degree9_verifier.py` (from `test_degree8_verifier.py`; adds 8 sum-9
  mutations: dropped (5,4) and (8,1) representatives, altered (6,3) resultant,
  altered (7,2) numerator, flipped (5,4) frequency sign, sum-9 system marked
  unresolved, a sum-9 factor (id > P2158) stripped of its witness, and the
  partial-certificate regression with `54_m4_nminus3` removed, which must
  report PARTIAL with (5,4) not certified and (8,1), (5,3) certified):
  **PASS**, 32 outcomes all rejected or correctly classified, plus 180
  Bareiss-vs-Leibniz determinant matrices. Output
  `results/degree9_mutation_tests.json`, log `results/test_degree9.log`
  (21:00-21:29 under contention).
- `crosscheck_degree9_sympy.py` (from `crosscheck_degree8_sympy.py`; 115 cases,
  gcd coverage of 480 forms; Chebyshev numerators, direct symbolic Sylvester
  determinants over `Z[t]`, no resultant/factor/root calls): **PASS** for all 115 cases / 5,520 systems (gcd coverage of 480
  forms), 2,168.1 s under contention (21:00-21:36). Output
  `results/crosscheck_degree9_sympy.json`, log `results/crosscheck_degree9_sympy.log`.
  The sum-9 claim is therefore confirmed by both secondary checks, exactly as
  the sum-8 claim was in iteration 1.

Prepared but **not run** (budget): `crosscheck_degree10_sympy.py` and
`test_degree10_verifier.py` (same construction, 181 cases / 765 forms, a (5,5)
coordinate-swap mutation added, witness-drop id > P3206). The sum-10 claim
rests on the standard-library checker alone, which is the paper's trust
model; the verifier diff from the sum-9 version is confined to constants, so
the sum-9 mutation tests cover its logic.

## What is missing

- Nothing is missing from the certificate: 66/66 representatives, 0
  unresolved systems, strict checker PASS.
- Not done: the degree-10 symbolic crosscheck and mutation suite (scripts
  exist, not run; each would take well over an hour on the 174 MB file).

## Files

- `plan_sum10.py`, `results/next_sum10_plan.json`
- `build_degree10_certificate.py`, `results/degree10_part_*.json` (9 parts),
  `results/build_degree10_*.log`, `results/part55a.out` ... `results/part91.out`,
  `results/certificate_degree10.json`, `results/degree10_generation_summary.json`
- `verify_degree10_stdlib.py`, `results/verification_degree10_stdlib.json`,
  `results/verify_degree10_stdlib.log` (strict run);
  `results/verification_degree10_partial_test.json`,
  `results/verify_degree10_partial_test.log` (partial run, superseded)
- `summarize_degree10.py`, `results/degree10_statistics.txt`
- `test_degree9_verifier.py`, `results/degree9_mutation_tests.json`, `results/test_degree9.log`
- `crosscheck_degree9_sympy.py`, `results/crosscheck_degree9_sympy.log`,
  `results/crosscheck_degree9_sympy.json`
- `crosscheck_degree10_sympy.py`, `test_degree10_verifier.py` (prepared, not run)
