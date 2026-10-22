#!/usr/bin/env python3
"""Exclude positive-dimensional nondegenerate fibers above nonlinear projections.
Checks all polynomial coefficients of both original reduced equations. Rational
base points are found exactly, not by a bounded search.
"""
from pathlib import Path
import sys,json,time,itertools
import sympy as s
from genus_exact import BASE,expr,x,y,require,tasks
OUT=Path(__file__).resolve().parent

def rational_points(polys):
 gb=s.groebner(polys,y,x,order='lex')
 if list(gb)==[1]:return [],[str(g) for g in gb]
 univ=[g for g in gb if not g.has(y)]
 require(univ,'positive-dimensional exceptional base locus')
 h=s.Poly(univ[0],x)
 for q in univ[1:]:h=s.gcd(h,s.Poly(q,x))
 pts=[]
 for xx in s.polys.polytools.ground_roots(h):
  ps=[s.Poly(g.subs(x,xx),y) for g in gb if g.subs(x,xx)!=0]
  require(ps,'exceptional vertical line in base')
  hh=ps[0]
  for q in ps[1:]:hh=s.gcd(hh,q)
  for yy in s.polys.polytools.ground_roots(hh):
   require(all(s.expand(g.subs({x:xx,y:yy}))==0 for g in polys),'bad exceptional point')
   pts.append((xx,yy))
 return pts,[str(g) for g in gb]

def main():
 st=time.time();results=[];allrec={}
 for name in ['D2','D3','D4','F+1','F+2']:
  rec=json.loads((BASE/'input/repro/certs'/f'{name}.json').read_text());allrec[name]=rec
  lookup={k:s.Symbol(v,real=True) for k,v in [('x','t'),('z','u'),('w','v')]}
  for sid,ss in enumerate(rec['systems']):
   fs=[f for f in ss['factors'] if f['type']=='nonlinear']
   if not fs:continue
   elim=lookup[ss['projection']['eliminated']];ab=[lookup[q] for q in ss['projection']['plane']]
   sub={ab[0]:x,ab[1]:y}
   cf=expr(ss['common_factor']) if ss.get('common_factor') else s.Integer(1)
   gs=[s.expand(s.cancel(expr(ss[k])/cf).subs(sub,simultaneous=True)) for k in ('G1','G2')]
   coeffs=[c for g in gs for c in s.Poly(g,elim).all_coeffs()]
   es=[s.expand(expr(e).subs(sub,simultaneous=True)) for e in rec['E_polys']]
   for fi,fr in enumerate(fs):
    F=s.expand(expr(fr['poly']).subs(sub,simultaneous=True));pts,gb=rational_points([F]+coeffs);checked=[]
    for xx,yy in pts:
     vals=[s.expand(e.subs({x:xx,y:yy})) for e in es];w=None
     for i in range(4):
      if vals[i]==0:w=['zero',i];break
     if w is None:
      for i,j in itertools.combinations(range(4),2):
       for sg in [-1,1]:
        if s.expand(vals[i]-sg*vals[j])==0:w=['equal',i,j,sg];break
       if w:break
     require(w,('nondegenerate exceptional full fiber',name,sid,xx,yy))
     checked.append({'point':[str(xx),str(yy)],'degeneracy_witness':w})
    results.append({'orbit':name,'system':sid,'source_polynomial':fr['poly'],'coefficient_ideal_groebner':gb,'full_fibers':checked})
  print(name,'PASS',flush=True)
 out={'status':'PASS','scope':'all finite rational full fibers above nonlinear projections; infinity handled by the established boundary lemma','factor_occurrences':len(results),'rational_full_fiber_occurrences':sum(len(r['full_fibers']) for r in results),'records':results,'seconds':round(time.time()-st,3)}
 (OUT/'nonlinear_vertical_fibers.json').write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in out.items() if k!='records'})
if __name__=='__main__':main()
