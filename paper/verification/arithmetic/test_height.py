#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as Q
from copy import deepcopy
import json
from height_exact import check_bezout,interval,require
from global_rank_one_bounds import min_outside
ROOT=Path(__file__).resolve().parent

def main():
 c=json.loads((ROOT/'height_certificate.json').read_text())['models'][0];w=c['bezout'];tests=[]
 for name,change in [('D',lambda q:q.__setitem__('D',q['D']+1)),('U coefficient',lambda q:q['X7']['U'].__setitem__(0,q['X7']['U'][0]+1)),('V coefficient',lambda q:q['Z7']['V'].__setitem__(2,q['Z7']['V'][2]+1))]:
  bad=deepcopy(w);change(bad)
  try:check_bezout(c['model'],bad)
  except RuntimeError:tests.append([name,'rejected'])
  else:raise RuntimeError('damaged Bezout witness accepted')
 for M in range(3,20):
  for residues in [[0],[1],[0,1,M-1]]:
   T=[-1,0,1]
   n=min_outside(M,residues,T)
   brute=min(abs(x) for x in range(-3*M,3*M+1) if x%M in {r%M for r in residues} and x not in T)
   require(n==brute,'residue minimum differs from finite exhaustive regression')
 tests.append(['residue minima','51 exact small-modulus regressions'])
 (ROOT/'height_tests.json').write_text(json.dumps({'status':'PASS','tests':tests},indent=2)+'\n');print(tests)
if __name__=='__main__':main()
