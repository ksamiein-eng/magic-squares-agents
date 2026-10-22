# Torsion-coset probe, iteration 2: height H = 4 (COMPLETE: 113/113 orbits)

Specialist: torsion-coset-prober (iteration 2). Code: `torsion_coset_probe_H4.py` (iteration-1 `torsion_coset_probe.py` with the H=4 overflow treatment, slim per-orbit checkpoints and a multiprocessing pool; the sweep, the three branches, the exact Gaussian-prime kernel test and the cross-checks are unchanged). Summary: `results/torsion_coset_H4_summary.json`; examples: `results/torsion_coset_H4_examples.json`; per-orbit checkpoints: `results/partial_H4/orbit_NNN.json`; log: `results/probe_H4.log`.

## Coverage

Grid: 24 projective values `0 -1 1 -2 -1/2 1/2 2 -3 -1/3 1/3 3 -4 -3/2 -2/3 -1/4 1/4 2/3 3/2 4 -4/3 -3/4 3/4 4/3 inf` (height <= 4 incl. 0 and infinity), 13824 triples; all 4 solved coordinates; all 48 signed systems; three branches (Cramer, line-circle, identically-zero family). Orbits completed: **113 of 113** (all 11,862 full-depth configurations up to signed coordinate permutation).
Grid norms p^2+q^2: [1, 2, 5, 10, 13, 17, 25]; split primes carried by grid coordinates: **[5, 13, 17]** (new at H=4 relative to H=3: 17 from 4/1, 1/4 and 25 = 5^2 from 4/3, 3/4; H=3 had only 5 and 13). Split primes occurring in any exponent vector, including the solved coordinate: [5, 13, 17].

## Counts

| quantity | H = 3 (iteration 1) | H = 4 (this run) |
|---|---|---|
| orbits | 113 | 113 |
| distinct rational points of solution varieties | 273024 | **662528** |
| &nbsp;&nbsp; class `all_torsion` | 12928 | 12928 |
| &nbsp;&nbsp; class `on_torsion_coset` | 260096 | 649600 |
| &nbsp;&nbsp; class `NOT_on_torsion_coset` | 0 | 0 |
| &nbsp;&nbsp; points with 4 torsion coordinate(s) | 12928 | 12928 |
| &nbsp;&nbsp; points with 3 torsion coordinate(s) | 69504 | 115840 |
| &nbsp;&nbsp; points with 2 torsion coordinate(s) | 36960 | 88096 |
| &nbsp;&nbsp; points with 1 torsion coordinate(s) | 99392 | 253440 |
| &nbsp;&nbsp; points with 0 torsion coordinate(s) | 54240 | 192224 |
| admissible points | 0 | **0** |
| degenerate: some sine zero AND two magnitudes equal | 273024 | 662528 |
| zero sine only / equal magnitudes only / neither | 0 / 0 / 0 | 0 / 0 / 0 |
| raw hits before dedup: Cramer / line-circle | 1935744 / 3591936 | 4816128 / 6491136 |
| float64 prefilter candidates (Cramer) -> exact hits | n/a (pure int64) | 16802384 -> 4816128 |
| free-angle families | 15152 | **23696** |
| &nbsp;&nbsp; families with degeneracy `row_identically_zero` | 15152 | 23696 |
| &nbsp;&nbsp; families with fixed-triple exponent rank 0 | 5792 | 5792 |
| &nbsp;&nbsp; families with fixed-triple exponent rank 1 | 8464 | 14768 |
| &nbsp;&nbsp; families with fixed-triple exponent rank 2 | 896 | 3136 |
| counterexample candidates (points / families) | 0 / 0 | **0 / 0** |
| brute-force + sympy cross-check (sample) | 400/400 agree | 452/452 agree, 0 disagree |
| sweep CPU time (sum over orbits) / wall | 254 s / 254 s (1 core) | 2097 s / 368 s (6 workers) |

## Exponent-rank distribution (all points, complete kernel test)

| rank | H = 2 | H = 3 | H = 4 |
|---|---|---|---|
| 0 | 12928 | 12928 | 12928 |
| 1 | 58240 | 204672 | 419840 |
| 2 | 0 | 55424 | 215936 |
| 3 | 0 | 0 | 13824 |
| 4 | 0 | 0 | 0 |

Maximal exponent rank observed at H = 4: **3** (EXCEEDS 2: see the examples file; the H<=3 observation "rank <= 2" does not persist).

Rank-3 points (13824 in total) occur only in orbits 0 (rows [[0, 0, 0, 1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, -1, 1]], 9216 points), 54 (rows [[0, 0, 1, -1], [1, -1, -1, 1], [1, -1, 0, 0], [1, -1, 1, -1]], 4608 points). They are still on a torsion coset (rank 3 < 4, one relation, e.g. z_1^-1 z_2 z_3 in {+-1,+-i} at t = (-1/13, -1/3, -4, -2/3) with supports {5,17}, {5}, {17}, {13}): the solved coordinate t = +-1/13 (norm 170 = 2*5*17) is what makes rank 3 reachable once the grid carries 17. Conjecture 8.6 only needs rank < 4, so this does not weaken the verdict; it does mean the stronger H<=3 pattern "codimension >= 2" is an artefact of small height. Note also the float64 prefilter is loose (16.8M candidates for 4.8M exact hits, because small det/Nc/Ns trivially pass |.|<1e6); this only costs time, every candidate was re-tested exactly.

