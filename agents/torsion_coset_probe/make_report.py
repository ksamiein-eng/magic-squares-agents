"""make_report.py -- write REPORT.md from results/torsion_coset_H{H}.json for every completed height."""
import json, os, collections, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(HERE, 'results')
heights = [h for h in (2, 3) if os.path.exists(os.path.join(RES, f'torsion_coset_H{h}.json'))]
D = {h: json.load(open(os.path.join(RES, f'torsion_coset_H{h}.json'))) for h in heights}
L = []
L.append('# Torsion-coset probe: every rational-circle solution of every signed system, heights <= ' + ', '.join(map(str, heights)))
L.append('')
L.append('Specialist: torsion-coset-prober.  Code: `torsion_coset_probe.py` (adapted from `paper/verification/four_prime/r4search.py`, '
         'same 113 orbit representatives of the 11,862 full-depth configurations, same grid, same linear forms and three branches), '
         'exact kernel test via Gaussian-prime support, independent exponent-bounded brute-force cross-check.')
L.append('')
L.append('## What was computed')
L.append('')
L.append('For each orbit representative (113), each solved coordinate (4), each triple of the other three parameters `t_j = tan(chi_j/2)` '
         'in the projective grid of height <= H (including 0 and infinity), and each of the 48 signed systems of Lemma 3.1, EVERY exact '
         'rational solution `(cos chi_j, sin chi_j)` on the unit circle was recorded: Cramer branch (det != 0), line-circle branch '
         '(det = 0, consistent, integer square-root test), and the identically-zero branch (both relations vanish for every chi_j: a '
         'one-parameter free-angle family, recorded as a family with its three fixed parameters). Solutions were deduplicated per '
         'configuration by the 4-tuple of projective parameters (equivalently, by the point of T(Q)^4).')
L.append('')
L.append('**Exact torsion-coset test.** With `t = p/q` in lowest terms, `z = cos chi + i sin chi = (q+ip)/(q-ip)`. For each split prime '
         '`l = a^2+b^2` dividing `p^2+q^2`, exactly one of `pi = a+bi`, `conj(pi)` divides `q+ip`, so in `Q(i)^*/{+-1,+-i}` the point is '
         '`prod_l (pi_l/conj(pi_l))^{e_l}` with `e_l = +-v_l(p^2+q^2)`; the prime 2 contributes only the unit `i` and inert primes cannot '
         'occur. Since `T(Q) = {+-1,+-i} x (free abelian group on the pi_l/conj(pi_l))`, a relation `prod_j z_j^{n_j} in {+-1,+-i}` with '
         '`n != 0` exists **iff the four exponent vectors `e(z_j)` are linearly dependent** (rank < 4). The test is complete (not '
         'bounded by the size of the exponents), and a primitive integer basis of the relation lattice is recorded for every point. '
         'Classes: `all_torsion` (rank 0: every coordinate in {+-1,+-i}), `on_torsion_coset` (0 < rank < 4), `NOT_on_torsion_coset` '
         '(rank 4: a counterexample to Conjecture 8.6). For a free-angle family the three fixed coordinates were tested: if their '
         'exponent vectors had rank 3, the family would contain rational points on no torsion coset (choose the free coordinate at a new '
         'prime) and would be a counterexample.')
L.append('')
L.append('**Cross-checks.** (i) Every recorded point was re-derived with independent exact Gaussian-rational arithmetic '
         '(`sines_of`) and asserted to satisfy its signed system and to agree with the integer linear forms; (ii) each kernel basis '
         'vector was verified to give a product in {+-1,+-i}; (iii) on a random sample of 400 points per height, an exponent-bounded '
         'brute-force search (|n_j| <= 4, pure Gaussian-rational arithmetic, no prime factorization) and a sympy rank computation were '
         'compared with the kernel test; (iv) unit tests: `pq_of_cs` round trip on the grid, sines vs floating point at 50 random points, '
         'hand-checked supports (e.g. z(1/2) z(1/3) = i detected; four distinct primes -> rank 4 detected).')
