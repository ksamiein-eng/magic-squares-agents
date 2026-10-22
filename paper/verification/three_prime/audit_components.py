"""Exact generic-component certificates with explicit exceptional fibers.
Uses true rational functions (never compares independently stripped numerators).
"""
from pathlib import Path
import sys,json,collections,itertools
from concurrent.futures import ProcessPoolExecutor
import sympy as s
from audit_inputs import expr,VS,T,U,V,numerator
from audit_fibers import witnesses

def roots_of_denoms(polys,var):
 ds=[]
 for p in polys:
  cs=p.all_coeffs() if isinstance(p,s.Poly) else [p]
  for c in cs:
   d=s.denom(s.cancel(c))
   if d!=1: ds.append(s.Poly(d,var))
 out=set()
 for d in ds: out.update(s.polys.polytools.ground_roots(d))
 return out,ds

def task(inp):
 name,vecs,ss,fr,ix,fi=inp
 lookup={'x':T,'z':U,'w':V}; a,b=[lookup[k] for k in ss['projection']['plane']];v=lookup[ss['projection']['eliminated']]
 f=expr(fr['poly']);P=s.Poly(f,a,b)
 bound,free=(b,a) if P.degree(b)==1 else (a,b)
 lead,constant=s.Poly(f,bound).all_coeffs();sub=s.cancel(-constant/lead); K=s.QQ.frac_field(free)
 common=expr(ss['common_factor']) if ss['common_factor'] else 1
 F=s.Poly(s.cancel(s.cancel(expr(ss['G1'])/common).subs(bound,sub)),v,domain=K)
 G=s.Poly(s.cancel(s.cancel(expr(ss['G2'])/common).subs(bound,sub)),v,domain=K)
 E=[s.Poly(s.cancel(numerator(m).subs(bound,sub)),v,domain=K) for m in vecs]
 rec={'orbit':name,'system':ix,'factor_index':fi,'type':fr['type'],'F':str(f),'substitution':{str(bound):str(sub)},'free_variable':str(free),'witnesses':[]}
 if F.is_zero and G.is_zero:
  ww=next((tag for tag,p in witnesses([p.as_expr() for p in E]) if s.cancel(p)==0),None)
  assert ww,(name,ix,'two zero polynomials without degeneracy')
  rec['whole_branch_witness']=ww; pols=E
 else:
  if G.is_zero:
   A=s.Poly(1/F.LC(),v,domain=K);B=s.Poly(0,v,domain=K);h=F.monic()
  elif F.is_zero:
   B=s.Poly(1/G.LC(),v,domain=K);A=s.Poly(0,v,domain=K);h=G.monic()
  else:A,B,h=F.gcdex(G)
  assert A*F+B*G==h
  W=s.Poly(1,v,domain=K)
  for fp,mul in h.factor_list()[1]:
   if fp.degree()==0:continue
   candidates=[(tag,s.Poly(x,v,domain=K)) for tag,x in witnesses([p.as_expr() for p in E])]
   pair=next(((tag,p) for tag,p in candidates if p.rem(fp).is_zero),None)
   assert pair,(name,ix,'generic degeneracy failed',str(fp.as_expr()))
   tag,wp=pair;W*=wp**mul;rec['witnesses'].append({'factor':str(fp.as_expr()),'identity':tag,'multiplicity':mul})
  quotient,rem=W.div(h);assert rem.is_zero
  rec.update({'bezout_A':str(A.as_expr()),'bezout_B':str(B.as_expr()),'gcd':str(h.as_expr()),'degeneracy_product':str(W.as_expr()),'quotient':str(quotient.as_expr())})
  pols=[F,G,A,B,h,W,quotient]+E
 exc,den=roots_of_denoms(pols+[sub],free)
 exc.update(s.polys.polytools.ground_roots(s.Poly(lead,free)))
 rec['exceptional_values']=sorted(str(x) for x in exc)
 rec['exceptional_values_are_audited_torsion_fibers']=exc<={s.Integer(-1),s.Integer(0),s.Integer(1)}
 return rec

def linear(root):
 out=[]
 for name in ['F-1','F-3']:
  r=json.load(open(root/'repro/certs'/f'{name}.json'))
  for ix,ss in enumerate(r['systems']):
   for fi,fr in enumerate(ss['factors']):
    if 'exact_verification' not in fr:continue
    F=expr(fr['poly']);P=s.Poly(F,U,domain=s.QQ.frac_field(T))
    G1=s.Poly(expr(ss['G1']),V);G2=s.Poly(expr(ss['G2']),V)
    aa,bb,cc=G1.all_coeffs();dd,ee,ff=G2.all_coeffs()
    A=s.expand(aa*ee-dd*bb);B=s.expand(aa*ff-dd*cc)
    assert s.expand(aa*G2.as_expr()-dd*G1.as_expr()-(A*V+B))==0
    rr=expr(fr['exact_verification']['gcd_root_v'])
    def remainder(x):return s.Poly(s.cancel(x),U,domain=s.QQ.frac_field(T)).rem(P)
    assert not remainder(A).is_zero and remainder(A*rr+B).is_zero
    line=fr['exact_verification']['lines_vanishing_identically'][0]['index']
    E=numerator(r['elements'][line]);assert remainder(E.subs(V,rr)).is_zero
    norm=s.resultant(A,F,U);assert norm!=0
    exc=set(s.polys.polytools.ground_roots(s.Poly(s.numer(s.cancel(norm)),T)))
    exc2,ds=roots_of_denoms([rr],T)
    exc|=exc2
    # In the polynomial remainder certificate, denominators can only add T-values;
    # collect coefficients of the actual divisions, not just the proposed root.
    for pol in [A*rr+B,E.subs(V,rr)]:
     qp,rem=s.Poly(s.cancel(pol),U,domain=s.QQ.frac_field(T)).div(P);assert rem.is_zero
     er,ds=roots_of_denoms([qp],T);exc|=er
    assert exc<={s.Integer(-1),s.Integer(0),s.Integer(1)},(name,ix,exc)
    out.append({'orbit':name,'system':ix,'factor_index':fi,'F':str(F),'linear_coefficient_A':str(A),'linear_constant_B':str(B),'root':str(rr),'vanishing_line':line,'exceptional_t':sorted(map(str,exc)),'norm':str(s.factor(norm)),'passed':True})
 return out

def main(root,out):
 jobs=[]
 for f in sorted((root/'repro/certs').glob('*.json')):
  r=json.load(open(f))
  for ix,ss in enumerate(r.get('systems',[])):
   for fi,fr in enumerate(ss['factors']):
    if fr['type'] in ['degenerate_component','isolated_line_points']:
     jobs.append((r['config'],r['elements'],ss,fr,ix,fi))
 with ProcessPoolExecutor(max_workers=4) as ex: rows=list(ex.map(task,jobs,chunksize=4))
 linearrows=linear(root)
 data={'generic_components':len(rows),'all_exceptional_values_are_audited_torsion_fibers':all(r['exceptional_values_are_audited_torsion_fibers'] for r in rows),'linear_relation_components':len(linearrows),'rows':rows,'linear_relation_rows':linearrows}
 out.write_text(json.dumps(data,indent=2));print({k:v for k,v in data.items() if not k.endswith('rows')})
if __name__=='__main__': main(Path(sys.argv[1]),Path(sys.argv[2]))
