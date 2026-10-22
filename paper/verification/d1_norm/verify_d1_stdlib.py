#!/usr/bin/env python3
"""Exact D1 norm and residual-curve verification, with no third-party packages.

Mathematical prerequisites: 2-isogeny descent rank formula; rational torsion
reduction; the rational-root theorem; Riemann-Hurwitz for a squarefree double
cover. No bounded search is used to prove any exclusion.
"""
from fractions import Fraction as Q
from itertools import combinations,permutations,product
from math import gcd,isqrt
from pathlib import Path
from collections import Counter
import json,sys

class ProofError(ValueError): pass
def need(b,m):
    if not b: raise ProofError(m)
def tr(a):
    a=list(a)
    while len(a)>1 and not a[-1]:a.pop()
    return a or [0]
def add(a,b):
    return tr([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])
def neg(a): return [-x for x in a]
def sub(a,b):return add(a,neg(b))
def scale(a,c):return tr([c*x for x in a])
def mul(a,b):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return tr(c)
def power(a,n):
    out=[1]
    for _ in range(n):out=mul(out,a)
    return out
def ev(a,x):
    y=0
    for c in reversed(a):y=y*x+c
    return y
def divrem(a,b):
    a=tr(map(Q,a));b=tr(map(Q,b));need(any(b),'zero divisor')
    out=[Q(0)]*max(1,len(a)-len(b)+1)
    while any(a) and len(a)>=len(b):
        j=len(a)-len(b);c=a[-1]/b[-1];out[j]+=c
        for i,v in enumerate(b):a[j+i]-=c*v
        a=tr(a)
    return tr(out),a
def pgcd(a,b):
    while any(b):a,b=b,divrem(a,b)[1]
    return scale(a,1/Q(a[-1])) if any(a) else [0]
