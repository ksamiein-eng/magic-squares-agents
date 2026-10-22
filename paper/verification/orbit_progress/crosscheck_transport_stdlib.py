#!/usr/bin/env python3
"""Independent standard-library check of integer circle maps and all signed rows.
Does not import SymPy, the transport producer, or the historical pipeline.
Prerequisite orbit exclusions remain the theorems stated in the manuscript.
"""
from pathlib import Path
from fractions import Fraction as Q
import json,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent/'three_prime/input/repro/certs'
class Invalid(ValueError):pass

def need(a,msg):
 if not a:raise Invalid(msg)
def mm(A,B):return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def det(M):
 a,b,c=M[0];d,e,f=M[1];g,h,i=M[2]
 return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)
def rr(A):
 A=[[Q(x) for x in row] for row in A];h=0
 for k in range(len(A[0])):
  ids=[i for i in range(h,len(A)) if A[i][k]]
  if not ids:continue
  i=ids[0];A[i],A[h]=A[h],A[i];p=A[h][k];A[h]=[x/p for x in A[h]]
  for j in range(len(A)):
   if j!=h:
    p=A[j][k];A[j]=[a-p*b for a,b in zip(A[j],A[h])]
  h+=1
  if h==len(A):break
 return tuple(tuple(x for x in row) for row in A)
def eq(tag):
 i,j,k,l,e,f=tag;C=[[0]*4 for _ in range(2)]
 C[0][i]=C[1][j]=1;C[0][k]=C[1][k]=-e;C[0][l]=-f;C[1][l]=f
 return C

def verify(report):
 need(report['new_factor_closures']==24 and report['new_closed_whole_orbits']==0,'wrong declared scope')
 rec={n:json.loads((ROOT/(n+'.json')).read_text()) for n in ['B1','B2','C','D1','D3','E2','F-1']}
 checked=0
 for r in report['torus_morphisms']:
  source,target=r['source'],r['target'];M=r['matrix']
  need(all(type(x) is int for row in M for x in row),'noninteger circle exponent')
  P=[[0]*4 for _ in range(4)]
  for i,(j,sg) in enumerate(r['signed_frequency_permutation']):
   need(sg in [1,-1],'not a sign');P[i][j]=sg
  need(all(sum(abs(x) for x in col)==1 for col in zip(*P)),'not a permutation')
  need(mm(rec[source]['elements'],M)==mm(P,rec[target]['elements']),'frequency multiplication identity')
  need(det(M)==r['determinant'] and abs(det(M))==r['degree'] and det(M)!=0,'incorrect torus degree')
  if 'inverse_matrix' in r:
   N=r['inverse_matrix'];I=[[int(i==j) for j in range(3)] for i in range(3)]
   need(all(type(x) is int for row in N for x in row),'inverse not integral')
   need(abs(det(M))==1 and mm(M,N)==mm(N,M)==I,'false torus isomorphism')
  links=r['signed_system_transport']
  need(len(links)==48 and {x['source_system'] for x in links}==set(range(48)),'missing signed rows')
  for link in links:
   si,ti=link['source_system'],link['target_system']
   left=mm(eq(rec[source]['systems'][si]['tag']),P);right=eq(rec[target]['systems'][ti]['tag'])
   need(rr(left)==rr(right),'signed row-space transport fails');checked+=1
 # Direct symbolic-frequency witness for the universal three-term addition.
 u=report['universal_addition_obstruction']
 need(mm(rec['F-1']['elements'],u['matrix'])==u['target_frequencies'] and abs(det(u['matrix']))==1,'universal frequency identity')
 need(checked==240,'unexpected count')
 need({r['target_system'] for r in report['new_transferred_closures']}==set(range(24,32)),'wrong transferred B1 systems')
 return {'status':'PASS','frequency_maps':5,'signed_row_spaces':checked,'universal_addition_map':True,'scope':'Integer torus transformations only; not a standalone proof of the source orbit theorems.'}
if __name__=='__main__':
 p=Path(sys.argv[1]) if len(sys.argv)>1 else HERE/'progress_verification.json'
 out=verify(json.loads(p.read_text()));(HERE/'transport_stdlib_verification.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS: 5 integer torus maps, 240 signed row-space identities, and the universal addition map.')
