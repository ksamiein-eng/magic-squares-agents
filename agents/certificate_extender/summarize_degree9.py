#!/usr/bin/env python3
"""Collect witness-prime, factor, timing and verification statistics for REPORT_sum9.md."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent/'results'
cert = json.loads((ROOT/'certificate_degree9.json').read_text())
ver = json.loads((ROOT/'verification_degree9_stdlib.json').read_text())
base_ids = {c['id'] for c in json.loads((ROOT/'certificate_degree8.json').read_text())['cases']}
by_id = {f['id']: f for f in cert['factor_catalog']}
new_cases = [c for c in cert['cases'] if c['id'] not in base_ids]
new_factor_ids = set()
for c in new_cases:
    for s in c['systems']:
        for r in s['factors']:
            new_factor_ids.add(r['factor_id'])
base_factor_ids = set()
for c in cert['cases']:
    if c['id'] in base_ids:
        for s in c['systems']:
            for r in s['factors']:
                base_factor_ids.add(r['factor_id'])
only_new = new_factor_ids - base_factor_ids
primes_new = Counter(by_id[k]['prime'] for k in only_new if by_id[k]['type'] == 'no_rational_root')
primes_all = Counter(f['prime'] for f in cert['factor_catalog'] if f['type'] == 'no_rational_root')
degs_new = Counter(len(by_id[k]['coefficients_high_to_low'])-1 for k in only_new)
linear = [(k, by_id[k]['root']) for k in new_factor_ids if by_id[k]['type'] == 'rational_root']
print('certificate status', cert['status'], 'cases', len(cert['cases']), 'systems', sum(len(c['systems']) for c in cert['cases']))
print('catalog factors', len(cert['factor_catalog']), 'rootless', sum(f['type']=='no_rational_root' for f in cert['factor_catalog']))
print('factors first appearing in sum-9 cases', len(only_new), 'of', len(new_factor_ids), 'used by sum-9 cases')
print('witness primes (new factors)', sorted(primes_new.items()))
print('witness primes (whole catalog)', sorted(primes_all.items()))
print('max witness prime overall', max(primes_all))
print('degree distribution of new factors', sorted(degs_new.items()))
print('max new factor degree', max(degs_new))
print('linear factors used by sum-9 cases', sorted(set(tuple(r) for _, r in linear)))
print()
print('| case | (k,l;m,n) | build s | max res deg | D bound | determinants | distinct factors | rootless | removed t |')
print('|---|---|---|---|---|---|---|---|---|')
vmap = {c['id']: c for c in ver['cases']}
tot_build = 0
for c in new_cases:
    v = vmap[c['id']]
    maxdeg = max(max(m[0] for m, _ in s['resultant']) for s in c['systems'])
    tot_build += c['build_seconds']
    print(f"| {c['id']} | ({c['bounds'][0]},{c['bounds'][1]};{c['drops'][0]},{c['drops'][1]}) | {c['build_seconds']:.1f} | {maxdeg} | {v['max_determinant_degree_bound']} | {v['exact_determinant_evaluations']} | {v['distinct_factors']} | {v['rootless_factors']} | {v['removed_t_systems']} |")
print()
print('total build seconds (sum over cases)', round(tot_build, 1))
print('verifier status', ver['status'], 'missing', ver['missing_cases'], 'systems', ver['total_systems'],
      'determinants', ver['exact_integer_determinants'], 'primes', ver['modular_primes'],
      'catalog', ver['distinct_catalog_factors'], 'rootless', ver['rootless_catalog_factors'],
      'elapsed', ver['elapsed_seconds'])
print('coverage routes', len(ver['normal_form_coverage']), Counter(r['route'] for r in ver['normal_form_coverage']))
sum9 = [r for r in ver['normal_form_coverage'] if sum(r['bounds']) == 9]
print('sum-9 routes', len(sum9), Counter(r['route'] for r in sum9))
for r in ver['normal_form_coverage']:
    if sum(r['bounds']) == 9 and r['route'] == 'direct_certificate':
        pass
fibers = Counter()
for c in ver['cases']:
    if c['id'] not in base_ids:
        for f in c['finite_fibers']:
            fibers[(tuple(f['parameter']), f['kind'])] += 1
        for key, b in c['projective_boundaries'].items():
            fibers[(key, b['kind'])] += 1
print('fiber/boundary degeneracy kinds (sum-9 cases)', sorted(fibers.items(),key=str))
