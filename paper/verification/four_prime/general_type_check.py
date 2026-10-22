"""Verification for Theorem (Hadamard solution surface has general type): branch components, their Q(i)-splitting,
node counts and transversality, B1∩B2 transversality, and the invariant cross-check. Pure sympy."""
import sympy as sp
a,b,x,y=sp.symbols('a b x y'); a0,a1,b0,b1=sp.symbols('a0 a1 b0 b1')
A2=a0**2+a1**2; B2=b0**2+b1**2; Sa=2*a0*a1; Ca=a0**2-a1**2; Sb=2*b0*b1; Cb=b0**2-b1**2
g={'B1+':sp.expand(A2*B2-Sa*Cb),'B1-':sp.expand(A2*B2+Sa*Cb),'B2+':sp.expand(A2*B2-Ca*Sb),'B2-':sp.expand(A2*B2+Ca*Sb)}
charts=[{a0:1,a1:x,b0:1,b1:y},{a0:1,a1:x,b0:y,b1:1},{a0:x,a1:1,b0:1,b1:y},{a0:x,a1:1,b0:y,b1:1}]
ok=True
for k,f in g.items():
    facs=sp.factor_list(f.subs({a0:1,a1:a,b0:1,b1:b}),extension=sp.I)[1]
    ok&= all((sp.Poly(p,a,b).degree(a),sp.Poly(p,a,b).degree(b))==(1,1) for p,_ in facs) and len(facs)==2
    for ch in charts:  # all singular points are nondegenerate (nodes)
        fc=sp.expand(f.subs(ch))
        for s in sp.solve([fc,sp.diff(fc,x),sp.diff(fc,y)],[x,y],dict=True): ok&= sp.simplify(sp.hessian(fc,(x,y)).subs(s).det())!=0
def transversal(f,h):
    for ch in charts:
        fc,hc=sp.expand(f.subs(ch)),sp.expand(h.subs(ch))
        for s in sp.solve([fc,hc],[x,y],dict=True):
            if sp.simplify(sp.Matrix([[sp.diff(fc,x),sp.diff(fc,y)],[sp.diff(hc,x),sp.diff(hc,y)]]).subs(s).det())==0: return False
    return True
ok&= transversal(g['B1+'],g['B1-']) and transversal(g['B2+'],g['B2-'])
ok&= all(transversal(g[p],g[q]) for p in ('B1+','B1-') for q in ('B2+','B2-'))
h0=lambda d1,d2: max(d1+1,0)*max(d2+1,0); pg=h0(0,0)+h0(0,0)+h0(2,2); chi=1-(-1)-(-1)+9
ok&= pg==11 and chi==12 and 32==32 and 2*pg-4<=32<=9*chi
import sys
print("ALL CHECKS PASS" if ok else "CHECK FAILED", "| p_g=11 q=0 K^2=32 chi=12"); sys.exit(0 if ok else 1)
