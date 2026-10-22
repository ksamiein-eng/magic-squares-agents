#!/usr/bin/env python3
"""Check the (2,1) certificate using only Python's standard library.
No SymPy, PARI, Sage, factorization, resultant, or root-solving library is used.
Sparse integer polynomials and a <=4 by 4 determinant are implemented below.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import json
import sys

Poly = dict[tuple[int, int], int]
ONE={(0,0):1}; T={(1,0):1}; U={(0,1):1}
ROOT=Path(__file__).resolve().parent


def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)


def add(*values: Poly) -> Poly:
    out:Poly={}
    for value in values:
        for m,c in value.items():out[m]=out.get(m,0)+c
    return {m:c for m,c in out.items() if c}


def scale(p: Poly,c:int) -> Poly:return {m:c*v for m,v in p.items() if c*v}


def mul(p: Poly,q: Poly) -> Poly:
    out:Poly={}
    for (a,b),v in p.items():
        for (c,d),w in q.items():out[(a+c,b+d)]=out.get((a+c,b+d),0)+v*w
    return {m:c for m,c in out.items() if c}


def power(p: Poly,n:int) -> Poly:
    require(isinstance(n,int) and n>=0,'bad power')
    result=ONE
    while n:
        if n&1:result=mul(result,p)
        p=mul(p,p);n//=2
    return result


def decode(terms:list,dimensions:int=2) -> Poly:
    out:Poly={}
    for m,c in terms:
        require(isinstance(c,int) and len(m)==dimensions and all(isinstance(n,int) and n>=0 for n in m),'bad polynomial encoding')
        key=(m[0],m[1] if dimensions==2 else 0)
        out[key]=out.get(key,0)+c
    return {m:c for m,c in out.items() if c}


def coeff_u(f:Poly,n:int) -> Poly:return {(i,0):c for (i,j),c in f.items() if j==n}


def determinant(matrix:list[list[Poly]]) -> Poly:
    n=len(matrix);out={}
    for p in permutations(range(n)):
        sign=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        term=ONE
        for i in range(n):term=mul(term,matrix[i][p[i]])
        out=add(out,scale(term,sign))
    return out


def sylvester(f:Poly,g:Poly) -> Poly:
    require(bool(f) and bool(g),'zero polynomial input')
    m=max(j for i,j in f);n=max(j for i,j in g)
    if m==0:return power(f,n)
    if n==0:return power(g,m)
    fc=[coeff_u(f,j) for j in range(m,-1,-1)]
    gc=[coeff_u(g,j) for j in range(n,-1,-1)]
    rows=[[{}]*i+fc+[{}]*(n-1-i) for i in range(n)]
    rows += [[{}]*i+gc+[{}]*(m-1-i) for i in range(m)]
    require(len(rows)<=4,'certificate exceeds designed determinant size')
    return determinant(rows)


def substitute_t(f:Poly,t0:int) -> Poly:
    result={}
    for (i,j),c in f.items():result[(0,j)]=result.get((0,j),0)+c*t0**i
    return {m:c for m,c in result.items() if c}


def rref_key(rows:list[list[int]]) -> tuple:
    a=[[Fraction(v) for v in row] for row in rows];row=0
    for j in range(4):
        pivot=next((r for r in range(row,2) if a[r][j]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row]
        q=a[row][j];a[row]=[v/q for v in a[row]]
        for r in range(2):
            if r!=row:
                q=a[r][j];a[r]=[v-q*w for v,w in zip(a[r],a[row])]
        row+=1
        if row==2:break
    return tuple(tuple(r) for r in a)


def rowspace(i,j,k,l,d,a,b):
    r=[0]*4;q=[0]*4;r[i]=1;r[k]=-a;r[l]=-b;q[j]=d;q[k]=-a;q[l]=b
    return rref_key([r,q])


def main(path:Path) -> dict:
    data=json.loads(path.read_text())
    require(data['schema']=='magic-squares-priority-repair/21/v1','wrong certificate schema')
    require(data['frequencies']==[[2,1],[2,-1],[1,1],[2,0]],'wrong frequencies')
    t2=power(T,2);u2=power(U,2);t4=power(T,4)
    first=scale(mul(mul(T,add(ONE,scale(t2,-1))),add(ONE,scale(u2,-1))),4)
    second=scale(mul(U,add(ONE,scale(t2,-6),t4)),2)
    E=[add(first,second),add(first,scale(second,-1)),
       add(scale(mul(mul(T,add(ONE,t2)),add(ONE,scale(u2,-1))),2),scale(mul(U,add(ONE,scale(t4,-1))),2)),
       scale(mul(mul(T,add(ONE,scale(t2,-1))),add(ONE,u2)),4)]
    require(len(data['area_numerators'])==4,'wrong offset count')
    require(all(decode(v)==e for v,e in zip(data['area_numerators'],E)),'offset formula mismatch')
    tags=[(i,j,k,l,a,b) for i,j in combinations(range(4),2)
          for k,l in permutations([v for v in range(4) if v not in (i,j)])
          for a,b in product((-1,1),repeat=2)]
    require(len(data['systems'])==48 and {tuple(s['assignment']) for s in data['systems']}==set(tags),'assignment coverage')
    reduced={rowspace(i,j,k,l,1,a,b) for i,j,k,l,a,b in tags}
    full={rowspace(i,j,k,l,d,a,b) for i,j,k,l in permutations(range(4)) for d,a,b in product((-1,1),repeat=3)}
    require(reduced==full and len(full)==48,'signed row-space coverage')
    factors={};primes=set();rootless=0
    for f in data['factor_catalog']:
        cs=f['coefficients_high_to_low'];deg=len(cs)-1
        require(deg>=1 and all(isinstance(c,int) for c in cs) and cs[0]!=0,'bad catalog polynomial')
        require(f['id'] not in factors,'duplicate factor label')
        factors[f['id']]={(deg-i,0):c for i,c in enumerate(cs) if c}
        if f['type']=='degenerate_root':
            require(deg==1 and -Fraction(cs[1],cs[0]) in (-1,0,1),'unproved linear root')
        else:
            require(f['type']=='no_rational_root','unrecognized status')
            p=f['prime'];require(p in (3,5,7) and cs[0]%p!=0,'bad modular prime or leading coefficient')
            residues=[]
            for r in range(p):
                value=0
                for c in cs:value=(value*r+c)%p
                residues.append(value)
            require(all(residues) and residues==f['residues'],'no-root witness fails')
            rootless+=1;primes.add(p)
    for record in data['systems']:
        i,j,k,l,a,b=record['assignment']
        G1=add(E[i],scale(E[k],-a),scale(E[l],-b))
        G2=add(E[j],scale(E[k],-a),scale(E[l],b))
        require(G1==decode(record['G1']) and G2==decode(record['G2']),'input system mismatch')
        require(isinstance(record['removed_t_factor'],bool),'bad removal flag')
        divisor=T if record['removed_t_factor'] else ONE
        F,G=decode(record['F']),decode(record['G'])
        require(mul(divisor,F)==G1 and mul(divisor,G)==G2,'removed factor mismatch')
        R=decode(record['resultant'],1)
        require(bool(R) and sylvester(F,G)==R,'determinant mismatch')
        require(isinstance(record['constant'],int) and record['constant']!=0,'bad constant')
        result=scale(ONE,record['constant'])
        for item in record['factors']:
            require(item['factor_id'] in factors and isinstance(item['exponent'],int) and item['exponent']>0,'bad factor reference')
            result=mul(result,power(factors[item['factor_id']],item['exponent']))
        require(result==R,'factorization identity fails')
    require(all(not substitute_t(E[3],v) for v in (-1,0,1)),'finite fibers')
    # Homogenize in t to degree 4 and in u to degree 2.
    require(not any(i==4 for i,j in E[3]),'t=infinity boundary')
    require(coeff_u(E[0],2)==coeff_u(E[1],2),'u=infinity boundary')
    require((4,2) not in E[3],'infinity/infinity intersection')
    return {'status':'PASS','verifier':'Python standard library only','systems':48,
            'raw_signed_assignments':192,'distinct_signed_row_spaces':48,
            'rootless_factors':rootless,'modular_primes':sorted(primes),
            'projective_boundaries':'verified','factorizations_and_determinants':'exact integer polynomial identities',
            'scope':'nonzero-drop (2,1) representative; written normal-form proof covers the other representatives'}

if __name__=='__main__':
    result=main(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'results'/'certificate_21.json')
    (ROOT/'results'/'verification_stdlib.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
