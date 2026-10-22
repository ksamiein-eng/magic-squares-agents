#!/usr/bin/env python3
"""Two reciprocal-octic rank-zero routes and complete lifts to recorded systems.
The first rank-zero quotient is proved by elementary 2-isogeny descent here;
the second is the already certified conductor-80 quartic from the baseline.
"""
from pathlib import Path
import json,sys,math
import sympy as s
from genus_exact import BASE,require
sys.path.insert(0,str(BASE))
from audit_inputs import expr,TAU
from audit_lifts import normal,lift_one,zeros_of_removed
OUT=Path(__file__).resolve().parent

def rank_zero_64():
 # E:y^2=x^3-4x, E':y^2=x^3+16x. E image has at most four classes.
 # Negative classes for E' are impossible by sign. Class 2 fails modulo 16.
 squares={n*n%16 for n in range(16)}
 residues={ (2*u**4+8*v**4)%16 for u in range(16) for v in range(16) if u%2 or v%2 }
 require(not(residues&squares),'2-isogenous class 2 is not locally obstructed')
 counts={}
 for p in (3,5):
  count=1+sum(sum(y*y%p==(x*x*x-4*x)%p for y in range(p)) for x in range(p));counts[p]=count
 require(math.gcd(*counts.values())==4,'torsion upper bound differs')
 return {'model':[0,0,0,-4,0],'isogenous_model':[0,0,0,16,0],'image_upper_sizes':[4,1],'class_2_obstruction_modulus':16,'primitive_residues':sorted(residues),'square_residues':sorted(squares),'torsion_upper_bound':4,'point_counts':counts,'rank':0}

def main():
 t=TAU;r=s.symbols('r');H1=t**8+4*t**6+22*t**4+4*t*t+1;H2=t**8-44*t**6+166*t**4-44*t*t+1
 Q1=r**4+16;Q2=r**4-48*r*r+256
 for H,Q in ((H1,Q1),(H2,Q2)):require(s.cancel(H/t**4-Q.subs(r,t+1/t))==0,'reciprocal quotient identity')
 require(s.expand(Q2.subs(r,4*t)/256-(t**4-3*t*t+1))==0,'conductor-80 quartic scaling')
 rz=rank_zero_64();jobs=[]
 for p in sorted((BASE/'input/repro/certs').glob('*.json')):
  rec=json.loads(p.read_text())
  for sid,ss in enumerate(rec.get('systems',[])):
   for fi,f in enumerate(ss['factors']):
    for qi,q in enumerate(f.get('quotients',[])):
     if q.get('curve_kind')!='genus>=2':continue
     N=normal(expr(q['D(tau)'])).as_expr()
     if s.expand(N-H1)==0 or s.expand(N-H2)==0:
      jobs.append((rec['config'],rec['elements'],ss,f,sid,fi,qi,['0','oo']+zeros_of_removed(expr(q['D(tau)']))));break
 results=[]
 for job in jobs:
  v=lift_one(job);require(v['passed'],('unresolved octic lift',v));results.append(v)
 baseline=json.loads((BASE/'lift_audit.json').read_text())
 prior={(q['orbit'],q['system'],q['factor']) for q in baseline['lifts']}
 fresh=[q for q in results if (q['orbit'],q['system'],q['factor']) not in prior]
 require(len(fresh)==24 and len(results)==32,'new versus rechecked lift counts')
 report={'status':'PASS','rank_zero_64_certificate':rz,'quotient_polynomials':[str(Q1),str(Q2)],'complete_quotient_parameters':['0','infinity'],'octic_polynomials':[str(H1),str(H2)],'complete_octic_parameters':['0','infinity'],'proof':'The rank-zero quotients have only parameter 0 and infinity; finite nonzero t would require t+1/t=0, impossible over Q.','lifted_factor_entries':len(results),'new_factor_closures':len(fresh),'previously_closed_rechecked':len(results)-len(fresh),'lifts':results,'note':'These close individual factor entries, not every factor of any additional whole orbit.'}
 (OUT/'reciprocal_octic_closures.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',len(results),'reciprocal-octic factor lifts;',len(fresh),'new closures')
if __name__=='__main__':main()
