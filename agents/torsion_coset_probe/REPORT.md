# Torsion-coset probe: every rational-circle solution of every signed system, heights <= 2, 3

Specialist: torsion-coset-prober.  Code: `torsion_coset_probe.py` (adapted from `paper/verification/four_prime/r4search.py`, same 113 orbit representatives of the 11,862 full-depth configurations, same grid, same linear forms and three branches), exact kernel test via Gaussian-prime support, independent exponent-bounded brute-force cross-check.

## What was computed

For each orbit representative (113), each solved coordinate (4), each triple of the other three parameters `t_j = tan(chi_j/2)` in the projective grid of height <= H (including 0 and infinity), and each of the 48 signed systems of Lemma 3.1, EVERY exact rational solution `(cos chi_j, sin chi_j)` on the unit circle was recorded: Cramer branch (det != 0), line-circle branch (det = 0, consistent, integer square-root test), and the identically-zero branch (both relations vanish for every chi_j: a one-parameter free-angle family, recorded as a family with its three fixed parameters). Solutions were deduplicated per configuration by the 4-tuple of projective parameters (equivalently, by the point of T(Q)^4).

**Exact torsion-coset test.** With `t = p/q` in lowest terms, `z = cos chi + i sin chi = (q+ip)/(q-ip)`. For each split prime `l = a^2+b^2` dividing `p^2+q^2`, exactly one of `pi = a+bi`, `conj(pi)` divides `q+ip`, so in `Q(i)^*/{+-1,+-i}` the point is `prod_l (pi_l/conj(pi_l))^{e_l}` with `e_l = +-v_l(p^2+q^2)`; the prime 2 contributes only the unit `i` and inert primes cannot occur. Since `T(Q) = {+-1,+-i} x (free abelian group on the pi_l/conj(pi_l))`, a relation `prod_j z_j^{n_j} in {+-1,+-i}` with `n != 0` exists **iff the four exponent vectors `e(z_j)` are linearly dependent** (rank < 4). The test is complete (not bounded by the size of the exponents), and a primitive integer basis of the relation lattice is recorded for every point. Classes: `all_torsion` (rank 0: every coordinate in {+-1,+-i}), `on_torsion_coset` (0 < rank < 4), `NOT_on_torsion_coset` (rank 4: a counterexample to Conjecture 8.6). For a free-angle family the three fixed coordinates were tested: if their exponent vectors had rank 3, the family would contain rational points on no torsion coset (choose the free coordinate at a new prime) and would be a counterexample.

**Cross-checks.** (i) Every recorded point was re-derived with independent exact Gaussian-rational arithmetic (`sines_of`) and asserted to satisfy its signed system and to agree with the integer linear forms; (ii) each kernel basis vector was verified to give a product in {+-1,+-i}; (iii) on a random sample of 400 points per height, an exponent-bounded brute-force search (|n_j| <= 4, pure Gaussian-rational arithmetic, no prime factorization) and a sympy rank computation were compared with the kernel test; (iv) unit tests: `pq_of_cs` round trip on the grid, sines vs floating point at 50 random points, hand-checked supports (e.g. z(1/2) z(1/3) = i detected; four distinct primes -> rank 4 detected).

## Height H = 2

Grid: 8 projective values ['0', '-1', '1', '-2', '-1/2', '1/2', '2', 'inf']; 512 triples; 113 orbits; 21696 (orbit, solved coordinate, system) array evaluations, each over all triples; sweep runtime 88 s.

