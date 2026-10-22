#!/usr/bin/env python3
from genus_exact import *
from copy import deepcopy
from pathlib import Path
import json

def main():
 tests=[]
 for name,F,want in [('node',y*y-x*x-x**3,1),('cusp',y*y-x**3,1),('tacnode',y*y-x**4,2),('triple',x*y*(y-x),3),('vertical cusp',x*x-y**3,1),('two tangent cusps',(y*y-x**3)*(y*y-2*x**3),8)]:
  got=local_delta(F)['delta'];require(got==want,(name,got,want));tests.append([name,got])
 for name,F,want in [('rational circle',x*x+y*y-1,0),('Fermat cubic',x**3+y**3+1,1),('nodal cubic',y*y-x*x*(x+1),0)]:
  got=genus(F)['geometric_genus'];require(got==want,(name,got,want));tests.append([name,got])
 # Recompute five representatives and compare full stored proof objects.
 data=json.loads((OUT/'nonlinear_genus_certificate.json').read_text())
 for name in ['D2','D3','D4','F+1','F+2']:
  rec=next(r for r in data['results'] if r['orbit']==name);F=s.sympify(rec['polynomial'],locals={'x':x,'y':y})
  fresh=genus(F)
  for key in fresh:require(fresh[key]==rec[key],('stored geometry mismatch',name,key))
  for key in ('geometric_genus','total_delta'):
   bad=deepcopy(rec);bad[key]+=1
   require(fresh[key]!=bad[key],'corruption escaped comparison')
  tests.append([name,'recomputed and altered genus/delta rejected'])
 (OUT/'geometry_tests.json').write_text(json.dumps({'status':'PASS','tests':tests},indent=2)+'\n');print(tests)
if __name__=='__main__':main()
