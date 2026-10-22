#!/usr/bin/env python3
"""Close the eight D3 nonlinear factors whose lifting cover is H_B H_C.
Uses the cited published rank-zero and order-five torsion of Cremona 11a3.
All morphism identities, group points, and exceptional parameter images are exact.
"""
from pathlib import Path
import sys,json
import sympy as s
from genus_exact import BASE,x,y,expr,require
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'arithmetic'))
from elliptic_exact import mul
from fractions import Fraction as Q
OUT=Path(__file__).resolve().parent;z,W=s.symbols('z W')

def rat_image(f,r):
 p,q=s.fraction(s.cancel(f));pp=s.Poly(p,z);qq=s.Poly(q,z)
 if r=='infinity':
  if pp.degree()>qq.degree():return 'infinity'
  if pp.degree()<qq.degree():return '0'
  return str(pp.LC()/qq.LC())
 r=s.Rational(r);a=pp.eval(r);b=qq.eval(r)
 require(a!=0 or b!=0,'rational map base point after cancellation')
 return 'infinity' if b==0 else str(a/b)

def main():
 H=(z**6-5*z**4+11*z*z+1)*(z**6+11*z**4-5*z*z+1)
 q=4*z*z/(z*z+1)**2;v=(W/(z*z+1)**3-1)/2
 identity=s.cancel((v*v+v-q**3+q*q)-(W*W-H)/(4*(z*z+1)**6))
 require(identity==0,'11a3 map identity fails')
 a=[0,-1,1,0,0];T=(Q(0),Q(0));points=[mul(a,k,T) for k in range(5)]
 require(len(set(points))==5 and mul(a,5,T) is None,'torsion group enumeration fails')
 require(set(P[0] for P in points if P is not None)=={Q(0),Q(1)},'unexpected torsion x')
 require(s.factor(s.together(q-1))==-(z-1)**2*(z+1)**2/(z*z+1)**2,'square equality')
 require(s.Poly(H,z).degree()==12 and s.gcd(s.Poly(H,z),s.Poly(s.diff(H,z),z)).degree()==0,'smooth genus-five cover')
 finite_points=[(0,1),(0,-1),(1,8),(1,-8),(-1,8),(-1,-8)]
 require(all(s.expand(H).subs(z,a)==b*b for a,b in finite_points),'cover point list')
 require(s.Poly(H,z).LC()==1,'two rational infinity points')
 data=json.loads((OUT/'d3_lifting_covers.json').read_text());closed=[]
 for r in data['records']:
  hh=s.sympify(r['hyperelliptic_polynomial'],locals={'z':z})
  if s.expand(hh-H)!=0:continue
  ims=[]
  for t in ['0','1','-1','infinity']:
   values=[rat_image(s.sympify(r['plane_normalization'][k],locals={'z':z}),t) for k in ('x','y')]
   require(any(v in ('0','1','-1','infinity') for v in values),'boundary needs additional verification')
   ims.append({'parameter':t,'plane_coordinates':values,'excluded_by':'previously verified finite special fiber or projective boundary'})
  # Lost finite lift-chart values must also map to a previously treated special fiber.
  for t in r['finite_rational_chart_exceptions']:
   vals=[rat_image(s.sympify(r['plane_normalization'][k],locals={'z':z}),t) for k in ('x','y')]
   require(any(v in ('0','1','-1','infinity') for v in vals),'exceptional chart needs additional proof')
  closed.append({'system':r['system'],'allowed_parameter_images':ims,'finite_chart_exceptions':r['finite_rational_chart_exceptions']})
 require(len(closed)==8,'D3 family count differs')
 out={'status':'PASS','scope':'eight nonlinear D3 factors; not closure of the whole orbit','external_premise':'Cremona 11a3=[0,-1,1,0,0] has rank 0 and torsion group of order 5; Table Two full group data','source_line':'11 a 3 [0,-1,1,0,0] 0 [5] [0:0:1]','elliptic_map':{'x':'4*z^2/(z^2+1)^2','y':'(W/(z^2+1)^3-1)/2'},'cover_polynomial':str(s.expand(H)),'complete_rational_z_parameters':['0','1','-1','infinity'],'complete_cover_affine_points':[list(P) for P in finite_points],'rational_points_at_infinity':2,'cover_rational_point_count':8,'closed_factors':closed}
 (OUT/'d3_rank_zero_family.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS: eight nonlinear D3 factors closed by rank-zero 11a3 route')
if __name__=='__main__':main()
