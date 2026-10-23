"""make_report_H5.py -- write REPORT_H5.md from results/torsion_coset_H5_summary.json (+ _examples.json, trichotomy_H5_exceptions.json)
and append an 'Iteration 3 (H=5)' section to REPORT.md.  Handles a partial run (orbits_completed < 113) explicitly.
Usage: python make_report_H5.py "<wall time string>" """
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, 'results')
d = json.load(open(os.path.join(RES, 'torsion_coset_H5_summary.json')))
ex = json.load(open(os.path.join(RES, 'torsion_coset_H5_examples.json')))
tx = json.load(open(os.path.join(RES, 'trichotomy_H5_exceptions.json')))
h4 = json.load(open(os.path.join(RES, 'torsion_coset_H4_summary.json')))
wall = sys.argv[1] if len(sys.argv) > 1 else 'n/a'
partial = d['partial']; done = d['orbits_completed']; N = d['orbits']
tag = f'PARTIAL: {done}/{N} orbits' if partial else f'COMPLETE: {done}/{N} orbits'
nc = d['points_by_class'].get('NOT_on_torsion_coset', 0); ncf = len(d['counterexample_candidates_families'])
tri = d['points_by_trichotomy']; pt = d['rank3_prediction_test']; og = d['overflow_guard']
done_orbits = sorted(o['orbit'] for o in d['per_orbit'])
h4_by_orbit = {o['orbit']: o for o in h4['per_orbit']}
L = []
L.append(f'# Torsion-coset probe, iteration 3: height H = 5, trichotomy and rank-3 prediction test ({tag})')
L.append('')
L.append('Specialist: torsion-coset-prober (iteration 3). Code: `torsion_coset_probe_H5.py` (iteration-2 `torsion_coset_probe_H4.py` with the '
         'H=5 overflow treatment, the trichotomy classification of every point, independent sympy re-verification of any type (ii)/(iii) point, '
         'and the rank-3 prediction test; the sweep, the three branches, the exact Gaussian-prime kernel test and the cross-checks are unchanged). '
         'Summary: `results/torsion_coset_H5_summary.json`; trichotomy exceptions: `results/trichotomy_H5_exceptions.json`; examples: '
         '`results/torsion_coset_H5_examples.json`; per-orbit checkpoints: `results/partial_H5/orbit_NNN.json`; log: `results/probe_H5.log`.')
L.append('')
L.append('## Headline')
L.append('')
if tri['ii'] == 0 and tri['iii'] == 0:
    L.append(f'**Every one of the {d["totals"]["points"]} rational points recorded at H = 5 ({done}/{N} orbits) is of trichotomy type (i): some sine vanishes.** '
             f'Type (ii) (admissible, would refute rigidity): 0. Type (iii) (all sines nonzero and A = 2B, would refute the vanishing-sine conjecture): 0. '
             f'`results/trichotomy_H5_exceptions.json` is an empty list.' + (' (PARTIAL: over the completed orbits only.)' if partial else ''))
else:
    L.append(f'**TRICHOTOMY EXCEPTIONS FOUND: type (ii) = {tri["ii"]}, type (iii) = {tri["iii"]}** -- full coordinates and independent sympy '
             f're-verification in `results/trichotomy_H5_exceptions.json` ({len(tx["exceptions"])} records). See the section "Trichotomy exceptions" below.')
L.append(f'Rank-3 prediction test: orbits with rank-3 points = {pt["orbits_with_rank3_points"]}; all inside the 23 predicted orbits: '
         f'**{"YES" if pt["prediction_holds"] else "NO -- violations " + str(pt["rank3_orbits_outside_prediction"])}**; '
         f'{pt["n_predicted_orbits_showing_rank3"]} of the 23 predicted orbits now show rank 3 (H = 4: 2 of 23). Max exponent rank: {d["max_exponent_rank_observed"]}; rank-4 points: {d["points_by_exponent_rank"].get("4", 0)}.')
