#!/usr/bin/env python3
"""Normalize recorded nonlinear projections by all singular point blowups.
Characteristic zero, P1 x P1 charts, exact algebraic coefficients, no genus proxy.
"""
from pathlib import Path
import sys,json,time,itertools,collections
from math import gcd
from concurrent.futures import ProcessPoolExecutor
import sympy as s
BASE=(Path(__file__).resolve().parents[1]/'three_prime')
sys.path.insert(0,str(BASE))
from audit_inputs import expr
x,y=s.symbols('x y'); OUT=Path(__file__).resolve().parent

def require(v,msg):
 if not v:raise RuntimeError(msg)

def norm(f):return s.Poly(s.expand(f),x,y,extension=True).as_expr()

def roots_all(p,z):
 p=s.Poly(p,z,extension=True)
 if p.degree()<=0:return []
 rr=s.roots(p.as_expr(),z)
 require(sum(rr.values())==p.degree(),('incomplete algebraic root list',p.as_expr(),rr))
 return sorted(rr,key=s.default_sort_key)

def fiber_gcd(polys,z):
 pp=[s.Poly(g,z,extension=True) for g in polys if g!=0]
 require(pp,'positive dimensional specialized singular fiber')
 h=pp[0]
 for p in pp[1:]:h=s.gcd(h,p)
 return h.monic().as_expr()

def affine_singulars(F):
 gb=s.groebner([F,s.diff(F,x),s.diff(F,y)],y,x,order='lex')
 if list(gb)==[1]:return [],[str(g) for g in gb]
 ex=[g for g in gb if not g.has(y)]
 require(ex,'singular locus not certified zero dimensional')
 pts=[]
 for xx in roots_all(fiber_gcd(ex,x),x):
  gy=fiber_gcd([s.expand(g.subs(x,xx)) for g in gb],y)
  for yy in roots_all(gy,y):
   require(all(s.simplify(g.subs({x:xx,y:yy}))==0 for g in gb),'wrong singular point')
   pts.append((xx,yy))
 return pts,[str(g) for g in gb]

def invert(F,a,b,cx,cy):
 return s.Poly.from_dict({(a-i if cx else i,b-j if cy else j):c for (i,j),c in s.Poly(F,x,y).terms()},(x,y)).as_expr()

def local_delta(F,depth=0):
 require(depth<12,'blowup depth limit')
 F=norm(F);p=s.Poly(F,x,y,extension=True)
 require(p.coeff_monomial(1)==0,'local point not on curve')
 m=min(i+j for (i,j),c in p.terms())
 rec={'multiplicity':m,'polynomial':str(F),'children':[]}
 if m<=1:rec['delta']=0;return rec
 tangent=s.Poly.from_dict({(i,j):c for (i,j),c in p.terms() if i+j==m},(x,y),domain=p.domain).as_expr()
 rec['tangent_cone']=str(tangent)
 slope=s.Poly(tangent.subs(x,1),y,extension=True)
 rep=s.gcd(slope,slope.diff())
 for c in roots_all(rep.as_expr(),y):
  raw=s.Poly(norm(F.subs(y,x*(c+y))),x,y,extension=True)
  require(all(i>=m for (i,j),a in raw.terms()),'nonexact blowup division')
  G=s.Poly.from_dict({(i-m,j):a for (i,j),a in raw.terms()},(x,y),domain=raw.domain).as_expr()
  child=local_delta(G,depth+1);child['direction']=str(c);rec['children'].append(child)
 vm=m-slope.degree()
 if vm>=2:
  raw=s.Poly(norm(F.subs(x,y*x)),x,y,extension=True)
  require(all(j>=m for (i,j),a in raw.terms()),'nonexact vertical blowup division')
  G=s.Poly.from_dict({(i,j-m):a for (i,j),a in raw.terms()},(x,y),domain=raw.domain).as_expr()
  child=local_delta(G,depth+1);child['direction']='infinity';rec['children'].append(child)
 rec['finite_tangent_squarefree_part']=str(slope.sqf_part().as_expr())
 rec['vertical_tangent_multiplicity']=int(vm)
 rec['delta']=m*(m-1)//2+sum(c['delta'] for c in rec['children'])
 return rec

