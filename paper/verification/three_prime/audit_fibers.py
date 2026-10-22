"""Independent exact audit of finite torsion fibers and generic removed branches.
Polynomial factorization/rational roots use SymPy; no supplied functions are imported.
"""
from pathlib import Path
import itertools,json,sys,collections,time
from concurrent.futures import ProcessPoolExecutor
import sympy as s
from audit_inputs import VS,numerator

def witnesses(E):
 return [(('zero',i),e) for i,e in enumerate(E)]+[(('equal',i,j,sg),E[i]-sg*E[j]) for i in range(4) for j in range(i) for sg in (-1,1)]

def degenerate(E):
 return next((w for w,e in witnesses(E) if s.expand(e)==0),None)

def task(inp):
 name,vecs,k,val=inp;Es=[numerator(v).subs(VS[k],val).expand() for v in vecs]
 a,b=[v for v in VS if v!=VS[k]]
 simple=degenerate(Es)
 if simple:return {'orbit':name,'variable':str(VS[k]),'value':val,'whole_fiber_witness':simple,'passed':True,'systems':0}
 unresolved=[];nondeg=[];count=0;common_count=0;isolated=0
 for i,j in itertools.combinations(range(4),2):
  other=[x for x in range(4) if x not in (i,j)]
  for k,l in itertools.permutations(other):
   for e,f in itertools.product([-1,1],repeat=2):
    tag=[i,j,k,l,e,f];count+=1
    F=s.Poly(Es[i]-e*Es[k]-f*Es[l],a,b,domain=s.QQ)
    G=s.Poly(Es[j]-e*Es[k]+f*Es[l],a,b,domain=s.QQ)
    h=s.gcd(F,G)
    if h.is_zero:
     unresolved.append({'tag':tag,'kind':'both equations identically zero'});continue
    for fac,power in s.factor_list(h.as_expr())[1]:
     pp=s.Poly(fac,a,b)
     if pp.is_ground:continue
     common_count+=1
     wit=next((w for w,x in witnesses(Es) if s.Poly(x,a,b).rem(pp).is_zero),None)
     if wit:continue
     if pp.degree(a)==0 or pp.degree(b)==0:
      v=a if pp.degree(b)==0 else b
      if not s.polys.polytools.ground_roots(s.Poly(fac,v)):continue
     unresolved.append({'tag':tag,'kind':'common branch','factor':str(fac)})
    FF=F.exquo(h).as_expr();GG=G.exquo(h).as_expr()
    R=s.resultant(FF,GG,b)
    if R==0:
     unresolved.append({'tag':tag,'kind':'zero reduced resultant'});continue
    for a0 in s.polys.polytools.ground_roots(s.Poly(R,a)):
     f0=s.Poly(FF.subs(a,a0),b);g0=s.Poly(GG.subs(a,a0),b);hb=s.gcd(f0,g0)
     if hb.is_zero:
      if not degenerate([x.subs(a,a0) for x in Es]):unresolved.append({'tag':tag,'kind':'free second variable','a':str(a0)})
      continue
     for b0 in s.polys.polytools.ground_roots(hb):
      vals=[x.subs({a:a0,b:b0}) for x in Es];isolated+=1
      if not degenerate(vals):nondeg.append({'tag':tag,'point':[str(a0),str(b0)],'Es':[str(x) for x in vals]})
 return {'orbit':name,'variable':str(VS[inp[2]]),'value':val,'systems':count,'common_factors':common_count,'isolated_points_checked':isolated,'unresolved':unresolved,'nondegenerate':nondeg,'passed':not unresolved and not nondeg}

def main(root,out):
 jobs=[]
 for f in sorted((root/'repro/certs').glob('*.json')):
  r=json.load(open(f))
  if 'systems' not in r:continue
  jobs.extend((r['config'],r['elements'],k,a) for k in range(3) for a in [0,1,-1])
 with ProcessPoolExecutor(max_workers=4) as ex:rows=list(ex.map(task,jobs,chunksize=3))
 data={'rows':rows,'fibers':len(rows),'passed':sum(r['passed'] for r in rows),'systems':sum(r['systems'] for r in rows),'unresolved_fibers':[r for r in rows if not r['passed']], 'infinity_boundary_proof':'After fixing one angle to pi, erase its frequency coordinate and ignore vector signs. A zero or duplicate projected vector is degenerate. Otherwise the four projected vectors are the entire nonzero projective {-1,0,1}^2 box, hence a frequency parallelogram excluded by the real-angle theorem.'}
 out.write_text(json.dumps(data,indent=2));print({k:v for k,v in data.items() if k!='rows'})
if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
