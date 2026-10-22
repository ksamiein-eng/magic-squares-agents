#!/usr/bin/env python3
"""Produce exact resultant certificates for the (2,1) rational-circle case.
No elliptic-curve packages or numerical root finders are used.
Run the separate verify_certificate_21.py after this program.
"""
from __future__ import annotations
import itertools
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent
t, u = sp.symbols('t u', real=True)
FREQUENCIES = ((2, 1), (2, -1), (1, 1), (2, 0))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def encode(poly: sp.Expr, variables: tuple) -> list:
    return [[list(m), int(c)] for m, c in sp.Poly(poly, *variables, domain=sp.ZZ).terms()]


def area_numerator(m: tuple[int, int]) -> sp.Expr:
    product = 1
    for v, n, k in zip((t, u), m, (2, 1)):
        product *= (1 + sp.I * (1 if n >= 0 else -1) * v) ** (2 * abs(n))
        product *= (1 + v*v) ** (k - abs(n))
    return sp.expand(sp.im(sp.expand(product)))


def assignments() -> list:
    return [(i, j, k, l, a, b)
            for i, j in itertools.combinations(range(4), 2)
            for k, l in itertools.permutations([v for v in range(4) if v not in (i, j)])
            for a, b in itertools.product((-1, 1), repeat=2)]


def build() -> dict:
    es = [area_numerator(m) for m in FREQUENCIES]
    factors: dict[tuple, dict] = {}
    records = []
    for sid, (i, j, k, l, a, b) in enumerate(assignments()):
        g1, g2 = sp.expand(es[i]-a*es[k]-b*es[l]), sp.expand(es[j]-a*es[k]+b*es[l])
        drop_t = (g1.subs(t, 0) == 0 and g2.subs(t, 0) == 0)
        divisor = t if drop_t else 1
        f, g = sp.cancel(g1/divisor), sp.cancel(g2/divisor)
        require(sp.expand(f*divisor-g1) == 0 and sp.expand(g*divisor-g2) == 0, 'bad division')
        result = sp.resultant(f, g, u)
        require(result != 0, f'zero resultant at {sid}')
        constant, factorization = sp.factor_list(result, t)
        product = sp.Integer(constant)
        listed = []
        for h, exponent in factorization:
            poly = sp.Poly(h, t, domain=sp.ZZ)
            coeff = tuple(int(c) for c in poly.all_coeffs())
            if coeff not in factors:
                ident = f'F{len(factors):02d}'
                entry = {'id': ident, 'coefficients_high_to_low': list(coeff)}
                if poly.degree() == 1:
                    root = -sp.Rational(coeff[1], coeff[0])
                    require(root in (-1, 0, 1), f'unexpected rational root {root}')
                    entry.update({'type': 'degenerate_root', 'root': str(root)})
                else:
                    prime = next((int(p) for p in sp.primerange(2, 200)
                                  if int(poly.LC()) % p != 0
                                  and all(int(poly.eval(r)) % p != 0 for r in range(p))), None)
                    require(prime is not None, f'no modular witness for {h}')
                    entry.update({'type': 'no_rational_root', 'prime': prime,
                                  'residues': [int(poly.eval(r)) % prime for r in range(prime)]})
                factors[coeff] = entry
            entry = factors[coeff]
            listed.append({'factor_id': entry['id'], 'exponent': int(exponent)})
            product *= h**exponent
        require(sp.expand(product-result) == 0, 'factorization product fails')
        records.append({'id': sid, 'assignment': [i,j,k,l,a,b], 'removed_t_factor': drop_t,
                        'G1': encode(g1,(t,u)), 'G2': encode(g2,(t,u)),
                        'F': encode(f,(t,u)), 'G': encode(g,(t,u)),
                        'resultant': encode(result,(t,)), 'constant': int(constant),
                        'factors': listed})
    return {'schema': 'magic-squares-priority-repair/21/v1',
            'scope': 'rational unit-circle angles; one nonzero-drop representative of exponent pair (2,1)',
            'frequencies': FREQUENCIES,
            'denominator': '(1+t^2)^2(1+u^2)',
            'area_numerators': [encode(e,(t,u)) for e in es],
            'variables': ['t','u'],
            'generator_sympy_version': sp.__version__,
            'factor_catalog': list(factors.values()), 'systems': records,
            'boundaries': {'t in {0,1,-1,infinity}': 'fourth offset vanishes',
                           'u=infinity': 'first two offsets coincide'},
            'claim': 'no nondegenerate rational-circle solution for this representative'}


if __name__ == '__main__':
    data = build()
    output = ROOT/'results'/'certificate_21.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2)+'\n')
    rootless = [f for f in data['factor_catalog'] if f['type']=='no_rational_root']
    summary = {'systems': len(data['systems']), 'catalog_size': len(data['factor_catalog']),
               'rootless_factors': len(rootless), 'modular_primes': sorted({f['prime'] for f in rootless}),
               'systems_with_removed_t': sum(s['removed_t_factor'] for s in data['systems']),
               'max_resultant_degree': max(max(term[0][0] for term in r['resultant']) for r in data['systems'])}
    (ROOT/'results'/'certificate_21_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
