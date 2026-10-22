import sympy as sp, sys, itertools
a,b,x,y=sp.symbols('a b x y'); a0,a1,b0,b1=sp.symbols('a0 a1 b0 b1')
sa,ca=2*a/(1+a**2),(1-a**2)/(1+a**2); sb,cb=2*b/(1+b**2),(1-b**2)/(1+b**2); SC=sa*cb; CS=ca*sb
def comps(F): num,den=sp.fraction(sp.together(F)); return [sp.expand(num-den),sp.expand(num+den)]
def homog(f): return sp.expand(f.subs({a:a1/a0,b:b1/b0})*a0**2*b0**2)
CH=[{a0:1,a1:x,b0:1,b1:y},{a0:1,a1:x,b0:y,b1:1},{a0:x,a1:1,b0:1,b1:y},{a0:x,a1:1,b0:y,b1:1}]
TYPES={'6':(2*CS,2*SC),'2':(2*CS,3*CS-SC),'4':(2*CS,SC+3*CS)}
t=sys.argv[1]; F1,F2=TYPES[t]; C=comps(F1)+comps(F2); names=['B1+','B1-','B2+','B2-']
H=[homog(c) for c in C]
# collect all intersection points of all pairs, as projective points, with local intersection multiplicity
def proj_pt(ch,s):  # return normalized ((a0,a1),(b0,b1))
    vals={k:(v.subs(s) if hasattr(v,'subs') else v) for k,v in ch.items()}
    A=(vals[a0],vals[a1]); B=(vals[b0],vals[b1])
    A=(1,sp.nsimplify(A[1]/A[0])) if A[0]!=0 else (0,1); B=(1,sp.nsimplify(B[1]/B[0])) if B[0]!=0 else (0,1)
    return (A,B)
def mult_at(fc,hc,s):   # intersection multiplicity via resultant order: use local Jacobian rank then higher contact
    J=sp.Matrix([[sp.diff(fc,x),sp.diff(fc,y)],[sp.diff(hc,x),sp.diff(hc,y)]]).subs(s)
    if sp.simplify(J.det())!=0: return 1
    # tangency: compute contact order by restricting h to a local parametrization of f (both smooth): use resultant in y and order of root in x after shifting
    sx,sy=s[x],s[y]
    R=sp.Poly(sp.resultant(fc,hc,y),x)
    k=0; Rr=R
    while Rr.eval(sx)==0 and k<8: Rr=sp.Poly(sp.quo(Rr.as_expr(),x-sx),x); k+=1
    return k
pts={}
for i_,j_ in itertools.combinations(range(4),2):
    for ch in CH:
        fc,hc=sp.expand(H[i_].subs(ch)),sp.expand(H[j_].subs(ch))
        G=sp.groebner([fc,hc],x,y,order='lex')
        if list(G)==[1]: continue
        for s in sp.solve(list(G),[x,y],dict=True):
            p=proj_pt(ch,s); m=mult_at(fc,hc,s)
            pts.setdefault(p,{})[(names[i_],names[j_])]=m
print(f"type {t}: sin u = {sp.simplify(F1*(1+a**2)*(1+b**2))}/den, sin v = {sp.simplify(F2*(1+a**2)*(1+b**2))}/den")
triple=[p for p,d in pts.items() if len({c for pair in d for c in pair})>=3]
tang=[(p,d) for p,d in pts.items() if any(m>1 for m in d.values())]
print(f"  distinct intersection points: {len(pts)}; triple points: {len(triple)}; tangency points: {len(tang)}")
for p,d in tang: print("    tangency at (a,b)=",(p[0][1] if p[0][0] else 'inf',p[1][1] if p[1][0] else 'inf'),":",{k:v for k,v in d.items()})
# singularities of components (smooth?) 
def smooth(f):
    fh=homog(f)
    for ch in CH:
        fc=sp.expand(fh.subs(ch))
        if list(sp.groebner([fc,sp.diff(fc,x),sp.diff(fc,y)],x,y,order='lex'))!=[1]: return False
    return True
sm=[smooth(c) for c in C]; print("  components smooth:",sm)
canon = all(sm) and not triple
print("  =>","all cover singularities are A_k (canonical): GENERAL TYPE, p_g=11, q=0, K^2=32" if canon else "triple point or singular component: needs case analysis")
