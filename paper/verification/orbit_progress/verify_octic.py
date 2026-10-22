#!/usr/bin/env python3
"""Exact rank-zero obstruction for H=t^8-13t^6+36t^4-13t^2+1.

No third-party packages. No bounded rational-point search. Uses the standard
2-isogeny rank formula, with exhaustive square-class obstructions and torsion
bounds checked below. The accompanying proof explains the logical deductions.
"""
from fractions import Fraction as Q
from math import gcd,isqrt
from pathlib import Path
import json,sys

class ProofError(ValueError): pass

def need(ok, message):
    if not ok: raise ProofError(message)

def trim(p):
    p=list(p)
    while len(p)>1 and not p[-1]: p.pop()
    return p

def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return trim(c)

def divrem(a,b):
    a=trim(map(Q,a));b=trim(map(Q,b));need(any(b),'zero polynomial divisor')
    c=[Q(0)]*max(1,len(a)-len(b)+1)
    while any(a) and len(a)>=len(b):
        k=len(a)-len(b);z=a[-1]/b[-1];c[k]+=z
        for j,x in enumerate(b): a[j+k]-=z*x
        a=trim(a)
    return trim(c),a

def squarefree(p):
    a=trim(p);b=[i*p[i] for i in range(1,len(p))]
    while any(b):a,b=b,divrem(a,b)[1]
    return len(trim(a))==1

def evaluate(p,x):
    a=0
    for c in reversed(p):a=a*x+c
    return a

def prime_factors(n):
    n=abs(n);out=[];p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:out.append(n)
    return out

def squareclasses(B):
    p=[1]
    for r in prime_factors(B):p += [x*r for x in p]
    return sorted(p+[-x for x in p])

def local_obstruction(A,B,d,p,e):
    need(B%d==0 and prime_factors(p)==[p] and e>=1,'bad local witness')
    m=p**e;S={x*x%m for x in range(m)};b=B//d
    # Independent implementations: all primitive pairs, and normalized charts.
    vals={(d*u**4+A*u*u*v*v+b*v**4)%m
          for u in range(m) for v in range(m) if u%p or v%p}
    chart1={(d*u**4+A*u*u+b)%m for u in range(m)}
    chart2={(d+A*v*v+b*v**4)%m for v in range(0,m,p)}
    brute=not(vals&S);charts=not((chart1|chart2)&S)
    need(brute==charts,'primitive charts disagree with all-pairs test')
    need(brute,'claimed local obstruction has a solution')
    return {'modulus':m,'primitive_residues':sorted(vals),'square_residues':sorted(S)}

