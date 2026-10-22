import sympy as sp, itertools, time, sys
from sympy import I
t,u=sp.symbols('t u')
Zc=(1+I*t)**2; Zbar=(1-I*t)**2; Wc=(1+I*u)**2; Wbar=(1-I*u)**2   # times 1/(1+t^2),1/(1+u^2)
# element -> (Gaussian numerator, needs which denominators) for zeta_E with x removed
# D2: E0=x+z+w -> ZW ; E1=x-z-w -> Zbar Wbar ; E2=x+z -> Z ; E3=x+w -> W
def zetas(conf):
    out=[]
    for m in conf:
        assert m[0]==1
        num=1; dz=0; dw=0
        if m[1]==1: num*=Zc; dz=1
        elif m[1]==-1: num*=Zbar; dz=1
        if m[2]==1: num*=Wc; dw=1
        elif m[2]==-1: num*=Wbar; dw=1
        # bring to common denominator (1+t^2)(1+u^2)
        num=num*(1+t**2)**(1-dz)*(1+u**2)**(1-dw)
        out.append(sp.expand(num))
    return out
CONF={'D2':[(1,1,1),(1,-1,-1),(1,1,0),(1,0,1)], 'D3':[(1,1,-1),(1,-1,1),(1,1,0),(1,0,1)], 'D4':[(1,1,-1),(1,-1,-1),(1,1,0),(1,0,1)]}

def gamma_curves(conf):
    Zs=zetas(conf); curves={}
    for r1,r4 in itertools.combinations(range(4),2):
        rest=[k for k in range(4) if k not in (r1,r4)]
        for r2 in rest:
            r3=[k for k in rest if k!=r2][0]
            for e2,e3 in itertools.product([1,-1],repeat=2):
                A=Zs[r1]-e2*Zs[r2]-e3*Zs[r3]; B=Zs[r4]-e2*Zs[r2]+e3*Zs[r3]
                L=sp.expand(sp.im(sp.expand(A*sp.conjugate(B))))  # t,u real
                fl=sp.factor_list(L)
                for f,_ in fl[1]:
                    P=sp.Poly(f,t,u)
                    if P.degree(t)==0 or P.degree(u)==0: continue
                    if P.total_degree()<=2: continue   # lines/conics: handle separately (degenerate loci)
                    key=str(f); curves.setdefault(key,[]).append(((r1,r4,r2,r3,e2,e3),A,B))
    return curves

def sing_points(F):
    """singular points of F(t,u)=0 in P^1xP^1: returns list of (chart, point, multiplicity, ordinary?)"""
    res=[]
    for ct,cu in itertools.product([0,1],repeat=2):
        G=F
        if ct: G=sp.expand(G.subs(t,1/t)*t**sp.Poly(F,t,u).degree(t))
        if cu: G=sp.expand(G.subs(u,1/u)*u**sp.Poly(F,t,u).degree(u))
        gb=sp.groebner([G,sp.diff(G,t),sp.diff(G,u)],t,u,order='lex')
        if list(gb)==[1]: continue
        sols=sp.solve(list(gb),[t,u],dict=True)
        for s in sols:
            t0,u0=s[t],s[u]
            if ct and t0==0 or cu and u0==0: pass  # at infinity in this chart, fine
            if not ct and not cu: pass
            # skip points already counted in another chart (points with t0!=0 in chart ct=1 were affine)
            if ct and t0!=0: continue
            if cu and u0!=0: continue
            # multiplicity: lowest total degree of Taylor expansion
            a,b=sp.symbols('a b')
            T=sp.Poly(sp.expand(G.subs({t:t0+a,u:u0+b})),a,b)
            m=min(sum(k) for k,_ in T.terms())
            lead=sum(c*a**k[0]*b**k[1] for k,c in T.terms() if sum(k)==m)
            disc_ok = sp.discriminant(sp.Poly(lead.subs(b,1),a))!=0 if m>=2 else None
            res.append(((ct,cu),(t0,u0),m,disc_ok))
    return res

if __name__=="__main__":
    name=sys.argv[1]; t0=time.time()
    curves=gamma_curves(CONF[name])
    print(f"{name}: {len(curves)} distinct nontrivial Gamma factors from 48 systems [{time.time()-t0:.0f}s]")
    for key,systems in curves.items():
        F=sp.sympify(key); P=sp.Poly(F,t,u); d1,d2=P.degree(t),P.degree(u)
        pa=(d1-1)*(d2-1)
        try:
            sp_=sing_points(F); delta=0; note=''
            for ch,pt,m,ok in sp_:
                if ok: delta+=m*(m-1)//2
                else: note+=f' non-ordinary({m}) at {pt};'
            print(f"  bideg ({d1},{d2}), p_a={pa}, singular pts {len(sp_)} (delta>={delta}) -> genus <= {pa-delta}{note}  [{len(systems)} systems, e.g. {systems[0][0]}]")
        except Exception as e:
            print(f"  bideg ({d1},{d2}), p_a={pa}: singularity computation failed: {e}")
