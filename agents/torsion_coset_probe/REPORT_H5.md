# Torsion-coset probe, iteration 3: height H = 5, trichotomy and rank-3 prediction test (COMPLETE: 113/113 orbits)

Specialist: torsion-coset-prober (iteration 3). Code: `torsion_coset_probe_H5.py` (iteration-2 `torsion_coset_probe_H4.py` with the H=5 overflow treatment, the trichotomy classification of every point, independent sympy re-verification of any type (ii)/(iii) point, and the rank-3 prediction test; the sweep, the three branches, the exact Gaussian-prime kernel test and the cross-checks are unchanged). Summary: `results/torsion_coset_H5_summary.json`; trichotomy exceptions: `results/trichotomy_H5_exceptions.json`; examples: `results/torsion_coset_H5_examples.json`; per-orbit checkpoints: `results/partial_H5/orbit_NNN.json`; log: `results/probe_H5.log`.

## Headline

**Every one of the 1916672 rational points recorded at H = 5 (113/113 orbits) is of trichotomy type (i): some sine vanishes.** Type (ii) (admissible, would refute rigidity): 0. Type (iii) (all sines nonzero and A = 2B, would refute the vanishing-sine conjecture): 0. `results/trichotomy_H5_exceptions.json` is an empty list.
Rank-3 prediction test: orbits with rank-3 points = [0, 54]; all inside the 23 predicted orbits: **YES**; 2 of the 23 predicted orbits now show rank 3 (H = 4: 2 of 23). Max exponent rank: 3; rank-4 points: 0.

## Coverage

Grid: 40 projective values `0 -1 1 -2 -1/2 1/2 2 -3 -1/3 1/3 3 -4 -3/2 -2/3 -1/4 1/4 2/3 3/2 4 -5 -1/5 1/5 5 -5/2 -4/3 -3/4 -2/5 2/5 3/4 4/3 5/2 -5/3 -3/5 3/5 5/3 -5/4 -4/5 4/5 5/4 inf` (height <= 5 incl. 0 and infinity), 64000 triples; all 4 solved coordinates; all 48 signed systems; three branches (Cramer, line-circle, identically-zero family). Orbits completed: **113 of 113** (all 11,862 full-depth configurations up to signed coordinate permutation).
Grid norms p^2+q^2: [1, 2, 5, 10, 13, 17, 25, 26, 29, 34, 41] (maximum 41 = 5^2+4^2, not 50, since 5/5 is not in lowest terms); split primes carried by grid coordinates: **[5, 13, 17, 29, 41]** (new at H=5 relative to H=4: 29 from 5/2, 2/5 and 41 from 5/4, 4/5; also 26 = 2*13 from 5/1, 1/5 and 34 = 2*17 from 5/3, 3/5). Split primes occurring in any exponent vector, including the solved coordinate: [5, 13, 17, 29, 41].

## Counts

| quantity | H = 4 (iteration 2) | H = 5 (this run) |
|---|---|---|
| orbits | 113 | 113 |
| distinct rational points of solution varieties | 662528 | **1916672** |
| &nbsp;&nbsp; class `all_torsion` | 12928 | 12928 |
| &nbsp;&nbsp; class `on_torsion_coset` | 649600 | 1903744 |
| &nbsp;&nbsp; class `NOT_on_torsion_coset` | 0 | 0 |
| &nbsp;&nbsp; points with 4 torsion coordinate(s) | 12928 | 12928 |
| &nbsp;&nbsp; points with 3 torsion coordinate(s) | 115840 | 208512 |
| &nbsp;&nbsp; points with 2 torsion coordinate(s) | 88096 | 242208 |
| &nbsp;&nbsp; points with 1 torsion coordinate(s) | 253440 | 692480 |
| &nbsp;&nbsp; points with 0 torsion coordinate(s) | 192224 | 760544 |
| admissible points | 0 | **0** |
| trichotomy type (i) / (ii) / (iii) | 662528 / 0 / 0 (re-derived: all H4 points had a zero sine) | **1916672 / 0 / 0** |
| degenerate: some sine zero AND two magnitudes equal | 662528 | 1916672 |
| zero sine only / equal magnitudes only / neither | 0 / 0 / 0 | 0 / 0 / 0 |
| raw hits before dedup: Cramer / line-circle | 4816128 / 6491136 | 14367744 / 13530624 |
| prefilter candidates (Cramer) -> exact hits | 16802384 -> 4816128 (float only) | 14367744 -> 14367744 (mod 2^64 and float) |
| free-angle families | 23696 | **46416** |
| &nbsp;&nbsp; families with degeneracy `row_identically_zero` | 23696 | 46416 |
| &nbsp;&nbsp; families with fixed-triple exponent rank 0 | 5792 | 5792 |
| &nbsp;&nbsp; families with fixed-triple exponent rank 1 | 14768 | 26736 |
| &nbsp;&nbsp; families with fixed-triple exponent rank 2 | 3136 | 13888 |
| families by trichotomy | all `row_identically_zero` | {'all_points_type_i_row_identically_zero': 46416} |
| counterexample candidates (points / families) | 0 / 0 | **0 / 0** |
| brute-force + sympy cross-check (sample) | 452/452 agree | 452/452 agree, 0 disagree |
| sweep CPU time (sum over orbits) / wall | 2097 s / 368 s (6 workers) | 4348 s / 734 s (6 workers) |

