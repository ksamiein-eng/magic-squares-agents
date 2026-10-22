#!/usr/bin/env python3
"""Rigorous rank-one height floors from matched published bases + exact sieves.
Global generation/ranks are cited Cremona Table Two inputs, not newly rerun
saturation computations. All maps, residues and height inequalities are checked.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,ast,sys
from verify_published_bases import records,BASE
from elliptic_exact import mul,neg,on_curve
from height_exact import require,interval
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE));from rebuild_sieves import one
NAMES={'A':'E_A','B':'E_B','C':'E_C','D':'E_D','E2last_(=A)':'E_A_cubic_E2','Dtw2':'E_D_tw2','Dtwm2':'E_D_twm2','Dtw5':'E_D_tw5'}
EX={'A':[-1,0,1],'B':[-2,0,2],'C':[-2,0,2],'D':[-2,0,2],'E2last_(=A)':[-1,0,1],'Dtw2':[-1,0,1],'Dtwm2':[0],'Dtw5':[0]}

def floorq(q):return q.numerator//q.denominator

def min_outside(M,residues,T):
 T=set(T);candidates=[]
 for r in residues:
  r=r%M
  candidates.extend(abs(r+k*M) for k in range(-3,4) if r+k*M not in T)
 n=min(candidates)
 # Exhaustively check all representatives with |a| < n by exact interval endpoints.
 for r in residues:
  r%=M
  lo=floorq(Q(-n-r,M))+1;hi=-floorq(Q(n+r,M))-1 # not used below; use simple floor for upper
  hi=floorq(Q(n-1-r,M))
  for k in range(lo,hi+1):require(r+k*M in T,'smaller unexcluded class representative')
 require(n>0,'no positive lower representative')
 return n

def main():
 src=json.loads((BASE/'input/chabauty_inputs/sieves_cubic.json').read_text())
 ch=json.loads((BASE/'chabauty_inputs_corrected.json').read_text())['curves']
 hs=json.loads((ROOT/'height_certificate.json').read_text())['models'];byheight={r['label']:r for r in hs}
 rows=records();bymodel={tuple(r['model']):r for r in rows};out=[]
 for name,key in NAMES.items():
  r=src['curves'][name];qq=ch[key]['quotient1_E'];old=r['weierstrass_a_invariants'];require(old==qq['original_weierstrass_model'],'original model mismatch')
  row=bymodel[tuple(qq['minimal_model'])];require(row['rank']==1 and row['torsion_structure']==[],'rank-one torsion-free published model needed')
  uu,rr,tt=[Q(qq['model_change'][z]) for z in ('u','r','t')]
  a1,b,a3,c,d=old;require(a1==a3==0,'original model needs general transform')
  calc=[0,(3*rr+b)/uu**2,2*tt/uu**3,(3*rr**2+2*b*rr+c)/uu**4,(rr**3+b*rr**2+c*rr+d-tt**2)/uu**6]
  require(calc==list(map(Q,row['model'])),'model change mismatch')
  G=tuple(map(Q,ast.literal_eval(r['generator_XY'][0])));Gmin=((G[0]-rr)/uu**2,(G[1]-tt)/uu**3)
  require(Gmin in [row['basis'][0],neg(row['model'],row['basis'][0])],'sieve point not a full generator up to sign')
  sv=one((name,r));require(sv['matches_uploaded'],'subgroup sieve mismatch')
  hh=byheight[row['label']];iv=interval(row['model'],row['basis'][0],hh['bezout'],6)
  lb=Q(iv['lower']);require(lb>0,'height lower endpoint not positive')
  n=min_outside(sv['M'],sv['computed_survivors'],EX[name]);exactfloor=lb*n*n
  A=int(r['f'].split()[0]);points=[]
  for k in EX[name]:
   P=mul(old,k,G);points.append({'index':k,'point':None if P is None else [str(z) for z in P], 's':None if P is None else str(P[0]/A)})
  out.append({'record':name,'published_label':row['label'],'original_model':old,'s_function':'X/'+str(A),'model_change':qq['model_change'],'full_generator_in_target':[str(z) for z in Gmin],'basis_premise':'Cremona published full basis, exact model/point match verified','M':sv['M'],'survivors':sv['computed_survivors'],'exceptions':points,'minimum_index_outside_exceptions':n,'generator_height_interval':iv,'height_floor_exact':str(exactfloor),'height_floor_integer':floorq(exactfloor),'scope':'Every rational point with the specified square-or-zero-or-infinity coordinate, outside exactly the listed points. Not automatically a full orbit classification.','sieve':sv})
  print(name,'index >=',n,'height >=',floorq(exactfloor),flush=True)
 result={'status':'PASS','scope':'global elliptic height bounds using cited published full bases; no fresh descent/saturation run claimed','canonical_height_normalization':'lim 4^-n h(x(2^n P)), twice Silverman','records':out}
 (ROOT/'global_rank_one_bounds.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
