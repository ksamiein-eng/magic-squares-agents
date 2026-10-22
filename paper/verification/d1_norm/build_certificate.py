#!/usr/bin/env python3
"""Discovery only. Acceptance is in independently implemented checkers."""
from pathlib import Path
import sys,json,itertools
import sympy as s
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent/'three_prime/input/repro/certs'
sys.path.insert(0,str(HERE.parent/'three_prime'))
from verify_rank_zero import image_bound,pointcount,inv
r=s.symbols('r');q=1+r*r
H=s.Matrix([[1-r*r,2*r,0],[1-r*r,-2*r,0],[q,0,0],[0,0,q]])
def coeff(p): return [int(c) for c in reversed(s.Poly(s.expand(p),r).all_coeffs())]
def factors(p):
 c,fs=s.factor_list(p);return {'constant':int(c),'factors':[{'coefficients':coeff(f),'multiplicity':int(n)} for f,n in fs]}
rec=json.loads((ROOT/'D1.json').read_text());rows=[]
for sid,ss in enumerate(rec['systems']):
 i,j,k,l,e,f=ss['tag'];R=s.zeros(2,4);R[0,i]=R[1,j]=1;R[0,k]=R[1,k]=-e;R[0,l]=-f;R[1,l]=f
 B=R*H;W=list(s.Matrix(list(B[0,:])).cross(s.Matrix(list(B[1,:]))));g=s.factor(s.gcd_list(W));w=[s.cancel(c/g) for c in W]
 N=s.expand(w[0]**2+w[1]**2);N0=s.cancel(N/q**2);M=s.expand(N-w[2]**2)
 rows.append({'system':sid,'tag':ss['tag'],'divisor':coeff(g),'divisor_factors':factors(g),'kernel':[coeff(c) for c in w],'norm_factor':coeff(N0),'second_norm':coeff(M),'status':'residual' if N0 in (r*r+9,9*r*r+1) else 'closed'})
models=[]
for A,B,pts in [(6,1,[[0,0],[-1,2],[-1,-2]]),(-3,4,[[0,0],[2,2],[2,-2]]),(18,1,[[0,0],[-1,4],[-1,-4]])]:
 E=[0,A,0,B,0];d=inv(E)[2]
 cts={str(p):pointcount(E,p) for p in [3,5,7] if d%p}
 models.append({'model':E,'images':[image_bound(A,B),image_bound(-2*A,A*A-4*B)],'good_prime_counts':cts,'affine_rational_points':pts,'torsion_order':4,'rank':0})
P=r**12+70*r**10-1009*r**8+7060*r**6-1009*r**4+70*r**2+1
out={'scope':'D1 norm obstruction: 40 of 48 signed systems closed, eight reduced to one genus-five existence problem. No full D1 closure.',
'frequency_matrix':rec['elements'],'canonical_frequency_matrix':[[1,1,0],[1,-1,0],[1,0,0],[0,0,1]],'angle_matrix':[[1,1,0],[0,0,1],[1,0,1]],'models':models,'systems':rows,
'residual_polynomial':coeff(P),'residual_known_finite_points':[[0,1],[0,-1],[1,72],[1,-72],[-1,72],[-1,-72]],'residual_infinity_points':2,'residual_points_complete':False,
'new_direct_D1_factors':[[i,1] for i in [10,11,13,15,16,17,20,22,26,27,29,31,32,33,36,38]],
'boundaries':['r=0 implies first two sines equal','r=infinity implies first two sines equal up to sign'],
'core_rank_premise':'Classical 2-isogeny descent formula and good-prime reduction of rational torsion; no elliptic-curve database rank input.'}
(HERE/'d1_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print('Built 48 kernel records and three rank-zero certificates.')
