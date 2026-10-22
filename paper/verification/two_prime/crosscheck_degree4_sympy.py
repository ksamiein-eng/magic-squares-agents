#!/usr/bin/env python3
"""Independent symbolic cross-check: Chebyshev sine formulas and direct determinants.
Does not import the producer or the standard-library verifier. Does not call
SymPy resultant, factorization, or rational-root routines.
"""
from __future__ import annotations
import json
import itertools
import time
from pathlib import Path
import sympy as sp
from sympy.polys.matrices import DomainMatrix

ROOT=Path(__file__).resolve().parent
t,u=sp.symbols('t u')
CASES={'21_m1_n0':(2,1,1,0),'31_m1_n0':(3,1,1,0),'31_m2_n0':(3,1,2,0),
       '22_m1_n1':(2,2,1,1),'22_m1_nminus1':(2,2,1,-1)}


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


def main():
    start=time.perf_counter()
    data=json.loads((ROOT/'results'/'certificate_degree4.json').read_text())
    require(data['schema']=='magic-squares/degree4/v2','schema')
    require(len(data['cases'])==5 and {x['id'] for x in data['cases']}==set(CASES),'coverage')
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
        for q in c['systems']:
            i,j,k,l,d,e=q['assignment']
            f,g=decode(q['F'],(t,u)),decode(q['G'],(t,u))
            require(sp.expand(f*t**q['removed_t_power']-E[i]+d*E[k]+e*E[l])==0,'first equation')
            require(sp.expand(g*t**q['removed_t_power']-E[j]+d*E[k]-e*E[l])==0,'second equation')
            R=decode(q['resultant'],(t,))
            require(sp.expand(direct_det(f,g)-R)==0,'direct symbolic determinant')
            P=q['constant']*sp.prod(catalog[x['factor_id']]**x['exponent'] for x in q['factors'])
            require(sp.Poly(P-R,t).is_zero,'factor product')
            count+=1
        print(c['id'],'PASS',flush=True)
    report={'status':'PASS','systems':count,'numerator_method':'Chebyshev T_n and U_(n-1)',
            'determinant_method':'direct symbolic Sylvester matrix over ZZ[t], SymPy DomainMatrix',
            'resultant_calls':0,'factorization_calls':0,'rational_root_solver_calls':0,
            'sympy':sp.__version__,'elapsed_seconds':round(time.perf_counter()-start,3)}
    (ROOT/'results'/'crosscheck_degree4_sympy.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
