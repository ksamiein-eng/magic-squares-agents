#!/usr/bin/env python3
"""Exact regressions for the repaired elementary core.
Finite triangle tests corroborate the written general proofs; they are not
represented as exhaustive tests of the magic-square problem.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction
from itertools import product, combinations, permutations
from math import gcd, isqrt, prod
from pathlib import Path
import json
import platform
import sympy as sp

ROOT=Path(__file__).resolve().parent
checks=[]

def check(name, condition, details=None):
    if not condition:
        raise RuntimeError('FAILED: '+name)
    checks.append({'name':name,'status':'PASS','details':details})
    print('PASS',name,details if details is not None else '')


def canon(v):
    for a in v:
        if a:
            return tuple(v) if a>0 else tuple(-x for x in v)
    return tuple(v)


def cset(vectors): return tuple(sorted(canon(v) for v in vectors))


def cmul(z,w): return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])


def cpow(z,n):
    if n<0: z=(z[0],-z[1]);n=-n
    value=(1,0)
    while n:
        if n&1: value=cmul(value,z)
        z=cmul(z,z);n//=2
    return value


def valuation(n,p):
    n=abs(n)
    if n==0: raise ValueError('valuation of zero')
    v=0
    while n%p==0: n//=p;v+=1
    return v


def run():
    a,b,e=sp.symbols('a b e')
    M=sp.Matrix([[e+a,e-a-b,e+b],[e-a+b,e,e+a-b],[e-b,e+a+b,e-a]])
    lines=[sum(M[i,j] for j in range(3)) for i in range(3)]
    lines += [sum(M[i,j] for i in range(3)) for j in range(3)]
    lines += [sum(M[i,i] for i in range(3)),sum(M[i,2-i] for i in range(3))]
    check('Lucas row/column/diagonal sums',all(sp.expand(x-3*e)==0 for x in lines))
    offsets=[0,a,-a,b,-b,a+b,-a-b,a-b,-a+b]
    product_diff=sp.prod(offsets[i]-offsets[j] for i,j in combinations(range(9),2))
    actual={str(sp.Poly(f,a,b).monic().as_expr()) for f,_ in sp.factor_list(product_diff)[1]}
    expected={str(sp.Poly(f,a,b).monic().as_expr()) for f in [a,b,a-b,a+b,a-2*b,a+2*b,2*a-b,2*a+b]}
    check('Lucas distinctness zero locus',actual==expected)
    t,u=sp.symbols('t u')
    sx,cx=2*t/(1+t*t),(1-t*t)/(1+t*t)
    sz,cz=2*u/(1+u*u),(1-u*u)/(1+u*u)
    pp,qq=sx*cz+cx*sz,sx*cz-cx*sz
    check('two real-angle identities',sp.cancel(pp**2*qq**2-(sx*sx-sz*sz)**2)==0 and
          sp.cancel(pp*pp+qq*qq-2*(sx*sx+sz*sz-2*sx*sx*sz*sz))==0)
    vals=[a,b,a+b,a-b];case_rows=[]
    for ij in combinations(range(4),2):
        kl=[k for k in range(4) if k not in ij]
        p,q=vals[ij[0]],vals[ij[1]];x,z=vals[kl[0]],vals[kl[1]]
        residual=sp.factor(p*p*q*q-(x*x-z*z)**2)
        other=sp.factor(p*p+q*q-2*(x*x+z*z-2*x*x*z*z))
        case_rows.append({'PQ':[str(p),str(q)],'first_residual':str(residual),'second_residual':str(other)})
    check('six real-angle cases',[r['first_residual'] for r in case_rows]==[
        '-15*a**2*b**2','3*a**2*b*(2*a - b)','-3*a**2*b*(2*a + b)',
        '-3*a*b**2*(a - 2*b)','-3*a*b**2*(a + 2*b)','0'] and
        case_rows[-1]['second_residual']=='4*a**2*b**2')
    limit=10000
    fac={y:{int(p):int(k) for p,k in sp.factorint(y).items()} for y in range(1,limit+1,2)}
    fac={y:fs for y,fs in fac.items() if all(p%4==1 for p in fs)}
    euclid=defaultdict(set)
    for m in range(2,isqrt(limit)+1):
        for n in range(1,m):
            d=m*m+n*n
            if d>limit or gcd(m,n)>1 or (m-n)%2==0: continue
            p0,q0=m*m-n*n,2*m*n
            for g in range(1,limit//d+1):
                y=g*d
                if y in fac: euclid[y].add(tuple(sorted((g*p0,g*q0))))
    gaussian_primes={}
    triangle_checks=0;gaussian_checks=0
    for y,fs in fac.items():
        check_count=(prod(2*k+1 for k in fs.values())-1)//2
        if len(euclid[y])!=check_count: raise RuntimeError(f'count at {y}')
        for p,q in euclid[y]:
            if p*p+q*q!=y*y or (p-q)**2+y*y+(p+q)**2!=3*y*y: raise RuntimeError('AP failure')
            g=gcd(p,q);d=y//g;delta=2*p*q
            for ell,k in fs.items():
                h=valuation(d,ell) if d%ell==0 else 0
                v=valuation(delta,ell)
                if not (v==2*(k-h) if h else v>=2*k): raise RuntimeError('valuation failure')
            triangle_checks+=1
        ell_list=list(fs)
        for ell in ell_list:
            if ell not in gaussian_primes:
                for A in range(1,isqrt(ell)+1):
                    B=isqrt(ell-A*A)
                    if B>0 and A*A+B*B==ell:
                        gaussian_primes[ell]=(A,B);break
        gs=set()
        for mvec in product(*(range(-fs[ell],fs[ell]+1) for ell in ell_list)):
            if not any(mvec) or canon(mvec)!=mvec: continue
            z=(1,0);unit=(Fraction(1),Fraction(0))
            for ell,mj in zip(ell_list,mvec):
                A,B=gaussian_primes[ell];kj=fs[ell]
                z=cmul(z,cmul(cpow((A,B),kj+mj),cpow((A,-B),kj-mj)))
                # Area circle point from its half-angle, independently of z.
                ht=Fraction(2*A*B,A*A-B*B)
                circle=((1-ht*ht)/(1+ht*ht),2*ht/(1+ht*ht))
                unit=cmul(unit,cpow(circle,mj))
            legs=tuple(sorted((abs(z[0]),abs(z[1]))))
            if legs[0]==0 or z[0]**2+z[1]**2!=y*y: raise RuntimeError('Gaussian representative')
            if abs(unit[1])!=Fraction(2*legs[0]*legs[1],y*y): raise RuntimeError('area angle mismatch')
            gs.add(legs);gaussian_checks+=1
        if gs!=euclid[y]: raise RuntimeError('Euclid/Gaussian disagreement')
    check('integral triangle count and valuation through y=10000',triangle_checks==3000,
          {'admissible_y':len(fac),'triangles':triangle_checks,'bound':limit})
    check('Gaussian representatives and corrected half-area-angle',gaussian_checks==3000,
          {'triangles':gaussian_checks,'independent_generation':'Euclidean versus Gaussian'})
    vectors=sorted({canon(v) for v in product((-1,0,1),repeat=3) if any(v)})
    admissible=[cset(S) for S in combinations(vectors,4) if all(sum(abs(v[j])==1 for v in S)>=3 for j in range(3))]
    group=list(product(tuple(product((-1,1),repeat=3)),tuple(permutations(range(3)))))
    def act(S,sg,pm): return cset(tuple(sg[j]*v[pm[j]] for j in range(3)) for v in S)
    seen=set();orbits=[]
    for S in admissible:
        if S in seen: continue
        orb={act(S,sg,pm) for sg,pm in group}; seen|=orb
        orbits.append({'representative':min(orb),'size':len(orb),'stabilizer_order':48//len(orb),
                       'members':sorted(orb)})
    check('three-prime orbit enumeration',(len(vectors),len(admissible),len(orbits))==(13,177,15),
          {'vectors':13,'admissible_sets':177,'orbits':15,'orbit_sizes':sorted(o['size'] for o in orbits)})
    def parallelogram(S):
        for r,s in permutations(S,2):
            for sign in (-1,1):
                v=tuple(sign*z for z in s)
                candidate=cset([r,v,tuple(x+y for x,y in zip(r,v)),tuple(x-y for x,y in zip(r,v))])
                if candidate==S:return {'u':r,'v':v}
        return None
    para=[{'set':S,'witness':parallelogram(S)} for S in admissible if parallelogram(S)]
    E1=cset([(0,1,0),(1,-1,-1),(1,0,-1),(1,1,-1)])
    E1_orbit={act(E1,sg,pm) for sg,pm in group}
    check('E1 is exactly the frequency-parallelogram orbit',{tuple(map(tuple,p['set'])) for p in para}==E1_orbit and len(para)==6)
    pair_records=[]
    for k in range(1,7):
        for l in range(1,k+1):
            if k+l>7:continue
            raw={cset([(k,l),(k,-l),(m,l),(k,n)]) for m in range(-k+1,k) for n in range(-l+1,l)}
            box=sorted({canon(v) for v in product(range(-k,k+1),range(-l,l+1)) if any(v)})
            direct={cset(S) for S in combinations(box,4) if all(sum(abs(v[j])==h for v in S)>=3 for j,h in enumerate((k,l)))}
            if raw!=direct:raise RuntimeError('two-prime shape not exhaustive')
            perms=[(0,1),(1,0)] if k==l else [(0,1)]
            def key(S):
                return min(cset(tuple(sg[j]*v[pm[j]] for j in range(2)) for v in S)
                           for sg in product((-1,1),repeat=2) for pm in perms)
            reps=sorted({key(S) for S in raw})
            pair_records.append({'exponents':[k,l],'raw_count':len(raw),'orbit_count':len(reps),'representatives':reps})
    totals=(len(pair_records),sum(r['raw_count'] for r in pair_records),sum(r['orbit_count'] for r in pair_records))
    check('complete two-prime configuration enumeration through exponent sum 7',totals==(12,168,85),
          {'pairs':totals[0],'raw_configurations':totals[1],'symmetry_classes':totals[2],
           'warning':'configuration coverage only, not a nonexistence proof for all pairs'})
    # Reciprocal genus-two covers and elliptic quotient invariants.
    s,w=sp.symbols('s w');fB=s**3+11*s*s-5*s+1;fC=s**3-5*s*s+11*s+1
    check('reciprocal cubic identity',sp.cancel(fC-s**3*fB.subs(s,1/s))==0)
    f6=fB.subs(s,w*w)
    discr=int(sp.discriminant(f6,w))
    check('genus-two cover smoothness',discr!=0,{'sextic_discriminant':discr})
    check('two quotient map identities',sp.cancel(f6/w**6-fC.subs(s,1/w**2))==0)
    # Pullback of ds/(2v) equals w dw/Y and -dw/Y respectively.
    check('independent pullback differentials',sp.cancel(sp.diff(w*w,w)/2-w)==0 and
          sp.cancel(sp.diff(w**-2,w)/(2*w**-3)+1)==0)
    def ej(a2,a4,a6):
        b2,b4,b6,b8=4*a2,2*a4,4*a6,4*a2*a6-a4*a4
        c4=b2*b2-24*b4
        delta=-b2*b2*b8-8*b4**3-27*b6*b6+9*b2*b4*b6
        return Fraction(c4**3,delta),delta
    jB,dB=ej(11,-5,1);jC,dC=ej(-5,11,1)
    def count(poly,p): return 1+sum((z*z-int(poly.subs(s,x)))%p==0 for x in range(p) for z in range(p))
    check('distinct elliptic quotients at good prime 3',dB%3!=0 and dC%3!=0 and (count(fB,3),count(fC,3))==(5,3),
          {'jB':str(jB),'jC':str(jC),'point_counts_mod_3':[5,3]})
    A,B,C,D,c=sp.symbols('A B C D c')
    f=A*s**3+B*s*s+C*s+D
    g=sp.cancel((1+c)**3*f.subs(s,(1-c)/(1+c)))
    ell=(A-B+C-D)*c/(8*D)+(-3*A-B+C+3*D)/(8*D)
    check('cubic coefficient law',sp.expand((g-8*D*(1+c*(1-c)*ell)).subs(B,7*D-A-C))==0)
    T=2*t/(1-t*t)
    check('double-angle lift identity',sp.cancel(1+T*T-(1+t*t)**2/(1-t*t)**2)==0 and
          sp.simplify(T.subs(t,2))==sp.Rational(-4,3) and
          sp.simplify(T.subs(t,sp.Rational(-1,2)))==sp.Rational(-4,3))
    out=ROOT/'results';out.mkdir(exist_ok=True)
    for filename,value in [('foundation_checks.json',{'status':'PASS','checks':checks,'python':platform.python_version(),'sympy':sp.__version__}),
                           ('orbits_3prime.json',{'orbits':orbits,'E1_members':para}),
                           ('configurations_2prime_sum7.json',pair_records),('real_angle_residuals.json',case_rows)]:
        (out/filename).write_text(json.dumps(value,indent=2)+'\n')
    print('ALL',len(checks),'CHECK GROUPS PASSED')

if __name__=='__main__':run()
