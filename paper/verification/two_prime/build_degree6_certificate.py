#!/usr/bin/env python3
"""Generate proof data for all two-prime exponent sums <= 6.
SymPy is a discovery tool, not part of the standard-library acceptance path.
The separate verifier reconstructs all inputs and checks every identity.
"""
from __future__ import annotations
import itertools
import json
import time
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent
t, u = sp.symbols('t u', real=True)
CASES = [('21_m1_n0', 2, 1, 1, 0), ('31_m1_n0', 3, 1, 1, 0),
         ('31_m2_n0', 3, 1, 2, 0), ('22_m1_n1', 2, 2, 1, 1),
         ('22_m1_nminus1', 2, 2, 1, -1),
         ('41_m1_n0', 4, 1, 1, 0), ('41_m3_n0', 4, 1, 3, 0),
         ('32_m1_n1', 3, 2, 1, 1), ('32_m1_nminus1', 3, 2, 1, -1),
         ('32_m2_n1', 3, 2, 2, 1), ('32_m2_nminus1', 3, 2, 2, -1)]

CASES += [('51_m1_n0', 5, 1, 1, 0), ('51_m2_n0', 5, 1, 2, 0), ('51_m3_n0', 5, 1, 3, 0), ('51_m4_n0', 5, 1, 4, 0), ('42_m1_n1', 4, 2, 1, 1), ('42_m1_nminus1', 4, 2, 1, -1), ('42_m3_n1', 4, 2, 3, 1), ('42_m3_nminus1', 4, 2, 3, -1), ('33_m1_n1', 3, 3, 1, 1), ('33_m1_nminus1', 3, 3, 1, -1), ('33_m1_n2', 3, 3, 1, 2), ('33_m1_nminus2', 3, 3, 1, -2), ('33_m2_n2', 3, 3, 2, 2), ('33_m2_nminus2', 3, 3, 2, -2)]


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


def build():
    start = time.perf_counter()
    catalog = {}
    cases = []
    for name, a, b, m, n in CASES:
        begin = time.perf_counter()
        freqs = [(a,b),(a,-b),(m,b),(a,n)]
        es = [make_numerator(v,(a,b)) for v in freqs]
        systems = []
        for sid, tag in enumerate(tags()):
            i,j,k,l,sg,sh = tag
            g1 = sp.expand(es[i]-sg*es[k]-sh*es[l])
            g2 = sp.expand(es[j]-sg*es[k]+sh*es[l])
            require(g1 != 0 and g2 != 0, 'zero input equation needs separate treatment')
            removed = min(min(mon[0] for mon,c in sp.Poly(g,t,u).terms()) for g in (g1,g2))
            f,g = [sp.Poly(sp.cancel(h/t**removed),t,u,domain=sp.ZZ).as_expr() for h in (g1,g2)]
            res = sp.resultant(f,g,u)
            require(res != 0, f'UNRESOLVED common nonvertical component: {name}, {sid}')
            constant, fs = sp.factor_list(res,t)
            refs = []
            for q, e in fs:
                poly = sp.Poly(q,t,domain=sp.ZZ)
                cs = tuple(int(c) for c in poly.all_coeffs())
                if cs not in catalog:
                    item = {'id': f'P{len(catalog):03d}', 'coefficients_high_to_low': list(cs)}
                    if poly.degree() == 1:
                        rr = -sp.Rational(cs[1],cs[0])
                        item.update(type='rational_root', root=[int(rr.p),int(rr.q)])
                    else:
                        pr = next((int(p) for p in sp.primerange(2,257)
                                   if cs[0]%p and all(int(poly.eval(r))%p for r in range(p))),None)
                        require(pr is not None,f'UNRESOLVED factor without small-prime witness: {q}')
                        item.update(type='no_rational_root', prime=pr,
                                    residues=[int(poly.eval(r))%pr for r in range(pr)])
                    catalog[cs] = item
                refs.append({'factor_id':catalog[cs]['id'],'exponent':int(e)})
            systems.append({'id':sid,'assignment':list(tag),'removed_t_power':int(removed),
                            'G1':encode(g1,(t,u)),'G2':encode(g2,(t,u)),
                            'F':encode(f,(t,u)),'G':encode(g,(t,u)),
                            'resultant':encode(res,(t,)), 'constant':int(constant), 'factors':refs})
        rec = {'id':name,'bounds':[a,b],'drops':[m,n],'frequencies':freqs,
               'area_numerators':[encode(e,(t,u)) for e in es],'systems':systems}
        cases.append(rec)
        (ROOT/'results').mkdir(exist_ok=True)
        (ROOT/'results'/'degree6_build_checkpoint.json').write_text(json.dumps({'status':'PARTIAL_GENERATION_NOT_VERIFIED','cases':cases,'factor_catalog':list(catalog.values())},indent=2)+'\n')
        print(name, 'systems',len(systems),'seconds',round(time.perf_counter()-begin,3),flush=True)
    result = {'schema':'magic-squares/degree6/v4',
              'scope':'rational-circle exclusion certificates; full-depth normal forms; all exponent sums <=6',
              'producer':{'python':'see release_environment.json','sympy':sp.__version__},
              'factor_catalog':list(catalog.values()),'cases':cases}
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/'certificate_degree6.json').write_text(json.dumps(result,indent=2)+'\n')
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
                      'max_resultant_degree':max(max(m[0] for m,v in s['resultant']) for s in c['systems'])})
    summary = {'status':'GENERATED_NOT_YET_INDEPENDENTLY_VERIFIED','cases':stats,
               'total_systems':sum(s['systems'] for s in stats),'distinct_catalog_factors':len(catalog),
               'rootless_catalog_factors':sum(v['type']=='no_rational_root' for v in catalog.values()),
               'elapsed_seconds':round(time.perf_counter()-start,3)}
    (ROOT/'results'/'degree6_generation_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))

if __name__ == '__main__':
    build()
