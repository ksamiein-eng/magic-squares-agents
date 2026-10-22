#!/usr/bin/env python3
"""Generate proof data for the two-prime exponent-sum-nine representatives.

SymPy is a discovery tool, not part of the standard-library acceptance path.
The separate verifier (verify_degree9_stdlib.py) reconstructs all inputs and
checks every identity.

Usage:
  python build_degree9_certificate.py --part NAME CASE_ID [CASE_ID ...]
      compute the listed cases, checkpointing after each one into
      results/degree9_part_NAME.json (resumable; finished cases are skipped)
  python build_degree9_certificate.py --merge
      merge results/certificate_degree8.json with every results/degree9_part_*.json
      into results/certificate_degree9.json (an UNRESOLVED case is recorded, never
      silently dropped; the merged file then carries status UNRESOLVED).
"""
from __future__ import annotations
import argparse
import itertools
import json
import sys
import time
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT/'results'
t, u = sp.symbols('t u', real=True)
WITNESS_PRIME_LIMIT = 257

# Representatives from plan_sum9.py (exact orbit coverage checked there).
NEW_CASES = [('54_m1_n1', 5, 4, 1, 1), ('54_m1_nminus1', 5, 4, 1, -1), ('54_m2_n1', 5, 4, 2, 1), ('54_m2_nminus1', 5, 4, 2, -1), ('54_m1_n3', 5, 4, 1, 3), ('54_m1_nminus3', 5, 4, 1, -3), ('54_m3_n1', 5, 4, 3, 1), ('54_m3_nminus1', 5, 4, 3, -1), ('54_m2_n3', 5, 4, 2, 3), ('54_m2_nminus3', 5, 4, 2, -3), ('54_m4_n1', 5, 4, 4, 1), ('54_m4_nminus1', 5, 4, 4, -1), ('54_m3_n3', 5, 4, 3, 3), ('54_m3_nminus3', 5, 4, 3, -3), ('54_m4_n3', 5, 4, 4, 3), ('54_m4_nminus3', 5, 4, 4, -3), ('63_m1_n1', 6, 3, 1, 1), ('63_m1_nminus1', 6, 3, 1, -1), ('63_m1_n2', 6, 3, 1, 2), ('63_m1_nminus2', 6, 3, 1, -2), ('63_m5_n1', 6, 3, 5, 1), ('63_m5_nminus1', 6, 3, 5, -1), ('63_m5_n2', 6, 3, 5, 2), ('63_m5_nminus2', 6, 3, 5, -2), ('72_m1_n1', 7, 2, 1, 1), ('72_m1_nminus1', 7, 2, 1, -1), ('72_m2_n1', 7, 2, 2, 1), ('72_m2_nminus1', 7, 2, 2, -1), ('72_m3_n1', 7, 2, 3, 1), ('72_m3_nminus1', 7, 2, 3, -1), ('72_m4_n1', 7, 2, 4, 1), ('72_m4_nminus1', 7, 2, 4, -1), ('72_m5_n1', 7, 2, 5, 1), ('72_m5_nminus1', 7, 2, 5, -1), ('72_m6_n1', 7, 2, 6, 1), ('72_m6_nminus1', 7, 2, 6, -1), ('81_m1_n0', 8, 1, 1, 0), ('81_m3_n0', 8, 1, 3, 0), ('81_m5_n0', 8, 1, 5, 0), ('81_m7_n0', 8, 1, 7, 0)]
BY_ID = {c[0]: c for c in NEW_CASES}


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def encode(p, variables):
    return [[list(m), int(c)] for m, c in sp.Poly(p, *variables, domain=sp.ZZ).terms() if c]


def make_numerator(m, bounds):
    z = sp.prod((1+sp.I*(1 if n >= 0 else -1)*v)**(2*abs(n))
                * (1+v*v)**(k-abs(n)) for v, n, k in zip((t,u), m, bounds))
    return sp.expand(sp.im(sp.expand(z)))


def tags():
    return [(i,j,k,l,a,b) for i,j in itertools.combinations(range(4),2)
            for k,l in itertools.permutations([z for z in range(4) if z not in (i,j)])
            for a,b in itertools.product((-1,1), repeat=2)]


def classify_factor(poly):
    """Catalog entry (without id) for an irreducible-over-Q factor from sympy."""
    cs = tuple(int(c) for c in poly.all_coeffs())
    item = {'coefficients_high_to_low': list(cs)}
    if poly.degree() == 1:
        rr = -sp.Rational(cs[1], cs[0])
        item.update(type='rational_root', root=[int(rr.p), int(rr.q)])
        return cs, item, None
    for p in sp.primerange(2, WITNESS_PRIME_LIMIT):
        p = int(p)
        if cs[0] % p == 0:
            continue
        residues = []
        ok = True
        for r in range(p):
            v = 0
            for c in cs:
                v = (v*r + c) % p
            residues.append(v)
            if v == 0:
                ok = False
                break
        if ok:
            item.update(type='no_rational_root', prime=p, residues=residues)
            return cs, item, None
    item.update(type='UNRESOLVED_no_small_prime_witness')
    return cs, item, f'factor of degree {poly.degree()} has no witness prime < {WITNESS_PRIME_LIMIT}'


