"""Exact on-curve tests, model-change identities, and conservative corrected QC inputs.
Does not certify rank or generator saturation and performs no quadratic Chabauty.
"""
from pathlib import Path
from fractions import Fraction as Q
from math import isqrt,gcd
from functools import reduce
import json,sys

def residual(a,pt):
 x,y=map(Q,pt);a1,a2,a3,a4,a6=map(Q,a)
 return y*y+a1*x*y+a3*y-(x*x*x+a2*x*x+a4*x+a6)

def invariants(a):
 a1,a2,a3,a4,a6=map(Q,a)
 b2=a1*a1+4*a2;b4=2*a4+a1*a3;b6=a3*a3+4*a6
 b8=a1*a1*a6+4*a2*a6-a1*a3*a4+a2*a3*a3-a4*a4
 return b2*b2-24*b4,-b2**3+36*b2*b4-216*b6,(-b2*b2*b8-8*b4**3-27*b6*b6+9*b2*b4*b6)

def powroot(q,n):
 assert q>=0
 def rt(k):
  lo,hi=0,max(1,k)
  while lo+1<hi:
   m=(lo+hi)//2
   if m**n<=k:lo=m
   else:hi=m
  x=hi if hi**n==k else lo
  assert x**n==k,(q,n)
  return x
 return Q(rt(q.numerator),rt(q.denominator))

def change(old,new):
 assert old[0]==old[2]==new[0]==0
 c4,c6,delta=invariants(old);C4,C6,Delta=invariants(new)
 u=powroot(c4/C4,4);r=(u*u*new[1]-old[1])/3;t=u**3*new[2]/2
 assert (3*r*r+2*old[1]*r+old[3])/u**4==new[3]
 assert (r**3+old[1]*r*r+old[3]*r+old[4]-t*t)/u**6==new[4]
 assert c6==u**6*C6 and delta==u**12*Delta
 return u,r,t

def card(a,p):
 return 1+sum(residual(a,(x,y))%p==0 for x in range(p) for y in range(p))

def multiply(a, point, n):
 assert a[0]==0 and n>=0
 def add(P,R):
  if P is None:return R
  if R is None:return P
  x,y=P;u,v=R
  if x==u and y+v+a[2]==0:return None
  slope=(3*x*x+2*a[1]*x+a[3])/(2*y+a[2]) if P==R else (v-y)/(u-x)
  X=slope*slope-a[1]-x-u
  R=(X,slope*(x-X)-y-a[2]);assert residual(a,R)==0
  return R
 result=None;P=tuple(map(Q,point))
 while n:
  if n&1:result=add(result,P)
  P=add(P,P);n//=2
 return result

def main(root,out):
 data=json.load(open(root/'chabauty_inputs/chabauty_inputs.json'));rows=[]
 for name,r in data['curves'].items():
  A,_,B,_,C,_,D=r['sextic_coeffs_w6_to_w0']
  for label,old,maptext in [('quotient1_E',[0,B,0,A*C,A*A*D],'X=A*w^2, Z=A*Y'),('quotient2_Ep',[0,C,0,B*D,A*D*D],'X=D/w^2, Z=D*Y/w^3')]:
   rec=r[label];a=rec['minimal_model'];key='generators_minmodel' if 'generators_minmodel' in rec else 'generators'
   gens=rec[key];u,shift,yt=change(old,a)
   newgens=[]
   for gen in gens:
    xy=[Q(x) for x in gen]; res=residual(a,xy);resold=residual(old,xy)
    assert resold==0,(name,label,'not on identified original model')
    new=[(xy[0]-shift)/u**2,(xy[1]-yt)/u**3]
    assert residual(a,new)==0
    newgens.append([str(x) for x in new])
    rows.append({'curve':name,'quotient':label,'old_point':gen,'stored_model':a,'on_stored_model':res==0,'residual':str(res),'on_original_model':resold==0,'original_model':old,'u':str(u),'r':str(shift),'t':str(yt),'corrected_point':[str(x) for x in new]})
   disc=invariants(a)[2];cts={str(p):card(a,p) for p in [3,5,7,11,13] if disc%p}
   bound=reduce(gcd,cts.values());divides=all(n%rec['torsion']==0 for p,n in cts.items() if int(p)!=rec['torsion'])
   rec['original_weierstrass_model']=old
   rec['original_point_to_curve_map']=maptext
   rec['model_change']={'convention':'X=u^2*x_min+r; Z=u^3*y_min+t','u':str(u),'r':str(shift),'t':str(yt)}
   rec['uploaded_points']=gens;rec['points_on_minimal_model_verified']=newgens
   rec.pop('generators_minmodel',None);rec.pop('generators',None)
   multiples=[multiply(a,pt,bound) for pt in newgens]
   assert all(pt is not None for pt in multiples)
   rec['non_torsion_witness']={'torsion_order_upper_bound':bound,'multiples_of_points':[[str(x) for x in pt] for pt in multiples]}
   rec['rank_lower_bound_verified']=1
   rec['rank_status']='rank at least one verified; uploaded exact rank and upper bound not independently certified'
   rec['basis_status']='on-curve points verified; generation and global saturation not certified'
   rec['finite_field_point_counts']=cts
   rec['torsion_order_divides_point_count_gcd']=bound
   rec['uploaded_torsion_consistent_with_counts']=divides
   print(name,label,'point',gens,'correct',newgens,'tors',rec['torsion'],'counts',cts,'bound',bound,flush=True)
  r['QC_status']='NOT RUN; supplied driver has only a bounded point search'
 data['description']='Corrected model-compatible points and explicit maps; rank and saturation remain reported, not certified. Not a completed QC calculation.'
 out.write_text(json.dumps({'points_checked':len(rows),'invalid_uploaded_point_model_pairs':sum(not r['on_stored_model'] for r in rows),'repairs':rows,'corrected_inputs':data},indent=2))
if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