## Trichotomy classification (Theorem "Trichotomy on a signed system")

Every recorded point was classified from its exact sines (Fractions) on EVERY signed system it satisfies: type (i) if some sine is 0; otherwise A = max(|s_k|,|s_l|), B = min(|s_k|,|s_l|) is computed for each system (i,j,k,l,eps,eta) the point satisfies, the identity {|s_i|,|s_j|} = {A+B, |A-B|} is asserted, and the point is type (iii) if A = 2B and type (ii) (admissible) otherwise; the script asserts that "admissible" (four nonzero distinct magnitudes with the Lemma-roles structure) and "A = 2B" are complementary on every system, i.e. that the trichotomy is exhaustive and exclusive on the data. Every free-angle family has a row whose sine vanishes identically, so all its points are type (i).

Overall: type (i) **1916672**, type (ii) **0**, type (iii) **0** (of 1916672 points).

| orbit | rows | points | type (i) | type (ii) | type (iii) | exponent ranks |
|---|---|---|---|---|---|---|
| 0 | [[0, 0, 0, 1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, -1, 1]] | 442464 | 442464 | 0 | 0 | {'0': 192, '1': 40608, '2': 244992, '3': 156672} |
| 1 | [[0, 0, 0, 1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, 1, -1]] | 63264 | 63264 | 0 | 0 | {'0': 192, '1': 20320, '2': 42752} |
| 2 | [[0, 0, 0, 1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, 1, 1]] | 61216 | 61216 | 0 | 0 | {'0': 192, '1': 19808, '2': 41216} |
| 3 | [[0, 0, 0, 1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, -1]] | 29184 | 29184 | 0 | 0 | {'0': 128, '1': 10240, '2': 18816} |
| 4 | [[0, 0, 0, 1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, 0]] | 40224 | 40224 | 0 | 0 | {'0': 192, '1': 13408, '2': 26624} |
| 5 | [[0, 0, 0, 1], [1, -1, -1, -1], [1, -1, 1, -1], [1, 1, -1, -1]] | 7200 | 7200 | 0 | 0 | {'0': 128, '1': 7072} |
| 6 | [[0, 0, 0, 1], [1, -1, -1, -1], [1, -1, 1, -1], [1, 1, -1, 0]] | 11136 | 11136 | 0 | 0 | {'0': 192, '1': 10944} |
| 7 | [[0, 0, 0, 1], [1, -1, -1, -1], [1, -1, 1, 0], [1, 1, -1, 1]] | 10592 | 10592 | 0 | 0 | {'0': 192, '1': 10400} |
| 8 | [[0, 0, 0, 1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1, 1]] | 6560 | 6560 | 0 | 0 | {'0': 128, '1': 6432} |
| 9 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, -1, 1]] | 15136 | 15136 | 0 | 0 | {'0': 96, '1': 5568, '2': 9472} |
| 10 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, 0, -1]] | 26304 | 26304 | 0 | 0 | {'0': 128, '1': 9664, '2': 16512} |
| 11 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, 0, 1]] | 18560 | 18560 | 0 | 0 | {'0': 128, '1': 6528, '2': 11904} |
| 12 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, 1, -1]] | 12480 | 12480 | 0 | 0 | {'0': 96, '1': 4448, '2': 7936} |
| 13 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, 1, 1]] | 12480 | 12480 | 0 | 0 | {'0': 96, '1': 4448, '2': 7936} |
| 14 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 1, -1, -1]] | 3616 | 3616 | 0 | 0 | {'0': 96, '1': 3520} |
| 15 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 1, -1, 1]] | 3968 | 3968 | 0 | 0 | {'0': 96, '1': 3872} |
| 16 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 1, 0, -1]] | 4928 | 4928 | 0 | 0 | {'0': 128, '1': 4800} |
| 17 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 0, 0]] | 68736 | 68736 | 0 | 0 | {'0': 192, '1': 20928, '2': 47616} |
| 18 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 0, 1]] | 12480 | 12480 | 0 | 0 | {'0': 96, '1': 4448, '2': 7936} |
| 19 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, -1]] | 39296 | 39296 | 0 | 0 | {'0': 128, '1': 11392, '2': 27776} |
| 20 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, 0]] | 12480 | 12480 | 0 | 0 | {'0': 96, '1': 4448, '2': 7936} |
| 21 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, 1]] | 23712 | 23712 | 0 | 0 | {'0': 128, '1': 7712, '2': 15872} |
| 22 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, 1, -1, -1]] | 7936 | 7936 | 0 | 0 | {'0': 128, '1': 7808} |
| 23 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, 1, -1, 0]] | 3104 | 3104 | 0 | 0 | {'0': 96, '1': 3008} |
| 24 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, 1, -1, 1]] | 8096 | 8096 | 0 | 0 | {'0': 128, '1': 7968} |
| 25 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, 1, 0, -1]] | 3424 | 3424 | 0 | 0 | {'0': 96, '1': 3328} |
| 26 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, 1, 0, 0]] | 11456 | 11456 | 0 | 0 | {'0': 192, '1': 11264} |
| 27 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 0, 0], [1, -1, 1, 1]] | 36480 | 36480 | 0 | 0 | {'0': 192, '1': 12480, '2': 23808} |
| 28 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 0, 0], [1, 1, -1, 1]] | 11968 | 11968 | 0 | 0 | {'0': 192, '1': 11776} |
| 29 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 0, 1], [1, -1, 1, 0]] | 26048 | 26048 | 0 | 0 | {'0': 128, '1': 9408, '2': 16512} |
| 30 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 0, 1], [1, 1, -1, -1]] | 3424 | 3424 | 0 | 0 | {'0': 96, '1': 3328} |
| 31 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 0, 1], [1, 1, -1, 0]] | 4064 | 4064 | 0 | 0 | {'0': 128, '1': 3936} |
| 32 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 0, 1], [1, 1, -1, 1]] | 3904 | 3904 | 0 | 0 | {'0': 96, '1': 3808} |
| 33 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1, -1]] | 6144 | 6144 | 0 | 0 | {'0': 128, '1': 6016} |
| 34 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1, 0]] | 2656 | 2656 | 0 | 0 | {'0': 96, '1': 2560} |
| 35 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1, 1]] | 8768 | 8768 | 0 | 0 | {'0': 128, '1': 8640} |
| 36 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 1, 0, 0]] | 9024 | 9024 | 0 | 0 | {'0': 192, '1': 8832} |
| 37 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, 1, -1, 0], [1, 1, -1, 1]] | 3552 | 3552 | 0 | 0 | {'0': 96, '1': 3456} |
| 38 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, 1, -1, 0], [1, 1, 0, -1]] | 10304 | 10304 | 0 | 0 | {'0': 128, '1': 7104, '2': 3072} |
| 39 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, 1, -1, 0], [1, 1, 0, 1]] | 5184 | 5184 | 0 | 0 | {'0': 128, '1': 5056} |
| 40 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, 1, -1, 0], [1, 1, 1, -1]] | 3232 | 3232 | 0 | 0 | {'0': 96, '1': 3136} |
| 41 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, 1, -1, 1], [1, 1, 0, 0]] | 50848 | 50848 | 0 | 0 | {'0': 192, '1': 18912, '2': 31744} |
| 42 | [[0, 0, 1, -1], [1, -1, -1, -1], [1, 1, -1, 1], [1, 1, 1, -1]] | 35424 | 35424 | 0 | 0 | {'0': 128, '1': 11488, '2': 23808} |
| 43 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, -1, -1, 1], [1, -1, 0, -1]] | 23648 | 23648 | 0 | 0 | {'0': 128, '1': 8544, '2': 14976} |
| 44 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, -1, -1, 1], [1, -1, 0, 1]] | 18560 | 18560 | 0 | 0 | {'0': 128, '1': 6528, '2': 11904} |
| 45 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, -1, -1, 1], [1, -1, 1, -1]] | 14656 | 14656 | 0 | 0 | {'0': 96, '1': 5088, '2': 9472} |
| 46 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, -1, -1, 1], [1, 1, -1, 1]] | 4096 | 4096 | 0 | 0 | {'0': 96, '1': 4000} |
| 47 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, -1, -1, 1], [1, 1, 0, -1]] | 5408 | 5408 | 0 | 0 | {'0': 128, '1': 5280} |
| 48 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, -1, 0, -1], [1, 1, -1, 1]] | 18176 | 18176 | 0 | 0 | {'0': 128, '1': 8576, '2': 9472} |
| 49 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, -1, 0, 1], [1, -1, 1, -1]] | 18560 | 18560 | 0 | 0 | {'0': 128, '1': 6528, '2': 11904} |
| 50 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, -1, 0, 1], [1, 1, -1, 1]] | 5376 | 5376 | 0 | 0 | {'0': 128, '1': 5248} |
| 51 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, -1, 1, -1], [1, 1, -1, 1]] | 3552 | 3552 | 0 | 0 | {'0': 96, '1': 3456} |
| 52 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, -1, 1, -1], [1, 1, 0, -1]] | 4288 | 4288 | 0 | 0 | {'0': 128, '1': 4160} |
| 53 | [[0, 0, 1, -1], [1, -1, -1, 0], [1, 1, -1, 1], [1, 1, 1, -1]] | 9952 | 9952 | 0 | 0 | {'0': 96, '1': 4352, '2': 5504} |
| 54 | [[0, 0, 1, -1], [1, -1, -1, 1], [1, -1, 0, 0], [1, -1, 1, -1]] | 249600 | 249600 | 0 | 0 | {'0': 192, '1': 30656, '2': 140416, '3': 78336} |
| 55 | [[0, 0, 1, -1], [1, -1, -1, 1], [1, -1, 1, -1], [1, 1, -1, 1]] | 35232 | 35232 | 0 | 0 | {'0': 128, '1': 11296, '2': 23808} |
| 56 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, -1, 1]] | 13664 | 13664 | 0 | 0 | {'0': 96, '1': 5632, '2': 7936} |
| 57 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, 0, -1]] | 2192 | 2192 | 0 | 0 | {'0': 80, '1': 2112} |
| 58 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, 0, 1]] | 1968 | 1968 | 0 | 0 | {'0': 80, '1': 1888} |
| 59 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, 1, -1]] | 3200 | 3200 | 0 | 0 | {'0': 96, '1': 3104} |
| 60 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, -1, 1, 1]] | 4320 | 4320 | 0 | 0 | {'0': 96, '1': 4224} |
| 61 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 0, -1, -1]] | 2384 | 2384 | 0 | 0 | {'0': 80, '1': 2304} |
| 62 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 0, -1, 1]] | 1488 | 1488 | 0 | 0 | {'0': 80, '1': 1408} |
| 63 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 0, 1, -1]] | 1840 | 1840 | 0 | 0 | {'0': 80, '1': 1760} |
| 64 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 0, 1, 1]] | 2064 | 2064 | 0 | 0 | {'0': 80, '1': 1984} |
| 65 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 1, -1, -1]] | 4448 | 4448 | 0 | 0 | {'0': 96, '1': 4352} |
| 66 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 1, -1, 1]] | 3072 | 3072 | 0 | 0 | {'0': 96, '1': 2976} |
| 67 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 1, 0, -1]] | 1648 | 1648 | 0 | 0 | {'0': 80, '1': 1568} |
| 68 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 1, 1, -1]] | 3264 | 3264 | 0 | 0 | {'0': 96, '1': 3168} |
| 69 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 0], [1, 1, 1, 1]] | 2912 | 2912 | 0 | 0 | {'0': 96, '1': 2816} |
| 70 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 0, 1]] | 3616 | 3616 | 0 | 0 | {'0': 96, '1': 3520} |
| 71 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, -1]] | 5920 | 5920 | 0 | 0 | {'0': 128, '1': 5792} |
| 72 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, 0]] | 3424 | 3424 | 0 | 0 | {'0': 96, '1': 3328} |
| 73 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, 1]] | 7904 | 7904 | 0 | 0 | {'0': 128, '1': 7776} |
| 74 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, 0, 1, -1]] | 2336 | 2336 | 0 | 0 | {'0': 96, '1': 2240} |
| 75 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, 0, 1, 1]] | 3392 | 3392 | 0 | 0 | {'0': 96, '1': 3296} |
| 76 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, 1, 1, -1]] | 7136 | 7136 | 0 | 0 | {'0': 128, '1': 7008} |
| 77 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, -1, 1], [1, 1, 1, 0]] | 2656 | 2656 | 0 | 0 | {'0': 96, '1': 2560} |
| 78 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 0, 1], [1, -1, 1, 0]] | 2320 | 2320 | 0 | 0 | {'0': 80, '1': 2240} |
| 79 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 0, 1], [1, -1, 1, 1]] | 4096 | 4096 | 0 | 0 | {'0': 96, '1': 4000} |
| 80 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 0, 1], [1, 0, -1, 1]] | 1424 | 1424 | 0 | 0 | {'0': 80, '1': 1344} |
| 81 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 0, 1], [1, 0, 1, -1]] | 1424 | 1424 | 0 | 0 | {'0': 80, '1': 1344} |
| 82 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 0, 1], [1, 1, -1, 1]] | 12704 | 12704 | 0 | 0 | {'0': 96, '1': 4672, '2': 7936} |
| 83 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 0, 1], [1, 1, 1, -1]] | 3968 | 3968 | 0 | 0 | {'0': 96, '1': 3872} |
| 84 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 0, -1, -1]] | 12480 | 12480 | 0 | 0 | {'0': 96, '1': 4448, '2': 7936} |
| 85 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 0, 1, 1]] | 12480 | 12480 | 0 | 0 | {'0': 96, '1': 4448, '2': 7936} |
| 86 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1, -1]] | 47456 | 47456 | 0 | 0 | {'0': 128, '1': 13024, '2': 34304} |
| 87 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1, 0]] | 3008 | 3008 | 0 | 0 | {'0': 96, '1': 2912} |
| 88 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1, 1]] | 7360 | 7360 | 0 | 0 | {'0': 128, '1': 7232} |
| 89 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, -1, 1, 1], [1, 1, 1, 1]] | 17664 | 17664 | 0 | 0 | {'0': 128, '1': 6656, '2': 10880} |
| 90 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 0, -1, -1], [1, 1, -1, -1]] | 15136 | 15136 | 0 | 0 | {'0': 96, '1': 5568, '2': 9472} |
| 91 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 0, -1, -1], [1, 1, -1, 0]] | 1552 | 1552 | 0 | 0 | {'0': 80, '1': 1472} |
| 92 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 0, -1, -1], [1, 1, 1, 1]] | 12480 | 12480 | 0 | 0 | {'0': 96, '1': 4448, '2': 7936} |
| 93 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 0, -1, 1], [1, 1, -1, 0]] | 1840 | 1840 | 0 | 0 | {'0': 80, '1': 1760} |
| 94 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 0, -1, 1], [1, 1, 0, -1]] | 1008 | 1008 | 0 | 0 | {'0': 80, '1': 928} |
| 95 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 0, -1, 1], [1, 1, 1, -1]] | 2208 | 2208 | 0 | 0 | {'0': 96, '1': 2112} |
| 96 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 0, -1, 1], [1, 1, 1, 0]] | 1424 | 1424 | 0 | 0 | {'0': 80, '1': 1344} |
| 97 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 1, -1, -1], [1, 1, -1, 0]] | 3456 | 3456 | 0 | 0 | {'0': 96, '1': 3360} |
| 98 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 1, -1, -1], [1, 1, -1, 1]] | 7616 | 7616 | 0 | 0 | {'0': 128, '1': 7488} |
| 99 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 1, -1, 0], [1, 1, 0, -1]] | 1232 | 1232 | 0 | 0 | {'0': 80, '1': 1152} |
| 100 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 1, -1, 0], [1, 1, 1, -1]] | 2784 | 2784 | 0 | 0 | {'0': 96, '1': 2688} |
| 101 | [[0, 1, -1, -1], [1, -1, -1, -1], [1, 1, -1, 1], [1, 1, 1, -1]] | 6080 | 6080 | 0 | 0 | {'0': 128, '1': 5952} |
| 102 | [[0, 1, -1, -1], [1, -1, -1, 0], [1, -1, 0, -1], [1, 0, -1, -1]] | 1744 | 1744 | 0 | 0 | {'0': 80, '1': 1664} |
| 103 | [[0, 1, -1, -1], [1, -1, -1, 0], [1, -1, 0, -1], [1, 0, -1, 1]] | 1616 | 1616 | 0 | 0 | {'0': 80, '1': 1536} |
| 104 | [[0, 1, -1, -1], [1, -1, -1, 0], [1, -1, 0, -1], [1, 0, 1, 1]] | 1488 | 1488 | 0 | 0 | {'0': 80, '1': 1408} |
| 105 | [[0, 1, -1, -1], [1, -1, -1, 0], [1, -1, 0, 1], [1, 0, -1, -1]] | 2000 | 2000 | 0 | 0 | {'0': 80, '1': 1920} |
| 106 | [[0, 1, -1, -1], [1, -1, -1, 0], [1, 0, 1, -1], [1, 1, 0, 1]] | 2000 | 2000 | 0 | 0 | {'0': 80, '1': 1920} |
| 107 | [[0, 1, -1, -1], [1, -1, 0, 1], [1, -1, 1, 0], [1, -1, 1, 1]] | 2672 | 2672 | 0 | 0 | {'0': 80, '1': 2592} |
| 108 | [[0, 1, -1, -1], [1, -1, 0, 1], [1, -1, 1, 0], [1, 0, 1, 1]] | 2000 | 2000 | 0 | 0 | {'0': 80, '1': 1920} |
| 109 | [[1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, -1], [1, -1, 1, 1]] | 1472 | 1472 | 0 | 0 | {'0': 128, '1': 1344} |
| 110 | [[1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, -1], [1, 1, -1, -1]] | 13568 | 13568 | 0 | 0 | {'0': 128, '1': 13440} |
| 111 | [[1, -1, -1, -1], [1, -1, -1, 1], [1, -1, 1, -1], [1, 1, -1, 1]] | 13952 | 13952 | 0 | 0 | {'0': 128, '1': 13824} |
| 112 | [[1, -1, -1, -1], [1, -1, 1, 1], [1, 1, -1, 1], [1, 1, 1, -1]] | 13952 | 13952 | 0 | 0 | {'0': 128, '1': 13824} |

