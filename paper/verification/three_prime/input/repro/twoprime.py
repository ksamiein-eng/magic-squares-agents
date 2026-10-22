import sympy as sp, time, sys
from itertools import combinations, product
from math import gcd as igcd

t, u = sp.symbols('t u', real=True)

def Zpow(var, k):
    return (1+sp.I*var)**(2*k) if k>=0 else (1-sp.I*var)**(2*(-k))

def Etilde(k, j, k1, k2):
    # sin(k x + j z) * (1+t^2)^k1 (1+u^2)^k2, with e^{ix}=(1+it)^2/(1+t^2), e^{iz}=(1+iu)^2/(1+u^2)
    val = sp.im(sp.expand(Zpow(t,k)*Zpow(u,j)))
    return sp.expand(val*(1+t**2)**(k1-abs(k))*(1+u**2)**(k2-abs(j)))

def rational_roots(polyexpr, var):
    P = sp.Poly(polyexpr, var)
    if P.is_zero: return None
    roots=[]
    for fac,mult in sp.factor_list(P.as_expr(), var)[1]:
        fp = sp.Poly(fac, var)
        if fp.degree()==1:
            a,b = fp.all_coeffs()
            roots.append(sp.Rational(-b,a))
    return roots

def height(tv):
    # denominator of the circle point (1+it)^2/(1+t^2) in lowest terms
    p,q = sp.fraction(sp.Rational(tv)); p,q=int(p),int(q)
    N = p*p+q*q
    return N//2 if (p%2==1 and q%2==1) else N

def analyze(k1,k2,mp,npr, verbose=False):
    exprs = [(k1,k2),(k1,-k2),(mp,k2),(k1,npr)]
    E = [Etilde(k,j,k1,k2) for k,j in exprs]
    report = {'systems':0,'curve_components':[],'degenerate_sols':0,'rational_sols':[]}
    for r1,r4 in combinations(range(4),2):
        rest=[i for i in range(4) if i not in (r1,r4)]
        for r2 in rest:
            r3=[i for i in rest if i!=r2][0]
            for e2,e3 in product([1,-1],repeat=2):
                report['systems']+=1
                G1 = sp.expand(E[r1]-e2*E[r2]-e3*E[r3])
                G2 = sp.expand(E[r4]-e2*E[r2]+e3*E[r3])
                g = sp.gcd(G1,G2)
                if sp.Poly(g,t,u).total_degree()>0:
                    report['curve_components'].append(((r1,r4,r2,r3,e2,e3),sp.factor(g)))
                    G1=sp.cancel(G1/g); G2=sp.cancel(G2/g)   # continue with the rest
                R = sp.resultant(G1,G2,u)
                troots = rational_roots(R,t)
                if troots is None:
                    report['curve_components'].append(((r1,r4,r2,r3,e2,e3),'resultant identically zero'))
                    continue
                for t0 in set(troots):
                    h = sp.gcd(sp.Poly(G1.subs(t,t0),u), sp.Poly(G2.subs(t,t0),u))
                    uroots = rational_roots(h.as_expr(),u) or []
                    for u0 in set(uroots):
                        vals=[sp.Rational(e.subs({t:t0,u:u0})) for e in E]
                        absv=[abs(v) for v in vals]
                        if 0 in absv or len(set(absv))<4:
                            report['degenerate_sols']+=1
                        else:
                            report['rational_sols'].append((t0,u0,vals,height(t0),height(u0)))
    return report

if __name__=="__main__":
    k1,k2=int(sys.argv[1]),int(sys.argv[2])
    seen=set()
    for mp in range(-(k1-1),k1):
        for npr in range(-(k2-1),k2):
            if (-mp,-npr) in seen: continue
            seen.add((mp,npr))
            t0=time.time()
            rep=analyze(k1,k2,mp,npr)
            print(f"(k1,k2)=({k1},{k2}) config m'={mp}, n'={npr}: systems={rep['systems']}, "
                  f"curve components={len(rep['curve_components'])}, degenerate rational sols={rep['degenerate_sols']}, "
                  f"NONDEGENERATE RATIONAL SOLS={rep['rational_sols']}  [{time.time()-t0:.1f}s]")
            for c in rep['curve_components']: print("   component:",c)
