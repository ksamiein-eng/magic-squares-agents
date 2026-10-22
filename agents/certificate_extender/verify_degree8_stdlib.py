#!/usr/bin/env python3
"""Verify all degree-eight proof data with Python's standard library only.

Adapted from verify_degree7_stdlib.py: adds the 32 exponent-sum-eight
representatives, the degree-8 schema, and coverage of the 308 raw normal forms
with k+l <= 8. With --allow-partial it verifies the cases that are present and
reports the missing ones (status PARTIAL); the default is strict.

Reconstructs sine numerators by the addition recurrence, checks all 48 signed
row spaces, and proves every resultant polynomial identity by exact integer
Sylvester determinants at D+1 points with an independently computed bound D.
No numerical approximation, root solver, factorization, or CAS is used.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations, permutations, product
from math import isqrt
from pathlib import Path
import argparse
import json
import sys
import time

Poly = dict[tuple[int,int], int]
ONE: Poly = {(0,0):1}
T: Poly = {(1,0):1}
U: Poly = {(0,1):1}
ROOT = Path(__file__).resolve().parent
EXPECTED = {
    '21_m1_n0': (2,1,1,0),
    '31_m1_n0': (3,1,1,0),
    '31_m2_n0': (3,1,2,0),
    '22_m1_n1': (2,2,1,1),
    '22_m1_nminus1': (2,2,1,-1),
    '41_m1_n0': (4,1,1,0), '41_m3_n0': (4,1,3,0),
    '32_m1_n1': (3,2,1,1), '32_m1_nminus1': (3,2,1,-1),
    '32_m2_n1': (3,2,2,1), '32_m2_nminus1': (3,2,2,-1),
}

EXPECTED.update({'51_m1_n0': (5, 1, 1, 0), '51_m2_n0': (5, 1, 2, 0), '51_m3_n0': (5, 1, 3, 0), '51_m4_n0': (5, 1, 4, 0), '42_m1_n1': (4, 2, 1, 1), '42_m1_nminus1': (4, 2, 1, -1), '42_m3_n1': (4, 2, 3, 1), '42_m3_nminus1': (4, 2, 3, -1), '33_m1_n1': (3, 3, 1, 1), '33_m1_nminus1': (3, 3, 1, -1), '33_m1_n2': (3, 3, 1, 2), '33_m1_nminus2': (3, 3, 1, -2), '33_m2_n2': (3, 3, 2, 2), '33_m2_nminus2': (3, 3, 2, -2)})


EXPECTED.update({'61_m1_n0': (6, 1, 1, 0), '61_m5_n0': (6, 1, 5, 0), '52_m1_n1': (5, 2, 1, 1), '52_m1_nminus1': (5, 2, 1, -1), '52_m2_n1': (5, 2, 2, 1), '52_m2_nminus1': (5, 2, 2, -1), '52_m3_n1': (5, 2, 3, 1), '52_m3_nminus1': (5, 2, 3, -1), '52_m4_n1': (5, 2, 4, 1), '52_m4_nminus1': (5, 2, 4, -1), '43_m1_n1': (4, 3, 1, 1), '43_m1_nminus1': (4, 3, 1, -1), '43_m1_n2': (4, 3, 1, 2), '43_m1_nminus2': (4, 3, 1, -2), '43_m3_n1': (4, 3, 3, 1), '43_m3_nminus1': (4, 3, 3, -1), '43_m3_n2': (4, 3, 3, 2), '43_m3_nminus2': (4, 3, 3, -2)})

EXPECTED.update({'44_m1_n1': (4, 4, 1, 1), '44_m1_nminus1': (4, 4, 1, -1), '44_m1_n3': (4, 4, 1, 3), '44_m1_nminus3': (4, 4, 1, -3), '44_m3_n3': (4, 4, 3, 3), '44_m3_nminus3': (4, 4, 3, -3), '53_m1_n1': (5, 3, 1, 1), '53_m1_nminus1': (5, 3, 1, -1), '53_m1_n2': (5, 3, 1, 2), '53_m1_nminus2': (5, 3, 1, -2), '53_m2_n1': (5, 3, 2, 1), '53_m2_nminus1': (5, 3, 2, -1), '53_m2_n2': (5, 3, 2, 2), '53_m2_nminus2': (5, 3, 2, -2), '53_m3_n1': (5, 3, 3, 1), '53_m3_nminus1': (5, 3, 3, -1), '53_m3_n2': (5, 3, 3, 2), '53_m3_nminus2': (5, 3, 3, -2), '53_m4_n1': (5, 3, 4, 1), '53_m4_nminus1': (5, 3, 4, -1), '53_m4_n2': (5, 3, 4, 2), '53_m4_nminus2': (5, 3, 4, -2), '62_m1_n1': (6, 2, 1, 1), '62_m1_nminus1': (6, 2, 1, -1), '62_m5_n1': (6, 2, 5, 1), '62_m5_nminus1': (6, 2, 5, -1), '71_m1_n0': (7, 1, 1, 0), '71_m2_n0': (7, 1, 2, 0), '71_m3_n0': (7, 1, 3, 0), '71_m4_n0': (7, 1, 4, 0), '71_m5_n0': (7, 1, 5, 0), '71_m6_n0': (7, 1, 6, 0)})

SIGNATURES=[(1,1),(2,1),(3,1),(2,2),(4,1),(3,2),(5,1),(4,2),(3,3),(6,1),(5,2),(4,3),(4,4),(5,3),(6,2),(7,1)]

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def add(*polys: Poly) -> Poly:
    out: Poly = {}
    for f in polys:
        for mon,c in f.items():
            out[mon] = out.get(mon,0)+c
    return {mon:c for mon,c in out.items() if c}


def scale(f: Poly, k: int) -> Poly:
    return {mon:k*c for mon,c in f.items() if k*c}


def mul(f: Poly, g: Poly) -> Poly:
    out: Poly = {}
    for (i,j),c in f.items():
        for (k,l),d in g.items():
            mon = (i+k,j+l)
            out[mon] = out.get(mon,0)+c*d
    return {mon:c for mon,c in out.items() if c}


def power(f: Poly, n: int) -> Poly:
    require(type(n) is int and n>=0, 'invalid polynomial power')
    r = ONE
    while n:
        if n&1:
            r = mul(r,f)
        f = mul(f,f)
        n //= 2
    return r


def decode(data: list, dimensions: int=2) -> Poly:
    require(isinstance(data,list), 'polynomial must be a list')
    out: Poly = {}
    for item in data:
        require(isinstance(item,list) and len(item)==2, 'invalid polynomial term')
        mon,c = item
        require(type(c) is int and isinstance(mon,list) and len(mon)==dimensions
                and all(type(n) is int and n>=0 for n in mon), 'invalid term encoding')
        key = (mon[0],mon[1] if dimensions==2 else 0)
        out[key] = out.get(key,0)+c
    return {mon:c for mon,c in out.items() if c}


def trig_numerator(variable: Poly, n: int, bound: int) -> tuple[Poly,Poly]:
    """Numerators of cos(n angle), sin(n angle), on denominator (1+v^2)^bound."""
    require(type(n) is int and abs(n)<=bound, 'frequency outside bound')
    c1 = add(ONE,scale(power(variable,2),-1))
    s1 = scale(variable,2)
    c,s = ONE,{}
    for _ in range(abs(n)):
        c,s = add(mul(c,c1),scale(mul(s,s1),-1)), add(mul(s,c1),mul(c,s1))
    if n<0:
        s = scale(s,-1)
    multiplier = power(add(ONE,power(variable,2)),bound-abs(n))
    return mul(c,multiplier),mul(s,multiplier)


def numerator(freq: tuple[int,int], bounds: tuple[int,int]) -> Poly:
    c,s = trig_numerator(T,freq[0],bounds[0])
    d,r = trig_numerator(U,freq[1],bounds[1])
    return add(mul(s,d),mul(c,r))


def signed_tags() -> list[tuple]:
    return [(i,j,k,l,a,b) for i,j in combinations(range(4),2)
            for k,l in permutations([v for v in range(4) if v not in (i,j)])
            for a,b in product((-1,1),repeat=2)]


def rref(rows: list[list[int]]) -> tuple:
    a = [[Fraction(x) for x in r] for r in rows]
    row = 0
    for col in range(4):
        pivot = next((r for r in range(row,2) if a[r][col]),None)
        if pivot is None:
            continue
        a[row],a[pivot] = a[pivot],a[row]
        v = a[row][col]
        a[row] = [x/v for x in a[row]]
        for r in range(2):
            if r != row:
                v = a[r][col]
                a[r] = [x-v*y for x,y in zip(a[r],a[row])]
        row += 1
        if row == 2:
            break
    return tuple(tuple(r) for r in a)


def rowspace(i,j,k,l,d,a,b) -> tuple:
    r = [0]*4
    s = [0]*4
    r[i],r[k],r[l] = 1,-a,-b
    s[j],s[k],s[l] = d,-a,b
    return rref([r,s])


def degree(f: Poly, variable: int) -> int:
    require(bool(f), 'degree of zero polynomial not supported')
    return max(m[variable] for m in f)


def evaluate_t_coeffs(f: Poly, t0: int, max_u: int) -> list[int]:
    return [sum(c*t0**i for (i,j),c in f.items() if j==k)
            for k in range(max_u,-1,-1)]


def integer_det(matrix: list[list[int]]) -> int:
    """Fraction-free Bareiss elimination, with exact-division checks and pivots."""
    n = len(matrix)
    require(all(len(row)==n for row in matrix),'non-square determinant')
    if n==0:
        return 1
    a = [row[:] for row in matrix]
    prev,sign = 1,1
    for k in range(n-1):
        pivot = next((r for r in range(k,n) if a[r][k]),None)
        if pivot is None:
            return 0
        if pivot!=k:
            a[k],a[pivot] = a[pivot],a[k]
            sign = -sign
        v = a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                value = a[i][j]*v-a[i][k]*a[k][j]
                q,r = divmod(value,prev)
                require(r==0, 'Bareiss non-exact division')
                a[i][j] = q
            a[i][k] = 0
        prev = v
    return sign*a[-1][-1]


def sylvester_at(f: Poly, g: Poly, t0: int, m: int, n: int) -> int:
    fc,gc = evaluate_t_coeffs(f,t0,m),evaluate_t_coeffs(g,t0,n)
    rows = [[0]*i+fc+[0]*(n-1-i) for i in range(n)]
    rows += [[0]*i+gc+[0]*(m-1-i) for i in range(m)]
    require(m+n>0,'constant/constant system needs a different proof')
    return integer_det(rows)


def verify_resultant(f: Poly,g: Poly,res: Poly) -> tuple[int,int]:
    require(bool(f) and bool(g) and bool(res),'zero equation or unresolved zero resultant')
    require(all(j==0 for i,j in res),'resultant contains u')
    m,n = degree(f,1),degree(g,1)
    D = n*degree(f,0)+m*degree(g,0)
    require(degree(res,0)<=D, 'recorded resultant exceeds proven degree bound')
    # The Sylvester determinant and res are polynomials of degree <= D.
    # Equality at D+1 distinct integers proves their identity, not a heuristic.
    for t0 in range(D+1):
        value = sum(c*t0**i for (i,j),c in res.items())
        require(value==sylvester_at(f,g,t0,m,n),f'Sylvester identity fails at t={t0}')
    return D,D+1


def prime(p: int) -> bool:
    return type(p) is int and p>=2 and all(p%d for d in range(2,isqrt(p)+1))


def witness_degeneracy(values: list[dict]) -> dict | None:
    for i,v in enumerate(values):
        if not v:
            return {'kind':'zero_offset','index':i}
    for i,j in combinations(range(4),2):
        if values[i]==values[j]:
            return {'kind':'equal_offsets','indices':[i,j],'sign':1}
        if values[i]=={mon:-c for mon,c in values[j].items()}:
            return {'kind':'equal_offsets','indices':[i,j],'sign':-1}
    return None


def finite_fiber(es: list[Poly], r: Fraction) -> dict:
    vals=[]
    for e in es:
        out={}
        for (i,j),c in e.items():
            out[j]=out.get(j,Fraction(0))+c*r**i
        vals.append({m:c for m,c in out.items() if c})
    found=witness_degeneracy(vals)
    require(found is not None, f'finite fiber t={r} is not certified degenerate')
    return {'parameter':[r.numerator,r.denominator],**found}


def boundary_fibers(es: list[Poly],bounds: tuple[int,int]) -> dict:
    a,b = bounds
    t_inf = [{j:c for (i,j),c in e.items() if i==2*a} for e in es]
    u_inf = [{i:c for (i,j),c in e.items() if j==2*b} for e in es]
    both = [{0:e[(2*a,2*b)]} if (2*a,2*b) in e else {} for e in es]
    output = {key:witness_degeneracy(v) for key,v in
              [('t_infinity',t_inf),('u_infinity',u_inf),('both_infinity',both)]}
    require(all(v is not None for v in output.values()), 'unresolved projective boundary')
    return output


def canonical_vector(v):
    v=tuple(v)
    require(any(v),'zero frequency vector')
    return v if next(c for c in v if c)>0 else tuple(-c for c in v)


def canonical_set(freqs):
    return tuple(sorted(canonical_vector(v) for v in freqs))


def normal(a,b,m,n):
    return ((a,b),(a,-b),(m,b),(a,n))


def orbit(freqs,bounds):
    perms=[(0,1),(1,0)] if bounds[0]==bounds[1] else [(0,1)]
    return {canonical_set([(s*v[pm[0]],q*v[pm[1]]) for v in freqs])
            for s,q in product((-1,1),repeat=2) for pm in perms}


def check_coverage(signatures=None) -> list[dict]:
    """Exhaustive equality checks of all necessary normal forms and proof routes.

    Every inherited route exhibits a source certificate, a coordinate permutation,
    and positive integer power-map multipliers. No asserted ratio rule is trusted.
    """
    routes=[]
    if signatures is None:
        signatures=SIGNATURES
    for a,b in signatures:
        direct={}
        for key,(k,l,m,n) in EXPECTED.items():
            if (a,b)==(k,l):
                for target in orbit(normal(k,l,m,n),(k,l)):
                    direct[target]=key
        for m in range(1-a,a):
            for n in range(1-b,b):
                target=canonical_set(normal(a,b,m,n))
                rec={'bounds':[a,b],'drops':[m,n]}
                if m==n==0:
                    require(target==canonical_set([(a,0),(0,b),(a,b),(a,-b)]),
                            'parallelogram identity')
                    rec['route']='real_angle_parallelogram'
                elif target in direct:
                    rec.update(route='direct_certificate',certificate=direct[target])
                else:
                    found=None
                    for key,(k,l,h,j) in EXPECTED.items():
                        base=normal(k,l,h,j)
                        for pm in [(0,1),(1,0)]:
                            kb,lb=(k,l)[pm[0]],(k,l)[pm[1]]
                            if a%kb or b%lb:
                                continue
                            d,e=a//kb,b//lb
                            scaled=tuple((d*v[pm[0]],e*v[pm[1]]) for v in base)
                            if target in orbit(scaled,(a,b)):
                                found={'route':'rational_circle_power_pullback',
                                       'certificate':key,'coordinate_permutation':list(pm),
                                       'frequency_coordinate_multipliers':[d,e]}
                                break
                        if found is not None:
                            break
                    require(found is not None,f'UNRESOLVED configuration {(a,b,m,n)}')
                    rec.update(found)
                routes.append(rec)
    require(len(routes)==sum((2*a-1)*(2*b-1) for a,b in signatures),'raw normal-form coverage count')
    require(signatures!=SIGNATURES or len(routes)==308,'raw normal-form coverage count')
    return routes


def verify(data: dict, allow_partial: bool=False) -> dict:
    start=time.perf_counter()
    require(data['schema']=='magic-squares/degree8/v6','unrecognized schema')
    cases=data['cases']
    present={c['id'] for c in cases}
    require(len(cases)==len(present) and present<=set(EXPECTED),'unknown or duplicate case')
    missing=sorted(set(EXPECTED)-present)
    require(allow_partial or not missing,'case coverage mismatch')
    require(not data.get('unresolved') and all(c.get('status') in (None,'PASS') for c in cases)
            and all(s.get('status') is None for c in cases for s in c['systems']),'certificate marks unresolved cases')
    tags=signed_tags()
    small={rowspace(i,j,k,l,1,a,b) for i,j,k,l,a,b in tags}
    full={rowspace(i,j,k,l,d,a,b) for i,j,k,l in permutations(range(4))
          for d,a,b in product((-1,1),repeat=3)}
    require(len(tags)==48 and len(full)==48 and small==full,'signed row-space coverage fails')
    factor_map={}
    roots={}
    rootless=set()
    primes=set()
    for record in data['factor_catalog']:
        key=record['id']
        require(key not in factor_map,'duplicate factor ID')
        cs=record['coefficients_high_to_low']
        require(isinstance(cs,list) and len(cs)>1 and all(type(c) is int for c in cs) and cs[0]!=0,
                'malformed catalog polynomial')
        degree_f=len(cs)-1
        factor_map[key]={(degree_f-i,0):c for i,c in enumerate(cs) if c}
        if record['type']=='rational_root':
            require(degree_f==1,'rational-root entry not linear')
            root=-Fraction(cs[1],cs[0])
            require(record['root']==[root.numerator,root.denominator],'incorrect rational root')
            roots[key]=root
        else:
            require(record['type']=='no_rational_root','unproved factor classification')
            p=record['prime']
            require(prime(p) and cs[0]%p!=0,'invalid prime or leading coefficient')
            residues=[]
            for z in range(p):
                v=0
                for c in cs:
                    v=(v*z+c)%p
                residues.append(v)
            require(all(residues) and residues==record['residues'],'modular no-root witness fails')
            rootless.add(key)
            primes.add(p)
    case_results=[]
    seen_factors=set()
    total_evaluations=0
    for case in cases:
        label=case['id']
        a,b,m,n=EXPECTED[label]
        freqs=normal(a,b,m,n)
        require(case['bounds']==[a,b] and case['drops']==[m,n]
                and case['frequencies']==[list(v) for v in freqs], 'frequency specification mismatch')
        es=[numerator(v,(a,b)) for v in freqs]
        require(len(case['area_numerators'])==4
                and all(e==decode(rec) for e,rec in zip(es,case['area_numerators'])), 'sine numerator mismatch')
        systems=case['systems']
        require(len(systems)==48 and {tuple(s['assignment']) for s in systems}==set(tags)
                and {s['id'] for s in systems}==set(range(48)), '48-system coverage fails')
        case_factors=set()
        case_roots=set()
        evaluations=0
        max_bound=0
        removed=0
        for system in systems:
            tag=tuple(system['assignment'])
            require(tags[system['id']]==tag,'system ID does not match tag')
            i,j,k,l,sg,sh=tag
            g1=add(es[i],scale(es[k],-sg),scale(es[l],-sh))
            g2=add(es[j],scale(es[k],-sg),scale(es[l],sh))
            require(g1==decode(system['G1']) and g2==decode(system['G2']), 'input relation mismatch')
            r=system['removed_t_power']
            require(type(r) is int and r>=0,'invalid removed factor')
            f,g=decode(system['F']),decode(system['G'])
            require(mul(power(T,r),f)==g1 and mul(power(T,r),g)==g2,
                    'division identity fails')
            if r:
                finite_fiber(es,Fraction(0))
                removed+=1
                case_roots.add(Fraction(0))
            res=decode(system['resultant'],1)
            bound,evaluated=verify_resultant(f,g,res)
            max_bound=max(max_bound,bound)
            evaluations+=evaluated
            c=system['constant']
            require(type(c) is int and c!=0,'invalid factorization constant')
            prod=scale(ONE,c)
            for entry in system['factors']:
                key=entry['factor_id']
                exponent=entry['exponent']
                require(key in factor_map and type(exponent) is int and exponent>0,
                        'invalid factorization entry')
                prod=mul(prod,power(factor_map[key],exponent))
                case_factors.add(key)
                if key in roots:
                    case_roots.add(roots[key])
            require(prod==res,'factor product is not the resultant')
        finite=[finite_fiber(es,r) for r in sorted(case_roots)]
        boundaries=boundary_fibers(es,(a,b))
        seen_factors |= case_factors
        total_evaluations+=evaluations
        case_results.append({'id':label,'status':'PASS','systems':48,
                             'removed_t_systems':removed,'distinct_factors':len(case_factors),
                             'rootless_factors':len(case_factors & rootless),
                             'max_determinant_degree_bound':max_bound,
                             'exact_determinant_evaluations':evaluations,
                             'finite_fibers':finite,'projective_boundaries':boundaries})
    require(seen_factors==set(factor_map),'unused catalog entries')
    complete=[sig for sig in SIGNATURES if all(key in present for key,v in EXPECTED.items() if v[:2]==sig)]
    coverage=check_coverage(complete)
    return {'status':'PASS' if not missing else 'PARTIAL','schema':'magic-squares/degree8-verification/v6',
            'missing_cases':missing,'fully_certified_signatures':[list(s) for s in complete],
            'verifier':'Python standard library only; no CAS',
            'cases':case_results,'total_systems':sum(r['systems'] for r in case_results),
            'new_degree_eight_systems':48*sum(1 for v in EXPECTED.values() if sum(v[:2])==8),'raw_signed_assignments':192,'distinct_signed_row_spaces':48,
            'distinct_catalog_factors':len(factor_map),'rootless_catalog_factors':len(rootless),
            'modular_primes':sorted(primes),'exact_integer_determinants':total_evaluations,
            'normal_form_coverage':coverage,
            'claim':('no nondegenerate rational-circle solution for the full-depth normal forms of all positive exponent pairs of sum at most eight' if not missing else 'PARTIAL: only the listed fully certified signatures are covered; the sum-eight claim is NOT established'),
            'arithmetic_consequence':('primitive central root p^k q^l with distinct primes requires k+l >= 9' if not missing else 'not established by this partial run'),
            'proof_boundary':'written normal-form and real-angle proofs plus the checked exact algebra; not a formal proof-assistant development',
            'elapsed_seconds':round(time.perf_counter()-start,3)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', nargs='?', type=Path, default=ROOT/'results'/'certificate_degree8.json')
    parser.add_argument('--allow-partial',action='store_true',help='Verify present cases only; report missing ones with status PARTIAL.')
    parser.add_argument('--output',type=Path,default=None,help='Optional verification JSON; otherwise stdout only.')
    args=parser.parse_args()
    report=verify(json.loads(args.certificate.read_text()),allow_partial=args.allow_partial)
    text=json.dumps(report,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(text,end='')

if __name__=='__main__':
    main()