L.append('')
L.append('## Coverage')
L.append('')
L.append(f'Grid: {d["grid_values"]} projective values `{" ".join(d["grid"])}` (height <= 5 incl. 0 and infinity), {d["triples"]} triples; '
         f'all 4 solved coordinates; all 48 signed systems; three branches (Cramer, line-circle, identically-zero family). '
         f'Orbits completed: **{done} of {N}**' + (f' (run cut at the 70-minute budget; every number below is over the completed orbits {done_orbits} only).' if partial else ' (all 11,862 full-depth configurations up to signed coordinate permutation).'))
L.append(f'Grid norms p^2+q^2: {d["grid_norms_p2_plus_q2"]} (maximum 41 = 5^2+4^2, not 50, since 5/5 is not in lowest terms); split primes carried by grid coordinates: '
         f'**{d["split_primes_in_grid"]}** (new at H=5 relative to H=4: 29 from 5/2, 2/5 and 41 from 5/4, 4/5; also 26 = 2*13 from 5/1, 1/5 and 34 = 2*17 from 5/3, 3/5). '
         f'Split primes occurring in any exponent vector, including the solved coordinate: {d["split_primes_in_all_supports_incl_solved_coord"]}.')
L.append('')
L.append('## Counts')
L.append('')
L.append('| quantity | H = 4 (iteration 2) | H = 5 (this run) |'); L.append('|---|---|---|')
L.append(f'| orbits | 113 | {done}{" (partial)" if partial else ""} |')
L.append(f'| distinct rational points of solution varieties | {h4["totals"]["points"]} | **{d["totals"]["points"]}** |')
for k in ['all_torsion', 'on_torsion_coset', 'NOT_on_torsion_coset']:
    L.append(f'| &nbsp;&nbsp; class `{k}` | {h4["points_by_class"].get(k, 0)} | {d["points_by_class"].get(k, 0)} |')
for k in sorted(d['points_by_number_of_torsion_coordinates'], key=int, reverse=True):
    L.append(f'| &nbsp;&nbsp; points with {k} torsion coordinate(s) | {h4["points_by_number_of_torsion_coordinates"].get(k, 0)} | {d["points_by_number_of_torsion_coordinates"][k]} |')
L.append(f'| admissible points | {h4["admissible_points"]} | **{d["admissible_points"]}** |')
L.append(f'| trichotomy type (i) / (ii) / (iii) | {h4["totals"]["points"]} / 0 / 0 (re-derived: all H4 points had a zero sine) | **{tri["i"]} / {tri["ii"]} / {tri["iii"]}** |')
dg = d['points_by_degeneracy']; dg4 = h4['points_by_degeneracy']
L.append(f'| degenerate: some sine zero AND two magnitudes equal | {dg4["both"]} | {dg["both"]} |')
L.append(f'| zero sine only / equal magnitudes only / neither | {dg4["zero_sine"]} / {dg4["equal_magnitudes"]} / {dg4["neither"]} | {dg["zero_sine"]} / {dg["equal_magnitudes"]} / {dg["neither"]} |')
L.append(f'| raw hits before dedup: Cramer / line-circle | {h4["system_evaluations"]["cramer_hits"]} / {h4["system_evaluations"]["singular_hits"]} | {d["system_evaluations"]["cramer_hits"]} / {d["system_evaluations"]["singular_hits"]} |')
L.append(f'| prefilter candidates (Cramer) -> exact hits | {h4["system_evaluations"].get("prefilter_candidates", 0)} -> {h4["system_evaluations"]["cramer_hits"]} (float only) | {d["system_evaluations"].get("prefilter_candidates", 0)} -> {d["system_evaluations"]["cramer_hits"]} (mod 2^64 and float) |')
L.append(f'| free-angle families | {h4["totals"]["families"]} | **{d["totals"]["families"]}** |')
for k, v in d['families_by_degeneracy'].items(): L.append(f'| &nbsp;&nbsp; families with degeneracy `{k}` | {h4["families_by_degeneracy"].get(k, 0)} | {v} |')
for k in sorted(d['families_by_rank_of_fixed_triple'], key=int):
    L.append(f'| &nbsp;&nbsp; families with fixed-triple exponent rank {k} | {h4["families_by_rank_of_fixed_triple"].get(k, 0)} | {d["families_by_rank_of_fixed_triple"][k]} |')