| quantity | value |
|---|---|
| distinct rational points of solution varieties found | **71168** |
| &nbsp;&nbsp; class `all_torsion` | 12928 |
| &nbsp;&nbsp; class `on_torsion_coset` | 58240 |
| &nbsp;&nbsp; class `NOT_on_torsion_coset` | 0 |
| &nbsp;&nbsp; points with 4 torsion coordinate(s) | 12928 |
| &nbsp;&nbsp; points with 3 torsion coordinate(s) | 23168 |
| &nbsp;&nbsp; points with 2 torsion coordinate(s) | 8544 |
| &nbsp;&nbsp; points with 1 torsion coordinate(s) | 20672 |
| &nbsp;&nbsp; points with 0 torsion coordinate(s) | 5856 |
| admissible points | **0** |
| degenerate: some sine zero AND two magnitudes equal | 71168 |
| degenerate: some sine zero only / equal magnitudes only / neither | 0 / 0 / 0 |
| raw hits before dedup: Cramer / line-circle | 457728 / 1549824 |
| free-angle families (distinct (solved coord, fixed triple)) | **8272** (raw identically-zero system evaluations 49632) |
| &nbsp;&nbsp; families with degeneracy `row_identically_zero` | 8272 |
| &nbsp;&nbsp; families whose fixed triple has exponent rank 0 | 5792 |
| &nbsp;&nbsp; families whose fixed triple has exponent rank 1 | 2480 |
| counterexample candidates (points of rank 4, or families with independent fixed triple) | **0 / 0** |
| brute-force / sympy cross-check | 400 points checked, 400 agree, 0 disagree |

Points with NO torsion coordinate: 5856; their exponent ranks: {1: 5856} (rank 4 would be a counterexample). Maximal projective height of any coordinate among recorded points: 11 (the solved coordinate is unconstrained in height).
Most frequent relation lattices (primitive kernel bases) among those points: `[[-1, 0, 1, 0], [-1, 1, 0, 0], [1, 0, 0, 1]]` x512; `[[-1, 0, 0, 1], [-1, 1, 0, 0], [1, 0, 1, 0]]` x448; `[[-1, 0, 0, 2], [-1, 0, 2, 0], [-1, 2, 0, 0]]` x384; `[[-2, 0, 1, 0], [-1, 0, 0, 1], [1, 1, 0, 0]]` x384; `[[-1, 1, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0]]` x352; `[[-1, 0, 0, 1], [-1, 0, 1, 0], [-1, 1, 0, 0]]` x352.

### Example points (no torsion coordinate)

- orbit 17, rows `[[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 0, 0]]`, system (i,j,k,l,e2,e3) = `[0, 1, 2, 3, -1, 1]`, branch ['cramer'], found 6 times:  
  `t = ['11/2', '-2', '-2', '-1/2']`, `z = ['-117/125+(44/125)i', '-3/5+(-4/5)i', '-3/5+(-4/5)i', '3/5+(-4/5)i']`,  
  sines `['-24/25', '24/25', '0', '-24/25']` (zero rows [2], equal-magnitude pairs [[0, 1], [0, 3], [1, 3]]),  
  Gaussian-prime exponents `[{'5': 3}, {'5': 1}, {'5': 1}, {'5': -1}]`, rank 1, relation basis `[[-1, 3, 0, 0], [-1, 0, 3, 0], [1, 0, 0, 3]]` (each n gives prod z_j^(n_j) in {+-1,+-i}; verified exactly).
- orbit 21, rows `[[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, 1]]`, system (i,j,k,l,e2,e3) = `[0, 1, 2, 3, -1, -1]`, branch ['cramer'], found 6 times:  
  `t = ['11/2', '-2', '-2', '2']`, `z = ['-117/125+(44/125)i', '-3/5+(-4/5)i', '-3/5+(-4/5)i', '-3/5+(4/5)i']`,  
  sines `['24/25', '-24/25', '0', '-24/25']` (zero rows [2], equal-magnitude pairs [[0, 1], [0, 3], [1, 3]]),  
  Gaussian-prime exponents `[{'5': 3}, {'5': 1}, {'5': 1}, {'5': -1}]`, rank 1, relation basis `[[-1, 3, 0, 0], [-1, 0, 3, 0], [1, 0, 0, 3]]` (each n gives prod z_j^(n_j) in {+-1,+-i}; verified exactly).
