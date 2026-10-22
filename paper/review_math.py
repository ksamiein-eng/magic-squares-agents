#!/usr/bin/env python3
"""Exact checks added in the mathematical proofread and appendix revision.

This supplements the two original acceptance implementations. It does not
prove historical priority, supply peer review, or classify all points of C.
Use --write-tables only when deliberately regenerating the appendix tables.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
from itertools import combinations, permutations, product
from math import gcd
import hashlib
import json
from pathlib import Path
import sympy as sp

ROOT = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def primitive_form(k, l, m, n):
    d, e = gcd(k, abs(m)), gcd(l, abs(n))
    return (k // d, l // e, m // d, n // e)

def equivalents(f):
    k,l,m,n=f
    return {(k,l,m,n),(k,l,-m,-n),(l,k,n,m),(l,k,-n,-m)}

def bivar(terms, t, u):
    return sum(int(c)*t**a*u**b for (a,b),c in terms)

def univar(terms, t):
    return sum(int(c)*t**a[0] for a,c in terms)

def ascending(v, r):
    return sum(c*r**i for i,c in enumerate(v))

def fmtpoly(p, r):
    return sp.latex(sp.expand(p), order='lex')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write-tables',action='store_true')
    ap.add_argument('--output',type=Path,default=ROOT/'verification_runs/mathematical_review.json')
    args=ap.parse_args()
    t,u,h,r,a,b,e=sp.symbols('t u h r a b e')
    checks=[]; files={}
    cert=json.loads((ROOT/'verification/two_prime/results/certificate_degree7.json').read_text())
    d1=json.loads((ROOT/'verification/d1_norm/d1_certificate.json').read_text())

    # Foundation identities: the accompanying proofs, not finite examples,
    # establish the integer/parity and valuation implications.
    lucas=sp.Matrix([[e+a,e-a-b,e+b],[e-a+b,e,e+a-b],[e-b,e+a+b,e-a]])
    sums=[sum(lucas[i,j] for j in range(3)) for i in range(3)]
    sums += [sum(lucas[i,j] for i in range(3)) for j in range(3)]
    sums += [sum(lucas[i,i] for i in range(3)),sum(lucas[i,2-i] for i in range(3))]
    need(all(sp.expand(x-3*e)==0 for x in sums),'Lucas line sums')
    roots=set()
    for x,y in combinations(list(lucas),2):
        f=sp.Poly(x-y,a,b)
        co=tuple(int(f.coeff_monomial(z)) for z in (a,b))
        d=gcd(*map(abs,co));co=tuple(c//d for c in co)
        if next(c for c in co if c)<0: co=tuple(-c for c in co)
        roots.add(co)
    need(roots=={(1,0),(0,1),(1,1),(1,-1),(1,2),(1,-2),(2,1),(2,-1)},'Lucas degeneracy factors')
    c=(1-t*t)/(1+t*t);s=2*t/(1+t*t)
    need(sp.cancel(c*c+s*s-1)==0 and sp.cancel(s/(1+c)-t)==0,'circle parameter and inverse')
    checks.append({'name':'foundation_polynomial_identities','status':'PASS','magic_lines':8,
                   'distinct_degeneracy_lines':8,'scope':'Symbolic identities; integrality and valuation implications are proved in the text.'})

    # Independently reduce all raw configurations by coordinate gcds, then use
    # only simultaneous drop signs and column interchange.
    cases=cert['cases'];direct={tuple(c['bounds']+c['drops']):c['id'] for c in cases}
    seen=set();coverage=[];summary=[]
    for k,l in sorted([(k,l) for k in range(1,7) for l in range(1,k+1) if k+l<=7],key=lambda z:(sum(z),-z[0])):
        raw=0
        for m in range(1-k,k):
            for n in range(1-l,l):
                raw+=1; p=primitive_form(k,l,m,n)
                if p[:2]==(1,1):
                    need(p[2:]==(0,0),'wrong elementary reduced form');route='parallelogram'
                else:
                    hits=[direct[x] for x in equivalents(p) if x in direct]
                    need(hits,f'uncovered raw form {(k,l,m,n)}')
                    route=sorted(hits)[0];seen.add(route)
                coverage.append({'raw':[k,l,m,n],'coordinate_gcds':[gcd(k,abs(m)),gcd(l,abs(n))],
                                 'reduced':list(p),'route':route})
        own=[c for c in cases if c['bounds']==[k,l]]
        summary.append((k,l,raw,len(own),48*len(own)))
    need(len(coverage)==168 and len(seen)==43 and len(direct)==43,'coverage totals')
    need(all(gcd(k,abs(m))==gcd(l,abs(n))==1 for k,l,m,n in direct),'direct case not coordinate-primitive')
    checks.append({'name':'independent_coordinate_gcd_coverage','status':'PASS','raw_forms':168,'direct_representatives':43,'signed_systems':2064})

    A=[r'\begin{center}',r'\small\setlength{\tabcolsep}{8pt}\renewcommand{\arraystretch}{1.15}',
       r'\begin{tabular}{crrr}',r'\toprule',r'$(k,\ell)$ & Raw forms & Direct cases & Signed systems\\',r'\midrule']
    for k,l,raw,num,ns in summary:A.append(f'$({k},{l})$ & {raw} & {num} & {ns:,}'+r'\\')
    A += [r'\midrule',r'Total & 168 & 43 & 2,064\\',r'\bottomrule',r'\end{tabular}',r'\end{center}']
    files['coverage_table.tex']='\n'.join(A)+'\n'
    fmap={f['id']:f for f in cert['factor_catalog']}
    rows=[r'{\small\setlength{\tabcolsep}{6pt}\renewcommand{\arraystretch}{1.12}',
          r'\begin{longtable}{ccccr}',r'\caption{The 43 direct cases. Every row contains 48 signed systems. $d_R$ is the largest actual resultant degree, not the larger degree bound used for verification. The last column counts distinct nonlinear no-root factors within the row.}\label{tab:representatives}\\',
          r'\toprule',r'$(k,\ell)$ & $(m,n)$ & $d_R$ & Possible rational $t$ & No-root factors\\',r'\midrule\endfirsthead',
          r'\toprule',r'$(k,\ell)$ & $(m,n)$ & $d_R$ & Possible rational $t$ & No-root factors\\',r'\midrule\endhead']
    computed=[]
    for case in cases:
        ids={f['factor_id'] for sy in case['systems'] for f in sy['factors']}
        rational={Fraction(*fmap[f]['root']) for f in ids if fmap[f]['type']=='rational_root'}
        if any(sy['removed_t_power'] for sy in case['systems']):rational.add(Fraction(0))
        need(rational in ({Fraction(0)},{Fraction(-1),Fraction(0),Fraction(1)}),'unexpected finite fiber')
        deg=max(max(term[0][0] for term in sy['resultant']) for sy in case['systems'])
        count=sum(fmap[f]['type']=='no_rational_root' for f in ids)
        k,l=case['bounds'];m,n=case['drops'];rt='0' if len(rational)==1 else r'0,\pm1'
        rows.append(f'$({k},{l})$ & $({m},{n})$ & {deg} & ${rt}$ & {count}'+r'\\')
        computed.append({'id':case['id'],'degree':deg,'rational_fibers':sorted(map(str,rational)),'rootless_factors':count})
    rows += [r'\bottomrule',r'\end{longtable}',r'}']
    files['representatives.tex']='\n'.join(rows)+'\n'

    # Fully worked certificate, checked from freshly reconstructed numerators.
    E=[4*t*(1-t*t)*(1-u*u)+2*u*(1-6*t*t+t**4),
       4*t*(1-t*t)*(1-u*u)-2*u*(1-6*t*t+t**4),
       2*t*(1+t*t)*(1-u*u)+2*u*(1-t**4),
       4*t*(1-t*t)*(1+u*u)]
    sy=cases[0]['systems'][0]
    F=sp.expand(E[0]+E[2]+E[3]);G=sp.expand(E[1]+E[2]-E[3])
    need(F==bivar(sy['F'],t,u) and G==bivar(sy['G'],t,u),'worked input mismatch')
    fc=sp.Poly(F,u).all_coeffs();gc=sp.Poly(G,u).all_coeffs()
    syl=sp.Matrix([fc+[0],[0]+fc,gc+[0],[0]+gc])
    det=sp.Poly(syl.det(method='domain-ge'),t).as_expr()
    J=3*t**12+26*t**10-251*t**8+716*t**6-803*t**4+250*t**2-5
    need(sp.expand(det-64*t*t*J)==0 and sp.expand(det-univar(sy['resultant'],t))==0,'worked resultant')
    residues=[int(J.subs(t,k))%7 for k in range(7)]
    need(residues==[2,6,3,5,5,3,6],'worked modular witness')
    checks.append({'name':'worked_resultant_certificate','status':'PASS','case':cases[0]['id'],'system':0,
                   'determinant_degree':14,'independent_degree_bound':14,'prime':7,'residues':residues})

    # Orbit tables and nonfaithful full-group convention.
    freq=json.loads((ROOT/'editorial/ordered_frequencies.json').read_text())
    def canon(v):
        v=tuple(v)
        return v if next(x for x in v if x)>0 else tuple(-x for x in v)
    V={canon(v) for v in product((-1,0,1),repeat=3) if any(v)}
    operations=list(product(product((-1,1),repeat=3),permutations(range(3))))
    def act(v,op):
        sg,pm=op;return canon(tuple(sg[i]*v[pm[i]] for i in range(3)))
    kernel=[op for op in operations if all(act(v,op)==v for v in V)]
    need(len(kernel)==2,'signed-permutation kernel')
    good={frozenset(S) for S in combinations(V,4) if all(sum(v[i]!=0 for v in S)>=3 for i in range(3))}
    union=set();sizes={}
    B=[r'{\small\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.18}',r'\begin{longtable}{lccccrr}',
       r'\caption{All admissible four-sets under signed coordinate permutations. The vector order is fixed for matrix identities. Stabilizers refer to the group of order 48.}\label{tab:orbits}\\',
       r'\toprule',r'Label & $v_0$ & $v_1$ & $v_2$ & $v_3$ & Size & Stab.\\',r'\midrule\endfirsthead',
       r'\toprule',r'Label & $v_0$ & $v_1$ & $v_2$ & $v_3$ & Size & Stab.\\',r'\midrule\endhead']
    for name,vs in freq.items():
        base=frozenset(canon(v) for v in vs)
        orb={frozenset(act(v,op) for v in vs) for op in operations}
        stab=sum(frozenset(act(v,op) for v in vs)==base for op in operations)
        need(len(orb)*stab==48 and not union.intersection(orb),'orbit or stabilizer mismatch')
        need(orb<=good,'inadmissible orbit');union|=orb;sizes[name]=[len(orb),stab]
        label={'E3':'E3=E4','F-1':r'F{-}1=F{-}3','F-2':r'F{-}2','F+1':r'F{+}1','F+2':r'F{+}2'}.get(name,name)
        B.append('$'+label+'$ & '+' & '.join('$('+','.join(map(str,v))+')$' for v in vs)+f' & {len(orb)} & {stab}'+r'\\')
    need(union==good and len(good)==177,'three-prime enumeration')
    B += [r'\midrule',r'\multicolumn{5}{l}{Total admissible four-sets} & 177 & \\',r'\bottomrule',r'\end{longtable}',r'}']
    files['orbits.tex']='\n'.join(B)+'\n'
    checks.append({'name':'orbit_stabilizer_convention','status':'PASS','full_group_order':48,'kernel_order':2,'effective_group_order':24,'orbits':sizes})

    # D1 normalization groups and their exact record indexing.
    tags=[(i,j,k,l,eps,eta) for i,j in combinations(range(4),2)
          for k,l in permutations([x for x in range(4) if x not in (i,j)])
          for eps,eta in product((1,-1),repeat=2)]
    need([tuple(s['tag']) for s in d1['systems']]==tags,'D1 assignment indexing')
    groups=defaultdict(list)
    for srec in d1['systems']:groups[tuple(srec['norm_factor'])].append(srec['system'])
    order=[(1,),(1,0,6,0,1),(4,0,-3,0,1),(1,0,-3,0,4),(1,0,18,0,1),(9,0,1),(1,0,9)]
    D=[r'\begin{center}\small',r'\begin{tabular}{lrp{0.47\linewidth}}',r'\toprule',r'$N(r)$ & Count & Zero-based record indices\\',r'\midrule']
    for pol in order:
        ids=groups[pol]
        D.append('$'+fmtpoly(ascending(pol,r),r)+'$ & '+str(len(ids))+' & '+', '.join(map(str,ids))+r'\\')
    D += [r'\bottomrule',r'\end{tabular}',r'\end{center}']
    files['d1_index_table.tex']='\n'.join(D)+'\n'
    # Verify the worked kernel from the displayed relation matrix itself.
    q=1+r*r; H=sp.Matrix([[1-r*r,2*r,0],[1-r*r,-2*r,0],[q,0,0],[0,0,q]])
    rel=sp.Matrix([[1,-1,0,-1],[0,-1,1,1]])
    cross=rel*H; cr=sp.Matrix(cross.row(0)).cross(sp.Matrix(cross.row(1)))
    need(all(sp.expand(x-y)==0 for x,y in zip(cr,2*r*sp.Matrix([[3*q,-r*q,-4*r*r]]))),'worked D1 kernel')
    checks.append({'name':'D1_catalog_indices_and_worked_kernel','status':'PASS','groups':{str(k):v for k,v in groups.items()},'residual_indices':[8,9,12,14,24,25,28,30]})

    # Arithmetic witnesses, including a primary-by-primary torsion bound.
    torsion=[]
    for A,B,prime_list,expected in [(6,1,[3,5],[4,8]),(-3,4,[3,5],[4,4]),(18,1,[3,7],[4,4])]:
        counts=[]
        for p in prime_list:
            need((16*B*B*(A*A-4*B))%p!=0,'bad reduction prime')
            n=1+sum((y*y-x**3-A*x*x-B*x)%p==0 for x in range(p) for y in range(p))
            counts.append(n)
        need(counts==expected,'elliptic counts')
        candidates=set(prime_list)
        for count in counts:candidates.update(map(int,sp.factorint(count)))
        valuations={}
        for ell in candidates:
            bounds=[]
            for p,num in zip(prime_list,counts):
                if p!=ell:
                    v=0
                    while num%ell==0:num//=ell;v+=1
                    bounds.append(v)
            need(bounds,'missing distinct reduction prime')
            valuations[ell]=min(bounds)
        need({p:v for p,v in valuations.items() if v}=={2:2},'torsion primary bound')
        torsion.append({'model':[0,A,0,B,0],'prime_counts':list(zip(prime_list,counts)),'torsion_upper_bound':4})
    modular=[(6,-7,-1,16),(6,-7,7,16),(-36,320,2,64),(-36,320,10,64)]
    residue_data=[]
    for A,B,d,mod in modular:
        vset={(d*x**4+A*x*x+B//d)%mod for x in range(mod)}
        uset={(d+A*x*x+(B//d)*x**4)%mod for x in range(0,mod,2)}
        sq={x*x%mod for x in range(mod)}
        need(not ((vset|uset)&sq),'false modular obstruction')
        residue_data.append({'A':A,'B':B,'d':d,'modulus':mod,'V_unit':sorted(vset),'U_unit_V_even':sorted(uset),'squares':sorted(sq)})
    checks.append({'name':'elliptic_primary_torsion_and_local_charts','status':'PASS','torsion':torsion,'residues':residue_data})

    # Short, independently printable squarefreeness witness.
    P=h**12+70*h**10-1009*h**8+7060*h**6-1009*h**4+70*h*h+1
    factors=[h*h-2,h*h+2,h**4-2,h**4+2]
    need(sp.Poly(P-sp.prod(factors),h,modulus=5).is_zero,'mod-5 factor product')
    for f in factors:need(sp.gcd(sp.Poly(f,h,modulus=5),sp.Poly(sp.diff(f,h),h,modulus=5)).degree()==0,'inseparable mod-5 factor')
    for f,g in combinations(factors,2):need(sp.gcd(sp.Poly(f,h,modulus=5),sp.Poly(g,h,modulus=5)).degree()==0,'mod-5 factors not coprime')
    x=sp.symbols('x')
    need(sp.expand(x**12*P.subs(h,1/x)-P.subs(h,x))==0,'infinity chart reciprocal identity')
    checks.append({'name':'genus_five_squarefreeness_and_infinity','status':'PASS','good_squarefree_prime':5,'degree':12,'genus':5,'specified_points':8,'all_rational_points_classified':False})
    evec=[h**4-62*h*h+1,h**4-14*h*h+1,h**4+34*h*h+1,-48*h*h]
    C=[r'\begin{center}\small',r'\begin{tabular}{cll}',r'\toprule',r'$(i,j)$ & $e_i-e_j$ & $e_i+e_j$\\',r'\midrule']
    pair_data=[]
    for i,j in combinations(range(4),2):
        diff=sp.expand(evec[i]-evec[j]);summ=sp.expand(evec[i]+evec[j])
        C.append(f'$({i},{j})$ & $'+sp.latex(sp.factor_terms(diff))+'$ & $'+sp.latex(sp.factor_terms(summ))+r'$\\')
        pair_data.append({'i':i,'j':j,'difference':str(diff),'sum':str(summ)})
    C += [r'\bottomrule',r'\end{tabular}',r'\end{center}']
    files['collision_table.tex']='\n'.join(C)+'\n'
    checks.append({'name':'exhaustive_reconstruction_collision_table','status':'PASS','pair_checks':12,'entries':4,'pairs':pair_data})

    for name,text in files.items():
        path=ROOT/'manuscript'/name
        if args.write_tables:path.write_text(text)
        else:need(path.read_text()==text,'appendix table differs from exact records: '+name)
    record={'status':'PASS','checks':checks,'new_table_files':list(files),
            'two_prime_case_summary':computed,'coverage':coverage,
            'scope':'Additional exact proofread and appendix checks; the main two-prime and D1 verifiers remain required.',
            'not_established':['historical priority','independent human peer review','complete residual genus-five point list'],
            'sympy_version':sp.__version__}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'status':'PASS','check_groups':len(checks),'tables':list(files)},indent=2))

if __name__=='__main__':main()
