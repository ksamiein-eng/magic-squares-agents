"""Reconstruct every stored trigonometric line and discriminant from its plane factor.
This verifies identities and square classes, not completeness of rational points.
"""
from pathlib import Path
import sys, json, collections, math
import sympy as s
from audit_inputs import expr, T,U,V,TAU
I=s.I

def spectrum(F,a,b):
    P=s.Poly(F,a,b); da,db=P.degree(a),P.degree(b)
    z,w=s.symbols('z w'); data={}
    # Homogenize the half-angle substitution on the two circle coordinates.
    Q=s.Poly(s.expand(sum(c*(-I*(z-1))**i*(z+1)**(da-i)*(-I*(w-1))**j*(w+1)**(db-j) for (i,j),c in P.terms())),z,w)
    return {(s.Rational(2*i-da,2),s.Rational(2*j-db,2)):c for (i,j),c in Q.terms()}

def reconstruct(F,a,b,mat,A,B):
    assert isinstance(A,int) and A>0 and isinstance(B,int) and B>0
    S=spectrum(F,a,b); M=s.Matrix(mat); inv=M.inv()
    coords={point:tuple((s.Matrix(1,2,point)*inv)) for point in S}
    assert abs(M.det())==1
    assert all(x in (-A,0,A) for x,y in coords.values())
    es=[2*y/B for x,y in coords.values()]
    assert all(e.is_Integer for e in es) and len({int(e)%2 for e in es})==1
    N=max(abs(int(e)) for e in es); cs={-A:0,0:0,A:0}
    for point,c in S.items():
        x,y=coords[point];e=int(2*y/B)
        term=(1+I*TAU)**e if e>=0 else (1-I*TAU)**(-e)
        cs[x]+=c*term*(1+TAU**2)**((N-abs(e))//2)
    cs={x:s.expand(v) for x,v in cs.items()}
    assert s.expand(cs[-A]-s.conjugate(cs[A]))==0 and s.im(cs[0])==0
    p=s.expand(2*s.re(cs[A]));q=s.expand(-2*s.im(cs[A]));r=-cs[0]
    return p,q,r,s.expand(p*p+q*q-r*r)

def main(root,out):
    rows=[];issues=[];cached={};models={}
    for path in sorted((root/'repro/certs').glob('*.json')):
        doc=json.load(open(path))
        for ix,system in enumerate(doc.get('systems',[])):
            lookup={'x':T,'z':U,'w':V}
            a,b=[lookup[x] for x in system['projection']['plane']]
            for fi,fr in enumerate(system['factors']):
                if fr['type']!='linear_in_circle_point': continue
                F=expr(fr['poly']);A=fr['A'];M=fr['basis_M']
                for qi,qrec in enumerate(fr['quotients']):
                    B=qrec['B'];key=(str(F),str(a),str(b),str(M),A,B)
                    if key not in cached:cached[key]=reconstruct(F,a,b,M,A,B)
                    p,q,r,D=cached[key]
                    for var,x in zip(['p','q','r'],[p,q,r]): assert s.expand(x-expr(qrec['line'][var]))==0,(path.name,ix,fi,qi,var)
                    assert s.expand(D-expr(qrec['D(tau)']))==0
                    row={'orbit':doc['config'],'system':ix,'factor':fi,'quotient':qi,'B':B,'kind':qrec['curve_kind'],'used':bool(qrec.get('used')),'D':str(D),'basis_det':int(s.det(s.Matrix(M)))}
                    if 'D_squarefree' in qrec.get('curve',{}):
                        red=expr(qrec['curve']['D_squarefree']); quot=s.cancel(D/red)
                        num,den=s.fraction(quot)
                        cn,fn=s.factor_list(num);cd,fd=s.factor_list(den)
                        assert all(e%2==0 for f,e in fn+fd) and s.sqrt(cn/cd).is_Rational
                        assert s.gcd(s.Poly(red,TAU),s.Poly(s.diff(red,TAU),TAU)).degree()==0
                        square=s.sqrt(cn/cd)*s.prod(f**(e//2) for f,e in fn)/s.prod(f**(e//2) for f,e in fd)
                        row['square_factor']=str(square)
                        roots=s.polys.polytools.ground_roots(s.Poly(s.numer(square),TAU))
                        row['rational_zeros_removed']=[str(x) for x in roots]
                        row['squarefree_degree']=s.degree(red,TAU)
                        curve=qrec['curve']
                        if curve.get('complete'):
                            vals=curve['tau_values'];unique=set(vals)
                            for val in unique:
                                if val=='oo':continue
                                vv=expr(val); assert s.sqrt(red.subs(TAU,vv)).is_Rational
                            row['stored_complete_count']=len([x for x in vals if x!='oo'])+(2 if 'oo' in unique and s.degree(red,TAU)%2==0 else 1 if s.degree(red,TAU)%2 else 0)
                            row['torsion_order']=curve['torsion']
                            assert row['stored_complete_count']==curve['torsion']
                            models[str(curve['minimal_model'])]=curve['rank_bounds']
                    rows.append(row)
        if 'systems' in doc: print(path.stem,'quotients checked',sum(r['orbit']==doc['config'] for r in rows),flush=True)
    data={'passed_identity_checks':True,'total_quotient_records':len(rows),'unique_identity_inputs':len(cached),'kinds':dict(collections.Counter(r['kind'] for r in rows)),'squarefactor_zero_records':sum(bool(r.get('rational_zeros_removed')) for r in rows),'complete_models':models,'rows':rows,'scope':'No point-lifting completeness, genus-of-nonlinear-components, rank or global saturation conclusion is implied.'}
    out.write_text(json.dumps(data,indent=2,default=str));print({k:v for k,v in data.items() if k!='rows'})
if __name__=='__main__':main(Path(sys.argv[1]),Path(sys.argv[2]))