## Trichotomy exceptions (type (ii) or (iii) points)

None. `results/trichotomy_H5_exceptions.json` holds an empty list. The vanishing-sine conjecture (and rigidity) survive every rational point with at least three parameters of height <= 5.

## Exponent-rank distribution and the rank-3 prediction test

| rank | H = 3 | H = 4 | H = 5 |
|---|---|---|---|
| 0 | 12928 | 12928 | 12928 |
| 1 | 204672 | 419840 | 712704 |
| 2 | 55424 | 215936 | 956032 |
| 3 | 0 | 13824 | 235008 |
| 4 | 0 | 0 | 0 |

Maximal exponent rank observed at H = 5: **3**; rank-4 points (off every torsion coset): 0.

The degeneracy-rank lemma predicts that rank-3 points can occur only in the 23 orbits satisfying the parallel-triple criterion (`results/rank_bound_prediction.json`): [0, 1, 2, 3, 4, 9, 10, 17, 19, 27, 29, 38, 41, 42, 43, 45, 48, 53, 54, 55, 56, 86, 90].
- Orbits with rank-3 points at H = 5: **[0, 54]** (2 orbits; H = 4: [0, 54]).
- Rank-3 orbits outside the prediction: **[]** -> prediction holds: **True**.
- Predicted orbits now showing rank 3: **2 of 23**; predicted orbits completed in this run: 23 of 23; predicted but not (yet) showing rank 3: [1, 2, 3, 4, 9, 10, 17, 19, 27, 29, 38, 41, 42, 43, 45, 48, 53, 55, 56, 86, 90].

