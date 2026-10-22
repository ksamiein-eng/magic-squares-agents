#!/usr/bin/env python3
"""Match exact models and points to cited published Cremona full-basis data.
The published rank/full-generation statement is an explicit external premise.
This program does not reproduce Cremona's rank and saturation computations.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,ast,copy
from elliptic_exact import *
ROOT=Path(__file__).resolve().parent
BASE=(Path(__file__).resolve().parents[1]/'three_prime')

def records():
 rows=[]
 for line in (ROOT/'cremona_basis_excerpt.txt').read_text().splitlines():
  if not line.strip():continue
  f=line.split();a=ast.literal_eval(f[3]);rank=int(f[4]);ts=ast.literal_eval(f[5])
  pts=[]
  for z in f[6:]:
   X,Y,Z=map(int,z.strip('[]').split(':'));pts.append((Q(X,Z),Q(Y,Z)))
  assert len(pts)==rank+len(ts) and all(on_curve(a,P) for P in pts)
  for d,P in zip(ts,pts[rank:]):assert mul(a,d,P) is None and P is not None
  rows.append({'label':f[0]+f[1]+f[2],'model':a,'rank':rank,'torsion_structure':ts,'basis':pts[:rank],'torsion_generators':pts[rank:],'source_line':line})
 return rows

def express(row,P):
 a=row['model'];gs=row['basis'];tors=row['torsion_generators'];ts=row['torsion_structure']
 if len(gs)!=1:return None
 for n in range(-5,6):
  for j in range(ts[0] if ts else 1):
   T=mul(a,j,tors[0]) if tors else None
   if add(a,mul(a,n,gs[0]),T)==P:return {'free_coefficient':n,'torsion_coefficient':j}
 raise RuntimeError('point not expressed in bounded coefficient window')

def main():
 rows=records();by_model={tuple(r['model']):r for r in rows}
 data=json.loads((BASE/'chabauty_inputs_corrected.json').read_text());new=copy.deepcopy(data);matched=[]
 for name,c in new['curves'].items():
  for key in ('quotient1_E','quotient2_Ep'):
   q=c[key];row=by_model[tuple(q['minimal_model'])]
   combos=[]
   for P in q['points_on_minimal_model_verified']:
    P=tuple(map(Q,P));combos.append(express(row,P))
   q['published_cremona_label']=row['label'];q['published_full_basis']=[[str(x) for x in p] for p in row['basis']]
   q['published_torsion_generators']=[[str(x) for x in p] for p in row['torsion_generators']]
   q['published_rank']=row['rank'];q['published_torsion_structure']=row['torsion_structure']
   q['old_point_in_published_basis']=combos
   q['rank_status']='Exact model matched to Cremona published rank; external arithmetic input, not a new descent run'
   q['basis_status']='Use the cited full basis and torsion generators; original point expressions independently checked'
   matched.append({'curve':name,'quotient':key,'cremona_label':row['label'],'point_expressions':combos})
 new['description']='Exact model-compatible data with published Cremona full bases; not a completed quadratic Chabauty calculation.'
 (ROOT/'chabauty_inputs_with_published_bases.json').write_text(json.dumps(new,indent=2)+'\n')
 report={'status':'PASS','external_premise':'Cremona ecdata Table Two full Mordell-Weil generators and ranks, not independently reproved here',
 'source_documentation':'https://johncremona.github.io/ecdata/','source_commit':'1e16f4523e20f14aecbc8fcc1db46b4e9f23a14f','models':len(rows),'matched_quotient_records':len(matched),'matches':matched}
 (ROOT/'published_basis_verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