def genus(F):
 F=s.Poly(F,x,y,domain=s.QQ).clear_denoms()[1].primitive()[1].as_expr()
 a=int(s.degree(F,x));b=int(s.degree(F,y))
 fact=s.factor_list(F,x,y)[1]
 require(len(fact)==1 and fact[0][1]==1,'polynomial reducible over Q')
 # Q-irreducibility + a smooth Q-point implies geometric irreducibility.
 witness=None
 for xx in (0,1,-1,2,-2,s.Rational(1,2),s.Rational(-1,2)):
  fy=s.Poly(F.subs(x,xx),y)
  if fy.is_zero:continue
  for yy in s.polys.polytools.ground_roots(fy):
   vals=[s.diff(F,z).subs({x:xx,y:yy}) for z in (x,y)]
   if any(v!=0 for v in vals):witness={'x':str(xx),'y':str(yy),'gradient':[str(v) for v in vals]};break
  if witness:break
 abs_cert={'method':'smooth rational point','point':witness} if witness else None
 if abs_cert is None and gcd(a,b)==1:
  abs_cert={'method':'coprime bidegrees','component_count_divides_gcd':1}
 if abs_cert is None:
  for xx in (0,1,-1,2,-2,s.Rational(1,2),s.Rational(-1,2)):
   fy=s.Poly(F.subs(x,xx),y)
   if fy.is_zero:continue
   for h,mul in s.factor_list(fy.as_expr(),y)[1]:
    deg=int(s.degree(h,y))
    if gcd(gcd(a,b),deg)!=1:continue
    singular=s.gcd(s.Poly(h,y),s.gcd(s.Poly(s.diff(F,x).subs(x,xx),y),s.Poly(s.diff(F,y).subs(x,xx),y)))
    if singular.degree()==0:
     abs_cert={'method':'smooth closed point and bidegree','x':str(xx),'irreducible_y_polynomial':str(h),'point_degree':deg,'component_count_divides_gcd':gcd(gcd(a,b),deg)}
     break
   if abs_cert:break
 require(abs_cert,('geometric irreducibility not certified',F))
 pts,gb=affine_singulars(F);charts=[((0,0),F,pts)]
 for cx,cy in ((1,0),(0,1)):
  G=invert(F,a,b,cx,cy);at=x if cx else y;z=y if cx else x
  h=fiber_gcd([s.expand(g.subs(at,0)) for g in (G,s.diff(G,x),s.diff(G,y))],z)
  qs=[(s.Integer(0),q) if cx else (q,s.Integer(0)) for q in roots_all(h,z)]
  charts.append(((cx,cy),G,qs))
 G=invert(F,a,b,1,1)
 corner=all(g.subs({x:0,y:0})==0 for g in (G,s.diff(G,x),s.diff(G,y)))
 charts.append(((1,1),G,[(s.Integer(0),s.Integer(0))] if corner else []))
 singulars=[]
 for chart,G,points in charts:
  for xx,yy in points:
   loc=norm(G.subs({x:x+xx,y:y+yy},simultaneous=True));tree=local_delta(loc)
   singulars.append({'chart':list(chart),'point':[str(xx),str(yy)],'resolution':tree,'delta':tree['delta']})
 delta=sum(q['delta'] for q in singulars)
 return {'polynomial':str(F),'bidegree':[a,b],'geometrically_irreducible':True,'smooth_rational_point':witness,'absolute_irreducibility_certificate':abs_cert,
 'affine_singular_groebner_basis':gb,'singularities':singulars,'arithmetic_genus':(a-1)*(b-1),
 'total_delta':delta,'geometric_genus':(a-1)*(b-1)-delta}

