#!/usr/bin/env python3
"""Normalize all genus-zero D3 projections and recover their quadratic covers.
The original solutions, not just their planar projection, require a square root
of the displayed discriminant. This computes genuine smooth-model genera.
"""
from pathlib import Path
import json,sys,time
import sympy as s
from genus_exact import BASE,expr,x,y,require,tasks,generic_lift
z=s.symbols('z');OUT=Path(__file__).resolve().parent

def sqfree_function(D):
 n,d=s.fraction(s.cancel(D));c,fac=s.factor_list(s.expand(n*d),z)
 c=s.Rational(c);require(c.q==1,'integer coefficient expected')
 sign=-1 if c<0 else 1;sq=s.Integer(1);hc=s.Integer(sign)
 for p,e in s.factorint(abs(int(c))).items():sq*=p**(e//2);hc*=p**(e%2)
 H=hc;S=sq
 for p,e in fac:H*=p**(e%2);S*=p**(e//2)
 H=s.expand(H);S=s.cancel(S/d)
 require(s.cancel(D-S*S*H)==0,'squarefree discriminant identity failed')
 require(s.gcd(s.Poly(H,z),s.Poly(s.diff(H,z),z)).degree()==0,'H not squarefree')
 return H,S

def main():
 st=time.time();jobs,_=tasks();out=[]
 for name,sid,ss,fr in jobs:
  if name!='D3':continue
  lookup={k:s.Symbol(v,real=True) for k,v in [('x','t'),('z','u'),('w','v')]}
  ab=[lookup[a] for a in ss['projection']['plane']];elim=lookup[ss['projection']['eliminated']]
  F=s.expand(expr(fr['poly']).subs({ab[0]:x,ab[1]:y},simultaneous=True));b=int(s.degree(F,y))
  P=s.Poly(s.cancel((x+z)**b*F.subs(y,(x*z-1)/(x+z))),x,z)
  R,rem=P.div(s.Poly((x*x+1)**3,x,z));require(rem.is_zero,'pencil base-point factor mismatch')
  require(R.degree(x)==1,'normalization pencil is not degree one')
  xx=s.cancel(-R.as_expr().subs(x,0)/s.diff(R.as_expr(),x));yy=s.cancel((xx*z-1)/(xx+z))
  require(s.cancel(F.subs({x:xx,y:yy},simultaneous=True))==0,'parametrization fails')
  require(s.cancel((xx*yy+1)/(xx-yy)-z)==0,'parameter inverse fails')
  cf=expr(ss['common_factor']) if ss.get('common_factor') else s.Integer(1)
  gs=[s.cancel(expr(ss[k])/cf).subs({ab[0]:xx,ab[1]:yy},simultaneous=True) for k in ('G1','G2')]
  coeffs=[[s.cancel(s.Poly(g,elim).nth(k)) for k in (0,1,2)] for g in gs]
  for i in range(3):
   for j in range(i):require(s.cancel(coeffs[0][i]*coeffs[1][j]-coeffs[0][j]*coeffs[1][i])==0,'equations not proportional on normalization')
  C,B,A=coeffs[0];require(A!=0,'quadratic degree drops generically')
  D=s.cancel(B*B-4*A*C);H,S=sqfree_function(D);deg=int(s.degree(H,z));require(deg>=3,'unexpected low-genus original cover')
  exceptions=set()
  for f in [xx,yy,A,S]:
   nu,de=s.fraction(f)
   for v in [de]+([nu] if f in [A,S] else []):
    for r in s.polys.polytools.ground_roots(v,z):exceptions.add(str(r))
  out.append({'system':sid,'plane_factor':fr['poly'],'plane_normalization':{'x':str(xx),'y':str(yy),'inverse':'(x*y+1)/(x-y)'},'quadratic_coefficients_low_to_high':[str(q) for q in coeffs[0]],'discriminant_square_multiplier':str(S),'hyperelliptic_polynomial':str(H),'degree':deg,'geometric_genus':(deg-1)//2,'generic_inverse_formula':'eliminated=(-B+S*W)/(2*A), with W^2=H(z)','finite_rational_chart_exceptions':sorted(exceptions)})
  print('D3',sid,'cover genus',(deg-1)//2,'H=',s.factor(H),flush=True)
 result={'status':'PASS','records':out,'genera':sorted(set(r['geometric_genus'] for r in out)),'count':len(out),'note':'Finite chart exceptions are retained for separate point classifications. Genus computation does not prove emptiness.','seconds':round(time.time()-st,3)}
 (OUT/'d3_lifting_covers.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