def matmul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def det3(a):return sum((-1 if sum(p[i]>p[j] for i in range(3) for j in range(i+1,3))%2 else 1)*a[0][p[0]]*a[1][p[1]]*a[2][p[2]] for p in permutations(range(3)))
def rref(a):
    a=[list(map(Q,r)) for r in a];k=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(k,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[k],a[pivot]=a[pivot],a[k];z=a[k][j];a[k]=[v/z for v in a[k]]
        for i in range(len(a)):
            if i!=k:
                z=a[i][j];a[i]=[v-z*w for v,w in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return tuple(tuple(r) for r in a if any(r))
def rows(tag):
    i,j,k,l,e,f=tag;a=[0]*4;b=[0]*4
    a[i]=b[j]=1;a[k]=b[k]=-e;a[l]=-f;b[l]=f
    return [a,b]
def tags():
    return [(i,j,k,l,e,f) for i,j in combinations(range(4),2) for k,l in permutations([v for v in range(4) if v not in (i,j)]) for e,f in product((1,-1),repeat=2)]
def factors(n):
    n=abs(n);out=[];p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:out.append(n)
    return out
def classes(B):
    d=[1]
    for p in factors(B):d += [x*p for x in d]
    return set(d+[-x for x in d])
def obstruction(A,B,d,w):
    b=B//d
    if w=='real':
        need(d<0 and b<0 and (A<=0 or A*A<4*d*b),'false real obstruction')
        return {'class':d,'witness':'negative real quartic'}
    p,e=w;need(p>1 and factors(p)==[p] and e>0,'not prime power')
    m=p**e;S={i*i%m for i in range(m)}
    # One implementation uses all primitive pairs, the other normalized charts.
    V={(d*u**4+A*u*u*v*v+b*v**4)%m for u in range(m) for v in range(m) if u%p or v%p}
    C={(d*u**4+A*u*u+b)%m for u in range(m)}|{(d+A*v*v+b*v**4)%m for v in range(0,m,p)}
    need(not V&S and not C&S,'a modular obstruction has a primitive solution')
    return {'class':d,'modulus':m,'primitive_residues':sorted(V),'square_residues':sorted(S)}
def count(A,B,p):
    brute=1+sum((y*y-x**3-A*x*x-B*x)%p==0 for x in range(p) for y in range(p))
    leg=1
    for x in range(p):
        z=(x**3+A*x*x+B*x)%p;leg+=1 if z==0 else 2 if pow(z,(p-1)//2,p)==1 else 0
    need(brute==leg,'point count methods disagree')
    return brute
def verify_models(data):
    need([q['model'] for q in data]==[[0,6,0,1,0],[0,-3,0,4,0],[0,18,0,1,0]],'wrong norm curves')
    results=[]
    for row in data:
        _,A,_,B,_=row['model'];need(B*(A*A-4*B)!=0,'singular elliptic model')
        need(len(row['images'])==2,'missing descent image');sizes=[];obs=[]
        for q,(a,b) in zip(row['images'],[(A,B),(-2*A,A*A-4*B)]):
            need((q['A'],q['B'])==(a,b),'wrong isogeny coefficients')
            keep=q['not_excluded'];exc={int(k):v for k,v in q['excluded'].items()}
            need(len(keep)==len(set(keep)) and not set(keep)&set(exc) and set(keep)|set(exc)==classes(b),'square-class coverage')
            for d,w in exc.items():obs.append(obstruction(a,b,d,w))
            sizes.append(len(keep))
        need(sizes[0]*sizes[1]==4 and row['rank']==0,'rank formula does not give zero')
        counts=[];ps=[]
        for p,n in row['good_prime_counts'].items():
            p=int(p);need(p>2 and factors(p)==[p] and (16*B*B*(A*A-4*B))%p,'not a good prime')
            need(count(A,B,p)==n,'point count wrong');counts.append(n);ps.append(p)
        need(len(set(ps))>=2 and gcd(*counts)==4,'torsion bound not four')
        points=row['affine_rational_points'];need(len(points)==3 and len(set(map(tuple,points)))==3,'wrong point count')
        for x,y in points:need(y*y==x**3+A*x*x+B*x,'point not on curve')
        need([0,0] in points and row['torsion_order']==4,'missing two-torsion point')
        for x,y in points:
            if x:
                need(x<0 or isqrt(x)**2!=x,'a nonzero elliptic x is a rational square')
        # An affine nonzero r on z^2=r^4+A*r^2+B maps to (r^2,r*z).
        need(mul([0,0,1],[B,0,A,0,1])==[0,0,B,0,A,0,1],'quartic quotient map')
        results.append({'model':row['model'],'rank':0,'torsion_order':4,'complete_rational_group':['O']+points,'image_upper_sizes':sizes,'obstructions':obs,'quartic_complete_parameters':['0','infinity']})
    return results

def verify(data):
    arithmetic=verify_models(data['models'])
    A=[[1,1,1],[1,1,-1],[1,1,0],[1,0,1]];B=[[1,1,0],[1,-1,0],[1,0,0],[0,0,1]];U=[[1,1,0],[0,0,1],[1,0,1]]
    need(data['frequency_matrix']==A and data['canonical_frequency_matrix']==B and data['angle_matrix']==U,'wrong D1 coordinate convention')
    need(matmul(B,U)==A and abs(det3(U))==1,'not a rational-torus isomorphism')
    tt=tags();need(len(tt)==48 and len({rref(rows(t)) for t in tt})==48,'48-system enumeration wrong')
    full=set()
    for i,j,k,l in permutations(range(4)):
        for sg,e,f in product((1,-1),repeat=3):
            a,b=rows((i,j,k,l,e,f));b[j]=sg;full.add(rref([a,b]))
    need(full=={rref(rows(t)) for t in tt},'fully signed coverage differs')
    recs=data['systems'];need(len(recs)==48 and {tuple(r['tag']) for r in recs}==set(tt),'missing/duplicate signed assignment')
    need([r['system'] for r in recs]==list(range(48)),'system order differs')
    q=[1,0,1];H=[[[1,0,-1],[0,2],[0]],[[1,0,-1],[0,-2],[0]],[q,[0],[0]],[[0],[0],q]]
    counts=Counter();closed=[];remaining=[]
    norm_status={(1,):'zero',(1,0,6,0,1):'quartic',(4,0,-3,0,1):'quartic',(1,0,-3,0,4):'reciprocal',(1,0,18,0,1):'quartic',(9,0,1):'residual',(1,0,9):'residual'}
    for row in recs:
        sid=row['system'];C=rows(tuple(row['tag']));L=[]
        for rr in C:
            L.append([sum_poly([scale(H[i][j],rr[i]) for i in range(4)]) for j in range(3)])
        cross=[sub(mul(L[0][1],L[1][2]),mul(L[0][2],L[1][1])),sub(mul(L[0][2],L[1][0]),mul(L[0][0],L[1][2])),sub(mul(L[0][0],L[1][1]),mul(L[0][1],L[1][0]))]
        w=row['kernel'];g=row['divisor'];need(len(w)==3,'wrong kernel dimension')
        for a,b in zip(cross,w):need(a==mul(g,b),'wrong cross-product identity')
        need(len(pgcd(pgcd(w[0],w[1]),w[2]))==1,'kernel could vanish at an unhandled fiber')
        gf=row['divisor_factors'];pr=[gf['constant']];need(gf['constant']!=0,'zero cross divisor')
        for f in gf['factors']:
            pp=f['coefficients'];m=f['multiplicity'];need(m>=1,'bad multiplicity')
            pr=mul(pr,power(pp,m))
            if pp==[0,1]:continue
            need(pp[-1]%5 and all(ev(pp,x)%5 for x in range(5)),'discarded divisor can have a nonzero rational root')
        need(pr==g,'divisor factor product')
        for rr in L:need(sum_poly([mul(a,b) for a,b in zip(rr,w)])==[0],'kernel not in row nullspace')
        n0=row['norm_factor'];N=add(mul(w[0],w[0]),mul(w[1],w[1]));need(N==mul(mul(q,q),n0),'wrong normalization factor')
        M=sub(N,mul(w[2],w[2]));need(M==row['second_norm'],'wrong second square condition')
        typ=norm_status.get(tuple(n0));need(typ is not None,'unclassified norm');counts[str(n0)]+=1
        if typ=='residual':
            expected=[9,0,19,0,-5,0,1] if n0==[9,0,1] else [1,0,-5,0,19,0,9]
            need(M==expected and row['status']=='residual','residual square system differs');remaining.append(sid)
        else:
            need(row['status']=='closed','wrong closure status')
            if typ=='zero':need(w[0]==[0],'zero norm case does not vanish')
            if typ=='reciprocal':need(n0==list(reversed([4,0,-3,0,1])),'wrong reciprocal reduction')
            closed.append(sid)
    need(len(closed)==40 and remaining==[8,9,12,14,24,25,28,30],'D1 proof boundary wrong')
    need(data['boundaries']==['r=0 implies first two sines equal','r=infinity implies first two sines equal up to sign'],'bad boundary claims')
    # Canonical first two values at r=0 and infinity are equal (cos beta +/-1).
    need(H[0][0][0]==H[1][0][0] and H[0][1][0]==H[1][1][0],'r=0 not handled')
    need(H[0][0][-1]==H[1][0][-1] and len(H[0][1])<3 and len(H[1][1])<3,'r=infinity not handled')
    residual=verify_residual(data)
    return {'status':'PASS','signed_systems':48,'closed_D1_systems':closed,'residual_D1_systems':remaining,'norm_catalog_counts':dict(counts),'elliptic_models':arithmetic,'residual':residual,'rank_database_premise':False,'whole_D1_closed':False,'scope':'Three complete genus-one quartic point lists, 40 closed D1 signed systems, and an exact remaining genus-five existence problem. No complete list for the residual genus-five curve.'}

def sum_poly(xs):
    out=[0]
    for p in xs:out=add(out,p)
    return out

def verify_residual(data):
    P=[1,0,70,0,-1009,0,7060,0,-1009,0,70,0,1];need(data['residual_polynomial']==P,'wrong residual polynomial')
    derivative=[i*P[i] for i in range(1,len(P))];need(len(pgcd(P,derivative))==1,'singular claimed genus-five double cover')
    fm=[1,0,83,0,-13,0,1];fp=[1,0,-13,0,83,0,1];need(mul(fm,fp)==P,'residual factor identity')
    # r = 6h/(1-h^2), S = 3(1+h^2)/(1-h^2).
    a=[1,0,-1];b=[1,0,1];sixh=[0,6]
    need(add(mul(sixh,sixh),scale(mul(a,a),9))==scale(mul(b,b),9),'conic parametrization')
    f=[9,0,19,0,-5,0,1]
    pull=sum_poly([scale(mul(power(sixh,i),power(a,6-i)),c) for i,c in enumerate(f) if c])
    need(pull==scale(P,9),'conic-to-genus-five pullback identity')
    # Circle reconstruction: (sin,cos) alpha and beta; gamma sine and cos=Y/D.
    ab=[1,0,-1];ac=[0,-2];aq=b
    bb=[0,12,0,-12];bc=[1,0,-38,0,1];bq=[1,0,34,0,1]
    need(add(mul(ab,ab),mul(ac,ac))==mul(aq,aq),'alpha is not a rational circle point')
    need(add(mul(bb,bb),mul(bc,bc))==mul(bq,bq),'beta is not a rational circle point')
    D=mul(aq,bq);G=[0,0,-48,0,48]
    need(add(P,mul(G,G))==mul(D,D),'gamma reconstruction identity')
    E=[add(mul(ab,bc),mul(ac,bb)),sub(mul(ab,bc),mul(ac,bb)),mul(ab,bq),G]
    need(sub(sub(E[0],E[1]),E[3])==[0] and sub(add(E[2],E[3]),E[1])==[0],'base system 8 does not hold')
    unscaled=[[1,0,-62,0,1],[1,0,-14,0,1],[1,0,34,0,1],[0,0,-48]]
    need(E==[mul(a,p) for p in unscaled],'offset reconstruction differs')
    # Every possible extra degeneracy is an integer root +/-1 of a monic
    # constant +/-1 factor, and direct evaluation excludes these roots.
    witnesses=[]
    for v in unscaled:
        if v==[0,0,-48]:continue
        need(v[-1]==1 and v[0]==1 and ev(v,1)!=0 and ev(v,-1)!=0,'zero-offset degeneracy has possible rational root')
    for i,j in combinations(range(4),2):
        for sign in (1,-1):
            p=sub(unscaled[i],scale(unscaled[j],sign))
            # Factor off a constant and h powers; the rest is either constant or
            # a monic quartic with constant 1 (or an equivalent rational scaling).
            p=tr(p)
            while p and p[0]==0:p=p[1:]
            need(bool(p),'identical offsets')
            if len(p)>1:
                lead=p[-1];p=scale(p,Q(1,lead))
                need(p[0]==1 and all(c.denominator==1 for c in map(Q,p)),'unexpected degeneracy polynomial')
                need(ev(p,1)!=0 and ev(p,-1)!=0,'unhandled rational degeneracy root')
            witnesses.append([i,j,sign])
    known=data['residual_known_finite_points']
    need(known==[[0,1],[0,-1],[1,72],[1,-72],[-1,72],[-1,-72]],'known points altered')
    for x,y in known:need(ev(P,x)==y*y,'known residual point is not on curve')
    need(data['residual_infinity_points']==2 and data['residual_points_complete'] is False,'unproved completeness claim')
    return {'genus':5,'polynomial_coefficients':P,'known_finite_points':known,'known_infinity_points':2,'complete_point_list_proved':False,'equivalent_existence_statement':'D1 has a nondegenerate rational-circle solution iff this genus-five curve has a rational point with h not in {0,1,-1,infinity}.','converse_reconstruction_checked':True,'degeneracy_witness_count':len(witnesses)}

if __name__=='__main__':
    here=Path(__file__).resolve().parent;p=Path(sys.argv[1]) if len(sys.argv)>1 else here/'d1_certificate.json'
    out=verify(json.loads(p.read_text()));(here/'d1_stdlib_verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: three rank-zero quartics; 40 D1 systems closed; eight residual systems reduce to one explicit genus-five curve.')