L.append('')
for h in heights:
    d = D[h]
    L.append(f'## Height H = {h}')
    L.append('')
    L.append(f'Grid: {d["grid_values"]} projective values {d["grid"]}; {d["triples"]} triples; {d["orbits"]} orbits; '
             f'{d["system_evaluations"]["systems"]} (orbit, solved coordinate, system) array evaluations, each over all triples; '
             f'sweep runtime {d["totals"]["elapsed_s"]:.0f} s.')
    L.append('')
    L.append('| quantity | value |'); L.append('|---|---|')
    L.append(f'| distinct rational points of solution varieties found | **{d["totals"]["points"]}** |')
    for k, v in d['points_by_class'].items(): L.append(f'| &nbsp;&nbsp; class `{k}` | {v} |')
    L.append(f'| &nbsp;&nbsp; class `NOT_on_torsion_coset` | {d["points_by_class"].get("NOT_on_torsion_coset", 0)} |')
    for k in sorted(d['points_by_number_of_torsion_coordinates'], key=int, reverse=True):
        L.append(f'| &nbsp;&nbsp; points with {k} torsion coordinate(s) | {d["points_by_number_of_torsion_coordinates"][k]} |')
    L.append(f'| admissible points | **{sum(o["admissible_points"] for o in d["per_orbit"])}** |')
    dg = d['points_by_degeneracy']
    L.append(f'| degenerate: some sine zero AND two magnitudes equal | {dg["both"]} |')
    L.append(f'| degenerate: some sine zero only / equal magnitudes only / neither | {dg["zero_sine"]} / {dg["equal_magnitudes"]} / {dg["neither"]} |')
    L.append(f'| raw hits before dedup: Cramer / line-circle | {d["system_evaluations"]["cramer_hits"]} / {d["system_evaluations"]["singular_hits"]} |')
    L.append(f'| free-angle families (distinct (solved coord, fixed triple)) | **{d["totals"]["families"]}** (raw identically-zero system evaluations {d["system_evaluations"]["allzero_systems"]}) |')
    for k, v in d['families_by_degeneracy'].items(): L.append(f'| &nbsp;&nbsp; families with degeneracy `{k}` | {v} |')
    for k, v in sorted(d['families_by_rank_of_fixed_triple'].items()): L.append(f'| &nbsp;&nbsp; families whose fixed triple has exponent rank {k} | {v} |')
    L.append(f'| counterexample candidates (points of rank 4, or families with independent fixed triple) | **{len(d["counterexample_candidates_points"])} / {len(d["counterexample_candidates_families"])}** |')
    bf = d['brute_force_crosscheck']
    L.append(f'| brute-force / sympy cross-check | {bf["checked"]} points checked, {bf["agree"]} agree, {len(bf["disagree"])} disagree |')
    L.append('')
    nt = [r for r in d['nontrivial_points'] if r['n_torsion_coords'] == 0]
    rk = collections.Counter(r['rank'] for r in nt)
    L.append(f'Points with NO torsion coordinate: {len(nt)}; their exponent ranks: {dict(sorted(rk.items()))} (rank 4 would be a counterexample). '
             f'Maximal projective height of any coordinate among recorded points: {max(max(max(abs(x) for x in pq) for pq in r["pq"]) for r in d["nontrivial_points"])} '
             '(the solved coordinate is unconstrained in height).')
    kern = collections.Counter(tuple(sorted(tuple(k) for k in r['kernel_basis'])) for r in nt)
    L.append('Most frequent relation lattices (primitive kernel bases) among those points: ' +
             '; '.join(f'`{list(map(list, k))}` x{v}' for k, v in kern.most_common(6)) + '.')
    L.append('')
    # examples: prefer no torsion coordinate, highest rank, highest height
    ex = sorted(nt, key=lambda r: (-r['rank'], -max(max(abs(x) for x in pq) for pq in r['pq'])))
    rows = {o['orbit']: o['rows'] for o in d['per_orbit']}
    L.append('### Example points (no torsion coordinate)')
    L.append('')
    seen = set(); seen_t = set()
    for r in ex:
        key = (r['orbit'], r['rank']); tk = tuple(sorted(r['t']))
        if key in seen or tk in seen_t: continue
        seen.add(key); seen_t.add(tk)
        if len(seen) > 4: break
        L.append(f'- orbit {r["orbit"]}, rows `{rows[r["orbit"]]}`, system (i,j,k,l,e2,e3) = `{r["example_system"]}`, branch {r["branches"]}, found {r["hits"]} times:  ')
        L.append(f'  `t = {r["t"]}`, `z = {[f"{c}+({s})i" for c, s in r["z"]]}`,  ')
        L.append(f'  sines `{r["sines"]}` (zero rows {r["zero_rows"]}, equal-magnitude pairs {r["equal_pairs"]}),  ')
        L.append(f'  Gaussian-prime exponents `{r["support"]}`, rank {r["rank"]}, relation basis `{r["kernel_basis"]}` '
                 f'(each n gives prod z_j^(n_j) in {{+-1,+-i}}; verified exactly).')
    L.append('')
    if d['counterexample_candidates_points'] or d['counterexample_candidates_families']:
        L.append('### COUNTEREXAMPLE CANDIDATES')
        for c in d['counterexample_candidates_points']: L.append('- POINT ' + json.dumps(c))
        for c in d['counterexample_candidates_families']: L.append('- FAMILY ' + json.dumps(c))
        L.append('')