- orbit 24, rows `[[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, 1, -1, 1]]`, system (i,j,k,l,e2,e3) = `[0, 1, 2, 3, -1, -1]`, branch ['cramer'], found 6 times:  
  `t = ['11/2', '-2', '1/2', '-1/2']`, `z = ['-117/125+(44/125)i', '-3/5+(-4/5)i', '3/5+(4/5)i', '3/5+(-4/5)i']`,  
  sines `['24/25', '-24/25', '0', '-24/25']` (zero rows [2], equal-magnitude pairs [[0, 1], [0, 3], [1, 3]]),  
  Gaussian-prime exponents `[{'5': 3}, {'5': 1}, {'5': 1}, {'5': -1}]`, rank 1, relation basis `[[-1, 3, 0, 0], [-1, 0, 3, 0], [1, 0, 0, 3]]` (each n gives prod z_j^(n_j) in {+-1,+-i}; verified exactly).
- orbit 35, rows `[[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1, 1]]`, system (i,j,k,l,e2,e3) = `[0, 1, 2, 3, -1, -1]`, branch ['singular'], found 6 times:  
  `t = ['-2', '2', '-11/2', '-2']`, `z = ['-3/5+(-4/5)i', '-3/5+(4/5)i', '-117/125+(-44/125)i', '-3/5+(-4/5)i']`,  
  sines `['-336/625', '336/625', '0', '336/625']` (zero rows [2], equal-magnitude pairs [[0, 1], [0, 3], [1, 3]]),  
  Gaussian-prime exponents `[{'5': 1}, {'5': -1}, {'5': -3}, {'5': 1}]`, rank 1, relation basis `[[1, 1, 0, 0], [3, 0, 1, 0], [-1, 0, 0, 1]]` (each n gives prod z_j^(n_j) in {+-1,+-i}; verified exactly).

## Height H = 3

Grid: 16 projective values ['0', '-1', '1', '-2', '-1/2', '1/2', '2', '-3', '-1/3', '1/3', '3', '-3/2', '-2/3', '2/3', '3/2', 'inf']; 4096 triples; 113 orbits; 21696 (orbit, solved coordinate, system) array evaluations, each over all triples; sweep runtime 254 s.

| quantity | value |
|---|---|
| distinct rational points of solution varieties found | **273024** |
| &nbsp;&nbsp; class `all_torsion` | 12928 |
| &nbsp;&nbsp; class `on_torsion_coset` | 260096 |
| &nbsp;&nbsp; class `NOT_on_torsion_coset` | 0 |
| &nbsp;&nbsp; points with 4 torsion coordinate(s) | 12928 |
| &nbsp;&nbsp; points with 3 torsion coordinate(s) | 69504 |
| &nbsp;&nbsp; points with 2 torsion coordinate(s) | 36960 |
| &nbsp;&nbsp; points with 1 torsion coordinate(s) | 99392 |
| &nbsp;&nbsp; points with 0 torsion coordinate(s) | 54240 |
| admissible points | **0** |
| degenerate: some sine zero AND two magnitudes equal | 273024 |
| degenerate: some sine zero only / equal magnitudes only / neither | 0 / 0 / 0 |
| raw hits before dedup: Cramer / line-circle | 1935744 / 3591936 |
| free-angle families (distinct (solved coord, fixed triple)) | **15152** (raw identically-zero system evaluations 90912) |
| &nbsp;&nbsp; families with degeneracy `row_identically_zero` | 15152 |
| &nbsp;&nbsp; families whose fixed triple has exponent rank 0 | 5792 |
| &nbsp;&nbsp; families whose fixed triple has exponent rank 1 | 8464 |
| &nbsp;&nbsp; families whose fixed triple has exponent rank 2 | 896 |
| counterexample candidates (points of rank 4, or families with independent fixed triple) | **0 / 0** |
| brute-force / sympy cross-check | 400 points checked, 400 agree, 0 disagree |