def count_curve(A,B,p):
    lhs=1+sum((y*y-x**3-A*x*x-B*x)%p==0 for x in range(p) for y in range(p))
    rhs=1
    for x in range(p):
        z=(x**3+A*x*x+B*x)%p
        rhs += 1 if not z else (2 if pow(z,(p-1)//2,p)==1 else 0)
    need(lhs==rhs,'point counting cross-check failed')
    return lhs

def certificate():
    return {
      'H_coefficients_low_to_high':[1,0,-13,0,36,0,-13,0,1],
      'Q_coefficients_low_to_high':[64,0,-17,0,1],
      'elliptic_model':[0,-17,0,64,0],
      'isogenous_model':[0,34,0,33,0],
      'images':[
        {'A':-17,'B':64,'allowed':[1],
         'excluded':{'-2':'negative','-1':'negative','2':[3,1]}},
        {'A':34,'B':33,'allowed':[-33,-1,1,33],
         'excluded':{'-11':[2,5],'-3':[2,5],'3':[2,6],'11':[2,6]}}
      ],
      'good_prime_counts':{'5':4,'7':4},
      'elliptic_rational_points':['O',['0','0']],
      'quartic_affine_points':[['0','8'],['0','-8']],
      'quartic_infinity_points':2,
      'octic_affine_points':[['0','1'],['0','-1']],
      'octic_infinity_points':2
    }

def verify(data):
    expected=certificate()
    # Fix the target problem, not just internally compatible arbitrary input.
    for k in ['H_coefficients_low_to_high','Q_coefficients_low_to_high',
              'elliptic_model','isogenous_model']:
        need(data[k]==expected[k],f'wrong target {k}')
    H=data['H_coefficients_low_to_high'];q=data['Q_coefficients_low_to_high']
    need(squarefree(H) and squarefree(q),'singular claimed smooth model')
    # Laurent identity H(t)/t^4 = Q(t+t^-1).
    def lm(a,b):
        c={}
        for i,x in a.items():
            for j,y in b.items():c[i+j]=c.get(i+j,0)+x*y
        return {i:x for i,x in c.items() if x}
    L={0:1};total={}
    for a in q:
        for j,c in L.items():total[j]=total.get(j,0)+a*c
        L=lm(L,{1:1,-1:1})
    need({j:c for j,c in total.items() if c}=={i-4:c for i,c in enumerate(H) if c},'Laurent quotient identity')
    # Map (r,s) -> (r^2,r*s), exactly: RHS = r^2 Q(r).
    need(mul([0,0,1],q)==[0,0,64,0,-17,0,1],'elliptic map identity')
    expected_pairs=[(-17,64),(34,33)];need(len(data['images'])==2,'missing descent image')
    local=[];sizes=[]
    for row,(A,B) in zip(data['images'],expected_pairs):
        need((row['A'],row['B'])==(A,B),'wrong descent curve')
        allow=row['allowed'];excluded={int(k):v for k,v in row['excluded'].items()}
        need(len(allow)==len(set(allow)),'duplicate image classes')
        need(not(set(allow)&set(excluded)) and set(allow)|set(excluded)==set(squareclasses(B)),'square-class coverage')
        for d,w in excluded.items():
            if w=='negative':
                need(d<0 and B//d<0 and A<0,'real sign obstruction fails')
                local.append({'A':A,'B':B,'class':d,'witness':'all quartic terms negative'})
            else:local.append({'A':A,'B':B,'class':d,**local_obstruction(A,B,d,*w)})
        sizes.append(len(allow))
    need(sizes==[1,4],'rank-zero image sizes differ')
    need(-2*(-17)==34 and (-17)**2-4*64==33,'2-isogeny identity')
    # Standard 2-isogeny formula yields rank <= 0. Verify torsion separately.
    disc=16*64**2*((-17)**2-4*64);counts=[]
    for p0,c in data['good_prime_counts'].items():
        p=int(p0);need(prime_factors(p)==[p] and p>2 and disc%p,'not a good odd prime')
        need(count_curve(-17,64,p)==c,'incorrect reduction count');counts.append(c)
    need(len(counts)>=2 and gcd(*counts)==4,'torsion bound is not four')
    need(isqrt(33)**2!=33,'unexpected rational 2-torsion roots')
    # Any point halving (0,0) has X^2=64; both candidate X are impossible over R.
    half_values={str(x):x**3-17*x*x+64*x for x in [-8,8]}
    need(all(z<0 for z in half_values.values()),'rational half not excluded')
    need(data['elliptic_rational_points']==['O',['0','0']],'incorrect complete group list')
    # The remaining points are direct substitutions and the two smooth infinities.
    for P in data['quartic_affine_points']:
        x,y=map(Q,P);need(evaluate(q,x)==y*y and x==0,'bad quartic point')
    for P in data['octic_affine_points']:
        x,y=map(Q,P);need(evaluate(H,x)==y*y and x==0,'bad octic point')
    need(data['quartic_affine_points']==expected['quartic_affine_points'] and data['octic_affine_points']==expected['octic_affine_points'],'point list coverage')
    need(data['quartic_infinity_points']==data['octic_infinity_points']==2 and H[-1]==q[-1]==1,'wrong infinity count')
    return {'status':'PASS','rank':0,'torsion_order':2,'descent_image_upper_sizes':sizes,
      'local_obstructions':local,'halving_candidates_rhs':half_values,
      'quartic_rational_points':4,'octic_rational_points':4,
      'complete_octic_parameters':['0','infinity'],
      'trust':'Python exact arithmetic plus standard 2-isogeny descent and rational torsion reduction theorems. No height search or external rank database.'}

if __name__=='__main__':
    here=Path(__file__).resolve().parent
    args=[a for a in sys.argv[1:] if a!='--generate']
    p=Path(args[0]) if args else here/'octic_certificate.json'
    if '--generate' in sys.argv:p.write_text(json.dumps(certificate(),indent=2)+'\n')
    out=verify(json.loads(p.read_text()))
    (here/'octic_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: rank zero, torsion order two, and complete four-point lists for the quartic and octic.')
