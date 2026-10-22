#!/usr/bin/env python3
"""Independent symbolic check of D1 norms and original-system transport.

Does not import the norm certificate producer or standard-library checker.
Earlier proof-status files are used only to count *new* entries. The new
40-system D1 exclusion is reconstructed independently from the equations.
"""
from pathlib import Path
from itertools import combinations,permutations,product
from collections import Counter
import sys,json
import sympy as s
HERE=Path(__file__).resolve().parent;BASE=HERE.parent/'three_prime';GEO=HERE.parent/'geometry';OLD=HERE.parent/'orbit_progress'
sys.path.insert(0,str(BASE))
from audit_inputs import expr,numerator,T,U,V

def need(b,m):
 if not b:raise ValueError(m)
def co(p,r):return [int(x) for x in reversed(s.Poly(s.expand(p),r).all_coeffs())]
def poly(cs,r):return sum(c*r**i for i,c in enumerate(cs))
def rows(tag):
 i,j,k,l,e,f=tag;R=s.zeros(2,4);R[0,i]=R[1,j]=1;R[0,k]=R[1,k]=-e;R[0,l]=-f;R[1,l]=f;return R

def run(data):
 r=s.symbols('r',real=True);q=1+r*r
 C=s.re(s.expand((1+s.I*r)**2));S=s.im(s.expand((1+s.I*r)**2))
 H=s.Matrix([[C,S,0],[C,-S,0],[q,0,0],[0,0,q]])
 records={}
 for p in (BASE/'input/repro/certs').glob('*.json'):
  d=json.loads(p.read_text())
  if 'systems' in d:records[d['config']]=d
 orig=records['D1'];a=s.Matrix(orig['elements']);basis=s.Matrix([[1,1,0],[0,0,1],[1,0,1]])
 canonical=a*basis.inv();need(canonical==s.Matrix(data['canonical_frequency_matrix']) and abs(basis.det())==1,'wrong change of torus coordinates')
 Es=[numerator(m) for m in orig['elements']];need(all(s.expand(e-expr(f))==0 for e,f in zip(Es,orig['E_polys'])),'old input numerator mismatch')
 good=[];rem=[];closed_methods=Counter()
 for sid,(old,row) in enumerate(zip(orig['systems'],data['systems'])):
  need(sid==row['system'] and row['tag']==old['tag'],'historical system labels differ')
  R=rows(old['tag'])
  need(s.expand((R*s.Matrix(Es))[0]-expr(old['G1']))==0 and s.expand((R*s.Matrix(Es))[1]-expr(old['G2']))==0,'historical equations differ')
  B=R*H;K=s.Matrix(list(B[0,:])).cross(s.Matrix(list(B[1,:])))
  w=s.Matrix([poly(c,r) for c in row['kernel']]);g=poly(row['divisor'],r)
  need(all(s.expand(u-g*v)==0 for u,v in zip(K,w)),'cross-product factorization')
  need(all(s.expand(x)==0 for x in B*w),'kernel identity')
  need(s.Poly(s.gcd_list(list(w)),r).degree()==0,'unexpected simultaneous kernel zero')
  n=s.factor((w[0]**2+w[1]**2)/q**2)
  need(s.expand(n-poly(row['norm_factor'],r))==0,'first norm')
  need(s.expand(w[0]**2+w[1]**2-w[2]**2-poly(row['second_norm'],r))==0,'second norm')
  if n in [r*r+9,9*r*r+1]:rem.append(sid)
  else:
   if n==1:need(w[0]==0,'constant-norm zero case');closed_methods['zero sine']+=1
   elif n in [r**4+6*r*r+1,r**4-3*r*r+4,r**4+18*r*r+1]:closed_methods['norm quartic']+=1
   else:need(n==4*r**4-3*r*r+1,'unknown norm');closed_methods['reciprocal norm quartic']+=1
   good.append(sid)
 need(len(good)==40 and rem==[8,9,12,14,24,25,28,30],'D1 status')
 # Remaining conic parameterization and rational-circle reconstruction are
 # recomputed symbolically rather than imported from the standalone checker.
 h,Y=s.symbols('h Y',real=True);P=h**12+70*h**10-1009*h**8+7060*h**6-1009*h**4+70*h**2+1
 Rpar=6*h/(1-h*h);f=lambda x:x**6-5*x**4+19*x*x+9
 need(s.cancel((1-h*h)**6*f(Rpar)-9*P)==0,'genus-five pullback')
 need(s.gcd(s.Poly(P,h),s.Poly(s.diff(P,h),h)).degree()==0,'residual polynomial not squarefree')
 aq=1+h*h;bq=h**4+34*h*h+1;D=aq*bq
 sa=(1-h*h)/aq;ca=-2*h/aq;sb=12*h*(1-h*h)/bq;cb=(h**4-38*h*h+1)/bq;sg=-48*h*h*(1-h*h)/D;cg=Y/D
 need(s.cancel(sa*sa+ca*ca-1)==s.cancel(sb*sb+cb*cb-1)==0,'reconstructed alpha/beta circle')
 need(s.cancel((sg*sg+cg*cg-1)*D**2-(Y*Y-P))==0,'reconstructed gamma circle')
 vals=s.Matrix([sa*cb+ca*sb,sa*cb-ca*sb,sa,sg]);need(all(s.cancel(x)==0 for x in rows(orig['systems'][8]['tag'])*vals),'base assignment not solved')
 A=[h**4-62*h*h+1,h**4-14*h*h+1,h**4+34*h*h+1,-48*h*h]
 Z=s.prod(A)*s.prod(A[i]**2-A[j]**2 for i,j in combinations(range(4),2))
 c,facs=s.factor_list(Z)
 for pp,mu in facs:
  if pp==h:continue
  p=s.Poly(pp,h);need(p.LC()==1 and abs(p.TC())==1 and p.eval(1)!=0 and p.eval(-1)!=0,'possible extra rational degeneracy')
 # Full projective r=0,infinity fibers have the first two sine magnitudes equal.
 need(H[0,:].subs(r,0)==H[1,:].subs(r,0),'zero boundary')
 top0=[s.Poly(v,r).nth(2) for v in H[0,:]];top1=[s.Poly(v,r).nth(2) for v in H[1,:]];need(top0==top1,'infinity boundary')
 # Three exact degree-two transports, each with all 48 assignment maps checked.
 maps=[('B2',[[1,-1,-2],[0,2,2],[0,0,1]]),('C',[[0,-2,1],[0,2,0],[1,1,0]]),('E2',[[0,2,0],[0,-2,1],[1,-1,0]])]
 transport=[];proved={('D1',i) for i in good}
 for target,mm in maps:
  M=s.Matrix(mm);At=s.Matrix(records[target]['elements']);W=a*M;PP=s.zeros(4,4)
  for i in range(4):
   matches=[(j,sgn) for j in range(4) for sgn in [1,-1] if W[i,:]==sgn*At[j,:]]
   need(len(matches)==1,'frequency image ambiguous');j,sgn=matches[0];PP[i,j]=sgn
  need(abs(PP.det())==1 and abs(M.det())==2 and W==PP*At,'bad monomial map')
  keys={tuple(rows(sy['tag']).rref()[0]):i for i,sy in enumerate(records[target]['systems'])};ss=[]
  for sid,sy in enumerate(orig['systems']):
   left=rows(sy['tag'])*PP;key=tuple(left.rref()[0]);need(key in keys,'target assignment missing');tid=keys[key]
   right=rows(records[target]['systems'][tid]['tag']);need(left.col_join(right).rank()==2,'row-space implication fails')
   ss.append({'source_system':sid,'target_system':tid,'source_closed_now':sid in good})
   if sid in good:proved.add((target,tid))
  transport.append({'source':'D1','target':target,'matrix':mm,'degree':2,'signed_permutation':[[int(x) for x in PP[i,:]] for i in range(4)],'systems':ss})
 # Count new factor entries against the previous verified ledger. This section
 # does not accept new proofs based merely on an empty point-search output.
 baseline=json.loads((BASE/'lift_audit.json').read_text())
 closed={(x['orbit'],x['system'],x['factor']) for x in baseline['factor_statuses'] if not x['status'].startswith('unresolved')}
 for x in json.loads((GEO/'reciprocal_octic_closures.json').read_text())['lifts']:closed.add((x['orbit'],x['system'],x['factor']))
 for x in json.loads((GEO/'d3_rank_zero_family.json').read_text())['closed_factors']:
  for j,f in enumerate(records['D3']['systems'][x['system']]['factors']):
   if f['type']=='nonlinear':closed.add(('D3',x['system'],j))
 previous=json.loads((OLD/'progress_verification.json').read_text())
 for x in previous['new_octic_factor_closures']:closed.add((x['orbit'],x['system'],x['factor']))
 for x in previous['new_transferred_closures']:
  for j in x['new_factor_indices']:closed.add((x['target'],x['target_system'],j))
 new={(label,i,j) for label,i in proved for j in range(len(records[label]['systems'][i]['factors']))}-closed
 need(len(new)==64 and Counter(x[0] for x in new)=={'D1':16,'B2':16,'C':16,'E2':16},'new factor count wrong')
 now=closed|new;ledger=[]
 for label in ['A','B1','B2','C','D1','D2','D3','D4','E1','E2','E3','F-1','F-2','F+1','F+2']:
  before=[(label,i,j) for i,sy in enumerate(records[label]['systems']) for j in range(len(sy['factors'])) if (label,i,j) not in closed]
  after=[x for x in before if x not in now]
  ledger.append({'orbit':label,'previous_unresolved_factors':len(before),'unresolved_factors':len(after),'new_factor_closures':len(before)-len(after),'unresolved_systems':sorted({x[1] for x in after}),'whole_orbit_closed':len(after)==0})
 need([x['orbit'] for x in ledger if x['whole_orbit_closed']]==['A','E1','E3','F-1','F-2'],'unproved whole-orbit assertion')
 report={'status':'PASS','closed_D1_systems':good,'residual_D1_systems':rem,'D1_methods':dict(closed_methods),'new_factor_closures':64,'new_factor_entries':[list(x) for x in sorted(new)],'torus_maps':transport,'rowspace_checks':144,'orbit_ledger':ledger,'genus_five_residual':str(P),'residual_completeness_proved':False,'residual_existence_equivalence_proved':True,'mathematical_dependency':'Three norm-quartic rank-zero certificates checked in verify_d1_stdlib.py; previous ledger only determines which entries are new.','software':'Python and exact SymPy polynomial/rational arithmetic; no Chabauty or external rank database for the new curves.'}
 return report

if __name__=='__main__':
 data=json.loads((HERE/'d1_certificate.json').read_text());report=run(data)
 (HERE/'d1_transfer_verification.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS: 64 new factor closures (16 each D1/B2/C/E2); 144 row-space checks; eight residual D1 systems on one genus-five curve.')