L.append(f'| families by trichotomy | all `row_identically_zero` | {d["families_by_trichotomy"]} |')
L.append(f'| counterexample candidates (points / families) | 0 / 0 | **{nc} / {ncf}** |')
L.append(f'| brute-force + sympy cross-check (sample) | 452/452 agree | {d["brute_force_crosscheck"]["agree"]}/{d["brute_force_crosscheck"]["checked"]} agree, {d["brute_force_crosscheck"]["n_disagree"]} disagree |')
L.append(f'| sweep CPU time (sum over orbits) / wall | 2097 s / 368 s (6 workers) | {d["totals"]["elapsed_s"]:.0f} s / {wall} (6 workers) |')
L.append('')
L.append('## Trichotomy classification (Theorem "Trichotomy on a signed system")')
L.append('')
L.append('Every recorded point was classified from its exact sines (Fractions) on EVERY signed system it satisfies: type (i) if some sine is 0; '
         'otherwise A = max(|s_k|,|s_l|), B = min(|s_k|,|s_l|) is computed for each system (i,j,k,l,eps,eta) the point satisfies, the identity '
         '{|s_i|,|s_j|} = {A+B, |A-B|} is asserted, and the point is type (iii) if A = 2B and type (ii) (admissible) otherwise; the script asserts '
         'that "admissible" (four nonzero distinct magnitudes with the Lemma-roles structure) and "A = 2B" are complementary on every system, i.e. '
         'that the trichotomy is exhaustive and exclusive on the data. Every free-angle family has a row whose sine vanishes identically, so all its points are type (i).')
L.append('')
L.append(f'Overall: type (i) **{tri["i"]}**, type (ii) **{tri["ii"]}**, type (iii) **{tri["iii"]}** (of {d["totals"]["points"]} points).')
L.append('')
L.append('| orbit | rows | points | type (i) | type (ii) | type (iii) | exponent ranks |'); L.append('|---|---|---|---|---|---|---|')
for o in sorted(d['per_orbit'], key=lambda o: o['orbit']):
    t = o['points_by_trichotomy']
    L.append(f'| {o["orbit"]} | {o["rows"]} | {o["n_points"]} | {t["i"]} | {t["ii"]} | {t["iii"]} | {dict(sorted(o["points_by_rank"].items()))} |')
L.append('')
L.append('## Trichotomy exceptions (type (ii) or (iii) points)')
L.append('')
if not tx['exceptions']:
    L.append('None. `results/trichotomy_H5_exceptions.json` holds an empty list. The vanishing-sine conjecture (and rigidity) survive every '
             f'rational point with at least three parameters of height <= 5{" on the completed orbits" if partial else ""}.')
else:
    L.append('| orbit | type | t | sines | A, B | independent sympy check |'); L.append('|---|---|---|---|---|---|')
    for e in tx['exceptions'][:50]:
        L.append(f'| {e["orbit"]} | {e["trichotomy_type"]} | {e["t"]} | {e["sines"]} | {e["AB_example"]} | {e["independent_sympy_check"]} |')
L.append('')
L.append('## Exponent-rank distribution and the rank-3 prediction test')
L.append('')
L.append('| rank | H = 3 | H = 4 | H = 5 |'); L.append('|---|---|---|---|')
h3r = {'0': 12928, '1': 204672, '2': 55424}
for k in ['0', '1', '2', '3', '4']:
    L.append(f'| {k} | {h3r.get(k, 0)} | {h4["points_by_exponent_rank"].get(k, 0)} | {d["points_by_exponent_rank"].get(k, 0)} |')
L.append('')
L.append(f'Maximal exponent rank observed at H = 5: **{d["max_exponent_rank_observed"]}**; rank-4 points (off every torsion coset): {d["points_by_exponent_rank"].get("4", 0)}.')
L.append('')
L.append(f'The degeneracy-rank lemma predicts that rank-3 points can occur only in the 23 orbits satisfying the parallel-triple criterion '
         f'(`results/rank_bound_prediction.json`): {pt["predicted_orbits_parallel_triple_criterion"]}.')