Points with NO torsion coordinate: 54240; their exponent ranks: {1: 32864, 2: 21376} (rank 4 would be a counterexample). Maximal projective height of any coordinate among recorded points: 46 (the solved coordinate is unconstrained in height).
Most frequent relation lattices (primitive kernel bases) among those points: `[[-1, 1, 0, 1], [-1, 1, 1, 0]]` x3584; `[[-1, 0, 0, 2], [-1, 0, 2, 0], [-1, 2, 0, 0]]` x2176; `[[-1, 0, 1, 0], [-1, 1, 0, 0], [1, 0, 0, 1]]` x2176; `[[-2, 0, 1, 0], [-1, 0, 0, 1], [1, 1, 0, 0]]` x2048; `[[-1, 0, 0, 1], [-1, 1, 0, 0], [1, 0, 1, 0]]` x1920; `[[-1, 1, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0]]` x1760.

### Example points (no torsion coordinate)

- orbit 17, rows `[[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 0, 0]]`, system (i,j,k,l,e2,e3) = `[0, 1, 2, 3, -1, 1]`, branch ['cramer'], found 6 times:  
  `t = ['41/3', '-3', '-3/2', '-2/3']`, `z = ['-836/845+(123/845)i', '-4/5+(-3/5)i', '-5/13+(-12/13)i', '5/13+(-12/13)i']`,  
  sines `['-120/169', '120/169', '0', '-120/169']` (zero rows [2], equal-magnitude pairs [[0, 1], [0, 3], [1, 3]]),  
  Gaussian-prime exponents `[{'5': -1, '13': 2}, {'5': -1}, {'13': 1}, {'13': -1}]`, rank 2, relation basis `[[-1, 1, 2, 0], [1, -1, 0, 2]]` (each n gives prod z_j^(n_j) in {+-1,+-i}; verified exactly).
- orbit 21, rows `[[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, 1]]`, system (i,j,k,l,e2,e3) = `[0, 1, 2, 3, -1, -1]`, branch ['cramer'], found 6 times:  
  `t = ['41/3', '-3', '-3/2', '3/2']`, `z = ['-836/845+(123/845)i', '-4/5+(-3/5)i', '-5/13+(-12/13)i', '-5/13+(12/13)i']`,  
  sines `['120/169', '-120/169', '0', '-120/169']` (zero rows [2], equal-magnitude pairs [[0, 1], [0, 3], [1, 3]]),  
  Gaussian-prime exponents `[{'5': -1, '13': 2}, {'5': -1}, {'13': 1}, {'13': -1}]`, rank 2, relation basis `[[-1, 1, 2, 0], [1, -1, 0, 2]]` (each n gives prod z_j^(n_j) in {+-1,+-i}; verified exactly).
- orbit 42, rows `[[0, 0, 1, -1], [1, -1, -1, -1], [1, 1, -1, 1], [1, 1, 1, -1]]`, system (i,j,k,l,e2,e3) = `[0, 2, 1, 3, -1, 1]`, branch ['singular'], found 6 times:  
  `t = ['-3/2', '3/2', '41/3', '-1/3']`, `z = ['-5/13+(-12/13)i', '-5/13+(12/13)i', '-836/845+(123/845)i', '4/5+(-3/5)i']`,  
  sines `['-2016/4225', '0', '2016/4225', '-2016/4225']` (zero rows [1], equal-magnitude pairs [[0, 2], [0, 3], [2, 3]]),  
  Gaussian-prime exponents `[{'13': 1}, {'13': -1}, {'5': -1, '13': 2}, {'5': 1}]`, rank 2, relation basis `[[1, 1, 0, 0], [-2, 0, 1, 1]]` (each n gives prod z_j^(n_j) in {+-1,+-i}; verified exactly).
