"""Complete rational lifting for certified finite quotients; no finite-height search.
The quotient point lists are justified by rankzero_quotient_audit.json and its verifier.
Every generic branch and torsion/projective boundary is audited separately.
"""
from pathlib import Path
import sys,json,itertools,collections
from concurrent.futures import ProcessPoolExecutor
import sympy as s
from audit_inputs import expr,VS,T,U,V,TAU,numerator
from audit_fibers import degenerate

def normal(P):
 c,fs=s.factor_list(P)
 red=s.Poly(s.expand(c*s.prod(f for f,e in fs if e%2)),TAU)
 co=int(red.content());square=s.prod(p**(2*(e//2)) for p,e in s.factorint(abs(co)).items())
 return s.Poly(s.expand(red.as_expr()/square),TAU)

def zeros_of_removed(D):
 zeros=[]
 for f,e in s.factor_list(D)[1]:
  if e>=2:zeros.extend(map(str,s.polys.polytools.ground_roots(s.Poly(f,TAU))))
 return zeros

def lift_one(payload):
 name,vecs,ss,fr,ix,fi,qi,taus=payload
 lookup={'x':T,'z':U,'w':V};a,b=[lookup[x] for x in ss['projection']['plane']];elim=lookup[ss['projection']['eliminated']]
 Es=[numerator(m) for m in vecs];F=expr(fr['poly']);q=fr['quotients'][qi];B=q['B'];M=fr['basis_M']
 p=s.Integer(1)
 for var,k in zip([a,b],M[1]):
  k*=B;p*= (1+s.I*var)**(2*k) if k>=0 else (1-s.I*var)**(-2*k)
 p=s.expand(p);g1=expr(ss['G1']);g2=expr(ss['G2']);points=[];unresolved=[];plane_points=0
 for ta in sorted(set(taus)):
  target=-s.Integer(1) if ta=='oo' else (1+s.I*expr(ta))**2
  H=s.expand(s.im(s.expand(p*s.conjugate(target))))
  if H==0:unresolved.append({'tau':ta,'reason':'identically zero lifting equation'});continue
  R=s.resultant(F,H,b)
  if R==0:unresolved.append({'tau':ta,'reason':'common lifting component','gcd':str(s.gcd(F,H))});continue
  for a0 in s.polys.polytools.ground_roots(s.Poly(R,a)):
   h=s.gcd(s.Poly(F.subs(a,a0),b),s.Poly(H.subs(a,a0),b))
   if h.is_zero:unresolved.append({'tau':ta,'reason':'free plane fiber','a':str(a0)});continue
   for b0 in s.polys.polytools.ground_roots(h):
    plane_points+=1;sub={a:a0,b:b0};f1=s.Poly(g1.subs(sub),elim);f2=s.Poly(g2.subs(sub),elim);he=s.gcd(f1,f2)
    if he.is_zero:
     ww=degenerate([x.subs(sub) for x in Es])
     if not ww:unresolved.append({'tau':ta,'reason':'free eliminated parameter','point':{str(a):str(a0),str(b):str(b0)}})
     else:points.append({'tau':ta,'point':{str(a):str(a0),str(b):str(b0)},'free_variable':str(elim),'witness':ww})
     continue
    for c0 in s.polys.polytools.ground_roots(he):
     pt=dict(sub);pt[elim]=c0;values=[x.subs(pt) for x in Es];ww=degenerate(values)
     assert ww,(name,ix,fi,ta,pt,values)
     points.append({'tau':ta,'point':{str(x):str(y) for x,y in pt.items()},'witness':ww})
 return {'orbit':name,'system':ix,'factor':fi,'quotient':qi,'tau_values':sorted(set(taus)),'plane_points_checked':plane_points,'lifts_checked':points,'unresolved':unresolved,'passed':not unresolved}

def main(root,out):
 rza=json.load(open(Path(__file__).with_name('rankzero_quotient_audit.json')))
 evens={tuple(r['coefficients']):r['rational_tau_with_tau_squared_equal_to_x'] for r in rza['even_quotients']}
 jobs=[];statuses=[]
 for path in sorted((root/'repro/certs').glob('*.json')):
  r=json.load(open(path))
  for ix,ss in enumerate(r.get('systems',[])):
   lookup={'x':T,'z':U,'w':V};a,b=[lookup[x] for x in ss['projection']['plane']]
   for fi,fr in enumerate(ss['factors']):
    row={'orbit':r['config'],'system':ix,'factor':fi,'type':fr['type'],'status':None}
    if fr['type'] in ['degenerate_component','isolated_line_points']:row['status']='component_audit'
    elif fr['type']=='univariate':
     F=expr(fr['poly']);var=next(iter(F.free_symbols));roots=s.polys.polytools.ground_roots(s.Poly(F,var))
     assert set(roots)<={s.Integer(-1),s.Integer(0),s.Integer(1)}
     row['status']='torsion_fiber_or_no_rational_root'
    elif 'exact_verification' in fr:row['status']='linear_relation_component_audit'
    elif fr['type']=='linear_in_circle_point':
     used=[(qi,q) for qi,q in enumerate(fr['quotients']) if q.get('used')]
     assert len(used)<=1
     if not used:row['status']='unresolved_no_finite_quotient'
     else:
      qi,q=used[0];D=expr(q['D(tau)']);taus=None
      if q['curve_kind']=='genus1':taus=list(set(q['curve']['tau_values']))
      elif q['curve_kind']=='genus>=2':
       P=normal(D)
       if all(ex[0]%2==0 for ex in P.monoms()) and P.degree()==8:
        coef=tuple(int(P.nth(2*i)) for i in range(4,-1,-1))
        if coef in evens:taus=evens[coef];row['even_quotient_coefficients']=coef
      elif q['curve_kind']=='none':
       c,fs=s.factor_list(D);assert all(e%2==0 for f,e in fs)
       assert not s.sqrt(c).is_Rational
       taus=[]
      if taus is None:row['status']='unresolved_higher_genus_or_positive_rank'
      else:
       taus=list(taus)+zeros_of_removed(D)
       if not taus:row['status']='no_rational_discriminant_point'
       else:
        row['status']='finite_lift_audit';jobs.append((r['config'],r['elements'],ss,fr,ix,fi,qi,taus))
    else:row['status']='unresolved_nonlinear'
    statuses.append(row)
 with ProcessPoolExecutor(max_workers=4) as ex:rows=list(ex.map(lift_one,jobs,chunksize=4))
 failed={(x['orbit'],x['system'],x['factor']) for x in rows if not x['passed']}
 orbits={}
 for label in sorted({r['orbit'] for r in statuses}):
  cur=[r for r in statuses if r['orbit']==label]
  bad=[r for r in cur if r['status'].startswith('unresolved') or (r['orbit'],r['system'],r['factor']) in failed]
  orbits[label]={'factor_entries':len(cur),'unresolved_factor_entries':len(bad),'closed_given_verified_upstream_checks':not bad,'statuses':dict(collections.Counter(r['status'] for r in cur))}
 out.write_text(json.dumps({'finite_quotient_factor_entries_lifted':len(rows),'failed_lifting_entries':len(failed),'orbits':orbits,'factor_statuses':statuses,'lifts':rows},indent=2))
 print('Lifted',len(rows),'failed',len(failed));print(json.dumps(orbits,indent=1))
if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