L.append(f'- Orbits with rank-3 points at H = 5: **{pt["orbits_with_rank3_points"]}** ({len(pt["orbits_with_rank3_points"])} orbits; H = 4: [0, 54]).')
L.append(f'- Rank-3 orbits outside the prediction: **{pt["rank3_orbits_outside_prediction"]}** -> prediction holds: **{pt["prediction_holds"]}**.')
L.append(f'- Predicted orbits now showing rank 3: **{pt["n_predicted_orbits_showing_rank3"]} of 23**; predicted orbits completed in this run: {len(pt["predicted_orbits_completed_in_this_run"])} of 23; '
         f'predicted but not (yet) showing rank 3: {pt["predicted_orbits_not_yet_showing_rank3"]}.')
r3 = [(o['orbit'], o['points_by_rank'].get('3', 0), h4_by_orbit.get(o['orbit'], {}).get('points_by_rank', {}).get('3', 0)) for o in d['per_orbit'] if o['points_by_rank'].get('3', 0)]
if r3:
    L.append('')
    L.append('| orbit | rank-3 points at H = 5 | rank-3 points at H = 4 |'); L.append('|---|---|---|')
    for o, a, b in sorted(r3): L.append(f'| {o} | {a} | {b} |')
L.append('')
L.append('## Verdict on Conjecture 8.6 (torsion-coset hypothesis) at H <= 5')
L.append('')
if nc == 0 and ncf == 0:
    L.append(f'**{"PARTIAL (" + str(done) + "/" + str(N) + " orbits): " if partial else ""}CONFIRMED on every rational point found.** All {d["totals"]["points"]} distinct rational points of the '
             f'solution varieties ({done} orbit representatives, all 48 signed systems, three parameters of height <= 5, fourth parameter '
             f'arbitrary) satisfy a nontrivial relation prod z_j^(n_j) in {{+-1,+-i}} by the complete exponent-rank test; 0 points are off every '
             f'torsion coset. All {d["totals"]["families"]} free-angle families have a fixed triple of exponent rank <= {max(map(int, d["families_by_rank_of_fixed_triple"]))} '
             f'(< 3), so every point of every family lies on a torsion coset as well. Admissible points: {d["admissible_points"]}.')
else:
    L.append(f'**COUNTEREXAMPLE CANDIDATES FOUND: {nc} points, {ncf} families** -- see `counterexample_candidates_*` in the summary JSON.')
L.append('')
L.append('## Examples: points with no torsion coordinate and the highest rank seen')
L.append('')
L.append('| orbit | t = (t_1..t_4) | rank | relation basis n (prod z_j^n_j in {+-1,+-i}) | supports |'); L.append('|---|---|---|---|---|')
for r in ex['examples'][:12]:
    L.append(f'| {r["orbit"]} | {r["t"]} | {r["rank"]} | {r["kernel_basis"]} | {r["support"]} |')
L.append('')
L.append('## Overflow-guard statement (requirement 1)')
L.append('')
L.append('Re-derived for H = 5. Grid norms p^2+q^2 <= 41 (the pair (5,5) is not coprime, so 50 does not occur), hence with three grid coordinates '
         '`Dfull = prod (p_j^2+q_j^2) <= 41^3 = 68921`; every row coefficient is bounded by Dfull; the signed-system coefficients A, B, C are sums of '
         'three row coefficients, `<= 3*68921 = 206763`; and `det, Nc, Ns` are two-term products, `<= 2*206763^2 = 8.55e10`. These are exact in int64 '
         '(limit 9.22e18) AND exactly representable in float64 (< 2^53 = 9.0e15); the script asserts both bounds from the ACTUAL per-orbit maxima '
         f'(`2*(3*mx)^2 < 2^62` and `< 2^53`). Observed maxima: row coefficient {og["max_abs_row_coeff"]} (bound 68921), |det|,|Nc|,|Ns| <= {og["max_abs_det_Nc_Ns"]} '
         f'(bound {og["bound_det_Nc_Ns"]}). The squares in the circle test `Nc^2+Ns^2 == det^2` reach ~7.3e21 > 2^63 and are NOT exact in int64; the test is '
         'therefore done as two NECESSARY prefilters followed by an exact re-test: (a) the identity evaluated in wrapping int64 arithmetic, i.e. exactly '
         'modulo 2^64 (a true solution satisfies it identically, so it is never rejected); (b) the float64 identity with tolerance '
         f'`8*2^-52*m^2 + 1`, m = actual max of |det|,|Nc|,|Ns| in the system (true rounding error < 5*2^-52*m^2; largest tolerance used {og["max_prefilter_tol"]:.3g}); '
         f'then (c) every survivor is re-tested with exact Python ints. Candidates after (a)+(b): {d["system_evaluations"].get("prefilter_candidates", 0)}; exact hits: '
         f'{d["system_evaluations"]["cramer_hits"]} (the mod-2^64 filter removes essentially all spurious candidates that the H=4 float-only filter let through). '
         'All other arithmetic (line-circle branch, point verification, sines, kernel test, trichotomy, independent sympy check) is Python int / Fraction / sympy Rational. No overflow was silently accepted.')