- orbit 55, rows `[[0, 0, 1, -1], [1, -1, -1, 1], [1, -1, 1, -1], [1, 1, -1, 1]]`, system (i,j,k,l,e2,e3) = `[0, 1, 2, 3, -1, -1]`, branch ['singular'], found 6 times:  
  `t = ['-3/2', '2/3', '41/3', '-3']`, `z = ['-5/13+(-12/13)i', '5/13+(12/13)i', '-836/845+(123/845)i', '-4/5+(-3/5)i']`,  
  sines `['-120/169', '-120/169', '120/169', '0']` (zero rows [3], equal-magnitude pairs [[0, 1], [0, 2], [1, 2]]),  
  Gaussian-prime exponents `[{'13': 1}, {'13': 1}, {'5': -1, '13': 2}, {'5': -1}]`, rank 2, relation basis `[[-1, 1, 0, 0], [2, 0, -1, 1]]` (each n gives prod z_j^(n_j) in {+-1,+-i}; verified exactly).

## Verdict

- **H = 2: Conjecture 8.6 (torsion-coset hypothesis) is CONFIRMED on every rational point found.** All 71168 distinct rational points of the solution varieties (all 113 orbits, all 48 signed systems, three parameters of height <= 2, fourth parameter arbitrary) satisfy a nontrivial relation prod z_j^(n_j) in {+-1,+-i}, by the complete exponent-rank test; 0 points are off every torsion coset. All 8272 free-angle families have a fixed triple of exponent rank <= 1 (always containing a torsion value), so every point of every family lies on a torsion coset as well. Every point is degenerate: some sine vanishes and two magnitudes coincide (71168 of 71168); every family has a row whose sine vanishes identically; 0 admissible points (consistent with Proposition 7.1 / r4search).
- **H = 3: Conjecture 8.6 (torsion-coset hypothesis) is CONFIRMED on every rational point found.** All 273024 distinct rational points of the solution varieties (all 113 orbits, all 48 signed systems, three parameters of height <= 3, fourth parameter arbitrary) satisfy a nontrivial relation prod z_j^(n_j) in {+-1,+-i}, by the complete exponent-rank test; 0 points are off every torsion coset. All 15152 free-angle families have a fixed triple of exponent rank <= 2 (always containing a torsion value), so every point of every family lies on a torsion coset as well. Every point is degenerate: some sine vanishes and two magnitudes coincide (273024 of 273024); every family has a row whose sine vanishes identically; 0 admissible points (consistent with Proposition 7.1 / r4search).

Caveat on strength of the evidence: at height <= 2 the only split prime available to grid coordinates is 5 (p^2+q^2 in {1,2,5}), so dependence among grid coordinates is automatic; the content of the test at H=2 is in the solved coordinate (height up to 11, new primes such as 13, 17, 25=5^2 can appear) and in the identity of the relation. At height <= 3 the grid carries the primes 5 and 13 (p^2+q^2 in {1,2,5,10,13,18}) and the solved coordinate reaches larger height, so rank-3 and rank-4 situations are possible in principle; none of rank 4 occurred.

## Coverage: exactly what was and was not covered

- Covered: all 113 orbit representatives (hence all 11,862 full-depth configurations up to signed coordinate permutation); all 4 choices of solved coordinate; all 48 signed systems; all triples of the other three parameters in the projective grid of height <= H including 0 and infinity; all three branches (Cramer, line-circle, identically-zero family). Every rational point of a solution variety with at least three parameters of height <= H is therefore recorded (the fourth is found exactly, whatever its height).
- Not covered: rational points all four of whose parameters have height > H; the classification of points inside a free-angle family is by the rank of the fixed triple (complete for the question asked, but individual family points were not enumerated); configurations with entries of absolute value > 1 (not full-depth in the {0,+-1} sense) and r != 4.
- Exactness: all arithmetic is integer/Fraction; the numpy stage is int64 with an overflow guard (valid for H <= 3). The brute-force cross-check is exponent-bounded (|n_j| <= 4) and was run on a 400-point sample per height, not on all points; the rank test itself is complete and was run on every point.

## Files

