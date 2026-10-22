#!/usr/bin/env python3
"""Check the focused article's explicit identities, tables and reference structure.

This supplements, and does not replace, the two-prime and D1 proof verifiers.
It does not certify novelty, source authority, or human peer review.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys
import sympy as sp

ROOT = Path(__file__).resolve().parent

def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def canon(v):
    v = tuple(v)
    for x in v:
        if x:
            return v if x > 0 else tuple(-a for a in v)
    return v

def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=ROOT/'verification_runs/paper_checks.json')
    args=ap.parse_args()
    checks=[]
    h,r=sp.symbols('h r', real=True)
    P=h**12+70*h**10-1009*h**8+7060*h**6-1009*h**4+70*h**2+1
    F=h**6-13*h**4+83*h**2+1
    G=h**6+83*h**4-13*h**2+1
    need(sp.expand(F*G-P)==0,'genus-five factor product')
    need(sp.gcd(P,sp.diff(P,h))==1,'genus-five squarefreeness')
    need([P.subs(h,x) for x in [0,1,-1]]==[1,5184,5184],'known point values')
    checks.append({'name':'genus_five_model','status':'PASS','degree':12,'genus':5,
                   'known_points':8,'point_list_complete':False})
    rr=6*h/(1-h**2);ss=3*(1+h**2)/(1-h**2)
    need(sp.cancel(ss**2-rr**2-9)==0,'conic parametrization')
    need(sp.cancel(rr/(ss+3)-h)==0,'conic inverse')
    need(sp.cancel((1-h**2)**6*(rr**6-5*rr**4+19*rr**2+9)-9*P)==0,
         'conic/sextic pullback')
    Q=h**4+34*h**2+1;D=(1+h**2)*Q
    sin_a=(1-h**2)/(1+h**2);cos_a=-2*h/(1+h**2)
    sin_b=12*h*(1-h**2)/Q;cos_b=(h**4-38*h**2+1)/Q
    sin_g=-48*h**2*(1-h**2)/D
    need(sp.cancel(sin_a**2+cos_a**2-1)==0,'first circle')
    need(sp.cancel(sin_b**2+cos_b**2-1)==0,'second circle')
    need(sp.cancel(sin_g**2+P/D**2-1)==0,'third circle')
    L=(1-h**2)/D
    e=[h**4-62*h**2+1,h**4-14*h**2+1,h**4+34*h**2+1,-48*h**2]
    actual=[sin_a*cos_b+cos_a*sin_b,sin_a*cos_b-cos_a*sin_b,sin_a,sin_g]
    for a,b in zip(actual,e):need(sp.cancel(a-L*b)==0,'signed reconstruction')
    need(sp.expand(e[0]-e[1]-e[3])==0,'first relation')
    need(sp.expand(e[2]-e[1]+e[3])==0,'second relation')
    coefficients=set()
    for expr in e+[e[i]+sg*e[j] for i,j in itertools.combinations(range(4),2) for sg in [-1,1]]:
        p=sp.Poly(expr,h);need(not p.is_zero,'identically degenerate entry/pair')
        power=min(m[0] for m,c in p.terms())
        q=sp.Poly(sp.cancel(expr/h**power),h).monic()
        if q.degree()==0:continue
        need(q.degree()==4 and q.coeff_monomial(h**3)==0 and q.coeff_monomial(h)==0,
             'nondegeneracy shape')
        need(q.TC()==1,'nondegeneracy constant')
        need(q.eval(1)!=0 and q.eval(-1)!=0,'nondegeneracy rational roots')
        coefficients.add(int(q.coeff_monomial(h**2)))
    need(coefficients=={-110,-62,-38,-14,10,34,82},'printed nondegeneracy coefficient list')
    checks.append({'name':'rational_reconstruction','status':'PASS',
                   'nondegeneracy_quartic_coefficients':sorted(coefficients)})
    # Recheck the introductory real-angle residual calculation algebraically.
    a,b=sp.symbols('a b');vals=[a,b,a+b,a-b]
    expected=[-15*a*a*b*b,3*a*a*b*(2*a-b),-3*a*a*b*(2*a+b),
              -3*a*b*b*(a-2*b),-3*a*b*b*(a+2*b),0]
    for pair,want in zip(itertools.combinations(range(4),2),expected):
        other=[i for i in range(4) if i not in pair]
        got=vals[pair[0]]**2*vals[pair[1]]**2-(vals[other[0]]**2-vals[other[1]]**2)**2
        need(sp.expand(got-want)==0,'real obstruction residual')
    checks.append({'name':'six_real_obstruction_residuals','status':'PASS'})
    frequencies=json.loads((ROOT/'editorial/ordered_frequencies.json').read_text())
    vectors={canon(v) for v in itertools.product([-1,0,1],repeat=3) if any(v)}
    adm={frozenset(c) for c in itertools.combinations(vectors,4)
         if all(sum(abs(v[i]) for v in c)>=3 for i in range(3))}
    ops=list(itertools.product(itertools.product([-1,1],repeat=3),itertools.permutations(range(3))))
    union=set();orbit_sizes={}
    for label,vs in frequencies.items():
        orb={frozenset(canon([sg[i]*v[perm[i]] for i in range(3)]) for v in vs) for sg,perm in ops}
        need(not (union&orb),'duplicate orbit representative')
        union|=orb;orbit_sizes[label]=len(orb)
    need(len(vectors)==13 and len(adm)==177 and union==adm and len(frequencies)==15,
         'orbit completeness')
    checks.append({'name':'rank_three_enumeration','status':'PASS','vectors':13,
                   'admissible_sets':177,'orbits':15,'sizes':orbit_sizes})
    maps=json.loads((ROOT/'editorial/transport_matrices.json').read_text())
    for row in maps:
        M=sp.Matrix(row['matrix']);S=sp.Matrix(frequencies[row['source']]);T=sp.Matrix(frequencies[row['target']])
        need(int(M.det())==row['determinant'] and M.det()!=0,'transport determinant')
        signed=sp.Matrix([list(sg*T[j,:]) for j,sg in row['signed_row_permutation']])
        need(S*M==signed,'transport identity')
    angle=sp.Matrix([[1,1,0],[0,0,1],[1,0,1]])
    canonical=sp.Matrix([[1,1,0],[1,-1,0],[1,0,0],[0,0,1]])
    need(angle.det()==1 and canonical*angle==sp.Matrix(frequencies['D1']),'D1 unimodular change')
    checks.append({'name':'four_torus_maps_and_D1_coordinates','status':'PASS'})
    cert=json.loads((ROOT/'verification/two_prime/results/certificate_degree7.json').read_text())
    cases=cert['cases'];catalog=cert['factor_catalog']
    need(len(cases)==43 and sum(len(c['systems']) for c in cases)==2064,'two-prime certificate totals')
    need(len(catalog)==1190,'factor catalog total')
    need(sum((2*k-1)*(2*l-1) for k in range(1,7) for l in range(1,k+1) if k+l<=7)==168,
         'raw two-prime total')
    checks.append({'name':'two_prime_printed_counts','status':'PASS','representatives':43,
                   'systems':2064,'catalog_factors':1190,'raw_forms':168})
    d1=json.loads((ROOT/'verification/d1_norm/d1_certificate.json').read_text())
    need(len(d1['systems'])==48,'D1 system count')
    status=collections.Counter(x['status'] for x in d1['systems'])
    need(status['closed']==40,'D1 closure count')
    need(d1['residual_points_complete'] is False,'false residual completeness')
    checks.append({'name':'D1_catalog_scope','status':'PASS','system_statuses':dict(status),
                   'residual_completeness_asserted':False})
    modular_rows=[(6,-7,-1,16,{7,12,15},{7,15}),
                  (6,-7,7,16,{7,12,15},{7,15}),
                  (-36,320,2,64,{32,48,62},{2,50}),
                  (-36,320,10,64,{6,32,48},{10,58})]
    for A,B,d,mod,v_chart,u_chart in modular_rows:
        got_v={(d*u**4+A*u*u+B//d)%mod for u in range(mod)}
        got_u={(d+A*v*v+(B//d)*v**4)%mod for v in range(0,mod,2)}
        squares={n*n%mod for n in range(mod)}
        need(got_v==v_chart and got_u==u_chart,'printed primitive-chart residues')
        need(not ((got_v|got_u)&squares),'quartic residue obstruction')
    checks.append({'name':'printed_descent_residue_table','status':'PASS','rows':4})
    # Check every manuscript citation and cross-reference key. This does not prove external content.
    tex_files=list((ROOT/'manuscript').glob('*.tex'))
    text='\n'.join(p.read_text() for p in tex_files)
    cites={x.strip() for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text) for x in group.split(',')}
    refs=json.loads((ROOT/'editorial/references.json').read_text())
    keys={r['key'] for r in refs};bibkeys=set(re.findall(r'\\bibitem\{([^}]+)\}',text))
    need(cites==keys==bibkeys,'cited bibliography mismatch')
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    need(len(labels)==len(set(labels)),'duplicate LaTeX label')
    targets=set(re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text))
    need(targets<=set(labels),'undefined cross-reference')
    need(r'\author{}' in text,'unexpected author assignment')
    need('ChatGPT and Claude were used for symbolic and computational work, implementation of verification code, and preparation and revision of the exposition.' in text,'missing AI assistance disclosure')
    need('The completeness assertion is not used anywhere' in text,'missing proof boundary')
    checks.append({'name':'bibliography_and_manuscript_structure','status':'PASS','references':len(refs),
                   'labels':len(labels),'claims_not_checked':['historical priority','independent human review']})
    report={'status':'PASS','checks':checks,'sympy_version':sp.__version__,
            'scope':'Article consistency and selected exact identities, not a substitute for the main certificate verifiers.',
            'paper_sha256':hashlib.sha256((ROOT/'manuscript/paper.tex').read_bytes()).hexdigest()}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':
    main()
