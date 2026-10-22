"""Elementary 2-isogeny rank-zero certificates and torsion upper bounds.
No third-party packages. Implements finite modular obstructions, not a general CAS.
The accompanying note states the standard 2-isogeny descent theorem used.
"""
from fractions import Fraction as Q
from math import gcd,isqrt
from functools import reduce
from pathlib import Path
import json,sys

def pfactors(n):
 n=abs(n);out=[];p=2
 while p*p<=n:
  if n%p==0:
   out.append(p)
   while n%p==0:n//=p
  p+=1
 if n>1:out.append(n)
 return out

def classes(B):
 ds=[1]
 for p in pfactors(B):ds+=[x*p for x in ds]
 return sorted(ds+[-x for x in ds])

def obstructed(A,B,d,w):
 assert B%d==0;b=B//d
 if w=='real':return d<0 and b<0 and (A<=0 or A*A<4*d*b)
 p,e=w;assert len(pfactors(p))==1 and pfactors(p)[0]==p and e>0
 m=p**e;squares={x*x%m for x in range(m)}
 return not any((d*t**4+A*t*t+b)%m in squares for t in range(m)) and not any((d+A*t*t+b*t**4)%m in squares for t in range(0,m,p))

def image_bound(A,B):
 keep=[];exclude={}
 mods=[(2,e) for e in range(1,9)]+[(3,e) for e in range(1,5)]+[(5,e) for e in range(1,4)]+[(p,1) for p in [7,11,13,17,19]]
 for d in classes(B):
  w=next((w for w in ['real']+mods if obstructed(A,B,d,w)),None)
  if w is None:keep.append(d)
  else:exclude[str(d)]=w
 return {'A':A,'B':B,'not_excluded':keep,'excluded':exclude}

def inv(a):
 a1,a2,a3,a4,a6=a;b2=a1*a1+4*a2;b4=a1*a3+2*a4;b6=a3*a3+4*a6;b8=a1*a1*a6+4*a2*a6-a1*a3*a4+a2*a3*a3-a4*a4
 return b2*b2-24*b4,-b2**3+36*b2*b4-216*b6,-b2*b2*b8-8*b4**3-27*b6*b6+9*b2*b4*b6

def pointcount(a,p):
 a1,a2,a3,a4,a6=a
 return 1+sum((y*y+a1*x*y+a3*y-x**3-a2*x*x-a4*x-a6)%p==0 for x in range(p) for y in range(p))

def refine_torsion(model,bound):
 if model==[0,1,0,-4,-4]:
  # All possible rational points of order 2 are at x=-2,-1,2.
  roots=[-2,-1,2];a2,a4,a6=model[1],model[3],model[4]
  for r in roots:
   assert r**3+a2*r*r+a4*r+a6==0
   A=3*r+a2;B=3*r*r+2*a2*r+a4
   if B>=0 and isqrt(B)**2==B:
    for X in {isqrt(B),-isqrt(B)}:
     z=A+2*X
     assert not (z>=0 and isqrt(z)**2==z)
  # x(2P)=0 on a shifted model forces x(P)^2=B;
  # no order-2 point has a rational half, so there is no order-4 point.
  assert bound==8
  return 4
 return bound

MODELS=[([0,0,0,-7,6],2),([0,1,0,-4,-4],2),([0,1,0,-24,36],3),([0,-1,0,-9,-7],-1),([0,-1,0,-3,2],2),([0,0,0,-351,1890],15),([0,0,0,-24003,1296702],66)]

def generate():
 out=[]
 for model,r in MODELS:
  a1,a2,a3,a4,a6=model;assert a1==a3==0 and r**3+a2*r*r+a4*r+a6==0
  A=3*r+a2;B=3*r*r+2*a2*r+a4
  left=image_bound(A,B);right=image_bound(-2*A,A*A-4*B)
  assert len(left['not_excluded'])*len(right['not_excluded'])==4
  discr=inv(model)[2];cts={str(p):pointcount(model,p) for p in [3,5,7,11,13,17,19] if discr%p}
  row={'model':model,'root_shift':r,'image_bounds':[left,right],'rank_upper_bound':0,'good_prime_cardinalities':cts,'rational_torsion_order_divides':refine_torsion(model,reduce(gcd,cts.values()))}
  out.append(row)
 return {'method':'2-isogeny descent: 2^(rank+2)=|alpha(E)|*|alpha(Eprime)|; both images bounded by surviving square classes. Finite-field orders bound rational torsion.','curves':out}

def verify(data):
 assert [(x['model'],x['root_shift']) for x in data['curves']]==MODELS
 for row in data['curves']:
  a1,a2,a3,a4,a6=row['model'];r=row['root_shift'];A=3*r+a2;B=3*r*r+2*a2*r+a4
  assert r**3+a2*r*r+a4*r+a6==0 and B*(A*A-4*B)!=0
  sizes=[]
  for g,(aa,bb) in zip(row['image_bounds'],[(A,B),(-2*A,A*A-4*B)]):
   assert (g['A'],g['B'])==(aa,bb)
   keep=set(g['not_excluded']);exc={int(k):v for k,v in g['excluded'].items()}
   assert not keep&set(exc) and keep|set(exc)==set(classes(bb))
   assert all(obstructed(aa,bb,d,w) for d,w in exc.items());sizes.append(len(keep))
  assert sizes[0]*sizes[1]<=4
  delta=inv(row['model'])[2];cts=[]
  for ps,n in row['good_prime_cardinalities'].items():
   p=int(ps);assert p>2 and pfactors(p)==[p] and delta%p and pointcount(row['model'],p)==n;cts.append(n)
  assert cts and refine_torsion(row['model'],reduce(gcd,cts))==row['rational_torsion_order_divides']
 return len(data['curves'])

if __name__=='__main__':
 out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('rank_zero_certificate.json')
 if '--generate' in sys.argv:
  data=generate();out.write_text(json.dumps(data,indent=2))
 else:data=json.loads(out.read_text())
 print('Verified rank zero and torsion bounds for',verify(data),'elliptic models')
