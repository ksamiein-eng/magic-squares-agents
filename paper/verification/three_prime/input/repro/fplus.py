import sympy as sp, itertools, time, sys
from sympy import I
from collections import Counter
t,u=sp.symbols('t u',real=True); Zs,Ws=sp.symbols('Zs Ws')
Zc=(1+I*t)**2; Zb=(1-I*t)**2; Wc=(1+I*u)**2; Wb=(1-I*u)**2
# common denominator (1+t^2)(1+u^2); numerators:
def zeta(mz,mw):
    num=1
    num*= Zc if mz==1 else (Zb if mz==-1 else (1+t**2))
    num*= Wc if mw==1 else (Wb if mw==-1 else (1+u**2))
    return sp.expand(num)
CONF={'F+1':[(1,1,1),(1,1,0),(1,0,1),(0,1,1)], 'F+2':[(1,1,-1),(1,1,0),(1,0,1),(0,1,1)]}
def curves(conf):
    xidx=[k for k,m in enumerate(conf) if m[0]==1]; nx=[k for k,m in enumerate(conf) if m[0]==0][0]
    Zeta={k:zeta(m[1],m[2]) for k,m in enumerate(conf)}
    out=[]
    for r1,r4 in itertools.combinations(range(4),2):
        rest=[k for k in range(4) if k not in (r1,r4)]
        for r2 in rest:
            r3=[k for k in rest if k!=r2][0]
            for e2,e3 in itertools.product([1,-1],repeat=2):
                roles={r1:1,r4:1,r2:1,r3:1}
                # relations as coefficient vectors on elements: Ra: E_r1 - e2 E_r2 - e3 E_r3 ; Rb: E_r4 - e2 E_r2 + e3 E_r3 ; Ra+Rb: E_r1+E_r4-2e2 E_r2 ; Ra-Rb: E_r1-E_r4-2e3 E_r3
                rels=[{r1:1,r2:-e2,r3:-e3},{r4:1,r2:-e2,r3:e3},{r1:1,r4:1,r2:-2*e2},{r1:1,r4:-1,r3:-2*e3}]
                hom=[R for R in rels if nx not in R][0]; inh=[R for R in rels if nx in R][0]
                A=sum(c*Zeta[k] for k,c in hom.items())
                Ap=sum(c*Zeta[k] for k,c in inh.items() if k!=nx); kappa=-inh[nx]   # Im(e^{ix} A') + inh[nx]*Im(ZW)=0
                ImAAp=sp.expand(sp.im(sp.expand(sp.conjugate(A)*Ap))); AA=sp.expand(sp.re(A)**2+sp.im(A)**2); ImZW=sp.expand(sp.im(Zeta[nx]))
                G=sp.expand(ImAAp**2 - kappa**2*AA*ImZW**2)
                out.append(((r1,r4,r2,r3,e2,e3),G,A,Ap,kappa))
    return out
def npoly_genus_tu(F):
    P=sp.Poly(F,t,u); d1,d2=P.degree(t),P.degree(u); tot=0
    for (i,j),c in P.terms(): tot+=c*(-I*(Zs-1))**i*(Zs+1)**(d1-i)*(-I*(Ws-1))**j*(Ws+1)**(d2-j)
    Q=sp.Poly(sp.expand(tot),Zs,Ws); pts=sorted(set((i,j) for (i,j),c in Q.terms()))
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in pts:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up)>=2 and cross(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    H=lo[:-1]+up[:-1]
    if len(H)<3: return 0,H
    def inside(a,b): return all(((H[(k+1)%len(H)][0]-H[k][0])*(b-H[k][1])-(H[(k+1)%len(H)][1]-H[k][1])*(a-H[k][0]))>0 for k in range(len(H)))
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    return sum(1 for a in range(min(xs),max(xs)+1) for b in range(min(ys),max(ys)+1) if inside(a,b)),H
if __name__=="__main__":
    name=sys.argv[1]; t0=time.time(); res=Counter(); detail={}
    for tag,G,A,Ap,kappa in curves(CONF[name]):
        fl=sp.factor_list(G)[1]
        facs=[]
        for f,k in fl:
            P=sp.Poly(f,t,u)
            if P.degree(t)==0 or P.degree(u)==0: continue
            g,H=npoly_genus_tu(f); facs.append(((P.degree(t),P.degree(u)),g,k))
        res[tuple(sorted(facs))]+=1; detail.setdefault(tuple(sorted(facs)),tag)
    print(f"{name}: factor structure of Gamma' over 48 systems  [(bidegree),Newton-genus,multiplicity]  [{time.time()-t0:.0f}s]")
    for k,v in res.most_common(): print(f"  {v:2d} systems e.g. {detail[k]}: {list(k)}")