| orbit | rank-3 points at H = 5 | rank-3 points at H = 4 |
|---|---|---|
| 0 | 156672 | 9216 |
| 54 | 78336 | 4608 |

## Verdict on Conjecture 8.6 (torsion-coset hypothesis) at H <= 5

**CONFIRMED on every rational point found.** All 1916672 distinct rational points of the solution varieties (113 orbit representatives, all 48 signed systems, three parameters of height <= 5, fourth parameter arbitrary) satisfy a nontrivial relation prod z_j^(n_j) in {+-1,+-i} by the complete exponent-rank test; 0 points are off every torsion coset. All 46416 free-angle families have a fixed triple of exponent rank <= 2 (< 3), so every point of every family lies on a torsion coset as well. Admissible points: 0.

## Examples: points with no torsion coordinate and the highest rank seen

| orbit | t = (t_1..t_4) | rank | relation basis n (prod z_j^n_j in {+-1,+-i}) | supports |
|---|---|---|---|---|
| 0 | ['-1/12', '-1/2', '-5/2', '-1/4'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'17': -1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '-1/5'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'13': 1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '-2/3'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'13': -1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '-3/2'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'13': 1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '-3/5'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'17': 1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '-4'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'17': 1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '-4/5'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'41': -1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '-5'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'13': -1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '-5/3'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'17': -1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '-5/4'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'41': 1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '1/4'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'17': 1}] |
| 0 | ['-1/12', '-1/2', '-5/2', '1/5'] | 3 | [[-1, 1, 1, 0]] | [{'5': -1, '29': 1}, {'5': -1}, {'29': 1}, {'13': -1}] |

