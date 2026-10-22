"""Exact general Weierstrass group operations, standard library only."""
from fractions import Fraction as Q

def on_curve(a,P):
 if P is None:return True
 x,y=map(Q,P);a1,a2,a3,a4,a6=a
 return y*y+a1*x*y+a3*y==x*x*x+a2*x*x+a4*x+a6

def neg(a,P):
 if P is None:return None
 x,y=P;return x,-y-a[0]*x-a[2]

def add(a,P,R):
 if P is None:return R
 if R is None:return P
 x,y=map(Q,P);u,v=map(Q,R);a1,a2,a3,a4,a6=a
 if x==u:
  if y+v+a1*x+a3==0:return None
  assert y==v
  d=2*y+a1*x+a3
  lam=(3*x*x+2*a2*x+a4-a1*y)/d
 else:lam=(v-y)/(u-x)
 nu=y-lam*x
 X=lam*lam+a1*lam-a2-x-u
 Y=-(lam+a1)*X-nu-a3
 out=(X,Y);assert on_curve(a,out);return out

def mul(a,n,P):
 if n<0:return mul(a,-n,neg(a,P))
 ans=None
 while n:
  if n&1:ans=add(a,ans,P)
  P=add(a,P,P);n//=2
 return ans

def invariants(a):
 a1,a2,a3,a4,a6=a
 b2=a1*a1+4*a2;b4=a1*a3+2*a4;b6=a3*a3+4*a6
 b8=a1*a1*a6+4*a2*a6-a1*a3*a4+a2*a3*a3-a4*a4
 disc=-b2*b2*b8-8*b4**3-27*b6*b6+9*b2*b4*b6
 c4=b2*b2-24*b4;c6=-b2**3+36*b2*b4-216*b6
 return b2,b4,b6,b8,disc,c4,c6
