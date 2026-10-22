# Certificate extension to exponent sum nine (iteration 2)

Agent: certificate-extender, iteration 2. Date: 2026-10-22, 18:06-18:30 EDT
(40-minute hard budget). Machine: Windows 11, Python 3.11, SymPy 1.13.1
(producer only; the acceptance checker is standard library only). All files
are in `C:\Users\kimia\magic-squares-agents\agents\certificate_extender\`.
The paper directory was not touched. Baseline: `results/certificate_degree8.json`
(75 cases, 3,600 systems, strict PASS in iteration 1; see `REPORT.md`).

## Result in one sentence

The rational-circle exclusion of Theorem 1.1 now holds for every two-parameter
frequency matrix `A_{k,l;m,n}` with `k+l <= 9`: all 40 new representatives of
the signatures (8,1), (7,2), (6,3), (5,4) are certified, the merged
certificate `results/certificate_degree9.json` (115 cases, 5,520 signed
systems, 87 MB) passes the independent standard-library checker
`verify_degree9_stdlib.py` in **strict mode** with `status: PASS` (305.5 s),
with no missing cases, no unresolved systems and no factor without a small
witness prime.

## Method (identical to the degree-7 / degree-8 pipeline)

1. `plan_sum9.py` (from `plan_sum8.py`; `SIGNATURES = [(5,4),(6,3),(7,2),(8,1)]`,
   `INHERIT_SUM = 8`): enumerate all raw normal forms `(m,n)`, `|m|<k`, `|n|<l`
   (172 raw forms with `k+l = 9`); a form whose reduced bounds
   `k/gcd(k,|m|) + l/gcd(l,|n|)` sum to at most 8 is inherited from the
   verified sum-<=8 certificate (integer-power inheritance); the rest are
   grouped into orbits under coordinate sign changes and signed row
   permutations (`canonical_set/normal/orbit` of the checker), representatives
   are chosen greedily (smallest `|m|+|n|` first), and the script asserts that
   the orbits are disjoint and cover the remaining set exactly. Output
   `results/next_sum9_plan.json`.
2. `build_degree9_certificate.py` (from `build_degree8_certificate.py`): for
   each representative and each of the 48 signed systems build `G1, G2`, strip
   the common `t`-power, compute `Res_u(F,G)` with SymPy, factor over `Z`, and
   search a witness prime `p < 257` for every nonlinear factor; a zero
   resultant or a factor without a witness is recorded as `UNRESOLVED`, never
   dropped (none occurred). Nine resumable parts ran as parallel background
   processes (`--part 54a..54d, 63a, 63b, 72a, 72b, 81`; logs
   `results/build_degree9_*.log`, `results/part54a.out` etc.), checkpointing
   after every case. `--merge` appends the parts to the degree-8 baseline,
   assigns catalog ids `P2159...`, and writes `results/certificate_degree9.json`
   (schema `magic-squares/degree9/v7`); if any representative were absent the
   merge would record status `PARTIAL_MISSING_CASES` with the list
   (exercised during the run, see the partial runs below).
3. `verify_degree9_stdlib.py` (from `verify_degree8_stdlib.py`; diff: 40 new
   expected cases, schema `degree9/v7`, 20 signatures / 480 raw forms in the
   coverage check, arithmetic consequence `k+l >= 10`). Standard library only,
   no import of the producer, no CAS: sine numerators by sine addition, the 48
   signed row spaces, the division identities, every resultant identity by
   exact integer Sylvester determinants (Bareiss) at `D+1` points with its own
   degree bound `D`, factor products and constants, every modular witness,
   every finite rational fiber `t in {0,+-1}` and the three projective
   boundaries via the collision identity, and explicit coverage routes for all
   480 raw normal forms with `k+l <= 9`. Strict mode refuses a certificate with
   missing cases; `--allow-partial` verifies the present cases and reports
   `PARTIAL` with the list of fully certified signatures.
4. `summarize_degree9.py` collects the statistics (`results/degree9_statistics.txt`).

## Representatives (40 new; from `plan_sum9.py`, exact orbit coverage asserted)

| signature | raw forms | inherited (reduced sum <= 8) | remaining | reps | orbit representatives (m,n) |
|---|---|---|---|---|---|
| (5,4) | 63 | 31 | 32 | 16 | (1,1), (1,-1), (2,1), (2,-1), (1,3), (1,-3), (3,1), (3,-1), (2,3), (2,-3), (4,1), (4,-1), (3,3), (3,-3), (4,3), (4,-3) |
| (6,3) | 55 | 39 | 16 | 8 | (1,1), (1,-1), (1,2), (1,-2), (5,1), (5,-1), (5,2), (5,-2) |
| (7,2) | 39 | 15 | 24 | 12 | (1,1), (1,-1), (2,1), (2,-1), (3,1), (3,-1), (4,1), (4,-1), (5,1), (5,-1), (6,1), (6,-1) |
| (8,1) | 15 | 7 | 8 | 4 | (1,0), (3,0), (5,0), (7,0) |

Total: 172 raw forms, 92 inherited, 80 remaining, 40 representatives,
1,920 new signed systems. Checker route census for the 172 sum-9 raw forms:
80 `direct_certificate`, 88 `rational_circle_power_pullback`,
4 `real_angle_parallelogram` (the `m=n=0` forms). Whole census for all 480
raw forms with `k+l <= 9`: 238 direct, 222 pullback, 20 parallelogram.

## What is certified by the independent checker

`python verify_degree9_stdlib.py --output results/verification_degree9_stdlib.json`
(strict mode, no `--allow-partial`) returned `status: PASS` in 305.46 s
(started 18:21:39, finished 18:26:48).

- Fully certified signatures: (8,1) all 4 representatives; (7,2) all 12;
  (6,3) all 8; (5,4) all 16 -- **all four signatures, all 40
  representatives**, plus the 75 baseline cases re-verified in the same run
  (20 fully certified signatures in total).
- Systems checked: 5,520 (= 3,600 baseline + 1,920 new); every one passes the
  row-space, numerator, division, Sylvester, factor-product, witness, fiber
  and boundary checks.
- Exact integer Sylvester determinants: 553,392 (296,880 baseline + 256,512
  new). Degree bounds `D` for the new cases: 160 for (5,4) (16x16 Sylvester
  matrices), 144 for (6,3), 112 for (7,2), 64 for (8,1); recorded resultant
  degrees 152-158, 136-142, 108-110 and 56-62 respectively.
- Factor catalog: 3,207 polynomials, 3,204 with a modular no-root witness, 3
  linear (roots 0, 1, -1). The 40 new cases use 1,096 catalog factors, 1,048
  of which first appear at sum 9. Largest new factor degree: 156.
- Witness primes for the 1,048 new factors: p=3: 498, p=5: 319, p=7: 153,
  p=11: 55, p=13: 13, p=17: 10. Whole catalog: 3: 1406, 5: 1066, 7: 500,
  11: 172, 13: 37, 17: 18, 19: 5. The largest witness prime is still 19, so
  the paper's sentence "witness prime in {3,5,7,11,13,17,19}" remains true at
  sum 9.
- Finite fibers: only `t in {0, 1, -1}` occur (`t=0` from the removed
  `t`-power in the four (8,1) cases, 6 systems each; `t=+-1` via the linear
  factors); all certified degenerate (zero offset or equal offsets), as are
  `t = inf`, `u = inf` and both.
- Unresolved cases: **none** (no zero resultant, no factor without a witness
  prime below 257).

Supporting runs (`--allow-partial`, both `PARTIAL` as expected, all present
cases PASS): `results/verification_degree9_partial_test.json` (first 10
finished cases, 305 s, pipeline check) and
`results/verification_degree9_partial_stage2.json` (first 32 finished cases,
268 s; already certified (8,1), (7,2), (6,3) fully and 8 of the 16 (5,4)
cases while the last (5,4) parts were still building). Both are superseded by
the strict run.

## Timings

Producer (SymPy, nine parallel processes on an 8-core machine, started
18:07:27, last part finished 18:21:22; about 14 minutes wall clock; 4,454 s
summed per-case CPU time). Per-case build times: (8,1) 10.1-13.2 s;
(6,3) 26.1-147.3 s; (7,2) 37.1-124.0 s; (5,4) 87.8-431.5 s (per-system
resultant/factor timings under `system_timings`; resultants 0.2-0.5 s,
factoring the degree-152..158 resultants 1-3 s each; the spread is CPU
contention). Merge: about 20 s (87 MB output). Strict stdlib verification:
305.5 s. Whole iteration: 18:06-18:30, inside the 40-minute budget.

## Theorem statement supported (exactly what the strict checker accepted)

**Theorem (exponent sum nine).** For every pair of positive integers `k, l`
with `k + l <= 9` and every `m, n` with `|m| < k`, `|n| < l`, the frequency
matrix `A_{k,l;m,n}` with rows `(k,l), (k,-l), (m,l), (k,n)` has no admissible
rational-circle point: every point of `P^1(Q) x P^1(Q)` makes one of the four
sine magnitudes vanish or two of them coincide.

**Corollary (reduced-denominator restriction).** An admissible rational-circle
point for `A_{k,l;m,n}` requires `k/gcd(k,|m|) + l/gcd(l,|n|) >= 10`.

**Arithmetic consequence (via the paper's two-prime lemma).** A primitive magic
square of nine distinct positive integer squares whose central root is
`p^k q^l` with distinct primes `p, q` requires `k + l >= 10`.

Not claimed: anything about `k + l >= 10`, anything about three or more
primes; the proof boundary is unchanged (written normal-form / real-angle
lemmas plus exactly checked algebra; Python and the checker remain in the
software trust boundary; no proof assistant).

## What is missing

- Nothing is missing from the certificate: 40/40 representatives, 0 unresolved
  systems, strict checker PASS.
- Not done in this iteration (budget): no SymPy symbolic crosscheck
  (`crosscheck_degree8_sympy.py` analogue) and no mutation-test suite
  (`test_degree8_verifier.py` analogue) at sum 9. The claim rests on the
  standard-library checker alone, which is the paper's trust model, but
  without the secondary confirmation iteration 1 had at sum 8. The verifier
  diff from the sum-8 version is confined to constants (expected cases,
  schema, counts), so the sum-8 mutation tests cover its logic.

## Files

- `plan_sum9.py`, `results/next_sum9_plan.json`
- `build_degree9_certificate.py`, `results/degree9_part_*.json`,
  `results/build_degree9_*.log`, `results/part54a.out` ... `results/part81.out`,
  `results/certificate_degree9.json`, `results/degree9_generation_summary.json`
- `verify_degree9_stdlib.py`, `results/verification_degree9_stdlib.json`,
  `results/verify_degree9_stdlib.log` (strict run);
  `results/verification_degree9_partial_test.json`,
  `results/verification_degree9_partial_stage2.json` (partial runs, superseded)
- `summarize_degree9.py`, `results/degree9_statistics.txt`
