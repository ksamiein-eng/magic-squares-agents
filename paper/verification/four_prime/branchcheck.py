import sympy as sp, sys
a,b,x,y=sp.symbols('a b x y'); a0,a1,b0,b1=sp.symbols('a0 a1 b0 b1')
sa,ca=2*a/(1+a**2),(1-a**2)/(1+a**2); sb,cb=2*b/(1+b**2),(1-b**2)/(1+b**2)
SC=sa*cb; CS=ca*sb          # sin a cos b, cos a sin b
def comps(F):   # numerators of F∓1, bidegree (2,2)
    num,den=sp.fraction(sp.together(F)); return [sp.expand(num-den),sp.expand(num+den)]
def homog(f): return sp.expand(f.subs({a:a1/a0,b:b1/b0})*a0**2*b0**2)
CH=[{a0:1,a1:x,b0:1,b1:y},{a0:1,a1:x,b0:y,b1:1},{a0:x,a1:1,b0:1,b1:y},{a0:x,a1:1,b0:y,b1:1}]
def sings(f):
    fh=homog(f); out=[]
    for ch in CH:
        fc=sp.expand(fh.subs(ch))
        G=sp.groebner([fc,sp.diff(fc,x),sp.diff(fc,y)],x,y,order='lex')
        if list(G)==[1]: continue
        for s in sp.solve(list(G),[x,y],dict=True):
            out.append('node' if sp.simplify(sp.hessian(fc,(x,y)).subs(s).det())!=0 else 'WORSE')
    return out
def transv(f,h):
    fh,hh=homog(f),homog(h)
    for ch in CH:
        fc,hc=sp.expand(fh.subs(ch)),sp.expand(hh.subs(ch))
        if sp.Poly(fc,x,y).total_degree()>0 and sp.Poly(hc,x,y).total_degree()>0 and sp.gcd(sp.Poly(fc,x,y),sp.Poly(hc,x,y)).total_degree()>0: return 'COMMON'
        G=sp.groebner([fc,hc],x,y,order='lex')
        if list(G)==[1]: continue
        for s in sp.solve(list(G),[x,y],dict=True):
            if sp.simplify(sp.Matrix([[sp.diff(fc,x),sp.diff(fc,y)],[sp.diff(hc,x),sp.diff(hc,y)]]).subs(s).det())==0: return False
    return True
TYPES={'6':(2*CS,2*SC),'2':(2*CS,3*CS-SC),'4':(2*CS,SC+3*CS)}
t=sys.argv[1]; F1,F2=TYPES[t]
c1,c2=comps(F1),comps(F2)
print(f"type {t}: sin u = {sp.simplify(F1*(1+a**2)*(1+b**2))}/den, sin v = {sp.simplify(F2*(1+a**2)*(1+b**2))}/den")
print("  bidegrees:",[(sp.Poly(c,a,b).degree(a),sp.Poly(c,a,b).degree(b)) for c in c1+c2])
print("  squarefree:",[sp.gcd(sp.Poly(c,a,b),sp.Poly(sp.diff(c,a),a,b)).total_degree()==0 and sp.gcd(sp.Poly(c,a,b),sp.Poly(sp.diff(c,b),a,b)).total_degree()==0 for c in c1+c2])
print("  Q(i)-irreducible factors per component:",[len(sp.factor_list(c,extension=sp.I)[1]) for c in c1+c2])
st=[sings(c) for c in c1+c2]; print("  singular points per component:",st)
tr={'B1+∩B1-':transv(*c1),'B2+∩B2-':transv(*c2)}
for i_,p in enumerate(c1):
    for j_,q in enumerate(c2): tr[f'B1{"+-"[i_]}∩B2{"+-"[j_]}']=transv(p,q)
print("  transversality:",tr)
ok=all(d==(2,2) for d in [(sp.Poly(c,a,b).degree(a),sp.Poly(c,a,b).degree(b)) for c in c1+c2]) and all(set(s)<={'node'} for s in st) and all(v is True for v in tr.values())
print("  =>","GENERAL TYPE, p_g=11, q=0, K^2=32 (only A1 singularities)" if ok else "needs finer analysis")
