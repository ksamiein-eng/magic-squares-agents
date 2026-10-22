#!/usr/bin/env python3
"""Independently verify certificate_21.json.
Reconstructs sines by addition/doubling; computes Sylvester determinants;
checks exact factor products and finite-field no-root witnesses.
Does NOT call resultant(), factor(), factor_list(), ground_roots(), or the producer.
"""
from __future__ import annotations
import itertools
import json
import sys
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent
t,u = sp.symbols('t u')


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def decode(terms: list, variables: tuple) -> sp.Expr:
    value = 0
    for monomial, coefficient in terms:
        require(isinstance(coefficient,int) and len(monomial)==len(variables), 'malformed coefficient')
        require(all(isinstance(n,int) and n>=0 for n in monomial), 'malformed exponent')
        value += coefficient * sp.prod(v**n for v,n in zip(variables,monomial))
    return sp.expand(value)


def sylvester_determinant(f: sp.Expr, g: sp.Expr) -> sp.Expr:
    """Direct determinant, independent of the producer's resultant algorithm."""
    fp,gp = sp.Poly(f,u),sp.Poly(g,u)
    m,n = fp.degree(),gp.degree()
    require(m>=0 and n>=0, 'zero input polynomial')
    if m==0: return sp.expand(fp.as_expr()**n)
    if n==0: return sp.expand(gp.as_expr()**m)
    fc,gc = fp.all_coeffs(),gp.all_coeffs()
    rows = [[0]*i+fc+[0]*(n-1-i) for i in range(n)]
    rows += [[0]*i+gc+[0]*(m-1-i) for i in range(m)]
    return sp.expand(sp.Matrix(rows).det(method='bareiss'))


def matrix(i,j,k,l,d,a,b):
    r,q=[0]*4,[0]*4
    r[i]=1;r[k]=-a;r[l]=-b
    q[j]=d;q[k]=-a;q[l]=b
    return sp.Matrix([r,q])


def polynomial_mod(coeff:list[int], r:int, p:int) -> int:
    value=0
    for c in coeff: value=(value*r+c)%p
    return value