- `torsion_coset_probe.py` -- sweep (`python torsion_coset_probe.py H`) and aggregation (`python torsion_coset_probe.py H aggregate`).
- `results/torsion_coset_H2.json` -- summary, per-orbit counts, cross-check, all 58240 non-all-torsion points with t, z, sines, exponents, rank, relation basis, degeneracy.
- `results/partial_H2/orbit_NNN.json` -- per-orbit checkpoints (all points incl. all-torsion, all families); `results/probe_H2.log` -- run log.
- `results/torsion_coset_H3.json` -- summary, per-orbit counts, cross-check, all 260096 non-all-torsion points with t, z, sines, exponents, rank, relation basis, degeneracy.
- `results/partial_H3/orbit_NNN.json` -- per-orbit checkpoints (all points incl. all-torsion, all families); `results/probe_H3.log` -- run log.

## Additional observation

- H=2: exponent rank over ALL 71168 points: {0: 12928, 1: 58240}. No point has rank 3 or 4: every rational point found lies on a torsion coset of a subtorus of dimension <= 2 (codimension >= 2), stronger than Conjecture 8.6 asks.
- H=3: exponent rank over ALL 273024 points: {0: 12928, 1: 204672, 2: 55424}. No point has rank 3 or 4: every rational point found lies on a torsion coset of a subtorus of dimension <= 2 (codimension >= 2), stronger than Conjecture 8.6 asks.

Note: the H=3 grid as built by r4search.py has 16 projective values (0, +-1, +-2, +-1/2, +-3, +-1/3, +-3/2, +-2/3, inf), i.e. 4096 triples; runtimes: H=2 sweep 101 s, H=3 sweep 296 s, aggregation (incl. cross-checks) about 1 min each, on one core.

## Iteration 2 (H=4)

Second iteration extended the sweep to projective height H = 4 (24 grid values, 13824 triples, all 4 solved coordinates, all 48 signed systems) -- COMPLETE: 113/113 orbits. Results: **662528 points**, classes {'all_torsion': 12928, 'on_torsion_coset': 649600}, exponent ranks {'0': 12928, '1': 419840, '2': 215936, '3': 13824} (max rank 3), 23696 families with fixed-triple ranks {'0': 5792, '1': 14768, '2': 3136}, counterexample candidates 0 points / 0 families, admissible points 0. New split primes in the grid at H = 4: 17 and 25 = 5^2 (grid primes [5, 13, 17]). The H <= 3 int64 guard is invalid at H = 4 and was replaced by an asserted int64 range for det/Nc/Ns plus a float64 prefilter with exact Python-int re-test of the circle equation. Full details, verdict and overflow-guard statement: `REPORT_H4.md`; code `torsion_coset_probe_H4.py`; data `results/torsion_coset_H4_summary.json`, `results/torsion_coset_H4_examples.json`, `results/partial_H4/`.

## Iteration 3 (H=5)

Third iteration extended the sweep to projective height H = 5 (40 grid values, 64000 triples, grid norms up to 41, new grid split primes 29 and 41; all 4 solved coordinates, all 48 signed systems) -- COMPLETE: 113/113 orbits. Results: **1916672 points**, classes {'all_torsion': 12928, 'on_torsion_coset': 1903744}, exponent ranks {'0': 12928, '1': 712704, '2': 956032, '3': 235008} (max rank 3), 46416 families with fixed-triple ranks {'0': 5792, '1': 26736, '2': 13888}, counterexample candidates 0 points / 0 families, admissible points 0. **Trichotomy** (every point classified on every system it satisfies): type (i) 1916672, type (ii) 0, type (iii) 0 -- the vanishing-sine conjecture holds on every recorded point. **Rank-3 prediction test**: rank-3 orbits [0, 54], all inside the 23 predicted orbits: True; 2/23 predicted orbits now show rank 3. Overflow guard re-derived (Dfull <= 41^3, det/Nc/Ns <= 8.55e10 exact in int64 and float64; circle test by mod-2^64 and float64 prefilters plus exact Python-int re-test). Full details: `REPORT_H5.md`; code `torsion_coset_probe_H5.py`; data `results/torsion_coset_H5_summary.json`, `results/trichotomy_H5_exceptions.json`, `results/partial_H5/`.
