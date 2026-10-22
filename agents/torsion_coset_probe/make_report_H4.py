"""make_report_H4.py -- write REPORT_H4.md from results/torsion_coset_H4_summary.json (+ _examples.json) and append an
'Iteration 2 (H=4)' pointer section to REPORT.md.  Handles a partial run (orbits_completed < 113) explicitly."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, 'results')
d = json.load(open(os.path.join(RES, 'torsion_coset_H4_summary.json')))
ex = json.load(open(os.path.join(RES, 'torsion_coset_H4_examples.json')))
h3 = json.load(open(os.path.join(RES, 'torsion_coset_H3_summary.json')))
wall = sys.argv[1] if len(sys.argv) > 1 else 'n/a'
partial = d['partial']; done = d['orbits_completed']; N = d['orbits']
tag = f'PARTIAL: {done}/{N} orbits' if partial else f'COMPLETE: {done}/{N} orbits'
nc = d['points_by_class'].get('NOT_on_torsion_coset', 0); ncf = len(d['counterexample_candidates_families'])
L = []
L.append(f'# Torsion-coset probe, iteration 2: height H = 4 ({tag})')
L.append('')
L.append('Specialist: torsion-coset-prober (iteration 2). Code: `torsion_coset_probe_H4.py` (iteration-1 `torsion_coset_probe.py` with the '
         'H=4 overflow treatment, slim per-orbit checkpoints and a multiprocessing pool; the sweep, the three branches, the exact '
         'Gaussian-prime kernel test and the cross-checks are unchanged). Summary: `results/torsion_coset_H4_summary.json`; examples: '
         '`results/torsion_coset_H4_examples.json`; per-orbit checkpoints: `results/partial_H4/orbit_NNN.json`; log: `results/probe_H4.log`.')
L.append('')
L.append('## Coverage')
L.append('')
L.append(f'Grid: {d["grid_values"]} projective values `{" ".join(d["grid"])}` (height <= 4 incl. 0 and infinity), {d["triples"]} triples; '
         f'all 4 solved coordinates; all 48 signed systems; three branches (Cramer, line-circle, identically-zero family). '
         f'Orbits completed: **{done} of {N}**' + (' (run cut at the hackathon budget; every number below is over the completed orbits only).' if partial else ' (all 11,862 full-depth configurations up to signed coordinate permutation).'))
L.append(f'Grid norms p^2+q^2: {d["grid_norms_p2_plus_q2"]}; split primes carried by grid coordinates: **{d["split_primes_in_grid"]}** '
         f'(new at H=4 relative to H=3: 17 from 4/1, 1/4 and 25 = 5^2 from 4/3, 3/4; H=3 had only 5 and 13). '
         f'Split primes occurring in any exponent vector, including the solved coordinate: {d["split_primes_in_all_supports_incl_solved_coord"]}.')
L.append('')
L.append('## Counts')
L.append('')
L.append('| quantity | H = 3 (iteration 1) | H = 4 (this run) |'); L.append('|---|---|---|')
L.append(f'| orbits | 113 | {done}{" (partial)" if partial else ""} |')
L.append(f'| distinct rational points of solution varieties | {h3["totals"]["points"]} | **{d["totals"]["points"]}** |')
for k in ['all_torsion', 'on_torsion_coset', 'NOT_on_torsion_coset']:
    L.append(f'| &nbsp;&nbsp; class `{k}` | {h3["points_by_class"].get(k, 0)} | {d["points_by_class"].get(k, 0)} |')
for k in sorted(d['points_by_number_of_torsion_coordinates'], key=int, reverse=True):
    L.append(f'| &nbsp;&nbsp; points with {k} torsion coordinate(s) | {h3["points_by_number_of_torsion_coordinates"].get(k, 0)} | {d["points_by_number_of_torsion_coordinates"][k]} |')
L.append(f'| admissible points | 0 | **{d["admissible_points"]}** |')
dg = d['points_by_degeneracy']; dg3 = h3['points_by_degeneracy']
L.append(f'| degenerate: some sine zero AND two magnitudes equal | {dg3["both"]} | {dg["both"]} |')
L.append(f'| zero sine only / equal magnitudes only / neither | {dg3["zero_sine"]} / {dg3["equal_magnitudes"]} / {dg3["neither"]} | {dg["zero_sine"]} / {dg["equal_magnitudes"]} / {dg["neither"]} |')
L.append(f'| raw hits before dedup: Cramer / line-circle | {h3["system_evaluations"]["cramer_hits"]} / {h3["system_evaluations"]["singular_hits"]} | {d["system_evaluations"]["cramer_hits"]} / {d["system_evaluations"]["singular_hits"]} |')
L.append(f'| float64 prefilter candidates (Cramer) -> exact hits | n/a (pure int64) | {d["system_evaluations"].get("prefilter_candidates", 0)} -> {d["system_evaluations"]["cramer_hits"]} |')
L.append(f'| free-angle families | {h3["totals"]["families"]} | **{d["totals"]["families"]}** |')
for k, v in d['families_by_degeneracy'].items(): L.append(f'| &nbsp;&nbsp; families with degeneracy `{k}` | {h3["families_by_degeneracy"].get(k, 0)} | {v} |')
for k in sorted(d['families_by_rank_of_fixed_triple'], key=int):
    L.append(f'| &nbsp;&nbsp; families with fixed-triple exponent rank {k} | {h3["families_by_rank_of_fixed_triple"].get(k, 0)} | {d["families_by_rank_of_fixed_triple"][k]} |')
L.append(f'| counterexample candidates (points / families) | 0 / 0 | **{nc} / {ncf}** |')
L.append(f'| brute-force + sympy cross-check (sample) | 400/400 agree | {d["brute_force_crosscheck"]["agree"]}/{d["brute_force_crosscheck"]["checked"]} agree, {d["brute_force_crosscheck"]["n_disagree"]} disagree |')
L.append(f'| sweep CPU time (sum over orbits) / wall | 254 s / 254 s (1 core) | {d["totals"]["elapsed_s"]:.0f} s / {wall} (6 workers) |')
L.append('')
L.append('## Exponent-rank distribution (all points, complete kernel test)')
L.append('')
L.append('| rank | H = 2 | H = 3 | H = 4 |'); L.append('|---|---|---|---|')
h2r = {'0': 12928, '1': 58240}; h3r = {'0': 12928, '1': 204672, '2': 55424}
for k in ['0', '1', '2', '3', '4']:
    L.append(f'| {k} | {h2r.get(k, 0)} | {h3r.get(k, 0)} | {d["points_by_exponent_rank"].get(k, 0)} |')
L.append('')
L.append(f'Maximal exponent rank observed at H = 4: **{d["max_exponent_rank_observed"]}** ' +
         ('(stays <= 2: every point lies on a torsion coset of a subtorus of dimension <= 2, codimension >= 2, as at H = 2, 3).' if d['max_exponent_rank_observed'] <= 2 else
          '(EXCEEDS 2: see the examples file; the H<=3 observation "rank <= 2" does not persist).'))
L.append('')
L.append('## Verdict on Conjecture 8.6 (torsion-coset hypothesis) at H <= 4')
L.append('')
if nc == 0 and ncf == 0:
    L.append(f'**{"PARTIAL (" + str(done) + "/" + str(N) + " orbits): " if partial else ""}CONFIRMED on every rational point found.** All {d["totals"]["points"]} distinct rational points of the '
             f'solution varieties ({done} orbit representatives, all 48 signed systems, three parameters of height <= 4, fourth parameter '
             f'arbitrary) satisfy a nontrivial relation prod z_j^(n_j) in {{+-1,+-i}} by the complete exponent-rank test; 0 points are off every '
             f'torsion coset. All {d["totals"]["families"]} free-angle families have a fixed triple of exponent rank <= {max(map(int, d["families_by_rank_of_fixed_triple"]))} '
             f'(< 3), so every point of every family lies on a torsion coset as well. Admissible points: {d["admissible_points"]} '
             f'(consistent with Proposition 7.1 / r4search). Together with iteration 1 this covers every rational point with at least three '
             f'parameters of height <= 4' + (' on the completed orbits.' if partial else '.'))
else:
    L.append(f'**COUNTEREXAMPLE CANDIDATES FOUND: {nc} points, {ncf} families** -- see `counterexample_candidates_*` in the summary JSON '
             f'(each point carries an independent re-verification of its system and a brute-force relation search |n_j| <= 8).')
L.append('')
L.append('## Examples: points with no torsion coordinate and the highest rank seen')
L.append('')
L.append('| orbit | t = (t_1..t_4) | rank | relation basis n (prod z_j^n_j in {+-1,+-i}) | supports |'); L.append('|---|---|---|---|---|')
for r in ex['examples'][:12]:
    L.append(f'| {r["orbit"]} | {r["t"]} | {r["rank"]} | {r["kernel_basis"]} | {r["support"]} |')
L.append('')
L.append('## Overflow-guard statement (requirement 1)')
L.append('')
L.append('The iteration-1 guard `3*mx < 39000` (which made `det^2` and `Nc^2+Ns^2` exact in int64) is NOT valid at H = 4: with three grid '
         'coordinates the common denominator is `Dfull = prod (p_j^2+q_j^2) <= 25^3 = 15625`, the row coefficients A, B, C of each '
         'signed system are sums of three such terms (`<= 3*15625 = 46875 > 39000`), and `det^2` can reach ~1.9e19 > 2^63. It was '
         'therefore replaced, not relaxed: (i) the script asserts from the ACTUAL maxima that `2*(3*mx)^2 < 2^62`, so `det`, `Nc`, `Ns` '
         f'(two-term products of A, B, C) are exact in int64 -- observed maxima: row coefficient {d["overflow_guard"]["max_abs_row_coeff"]}, '
         f'|det|,|Nc|,|Ns| <= {d["overflow_guard"]["max_abs_det_Nc_Ns"]} (int64 limit 9.22e18); (ii) the circle test `Nc^2+Ns^2 == det^2` is '
         'done as a float64 prefilter `|Nc^2+Ns^2-det^2| < 1e6` -- each square is < 2e19 so its float64 rounding error is < 2e19 * 2^-52 '
         '< 5e3 and a true solution can never be rejected -- followed by an exact Python-int re-test of every candidate; the number of '
         f'candidates ({d["system_evaluations"].get("prefilter_candidates", 0)}) versus exact hits ({d["system_evaluations"]["cramer_hits"]}) is recorded. '
         'All other arithmetic (line-circle branch, point verification, kernel test) is Python int / Fraction as before. No overflow was '
         'silently accepted.')
L.append('')
L.append('## Runtime and files')
L.append('')
L.append(f'Sweep: {d["totals"]["elapsed_s"]:.0f} s CPU over {done} orbits, wall {wall} with 6 worker processes (H = 3: 254 s on one core; the '
         'per-orbit cost grew by about the 3.4x triple-count ratio plus the Python-side point processing). Output deliberately small: the '
         'per-orbit checkpoints hold counts, distributions, counterexample candidates, <= 20 examples and the in-orbit cross-check sample '
         '(no full point lists), so there is no multi-hundred-MB JSON for H = 4.')
L.append('')
L.append('- `results/torsion_coset_H4_summary.json` -- totals, points_by_class, points_by_exponent_rank, points_by_number_of_torsion_coordinates, '
         'points_by_degeneracy, families_by_degeneracy, families_by_rank_of_fixed_triple, counterexample candidates, max exponent rank, '
         'split primes in grid / supports, overflow-guard maxima, per-orbit counts, cross-check tally, `partial` flag.')
L.append('- `results/torsion_coset_H4_examples.json` -- up to 20 points with no torsion coordinate and the highest exponent rank, with relation basis.')
L.append('- `results/partial_H4/orbit_NNN.json`, `results/probe_H4.log`, `results/run_H4.out`.')
open(os.path.join(HERE, 'REPORT_H4.md'), 'w').write('\n'.join(L) + '\n')

rep = open(os.path.join(HERE, 'REPORT.md')).read()
marker = '## Iteration 2 (H=4)'
sec = [marker, '',
       f'Second iteration extended the sweep to projective height H = 4 (24 grid values, 13824 triples, all 4 solved coordinates, all 48 '
       f'signed systems) -- {tag}. Results: **{d["totals"]["points"]} points**, classes {d["points_by_class"]}, exponent ranks '
       f'{d["points_by_exponent_rank"]} (max rank {d["max_exponent_rank_observed"]}), {d["totals"]["families"]} families with fixed-triple ranks '
       f'{d["families_by_rank_of_fixed_triple"]}, counterexample candidates {nc} points / {ncf} families, admissible points {d["admissible_points"]}. '
       f'New split primes in the grid at H = 4: 17 and 25 = 5^2 (grid primes {d["split_primes_in_grid"]}). The H <= 3 int64 guard is invalid at '
       f'H = 4 and was replaced by an asserted int64 range for det/Nc/Ns plus a float64 prefilter with exact Python-int re-test of the circle '
       f'equation. Full details, verdict and overflow-guard statement: `REPORT_H4.md`; code `torsion_coset_probe_H4.py`; data '
       f'`results/torsion_coset_H4_summary.json`, `results/torsion_coset_H4_examples.json`, `results/partial_H4/`.', '']
if marker in rep: rep = rep[:rep.index(marker)]
open(os.path.join(HERE, 'REPORT.md'), 'w').write(rep.rstrip('\n') + '\n\n' + '\n'.join(sec))
print('REPORT_H4.md written; REPORT.md appended;', tag)
