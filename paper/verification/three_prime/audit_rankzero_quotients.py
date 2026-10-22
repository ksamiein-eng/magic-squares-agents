"""Validate genus-one identifications and complete rational-point counts.
Standard binary-quartic Jacobian invariants + the independent rank-zero certificate.
"""
import sys,json,collections,itertools
from pathlib import Path
import sympy as s
from audit_inputs import expr,TAU
from audit_chabauty import invariants,powroot
from verify_rank_zero import verify

def match(P,model):
 a,b,c,d,e=map(int,P.all_coeffs());I=12*a*e-3*b*d+c*c;J=72*a*c*e+9*b*c*d-27*a*d*d-27*b*b*e-2*c**3
 C4,C6,delta=invariants(model)
 u=powroot(16*I/C4,4)
 assert 32*J==u**6*C6
 return {'I':str(I),'J':str(J),'scale_u':str(u)}

def main(root,out):
 data=json.load(open(Path(__file__).with_name('rank_zero_certificate.json')));verify(data)
 bounds={tuple(r['model']):r['rational_torsion_order_divides'] for r in data['curves']}
 records=[]
 for f in sorted((root/'repro/certs').glob('*.json')):
  rec=json.load(open(f))
  for ix,ss in enumerate(rec.get('systems',[])):
   for fi,fr in enumerate(ss['factors']):
    for qi,q in enumerate(fr.get('quotients',[])):
     if q['curve_kind']!='genus1':continue
     c=q['curve'];model=tuple(c['minimal_model']);P=s.Poly(expr(c['D_squarefree']),TAU)
     iden=match(P,model);count=0
     for val,mult in collections.Counter(c['tau_values']).items():
      if val=='oo':continue
      z=P.eval(expr(val));assert s.sqrt(z).is_Rational
      assert mult<=(1 if z==0 else 2)
      count+=mult
     if P.degree()%2==0 and s.sqrt(P.LC()).is_Rational:count+=2
     assert count==bounds[model],(model,count,bounds[model])
     records.append({'orbit':rec['config'],'system':ix,'factor':fi,'quotient':qi,'identification':iden,'complete_point_count':count})
 even=[]
 for coeffs,model,points in [
 ([1,0,14,0,1],(0,0,0,-351,1890),[('-1','4'),('0','1'),('1','4')]),
 ([81,144,142,16,1],(0,0,0,-24003,1296702),[('-1','8'),('-1/3','8/3'),('-1/9','8/9'),('0','1'),('1/3','16/3')]),
 ([1,16,142,144,81],(0,0,0,-24003,1296702),[('-9','72'),('-3','24'),('-1','8'),('0','9'),('3','48')])]:
  P=s.Poly.from_list(coeffs,gens=TAU);iden=match(P,model)
  for x,y in points:assert P.eval(expr(x))==expr(y)**2
  assert len({x for x,y in points})==len(points) and all(expr(y)!=0 for x,y in points)
  assert 2*len(points)+2==bounds[model]
  tau=[]
  for x,y in points:
   r=s.sqrt(expr(x))
   if r.is_Rational:tau.extend([str(r),str(-r)])
  even.append({'coefficients':coeffs,'Jacobian_model':model,'identification':iden,'points_up_to_y_sign':points,'two_rational_infinities':True,'complete_point_count':bounds[model],'rational_tau_with_tau_squared_equal_to_x':sorted(set(tau))+['oo']})
 out.write_text(json.dumps({'direct_genus_one_records_certified':len(records),'records':records,'even_quotients':even},indent=2));print('Complete point counts verified:',len(records),'direct records and',len(even),'even quotients')
if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