def generic_lift(ss,F):
 lookup={k:s.Symbol(v,real=True) for k,v in [('x','t'),('z','u'),('w','v')]}
 elim=lookup[ss['projection']['eliminated']]; ab=[lookup[a] for a in ss['projection']['plane']]
 cf=expr(ss['common_factor']) if ss.get('common_factor') else s.Integer(1)
 gs=[s.expand(s.cancel(expr(ss[k])/cf).subs({ab[0]:x,ab[1]:y},simultaneous=True)) for k in ('G1','G2')]
 P=s.Poly(F,x,y,domain=s.QQ)
 def mod(f):return s.Poly(f,x,y,domain=s.QQ).rem(P).as_expr()
 C=[[mod(s.Poly(g,elim).nth(k)) for k in (0,1,2)] for g in gs]
 h0=s.expand(C[1][2]*C[0][0]-C[0][2]*C[1][0])
 h1=s.expand(C[1][2]*C[0][1]-C[0][2]*C[1][1])
 if mod(h1)==0:
  for c,b,a in C:
   if a==0 and b!=0:h0,h1=c,b;break
 if mod(h1)==0:
  return {'status':'generic_degree_not_yet_resolved','coefficients':[[str(a) for a in row] for row in C]}
 for c,b,a in C:
  require(mod(s.expand(a*h0*h0-b*h0*h1+c*h1*h1))==0,'inverse does not satisfy original equations')
 return {'status':'birational','inverse_numerator':str(-h0),'inverse_denominator':str(h1),'eliminated':str(elim)}

def one_case(payload):
 name,idx,ss,fr=payload; start=time.time()
 lookup={k:s.Symbol(v,real=True) for k,v in [('x','t'),('z','u'),('w','v')]}
 ab=[lookup[a] for a in ss['projection']['plane']]
 F=expr(fr['poly']).subs({ab[0]:x,ab[1]:y},simultaneous=True)
 try:
  result=genus(F);result['generic_lift']=generic_lift(ss,F)
  result.update(orbit=name,system=idx,source_polynomial=fr['poly'],status='PASS',seconds=round(time.time()-start,3))
  require(result['geometric_genus']>=0,'negative computed genus')
 except Exception as ex:
  result={'orbit':name,'system':idx,'source_polynomial':fr['poly'],'status':'UNRESOLVED','error':str(ex),'seconds':round(time.time()-start,3)}
 return result

def tasks():
 jobs=[];occurrences=[]
 for name in ['D2','D3','D4','F+1','F+2']:
  d=json.loads((BASE/'input/repro/certs'/f'{name}.json').read_text());seen={}
  for idx,ss in enumerate(d['systems']):
   for j,fr in enumerate(ss['factors']):
    if fr['type']!='nonlinear':continue
    key=fr['poly']
    if key not in seen:
     seen[key]=len(jobs);jobs.append((name,idx,ss,fr))
    occurrences.append({'orbit':name,'system':idx,'factor_index':j,'job':seen[key]})
 return jobs,occurrences

def main():
 out=OUT/'nonlinear_genus_certificate.json'; start=time.time();jobs,occ=tasks()
 if '--probe' in sys.argv:
  jobs=[next(q for q in jobs if q[0]==n) for n in ['D2','D3','D4','F+1','F+2']]
  results=[one_case(q) for q in jobs]
  for r in results:
   print(r['orbit'],r['status'],r.get('geometric_genus'),r.get('generic_lift',{}).get('status'),r.get('error'),flush=True)
  (OUT/'probe_results.json').write_text(json.dumps(results,indent=2))
  return
 results=[]
 with ProcessPoolExecutor(max_workers=4) as pool:
  for k,r in enumerate(pool.map(one_case,jobs,chunksize=1),1):
   results.append(r)
   print(k,'/',len(jobs),r['orbit'],r['status'],'g=',r.get('geometric_genus'),r.get('error',''),flush=True)
   (OUT/'genus_checkpoint.json').write_text(json.dumps({'status':'PARTIAL','results':results},indent=2))
 summary={n:dict(collections.Counter(str(r.get('geometric_genus','UNRESOLVED')) for r in results if r['orbit']==n)) for n in ['D2','D3','D4','F+1','F+2']}
 result={'status':'PASS' if all(r['status']=='PASS' for r in results) else 'INCOMPLETE','method':'P1xP1 arithmetic genus minus all local delta invariants, computed by exact blowups','results':results,'occurrences':occ,'summary':summary,'seconds':round(time.time()-start,3)}
 out.write_text(json.dumps(result,indent=2))
 print(json.dumps(summary,indent=2),flush=True)

if __name__=='__main__':main()