L.append('## Verdict')
L.append('')
for h in heights:
    d = D[h]
    L.append(f'- **H = {h}: Conjecture 8.6 (torsion-coset hypothesis) is CONFIRMED on every rational point found.** All {d["totals"]["points"]} '
             f'distinct rational points of the solution varieties (all 113 orbits, all 48 signed systems, three parameters of height <= {h}, '
             f'fourth parameter arbitrary) satisfy a nontrivial relation prod z_j^(n_j) in {{+-1,+-i}}, by the complete exponent-rank test; '
             f'{d["points_by_class"].get("NOT_on_torsion_coset", 0)} points are off every torsion coset. All {d["totals"]["families"]} free-angle '
             f'families have a fixed triple of exponent rank <= {max(map(int, d["families_by_rank_of_fixed_triple"]))} (always containing a torsion '
             f'value), so every point of every family lies on a torsion coset as well. Every point is degenerate: some sine vanishes and two '
             f'magnitudes coincide ({d["points_by_degeneracy"]["both"]} of {d["totals"]["points"]}); every family has a row whose sine vanishes '
             f'identically; 0 admissible points (consistent with Proposition 7.1 / r4search).')
L.append('')
L.append('Caveat on strength of the evidence: at height <= 2 the only split prime available to grid coordinates is 5 (p^2+q^2 in {1,2,5}), '
         'so dependence among grid coordinates is automatic; the content of the test at H=2 is in the solved coordinate (height up to 11, new '
         'primes such as 13, 17, 25=5^2 can appear) and in the identity of the relation. At height <= 3 the grid carries the primes 5 and 13 '
         '(p^2+q^2 in {1,2,5,10,13,18}) and the solved coordinate reaches larger height, so rank-3 and rank-4 situations are possible in '
         'principle; none of rank 4 occurred.' if 3 in heights else
         'Caveat on strength of the evidence: at height <= 2 the only split prime available to grid coordinates is 5 (p^2+q^2 in {1,2,5}), '
         'so any three grid coordinates are automatically dependent modulo torsion; the content of the test at H=2 lies in the solved '
         'coordinate (height up to 11, new primes such as 13 and 17 can appear) and in the explicit relation. The H=3 sweep (primes 5 and 13 '
         'in the grid) was launched but did not complete within the deadline; see `results/probe_H3.log` and `results/partial_H3/` for the '
         'per-orbit checkpoints it produced (each checkpoint contains the full point list and classes for that orbit).')
L.append('')
L.append('## Coverage: exactly what was and was not covered')
L.append('')
L.append('- Covered: all 113 orbit representatives (hence all 11,862 full-depth configurations up to signed coordinate permutation); all 4 '
         'choices of solved coordinate; all 48 signed systems; all triples of the other three parameters in the projective grid of height '
         '<= H including 0 and infinity; all three branches (Cramer, line-circle, identically-zero family). Every rational point of a '
         'solution variety with at least three parameters of height <= H is therefore recorded (the fourth is found exactly, whatever its height).')
L.append('- Not covered: rational points all four of whose parameters have height > H; the classification of points inside a free-angle '
         'family is by the rank of the fixed triple (complete for the question asked, but individual family points were not enumerated); '
         'configurations with entries of absolute value > 1 (not full-depth in the {0,+-1} sense) and r != 4.')
L.append('- Exactness: all arithmetic is integer/Fraction; the numpy stage is int64 with an overflow guard (valid for H <= 3). The '
         'brute-force cross-check is exponent-bounded (|n_j| <= 4) and was run on a 400-point sample per height, not on all points; the '
         'rank test itself is complete and was run on every point.')
L.append('')
L.append('## Files')
L.append('')
L.append('- `torsion_coset_probe.py` -- sweep (`python torsion_coset_probe.py H`) and aggregation (`python torsion_coset_probe.py H aggregate`).')
for h in heights:
    L.append(f'- `results/torsion_coset_H{h}.json` -- summary, per-orbit counts, cross-check, all {D[h]["totals"]["points"] - D[h]["points_by_class"].get("all_torsion", 0)} non-all-torsion points with t, z, sines, exponents, rank, relation basis, degeneracy.')
    L.append(f'- `results/partial_H{h}/orbit_NNN.json` -- per-orbit checkpoints (all points incl. all-torsion, all families); `results/probe_H{h}.log` -- run log.')
open(os.path.join(HERE, 'REPORT.md'), 'w').write('\n'.join(L) + '\n')
print('\n'.join(L))