def verify(path:Path) -> dict:
    data=json.loads(path.read_text())
    require(data['schema']=='magic-squares-priority-repair/21/v1','wrong schema')
    # A second derivation of the four numerators, using sine addition/doubling.
    st,ct = 2*t/(1+t*t),(1-t*t)/(1+t*t)
    su,cu = 2*u/(1+u*u),(1-u*u)/(1+u*u)
    s2,c2 = 2*st*ct,ct*ct-st*st
    denominator=(1+t*t)**2*(1+u*u)
    es=[sp.cancel(z*denominator) for z in (s2*cu+c2*su,s2*cu-c2*su,st*cu+ct*su,s2)]
    require(list(map(list,((2,1),(2,-1),(1,1),(2,0))))==data['frequencies'],'wrong frequencies')
    require(len(data['area_numerators'])==4,'wrong number of offsets')
    for e,encoded in zip(es,data['area_numerators']):
        require(sp.expand(e-decode(encoded,(t,u)))==0,'incorrect offset polynomial')
    tags=[(i,j,k,l,a,b) for i,j in itertools.combinations(range(4),2)
          for k,l in itertools.permutations([v for v in range(4) if v not in (i,j)])
          for a,b in itertools.product((-1,1),repeat=2)]
    require(len(data['systems'])==48,'wrong system count')
    require({tuple(r['assignment']) for r in data['systems']}==set(tags),'incomplete assignment set')
    full={tuple(matrix(i,j,k,l,d,a,b).rref()[0])
          for i,j,k,l in itertools.permutations(range(4))
          for d,a,b in itertools.product((-1,1),repeat=3)}
    reduced={tuple(matrix(i,j,k,l,1,a,b).rref()[0]) for i,j,k,l,a,b in tags}
    require(full==reduced and len(reduced)==48,'signed row-space coverage failure')
    catalog={};primes=set()
    require(len({f['id'] for f in data['factor_catalog']})==len(data['factor_catalog']),'duplicate factor id')
    for entry in data['factor_catalog']:
        coeff=entry['coefficients_high_to_low']
        require(coeff and all(isinstance(c,int) for c in coeff) and coeff[0]!=0,'bad factor')
        polynomial=sum(c*t**(len(coeff)-1-i) for i,c in enumerate(coeff))
        if entry['type']=='degenerate_root':
            require(len(coeff)==2,'nonlinear factor labeled linear')
            root=-sp.Rational(coeff[1],coeff[0])
            require(root in (-1,0,1) and str(root)==entry['root'],'bad root')
        else:
            require(entry['type']=='no_rational_root','unknown factor status')
            p=entry['prime']; require(p in (3,5,7),'unexpected modulus')
            require(coeff[0]%p!=0,'leading coefficient divisible by witness prime')
            residues=[polynomial_mod(coeff,r,p) for r in range(p)]
            require(all(residues) and residues==entry['residues'],'modular no-root witness fails')
            primes.add(p)
        catalog[entry['id']]=polynomial
    for record in data['systems']:
        i,j,k,l,a,b=record['assignment']
        expected=(sp.expand(es[i]-a*es[k]-b*es[l]),sp.expand(es[j]-a*es[k]+b*es[l]))
        g1,g2=decode(record['G1'],(t,u)),decode(record['G2'],(t,u))
        require(all(sp.expand(v-w)==0 for v,w in zip(expected,(g1,g2))),'bad system')
        divisor=t if record['removed_t_factor'] else 1
        f,g=decode(record['F'],(t,u)),decode(record['G'],(t,u))
        require(sp.expand(divisor*f-g1)==0 and sp.expand(divisor*g-g2)==0,'bad divisor')
        # Only t=0 can be removed, and its fourth offset vanishes identically.
        if record['removed_t_factor']:
            require(sp.expand(es[3].subs(t,0))==0,'removed component is not degenerate')
        R=decode(record['resultant'],(t,))
        require(R!=0 and sp.expand(sylvester_determinant(f,g)-R)==0,'Sylvester determinant mismatch')
        product=sp.Integer(record['constant'])
        require(product!=0,'zero factorization constant')
        for item in record['factors']:
            require(item['factor_id'] in catalog and isinstance(item['exponent'],int) and item['exponent']>0,'bad factor ref')
            product *= catalog[item['factor_id']]**item['exponent']
        require(sp.expand(product-R)==0,'factor product mismatch')
    # Whole projective boundary components, not a numerical selection of points.
    for t0 in (-1,0,1): require(sp.expand(es[3].subs(t,t0))==0,'bad finite degeneration')
    h=sp.symbols('h')
    e_t_infinity=[sp.Poly(e,t).nth(4) for e in es]
    require(e_t_infinity[3]==0,'t=infinity not degenerate')
    e_u_infinity=[sp.Poly(e,u).nth(2) for e in es]
    require(sp.expand(e_u_infinity[0]-e_u_infinity[1])==0,'u=infinity not degenerate')
    # Both infinities: the fourth numerator vanishes; homogeneous denominator is 1.
    require(sp.Poly(es[3],t,u).coeff_monomial(t**4*u**2)==0,'corner not degenerate')
    return {'status':'PASS','systems_verified':48,'signed_row_spaces_verified':48,
            'raw_signed_assignments_compared':192,'factor_count':len(catalog),
            'rootless_factor_count':sum(f['type']=='no_rational_root' for f in data['factor_catalog']),
            'modular_primes':sorted(primes),'only_possible_finite_t':['-1','0','1'],
            'projective_boundaries':'both lines and their intersection proved degenerate',
            'claim':'(2,1) nonzero-drop representative has no nondegenerate rational-circle solution',
            'sympy_version':sp.__version__}


if __name__=='__main__':
    result=verify(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'results'/'certificate_21.json')
    (ROOT/'results'/'verification_21.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
