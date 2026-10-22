#!/usr/bin/env python3
"""Independent symbolic cross-check: Chebyshev sine formulas and direct determinants.
Does not import the producer or the standard-library verifier. Does not call
SymPy resultant, factorization, or rational-root routines.
"""
from __future__ import annotations
import json
import itertools
import time
from math import gcd
from pathlib import Path
import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOT=Path(__file__).resolve().parent
t,u=sp.symbols('t u')
CASES={'21_m1_n0':(2,1,1,0),'31_m1_n0':(3,1,1,0),'31_m2_n0':(3,1,2,0),
       '22_m1_n1':(2,2,1,1),'22_m1_nminus1':(2,2,1,-1),
       '41_m1_n0':(4,1,1,0),'41_m3_n0':(4,1,3,0),
       '32_m1_n1':(3,2,1,1),'32_m1_nminus1':(3,2,1,-1),
       '32_m2_n1':(3,2,2,1),'32_m2_nminus1':(3,2,2,-1)}


def require(ok,msg):
    if not ok: raise RuntimeError(msg)


def decode(terms,vs):
    return sp.Poly.from_dict({tuple(m):c for m,c in terms},vs,domain=sp.ZZ).as_expr()


def trig(v,k):
    x=(1-v*v)/(1+v*v)
    if k==0:return sp.Integer(1),sp.Integer(0)
    return sp.chebyshevt(abs(k),x), (1 if k>0 else -1)*2*v/(1+v*v)*sp.chebyshevu(abs(k)-1,x)


def make(freq,a,b):
    c,s=trig(t,freq[0]);d,r=trig(u,freq[1])
    return sp.Poly(sp.cancel((s*d+c*r)*(1+t*t)**a*(1+u*u)**b),t,u,domain=sp.ZZ).as_expr()


def direct_det(f,g):
    m,n=sp.degree(f,u),sp.degree(g,u)
    fc=sp.Poly(f,u).all_coeffs();gc=sp.Poly(g,u).all_coeffs()
    rows=[[0]*i+fc+[0]*(n-1-i) for i in range(n)]
    rows += [[0]*i+gc+[0]*(m-1-i) for i in range(m)]
    return DomainMatrix.from_Matrix(sp.Matrix(rows)).det().as_expr()


def degenerate(values):
    values=[sp.expand(x) for x in values]
    if any(x==0 for x in values):
        return True
    return any(sp.expand(values[i]-sg*values[j])==0
               for i,j in itertools.combinations(range(4),2) for sg in [-1,1])


def canonical(freqs):
    normalized=[]
    for v in freqs:
        sg=1 if next(x for x in v if x)!=0 and next(x for x in v if x)>0 else -1
        normalized.append(tuple(sg*x for x in v))
    return tuple(sorted(normalized))


def full_orbit(freqs):
    return {canonical([(s*v[pm[0]],q*v[pm[1]]) for v in freqs])
            for pm in [(0,1),(1,0)] for s,q in itertools.product([-1,1],repeat=2)}


def gcd_coverage():
    bases={}
    for key,(a,b,m,n) in CASES.items():
        for v in full_orbit([(a,b),(a,-b),(m,b),(a,n)]):
            bases[v]=key
    para=full_orbit([(1,1),(1,-1),(0,1),(1,0)])
    checked=0
    for a,b in [(1,1),(2,1),(3,1),(2,2),(4,1),(3,2)]:
        for m in range(1-a,a):
            for n in range(1-b,b):
                d,e=gcd(a,abs(m)),gcd(b,abs(n))
                target=canonical([(a//d,b//e),(a//d,-b//e),(m//d,b//e),(a//d,n//e)])
                require(target in bases or target in para,'gcd-normalized configuration missing')
                checked+=1
    require(checked==40,'gcd coverage count')
    return checked


def main():
    start=time.perf_counter()
    data=json.loads((ROOT/'results'/'certificate_degree5.json').read_text())
    require(data['schema']=='magic-squares/degree5/v3','schema')
    require(len(data['cases'])==11 and {x['id'] for x in data['cases']}==set(CASES),'coverage')
    tags=[(i,j,k,l,c,d) for i,j in itertools.combinations(range(4),2)
          for k,l in itertools.permutations([z for z in range(4) if z not in (i,j)])
          for c,d in itertools.product((-1,1),repeat=2)]
    catalog={}
    for f in data['factor_catalog']:
        p=sp.Poly.from_list(f['coefficients_high_to_low'],gens=t,domain=sp.ZZ)
        catalog[f['id']]=p.as_expr()
        if f['type']=='no_rational_root':
            r=f['prime']
            require(sp.isprime(r) and int(p.LC())%r!=0 and all(int(p.eval(j))%r for j in range(r)), 'modular witness')
        else:
            require(p.degree()==1 and p.eval(sp.Rational(*f['root']))==0,'linear root')
    count=0
    for c in data['cases']:
        a,b,m,n=CASES[c['id']]
        freqs=[(a,b),(a,-b),(m,b),(a,n)]
        E=[make(v,a,b) for v in freqs]
        require(all(sp.expand(e-decode(q,(t,u)))==0 for e,q in zip(E,c['area_numerators'])),'Chebyshev reconstruction')
        require(len(c['systems'])==48 and {tuple(q['assignment']) for q in c['systems']}==set(tags),'signed coverage')
        rational_fibers=set()
        for q in c['systems']:
            i,j,k,l,d,e=q['assignment']
            f,g=decode(q['F'],(t,u)),decode(q['G'],(t,u))
            if q['removed_t_power']:
                rational_fibers.add(sp.Rational(0))
            by_id={rec['id']:rec for rec in data['factor_catalog']}
            for part in q['factors']:
                rec=by_id[part['factor_id']]
                if rec['type']=='rational_root': rational_fibers.add(sp.Rational(*rec['root']))
            require(sp.expand(f*t**q['removed_t_power']-E[i]+d*E[k]+e*E[l])==0,'first equation')
            require(sp.expand(g*t**q['removed_t_power']-E[j]+d*E[k]-e*E[l])==0,'second equation')
            R=decode(q['resultant'],(t,))
            require(sp.expand(direct_det(f,g)-R)==0,'direct symbolic determinant')
            P=q['constant']*sp.prod(catalog[x['factor_id']]**x['exponent'] for x in q['factors'])
            require(sp.Poly(P-R,t).is_zero,'factor product')
            count+=1
        for rr in rational_fibers:
            require(degenerate([p.subs(t,rr) for p in E]),'finite fiber not identically degenerate')
        ti=[sp.Poly(p,t).nth(2*a) for p in E]
        ui=[sp.Poly(p,u).nth(2*b) for p in E]
        both=[sp.Poly(p,t,u).coeff_monomial(t**(2*a)*u**(2*b)) for p in E]
        require(all(degenerate(v) for v in (ti,ui,both)),'projective boundary not degenerate')
        print(c['id'],'PASS',flush=True)
    report={'status':'PASS','systems':count,'numerator_method':'Chebyshev T_n and U_(n-1)',
            'determinant_method':'direct symbolic Sylvester matrix over ZZ[t], SymPy DomainMatrix',
            'resultant_calls':0,'factorization_calls':0,'rational_root_solver_calls':0,
            'normal_forms_checked_by_gcd_reduction':gcd_coverage(),
            'finite_fibers_and_projective_boundaries':'independent symbolic identities checked',
            'sympy':sp.__version__,'elapsed_seconds':round(time.perf_counter()-start,3)}
    (ROOT/'results'/'crosscheck_degree5_sympy.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