## Verdict on Conjecture 8.6 (torsion-coset hypothesis) at H <= 4

**CONFIRMED on every rational point found.** All 662528 distinct rational points of the solution varieties (113 orbit representatives, all 48 signed systems, three parameters of height <= 4, fourth parameter arbitrary) satisfy a nontrivial relation prod z_j^(n_j) in {+-1,+-i} by the complete exponent-rank test; 0 points are off every torsion coset. All 23696 free-angle families have a fixed triple of exponent rank <= 2 (< 3), so every point of every family lies on a torsion coset as well. Admissible points: 0 (consistent with Proposition 7.1 / r4search). Together with iteration 1 this covers every rational point with at least three parameters of height <= 4.

## Examples: points with no torsion coordinate and the highest rank seen

| orbit | t = (t_1..t_4) | rank | relation basis n (prod z_j^n_j in {+-1,+-i}) | supports |
|---|---|---|---|---|
| 0 | ['-1/13', '-1/3', '-4', '-2/3'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'5': 1}, {'17': 1}, {'13': -1}] |
| 0 | ['-1/13', '-1/3', '-4', '-3/2'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'5': 1}, {'17': 1}, {'13': 1}] |
| 0 | ['-1/13', '-1/3', '-4', '2/3'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'5': 1}, {'17': 1}, {'13': 1}] |
| 0 | ['-1/13', '-1/3', '-4', '3/2'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'5': 1}, {'17': 1}, {'13': -1}] |
| 0 | ['-1/13', '-1/3', '1/4', '-2/3'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'5': 1}, {'17': 1}, {'13': -1}] |
| 0 | ['-1/13', '-1/3', '1/4', '-3/2'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'5': 1}, {'17': 1}, {'13': 1}] |
| 0 | ['-1/13', '-1/3', '1/4', '2/3'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'5': 1}, {'17': 1}, {'13': 1}] |
| 0 | ['-1/13', '-1/3', '1/4', '3/2'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'5': 1}, {'17': 1}, {'13': -1}] |
| 0 | ['-1/13', '-4', '-1/3', '-2/3'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'17': 1}, {'5': 1}, {'13': -1}] |
| 0 | ['-1/13', '-4', '-1/3', '-3/2'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'17': 1}, {'5': 1}, {'13': 1}] |
| 0 | ['-1/13', '-4', '-1/3', '2/3'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'17': 1}, {'5': 1}, {'13': 1}] |
| 0 | ['-1/13', '-4', '-1/3', '3/2'] | 3 | [[-1, 1, 1, 0]] | [{'5': 1, '17': 1}, {'17': 1}, {'5': 1}, {'13': -1}] |

## Overflow-guard statement (requirement 1)

The iteration-1 guard `3*mx < 39000` (which made `det^2` and `Nc^2+Ns^2` exact in int64) is NOT valid at H = 4: with three grid coordinates the common denominator is `Dfull = prod (p_j^2+q_j^2) <= 25^3 = 15625`, the row coefficients A, B, C of each signed system are sums of three such terms (`<= 3*15625 = 46875 > 39000`), and `det^2` can reach ~1.9e19 > 2^63. It was therefore replaced, not relaxed: (i) the script asserts from the ACTUAL maxima that `2*(3*mx)^2 < 2^62`, so `det`, `Nc`, `Ns` (two-term products of A, B, C) are exact in int64 -- observed maxima: row coefficient 15625, |det|,|Nc|,|Ns| <= 1392750552 (int64 limit 9.22e18); (ii) the circle test `Nc^2+Ns^2 == det^2` is done as a float64 prefilter `|Nc^2+Ns^2-det^2| < 1e6` -- each square is < 2e19 so its float64 rounding error is < 2e19 * 2^-52 < 5e3 and a true solution can never be rejected -- followed by an exact Python-int re-test of every candidate; the number of candidates (16802384) versus exact hits (4816128) is recorded. All other arithmetic (line-circle branch, point verification, kernel test) is Python int / Fraction as before. No overflow was silently accepted.

## Runtime and files

Sweep: 2097 s CPU over 113 orbits, wall 368 s with 6 worker processes (H = 3: 254 s on one core; the per-orbit cost grew by about the 3.4x triple-count ratio plus the Python-side point processing). Output deliberately small: the per-orbit checkpoints hold counts, distributions, counterexample candidates, <= 20 examples and the in-orbit cross-check sample (no full point lists), so there is no multi-hundred-MB JSON for H = 4.

- `results/torsion_coset_H4_summary.json` -- totals, points_by_class, points_by_exponent_rank, points_by_number_of_torsion_coordinates, points_by_degeneracy, families_by_degeneracy, families_by_rank_of_fixed_triple, counterexample candidates, max exponent rank, split primes in grid / supports, overflow-guard maxima, per-orbit counts, cross-check tally, `partial` flag.
- `results/torsion_coset_H4_examples.json` -- up to 20 points with no torsion coordinate and the highest exponent rank, with relation basis.
- `results/partial_H4/orbit_NNN.json`, `results/probe_H4.log`, `results/run_H4.out`.