L.append('')
L.append('## Runtime and files')
L.append('')
L.append(f'Sweep: {d["totals"]["elapsed_s"]:.0f} s CPU over {done} orbits, wall {wall} with 6 worker processes (H = 4: 2097 s CPU / 368 s wall). '
         'Output deliberately small: per-orbit checkpoints hold counts, distributions, trichotomy tallies, exceptions, counterexample candidates, <= 20 examples '
         'and the in-orbit cross-check sample (no full point lists).')
L.append('')
L.append('- `results/torsion_coset_H5_summary.json` -- H4 schema plus `points_by_trichotomy`, `families_by_trichotomy`, `n_trichotomy_exceptions`, '
         '`rank3_prediction_test`, per-orbit `points_by_trichotomy`, and the extended `overflow_guard` block.')
L.append('- `results/trichotomy_H5_exceptions.json` -- every type (ii)/(iii) point with full coordinates and independent sympy re-verification (empty list if none).')
L.append('- `results/torsion_coset_H5_examples.json` -- up to 20 points with no torsion coordinate and the highest exponent rank, with relation basis.')
L.append('- `results/partial_H5/orbit_NNN.json`, `results/probe_H5.log`, `results/run_H5.out`.')
open(os.path.join(HERE, 'REPORT_H5.md'), 'w').write('\n'.join(L) + '\n')

rep = open(os.path.join(HERE, 'REPORT.md')).read()
marker = '## Iteration 3 (H=5)'
sec = [marker, '',
       f'Third iteration extended the sweep to projective height H = 5 (40 grid values, 64000 triples, grid norms up to 41, new grid split primes 29 and 41; '
       f'all 4 solved coordinates, all 48 signed systems) -- {tag}. Results: **{d["totals"]["points"]} points**, classes {d["points_by_class"]}, exponent ranks '
       f'{d["points_by_exponent_rank"]} (max rank {d["max_exponent_rank_observed"]}), {d["totals"]["families"]} families with fixed-triple ranks '
       f'{d["families_by_rank_of_fixed_triple"]}, counterexample candidates {nc} points / {ncf} families, admissible points {d["admissible_points"]}. '
       f'**Trichotomy** (every point classified on every system it satisfies): type (i) {tri["i"]}, type (ii) {tri["ii"]}, type (iii) {tri["iii"]} -- '
       + ('the vanishing-sine conjecture holds on every recorded point. ' if tri['ii'] == 0 and tri['iii'] == 0 else 'EXCEPTIONS FOUND, see `results/trichotomy_H5_exceptions.json`. ')
       + f'**Rank-3 prediction test**: rank-3 orbits {pt["orbits_with_rank3_points"]}, all inside the 23 predicted orbits: {pt["prediction_holds"]}; '
       f'{pt["n_predicted_orbits_showing_rank3"]}/23 predicted orbits now show rank 3. Overflow guard re-derived (Dfull <= 41^3, det/Nc/Ns <= 8.55e10 exact in int64 and float64; '
       f'circle test by mod-2^64 and float64 prefilters plus exact Python-int re-test). Full details: `REPORT_H5.md`; code `torsion_coset_probe_H5.py`; data '
       f'`results/torsion_coset_H5_summary.json`, `results/trichotomy_H5_exceptions.json`, `results/partial_H5/`.', '']
if marker in rep: rep = rep[:rep.index(marker)]
open(os.path.join(HERE, 'REPORT.md'), 'w').write(rep.rstrip('\n') + '\n\n' + '\n'.join(sec))
print('REPORT_H5.md written; REPORT.md appended;', tag)