def build_case(name, a, b, m, n, catalog, log):
    """Return (record, unresolved_messages). catalog: dict coeff-tuple -> item."""
    begin = time.perf_counter()
    freqs = [(a,b),(a,-b),(m,b),(a,n)]
    es = [make_numerator(v,(a,b)) for v in freqs]
    systems = []
    unresolved = []
    timings = []
    for sid, tag in enumerate(tags()):
        s0 = time.perf_counter()
        i,j,k,l,sg,sh = tag
        g1 = sp.expand(es[i]-sg*es[k]-sh*es[l])
        g2 = sp.expand(es[j]-sg*es[k]+sh*es[l])
        require(g1 != 0 and g2 != 0, 'zero input equation needs separate treatment')
        removed = min(min(mon[0] for mon,c in sp.Poly(g,t,u).terms()) for g in (g1,g2))
        f,g = [sp.Poly(sp.cancel(h/t**removed),t,u,domain=sp.ZZ).as_expr() for h in (g1,g2)]
        res = sp.resultant(f,g,u)
        s1 = time.perf_counter()
        if res == 0:
            unresolved.append(f'UNRESOLVED common nonvertical component: {name}, system {sid}')
            systems.append({'id':sid,'assignment':list(tag),'removed_t_power':int(removed),
                            'G1':encode(g1,(t,u)),'G2':encode(g2,(t,u)),
                            'F':encode(f,(t,u)),'G':encode(g,(t,u)),
                            'resultant':[],'constant':0,'factors':[],
                            'status':'UNRESOLVED_zero_resultant'})
            log(f'  {name} system {sid}: ZERO RESULTANT (unresolved)')
            continue
        constant, fs = sp.factor_list(res,t)
        s2 = time.perf_counter()
        refs = []
        for q, e in fs:
            poly = sp.Poly(q,t,domain=sp.ZZ)
            cs = tuple(int(c) for c in poly.all_coeffs())
            if cs not in catalog:
                cs, item, problem = classify_factor(poly)
                catalog[cs] = item
                if problem:
                    unresolved.append(f'{name}, system {sid}: {problem}: {q}')
                    log(f'  {name} system {sid}: {problem}')
            refs.append({'coefficients':list(cs),'exponent':int(e)})
        rec = {'id':sid,'assignment':list(tag),'removed_t_power':int(removed),
               'G1':encode(g1,(t,u)),'G2':encode(g2,(t,u)),
               'F':encode(f,(t,u)),'G':encode(g,(t,u)),
               'resultant':encode(res,(t,)), 'constant':int(constant), 'factors':refs}
        if any(catalog[tuple(r['coefficients'])].get('type','').startswith('UNRESOLVED') for r in refs):
            rec['status'] = 'UNRESOLVED_factor_without_witness'
        systems.append(rec)
        timings.append({'system':sid,'resultant_seconds':round(s1-s0,3),'factor_seconds':round(s2-s1,3),
                        'resultant_degree':int(sp.degree(res,t))})
        if sid % 8 == 7:
            log(f'  {name} system {sid}: res {s1-s0:.1f}s factor {s2-s1:.1f}s deg {sp.degree(res,t)}')
    elapsed = time.perf_counter()-begin
    rec = {'id':name,'bounds':[a,b],'drops':[m,n],'frequencies':freqs,
           'area_numerators':[encode(e,(t,u)) for e in es],'systems':systems,
           'build_seconds':round(elapsed,3),'system_timings':timings}
    if unresolved:
        rec['status'] = 'UNRESOLVED'
        rec['unresolved'] = unresolved
    return rec, unresolved