## Overflow-guard statement (requirement 1)

Re-derived for H = 5. Grid norms p^2+q^2 <= 41 (the pair (5,5) is not coprime, so 50 does not occur), hence with three grid coordinates `Dfull = prod (p_j^2+q_j^2) <= 41^3 = 68921`; every row coefficient is bounded by Dfull; the signed-system coefficients A, B, C are sums of three row coefficients, `<= 3*68921 = 206763`; and `det, Nc, Ns` are two-term products, `<= 2*206763^2 = 8.55e10`. These are exact in int64 (limit 9.22e18) AND exactly representable in float64 (< 2^53 = 9.0e15); the script asserts both bounds from the ACTUAL per-orbit maxima (`2*(3*mx)^2 < 2^62` and `< 2^53`). Observed maxima: row coefficient 68921 (bound 68921), |det|,|Nc|,|Ns| <= 27124440520 (bound 85501876338). The squares in the circle test `Nc^2+Ns^2 == det^2` reach ~7.3e21 > 2^63 and are NOT exact in int64; the test is therefore done as two NECESSARY prefilters followed by an exact re-test: (a) the identity evaluated in wrapping int64 arithmetic, i.e. exactly modulo 2^64 (a true solution satisfies it identically, so it is never rejected); (b) the float64 identity with tolerance `8*2^-52*m^2 + 1`, m = actual max of |det|,|Nc|,|Ns| in the system (true rounding error < 5*2^-52*m^2; largest tolerance used 1.31e+06); then (c) every survivor is re-tested with exact Python ints. Candidates after (a)+(b): 14367744; exact hits: 14367744 (the mod-2^64 filter removes essentially all spurious candidates that the H=4 float-only filter let through). All other arithmetic (line-circle branch, point verification, sines, kernel test, trichotomy, independent sympy check) is Python int / Fraction / sympy Rational. No overflow was silently accepted.

## Runtime and files

Sweep: 4348 s CPU over 113 orbits, wall 734 s with 6 worker processes (H = 4: 2097 s CPU / 368 s wall). Output deliberately small: per-orbit checkpoints hold counts, distributions, trichotomy tallies, exceptions, counterexample candidates, <= 20 examples and the in-orbit cross-check sample (no full point lists).

- `results/torsion_coset_H5_summary.json` -- H4 schema plus `points_by_trichotomy`, `families_by_trichotomy`, `n_trichotomy_exceptions`, `rank3_prediction_test`, per-orbit `points_by_trichotomy`, and the extended `overflow_guard` block.
- `results/trichotomy_H5_exceptions.json` -- every type (ii)/(iii) point with full coordinates and independent sympy re-verification (empty list if none).
- `results/torsion_coset_H5_examples.json` -- up to 20 points with no torsion coordinate and the highest exponent rank, with relation basis.
- `results/partial_H5/orbit_NNN.json`, `results/probe_H5.log`, `results/run_H5.out`.
