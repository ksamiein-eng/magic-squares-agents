"""verify_hadamard_types.py [I|II|III|IV|all]
Checks every hypothesis of Theorem (All Hadamard solution surfaces have general type) for one branch-pair type:
  * four branch components of bidegree (2,2), reduced, no common components
  * every singular point of a component is an ordinary node (nondegenerate Hessian), in all four charts
  * no point lies on three components; nodes of B1 lie off B2 and conversely
  * every B1∩B2 point is transversal or a simple tangency (finite contact, both components smooth there)
Exit status 0 iff all hold. Pure sympy."""
import sympy as sp, sys, itertools
a,b,x,y=sp.symbols('a b x y'); a0,a1,b0,b1=sp.symbols('a0 a1 b0 b1')
sa,ca=2*a/(1+a**2),(1-a**2)/(1+a**2); sb,cb=2*b/(1+b**2),(1-b**2)/(1+b**2); SC=sa*cb; CS=ca*sb
TYPES={'I':(SC,CS),'II':(2*CS,2*SC),'III':(2*CS,3*CS-SC),'IV':(2*CS,SC+3*CS)}
CH=[{a0:1,a1:x,b0:1,b1:y},{a0:1,a1:x,b0:y,b1:1},{a0:x,a1:1,b0:1,b1:y},{a0:x,a1:1,b0:y,b1:1}]
def comps(F): num,den=sp.fraction(sp.together(F)); return [sp.expand(num-den),sp.expand(num+den)]
def homog(f): return sp.expand(f.subs({a:a1/a0,b:b1/b0})*a0**2*b0**2)
def ppt(ch,s):
    v={k:(w.subs(s) if hasattr(w,'subs') else w) for k,w in ch.items()}
    A=('inf' if v[a0]==0 else sp.nsimplify(v[a1]/v[a0])); B=('inf' if v[b0]==0 else sp.nsimplify(v[b1]/v[b0])); return (A,B)
def on(fh,pt):
    A,B=pt; sub={a0:(0 if A=='inf' else 1),a1:(1 if A=='inf' else A),b0:(0 if B=='inf' else 1),b1:(1 if B=='inf' else B)}
    return sp.simplify(fh.subs(sub))==0
def run(t):
    F1,F2=TYPES[t]; C=comps(F1)+comps(F2); H=[homog(c) for c in C]; names=['B1+','B1-','B2+','B2-']; ok=True; notes=[]
    # bidegree, reduced, no common components
    for c in C:
        P=sp.Poly(c,a,b); ok&=(P.degree(a),P.degree(b))==(2,2)
        ok&= sp.gcd(P,sp.Poly(sp.diff(c,a),a,b)).total_degree()==0 or sp.gcd(P,sp.Poly(sp.diff(c,b),a,b)).total_degree()==0
    for i,j in itertools.combinations(range(4),2):
        ok&= sp.gcd(sp.Poly(C[i],a,b),sp.Poly(C[j],a,b)).total_degree()==0
    # component singularities: all nodes
    sing={n:{} for n in names}
    for idx,(n,fh) in enumerate(zip(names,H)):
        for ch in CH:
            fc=sp.expand(fh.subs(ch)); G=sp.groebner([fc,sp.diff(fc,x),sp.diff(fc,y)],x,y,order='lex')
            if list(G)==[1]: continue
            for s in sp.solve(list(G),[x,y],dict=True):
                node=sp.simplify(sp.hessian(fc,(x,y)).subs(s).det())!=0; sing[n][ppt(ch,s)]=node
        ok&= all(sing[n].values()); notes.append(f"{n}: {len(sing[n])} singular pt(s), all nodes={all(sing[n].values())}")
    # nodes off the other divisor
    for n in ('B1+','B1-'):
        for p in sing[n]: ok&= not (on(H[2],p) or on(H[3],p))
    for n in ('B2+','B2-'):
        for p in sing[n]: ok&= not (on(H[0],p) or on(H[1],p))
    # pairwise intersections: transversal or simple tangency; collect for triple points
    pts={}; tang=0; trans=0
    for i,j in itertools.combinations(range(4),2):
        for ch in CH:
            fc,hc=sp.expand(H[i].subs(ch)),sp.expand(H[j].subs(ch)); G=sp.groebner([fc,hc],x,y,order='lex')
            if list(G)==[1]: continue
            for s in sp.solve(list(G),[x,y],dict=True):
                p=ppt(ch,s); pts.setdefault(p,set()).update({names[i],names[j]})
                J=sp.Matrix([[sp.diff(fc,x),sp.diff(fc,y)],[sp.diff(hc,x),sp.diff(hc,y)]]).subs(s)
                if sp.simplify(J.det())!=0: trans+=1
                else:
                    # simple tangency: both smooth here and contact order exactly 2. The contact order is read from the
                    # multiplicity of x=s[x] as a root of Res_y(f,h), which sums the intersection multiplicities of ALL
                    # intersection points sharing this x-coordinate; this can only over-count, so k==2 at a non-transversal
                    # point certifies a simple tangency (never under-certifies). A failure here would be conservative.
                    gf=[sp.diff(fc,x).subs(s),sp.diff(fc,y).subs(s)]; gh=[sp.diff(hc,x).subs(s),sp.diff(hc,y).subs(s)]
                    smooth_both=any(v!=0 for v in gf) and any(v!=0 for v in gh)
                    R=sp.Poly(sp.resultant(fc,hc,y),x); k=0; Rr=R
                    while Rr.degree()>=0 and Rr.eval(s[x])==0 and k<6: Rr=sp.Poly(sp.quo(Rr.as_expr(),x-s[x]),x); k+=1
                    ok&= smooth_both and k==2; tang+=1
    triple=[p for p,S in pts.items() if len(S)>=3]; ok&= not triple
    print(f"type {t}: {' | '.join(notes)} | intersections: {trans} transversal, {tang} simple tangencies, triple points {len(triple)} | {'OK' if ok else 'FAIL'}")
    return ok
if __name__=="__main__":
    which=sys.argv[1] if len(sys.argv)>1 else 'all'
    res=[run(t) for t in (TYPES if which=='all' else [which])]
    print("ALL HYPOTHESES OF THEOREM (general type) VERIFIED" if all(res) else "FAILURE"); sys.exit(0 if all(res) else 1)