def run_part(part, case_ids):
    RESULTS.mkdir(exist_ok=True)
    out = RESULTS/f'degree9_part_{part}.json'
    logf = RESULTS/f'build_degree9_{part}.log'
    def log(msg):
        line = f'[{time.strftime("%H:%M:%S")}] {msg}'
        print(line, flush=True)
        with logf.open('a') as fh:
            fh.write(line+'\n')
    if out.exists():
        data = json.loads(out.read_text())
        catalog = {tuple(v['coefficients_high_to_low']): v for v in data['factor_catalog']}
        cases = list(data['cases'])
        log(f'resuming part {part}: {[c["id"] for c in cases]} already done')
    else:
        catalog, cases = {}, []
    done = {c['id'] for c in cases}
    for cid in case_ids:
        require(cid in BY_ID, f'unknown case id {cid}')
        if cid in done:
            continue
        name,a,b,m,n = BY_ID[cid]
        log(f'start {name}')
        rec, unresolved = build_case(name,a,b,m,n,catalog,log)
        cases.append(rec)
        status = 'PARTIAL_GENERATION_NOT_VERIFIED' + (' (contains UNRESOLVED cases)' if any(c.get('status')=='UNRESOLVED' for c in cases) else '')
        out.write_text(json.dumps({'status':status,'part':part,'cases':cases,
                                   'factor_catalog':list(catalog.values())})+'\n')
        log(f'done {name} systems {len(rec["systems"])} seconds {rec["build_seconds"]} unresolved {len(unresolved)}')
    log(f'part {part} complete')


def merge():
    baseline = json.loads((RESULTS/'certificate_degree8.json').read_text())
    require(baseline['schema']=='magic-squares/degree8/v6','unexpected baseline schema')
    catalog = {tuple(c['coefficients_high_to_low']): c for c in baseline['factor_catalog']}
    cases = list(baseline['cases'])
    have = {}
    for part in sorted(RESULTS.glob('degree9_part_*.json')):
        data = json.loads(part.read_text())
        part_catalog = {tuple(v['coefficients_high_to_low']): v for v in data['factor_catalog']}
        for c in data['cases']:
            require(c['id'] not in have, f'case {c["id"]} appears in two parts')
            have[c['id']] = (c, part_catalog)
    unresolved = []
    missing = [c[0] for c in NEW_CASES if c[0] not in have]
    for name,a,b,m,n in NEW_CASES:
        if name not in have:
            continue
        c, part_catalog = have[name]
        for s in c['systems']:
            refs = []
            for r in s['factors']:
                cs = tuple(r['coefficients'])
                if cs not in catalog:
                    item = dict(part_catalog[cs])
                    item = {'id': f'P{len(catalog):04d}', **item}
                    catalog[cs] = item
                refs.append({'factor_id': catalog[cs]['id'], 'exponent': r['exponent']})
            s['factors'] = refs
        if c.get('status') == 'UNRESOLVED':
            unresolved.extend(c['unresolved'])
        cases.append(c)
    status = 'UNRESOLVED' if unresolved else ('PARTIAL_MISSING_CASES' if missing else 'GENERATED_NOT_YET_INDEPENDENTLY_VERIFIED')
    result = {'schema':'magic-squares/degree9/v7',
              'scope':'rational-circle exclusion certificates; full-depth normal forms; all exponent sums <=9',
              'producer':{'python':sys.version.split()[0],'sympy':sp.__version__},
              'status':status,'missing_cases':missing,'unresolved':unresolved,
              'factor_catalog':list(catalog.values()),'cases':cases}
    (RESULTS/'certificate_degree9.json').write_text(json.dumps(result,indent=1)+'\n')
    by_id = {v['id']:v for v in catalog.values()}
    stats = []
    for c in cases:
        used = {q['factor_id'] for s in c['systems'] for q in s['factors']}
        nf = [by_id[k] for k in used if by_id[k]['type']=='no_rational_root']
        stats.append({'id':c['id'],'systems':len(c['systems']),
                      'removed_t_systems':sum(s['removed_t_power']>0 for s in c['systems']),
                      'distinct_factors':len(used),'rootless_factors':len(nf),
                      'rational_t_roots':sorted({str(sp.Rational(*by_id[k]['root'])) for k in used if by_id[k]['type']=='rational_root'}),
                      'modular_primes':sorted({v['prime'] for v in nf}),
                      'max_resultant_degree':max(max((m[0] for m,v in s['resultant']),default=-1) for s in c['systems']),
                      'build_seconds':c.get('build_seconds')})
    summary = {'status':status,'missing_cases':missing,'unresolved':unresolved,'cases':stats,
               'total_systems':sum(s['systems'] for s in stats),'distinct_catalog_factors':len(catalog),
               'rootless_catalog_factors':sum(v['type']=='no_rational_root' for v in catalog.values()),
               'new_cases_present':len(have),'new_cases_expected':len(NEW_CASES)}
    (RESULTS/'degree9_generation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k!='cases'},indent=2))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--part')
    ap.add_argument('--merge', action='store_true')
    ap.add_argument('cases', nargs='*')
    args = ap.parse_args()
    if args.merge:
        merge()
    else:
        require(args.part and args.cases, 'need --part NAME and case ids, or --merge')
        run_part(args.part, args.cases)

if __name__ == '__main__':
    main()
