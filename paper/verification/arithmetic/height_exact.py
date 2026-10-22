#!/usr/bin/env python3
"""Standard-library checks of duplication-map canonical-height intervals.
Canonical height is normalized as lim 4^-n h(x(2^n P)).
No floating-point evaluations are used for acceptance.
"""
from fractions import Fraction as Q
from math import gcd
from pathlib import Path
import json,sys
from elliptic_exact import on_curve,invariants,mul,add
sys.set_int_max_str_digits(0)

def require(v,m):
 if not v:raise RuntimeError(m)

def conv(a,b):
 r=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):r[i+j]+=x*y
 return r

def plus(a,b):return [x+y for x,y in zip(a,b)]

def forms(a):
 b2,b4,b6,b8,_,_,_=invariants(a)
 # Coefficients of X^j Z^(4-j), lowest j first.
 return [-b8,-2*b6,-b4,0,1],[b6,2*b4,b2,4,0]

def check_log2():
 z=Q(1,3);N=30
 s=2*sum((z**(2*j+1)/Q(2*j+1) for j in range(N)),Q(0))
 tail=2*z**(2*N+1)/(Q(2*N+1)*(1-z*z))
 L=Q(693147180559945309,10**18);U=Q(693147180559945310,10**18)
 require(L<s and s+tail<U,'log(2) enclosure invalid')
 return L,U

def log_integer_bounds(n):
 require(type(n) is int and n>=1,'positive integer log input')
 if n==1:return Q(0),Q(0)
 L,U=check_log2();b=n.bit_length()
 return (b-1)*L,b*U

def check_bezout(model,record):
 F,G=forms(model);D=record['D'];N=0
 require(type(D) is int and D>0,'Bezout denominator must be positive integer')
 for key,index in (('X7',7),('Z7',0)):
  r=record[key];U,V=r['U'],r['V']
  require(len(U)==len(V)==4 and all(type(x) is int for x in U+V),'Bezout coefficient format')
  got=plus(conv(U,F),conv(V,G));want=[0]*8;want[index]=D
  require(got==want,'Bezout homogeneous identity failed')
  N=max(N,sum(map(abs,U+V)))
 require(N>=1,'zero Bezout norm')
 M=max(sum(map(abs,F)),sum(map(abs,G)))
 return N,M

def homogeneous_eval(cs,a,b):return sum(c*a**j*b**(4-j) for j,c in enumerate(cs))

def interval(model,P,witness,steps=6):
 require(on_curve(model,P),'initial point is not on model')
 require(P is not None,'infinite point unsupported by non-torsion interval')
 N,M=check_bezout(model,witness);F,G=forms(model)
 a,b=P[0].numerator,P[0].denominator
 require(gcd(a,b)==1,'initial x not reduced')
 for _ in range(steps):
  aa=homogeneous_eval(F,a,b);bb=homogeneous_eval(G,a,b)
  d=gcd(aa,bb);require(d>0 and witness['D']%d==0,'gcd not controlled by Bezout denominator')
  a,b=aa//d,bb//d
  if b<0:a,b=-a,-b
 H=max(abs(a),abs(b));hlo,hhi=log_integer_bounds(H)
 nl,nu=log_integer_bounds(N);ml,mu=log_integer_bounds(M)
 lower=(hlo-nu/3)/(4**steps);upper=(hhi+mu/3)/(4**steps)
 return {'lower':str(lower),'upper':str(upper),'doubling_steps':steps,'final_x_height_bits':H.bit_length(),'lower_error_norm':N,'upper_error_norm':M}

def main(path):
 data=json.loads(Path(path).read_text());report=[]
 for row in data['models']:
  N,M=check_bezout(row['model'],row['bezout'])
  for p in row['points']:
   P=tuple(map(Q,p['point']));calc=interval(row['model'],P,row['bezout'],p['interval']['doubling_steps'])
   require(calc==p['interval'],'stored interval differs')
   report.append({'label':row['label'],'point':p['point'],'interval':calc,'tag':p['tag']})
 out={'status':'PASS','normalization':'lim 4^-n h(x(2^nP)); twice the usual Silverman canonical height','method':'integer homogeneous Bezout identities and rational logarithm bounds','models':len(data['models']),'point_intervals':len(report),'rows':report}
 Path(path).with_name('height_verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))

if __name__=='__main__':main(sys.argv[1] if len(sys.argv)>1 else str(Path(__file__).with_name('height_certificate.json')))
