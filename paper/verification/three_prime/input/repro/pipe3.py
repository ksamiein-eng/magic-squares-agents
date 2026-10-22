import sympy as sp, itertools, time, sys
import cypari2
pari=cypari2.Pari(); pari.allocatemem(10**9)
exec(open('/tmp/tp/setup.py').read())
tau=sp.symbols('tau',real=True); rho=sp.symbols('rho',positive=True)
ANG={t:'x',u:'z',v:'w'}; I=sp.I

def rational_roots(expr,var):
    P=sp.Poly(expr,var)
    if P.is_zero: return None
    out=[]
    for f,_ in sp.factor_list(P.as_expr(),var)[1]:
        fp=sp.Poly(f,var)
        if fp.degree()==1:
            a,b=fp.all_coeffs(); out.append(sp.Rational(-b,a))
    return out
def to_pari(expr): return pari(str(sp.expand(expr)).replace('**','^').replace('tau','x'))

def support(F,a,b):
    """frequency support of F(a,b) as trig poly: returns dict {(m,n):coef} with m,n in (1/2)Z, via t=tan(x/2)."""
    P=sp.Poly(F,a,b); d1,d2=P.degree(a),P.degree(b)
    z1,z2=sp.symbols('z1 z2')
    tot=0
    for (i,j),c in P.terms():
        tot+= c*(-I*(z1-1))**i*(z1+1)**(d1-i)*(-I*(z2-1))**j*(z2+1)**(d2-j)
    Q=sp.Poly(sp.expand(tot),z1,z2)
    return {(i-sp.Rational(d1,2),j-sp.Rational(d2,2)):c for (i,j),c in Q.terms()}

MATS=[sp.Matrix(2,2,m) for m in itertools.product(range(-2,3),repeat=4) if sp.Matrix(2,2,m).det()!=0]
MATS.sort(key=lambda M:(abs(M.det()),sum(abs(e) for e in M)))

def find_linear_basis(S):
    """find M with (psi,phi)=M(x,z) s.t. F is linear in e^{iA psi} (A integer>0) and phi-freqs all integer or all half-integer."""
    pts=list(S.keys())
    for M in MATS:
        Minv=M.inv()
        new=[ (sp.Matrix([[m,n]])*Minv) for m,n in pts]
        mp=[row[0] for row in new]; npp=[row[1] for row in new]
        nz=[abs(x) for x in mp if x!=0]
        if not nz: continue
        A=nz[0]
        if not A.is_integer or any(abs(x) not in (0,A) for x in mp): continue
        fr=set((2*x)%2 for x in npp)
        if len(fr)!=1: continue
        return M,int(A),dict(zip(pts,zip(mp,npp)))
    return None

def valid_Bs(coords):
    from math import gcd
    es=[int(2*n) for m,n in coords.values()]
    B0=0
    for e in es: B0=gcd(B0,abs(e))
    if B0==0: return []
    return [B for B in range(B0,0,-1) if B0%B==0 and len(set((e//B)%2 for e in es))==1]
def discriminant(S,M,A,coords,B=None):
    """F = sum_k c_k(phi) e^{ikA psi}; returns (D(tau),p,q,r,B) with tau=tan(B*phi/2)."""
    Bs=valid_Bs(coords)
    if not Bs: return None
    if B is None: B=Bs[0]
    if B not in Bs: return None
    es=[int(2*n) for m,n in coords.values()]
    N=max(abs(e)//B for e in es)
    c={-1:0,0:0,1:0}
    for (m,n),coef in S.items():
        mp,np_=coords[(m,n)]; k=int(mp/A) if mp!=0 else 0
        e=int(2*np_)//B
        term=(1+I*tau)**e if e>=0 else (1-I*tau)**(-e)
        term=term*rho**(N-abs(e))
        c[k]+=coef*term
    def realify(expr):
        expr=sp.expand(expr).subs(rho**2,1+tau**2); expr=sp.expand(expr)
        expr=sp.expand(expr.replace(lambda e: e.is_Pow and e.base==rho, lambda e: (1+tau**2)**(e.exp/2) if e.exp%2==0 else e))
        return expr
    c1=realify(c[1]); c0=realify(c[0])
    if c1.has(rho) or c0.has(rho): return None
    P1=sp.Poly(c1,tau); P0=sp.Poly(c0,tau)
    p=sum(2*sp.re(co)*tau**k[0] for k,co in P1.terms()); q=sum(-2*sp.im(co)*tau**k[0] for k,co in P1.terms())
    r=sum(-sp.re(co)*tau**k[0] for k,co in P0.terms())
    if any(sp.im(co)!=0 for k,co in P0.terms()): return None
    D=sp.Poly(sp.expand(p**2+q**2-r**2),tau)
    return D,p,q,r,B

def quartic_points(Dp,H):
    if Dp.is_zero: return ('zero',[],None)
    fl=sp.factor_list(Dp.as_expr()); red=fl[0]
    for f,m in fl[1]: red*=f**(m%2)
    Dred=sp.Poly(sp.expand(red),tau); d=Dred.degree()
    if d==0:
        cst=Dred.all_coeffs()[0]
        return ('genus0',None,{'D':str(Dred.as_expr())}) if (cst>0 and sp.sqrt(cst).is_rational) else ('none',[],{'D':str(Dred.as_expr())})
    pol=to_pari(Dred.as_expr())
    pts=pari.hyperellratpoints(pol,H) if d>=2 else pari.hyperellratpoints(pol*pari('x^0'),H)
    taus=[]
    for P in pts:
        P=str(P).strip('[]').split(',')
        if len(P)==2: taus.append(sp.Rational(P[0]))
        else:
            x,y,zz=[sp.Rational(w) for w in P]; taus.append(sp.oo if zz==0 else x/zz)
    lc=Dred.LC()
    if d%2==0 and lc>0 and sp.sqrt(lc).is_rational: taus+=[sp.oo]
    if d<=2: return ('genus0',taus,{'D':str(Dred.as_expr())})
    if d in (3,4):
        Ew=pari.ellinit(pari.ellfromeqn(pari('y^2')-pol)); rk=pari.ellrank(Ew); tors=int(pari.elltors(Ew)[0])
        rk=(int(rk[0]),int(rk[1]))
        # number of rational points on the quartic (projective): affine ones + points at infinity (2 if lc square)
        ninf= 2 if (d==4 and lc>0 and sp.sqrt(lc).is_rational) else (1 if d==3 else 0)
        npts=len([x for x in taus if x!=sp.oo])+ninf
        complete=(rk==(0,0) and (npts==tors or npts==0))
        return ('genus1',taus,{'D':str(Dred.as_expr()),'rank':rk,'torsion':tors,'npts':npts,'complete':complete})
    return ('genus>=2',taus,{'D':str(Dred.as_expr()),'genus':(d-1)//2 if d%2 else (d-2)//2,'npts':len(taus)})

def lift(F,G1,G2,Es,taus,M,a,b,elim,B=1):
    """phi = M[1,0]*theta_a + M[1,1]*theta_b ; tan(phi/2)=tau0 -> H(a,b)=0 ; solve with F."""
    sols=[]
    Pa=(1+I*a)**(2*M[1,0]) if M[1,0]>=0 else (1-I*a)**(-2*M[1,0])
    Pb=(1+I*b)**(2*M[1,1]) if M[1,1]>=0 else (1-I*b)**(-2*M[1,1])
    P=sp.expand((Pa*Pb)**B)
    for ta in set(taus):
        Q0=-1 if ta==sp.oo else (1+I*ta)**2
        H=sp.expand(sp.im(sp.expand(P*sp.conjugate(Q0))))
        if H==0: continue
        R=sp.resultant(F,H,b)
        if R==0:
            g=sp.gcd(F,H); Fq=sp.cancel(F/g); R=sp.resultant(Fq,H,b) if Fq!=1 else 0
            sols.append(({'note':'F shares component with phi=const'},None)); 
            if R==0: continue
        for a0 in set(rational_roots(R,a) or []):
            h=sp.gcd(sp.Poly(F.subs(a,a0),b),sp.Poly(H.subs(a,a0),b))
            for b0 in set(rational_roots(h.as_expr(),b) or []):
                hv=sp.gcd(sp.Poly(G1.subs({a:a0,b:b0}),elim),sp.Poly(G2.subs({a:a0,b:b0}),elim))
                for e0 in set(rational_roots(hv.as_expr(),elim) or []):
                    pt={a:a0,b:b0,elim:e0}; vals=[sp.Rational(e.subs(pt)) for e in Es]; ab=[abs(x) for x in vals]
                    if 0 not in ab and len(set(ab))==4: sols.append((pt,vals))
    return sols

def component_degenerate(F,G1,G2,Es,a,b,elim):
    """F linear in b (or a): parametrize and check identically |E_i|=|E_j| or E_i=0 on each v-branch."""
    P=sp.Poly(F,a,b)
    if P.degree(b)==1:
        co=P.all_coeffs() if False else None
        c1=sp.Poly(F,b).all_coeffs(); sol={b:sp.cancel(-c1[1]/c1[0])}; free=a
    elif P.degree(a)==1:
        c1=sp.Poly(F,a).all_coeffs(); sol={a:sp.cancel(-c1[1]/c1[0])}; free=b
    else: return None
    g1=sp.numer(sp.together(G1.subs(sol))); g2=sp.numer(sp.together(G2.subs(sol)))
    h=sp.gcd(sp.Poly(g1,elim),sp.Poly(g2,elim))
    if h.degree()==0: return 'no common v-branch (finite)'
    Ev=[sp.numer(sp.together(e.subs(sol))) for e in Es]
    res=[]
    for fac,_ in sp.factor_list(h.as_expr(),elim)[1]:
        if sp.Poly(fac,elim).degree()==0: continue
        ok=False
        for i in range(4):
            if sp.rem(sp.Poly(Ev[i],elim),sp.Poly(fac,elim)).is_zero: ok=True; break
            for j in range(i+1,4):
                if sp.rem(sp.Poly(sp.expand(Ev[i]**2-Ev[j]**2),elim),sp.Poly(fac,elim)).is_zero: ok=True; break
            if ok: break
        res.append(ok)
    return all(res)

def run(name,H=5000):
    Es=[E(m) for m in CONF[name]]
    out={'systems':0,'g1':{},'g2':[],'g0':[],'unres':[],'flags':[],'sols':[],'deg_comp':0,'univ':set()}
    for tag,G1,G2 in systems(Es):
        out['systems']+=1
        g=sp.gcd(G1,G2)
        if sp.Poly(g,t,u,v).total_degree()>0:
            out['flags'].append((tag,'common factor',sp.factor(g))); G1=sp.cancel(G1/g); G2=sp.cancel(G2/g)
        cands=[]
        for elim,(a,b) in ((v,(t,u)),(u,(t,v)),(t,(u,v))):
            R=sp.resultant(G1,G2,elim)
            if R==0: continue
            fl=sp.factor_list(R)[1]
            nbad=0
            for f,_ in fl:
                Pf=sp.Poly(f,a,b)
                if Pf.degree(a)<=1 or Pf.degree(b)<=1: continue
                if find_linear_basis(support(f,a,b)) is None: nbad+=1
            score=(nbad,max(sp.Poly(f,a,b).degree(a)+sp.Poly(f,a,b).degree(b) for f,_ in fl))
            cands.append((score,elim,a,b,fl))
        if not cands: out['flags'].append((tag,'all resultants zero')); continue
        cands.sort(key=lambda c:c[0]); _,elim,a,b,fl=cands[0]
        for F,_ in fl:
            P=sp.Poly(F,a,b)
            if P.degree(b)==0 or P.degree(a)==0:
                var=a if P.degree(b)==0 else b
                for r0 in (rational_roots(F,var) or []): out['univ'].add((ANG[var],r0))
                continue
            if P.degree(a)==1 or P.degree(b)==1:
                cd=component_degenerate(F,G1,G2,Es,a,b,elim)
                if cd is True: out['deg_comp']+=1; continue
                if cd=='no common v-branch (finite)':
                    # isolated points: parametrize the line and solve the 1-parameter system exactly
                    Pf=sp.Poly(F,a,b)
                    if Pf.degree(b)==1:
                        c1=sp.Poly(F,b).all_coeffs(); sol={b:sp.cancel(-c1[1]/c1[0])}; free=a
                    else:
                        c1=sp.Poly(F,a).all_coeffs(); sol={a:sp.cancel(-c1[1]/c1[0])}; free=b
                    g1=sp.numer(sp.together(G1.subs(sol))); g2=sp.numer(sp.together(G2.subs(sol)))
                    Rr=sp.resultant(g1,g2,elim)
                    if Rr==0: out['unres'].append((tag,'line component: zero resultant',sp.factor(F))); continue
                    for f0 in set(rational_roots(Rr,free) or []):
                        pt={free:f0}; other=[k for k in sol][0]; pt[other]=sp.Rational(sol[other].subs(free,f0)) if sp.denom(sol[other].subs(free,f0))!=0 else None
                        if pt[other] is None: continue
                        hv=sp.gcd(sp.Poly(G1.subs(pt),elim),sp.Poly(G2.subs(pt),elim))
                        for e0 in set(rational_roots(hv.as_expr(),elim) or []):
                            pt2=dict(pt); pt2[elim]=e0
                            vals=[sp.Rational(e.subs(pt2)) for e in Es]; ab=[abs(x) for x in vals]
                            if 0 not in ab and len(set(ab))==4: out['sols'].append((pt2,vals))
                    out['deg_comp']+=1; continue
                out['unres'].append((tag,'rational component not identically degenerate',sp.factor(F),cd)); continue
            S=support(F,a,b); fb=find_linear_basis(S)
            if fb is None: out['unres'].append((tag,ANG[a],ANG[b],(P.degree(a),P.degree(b)),'no linear basis',sorted(S.keys()))); continue
            M,A,coords=fb
            dd=discriminant(S,M,A,coords)
            if dd is None: out['unres'].append((tag,'discriminant not rational',str(M))); continue
            D,p,q,r,B=dd
            kind,taus,data=quartic_points(D,H)
            if kind=='genus1':
                key=data['D']; rec=out['g1'].setdefault(key,dict(data,count=0,M=str(M.tolist()))); rec['count']+=1
                if not data['complete']: out['flags'].append((tag,'genus1 incomplete',data))
                out['sols']+=lift(F,G1,G2,Es,taus,M,a,b,elim,B)
            elif kind=='genus>=2':
                out['g2'].append((tag,data,str(M.tolist()))); out['sols']+=lift(F,G1,G2,Es,taus,M,a,b,elim,B)
            elif kind=='genus0':
                out['g0'].append((tag,data,str(M.tolist()),sp.factor(F)))
            elif kind in ('none','zero'): pass
    return out

def fibers(name):
    Es=[E(m) for m in CONF[name]]; sols=[]; comps=[]
    for var,(a,b) in ((t,(u,v)),(u,(t,v)),(v,(t,u))):
        for val in (0,1,-1):
            Es0=[sp.expand(e.subs(var,val)) for e in Es]
            if any(e==0 for e in Es0) or any(sp.expand(Es0[i]**2-Es0[j]**2)==0 for i in range(4) for j in range(i+1,4)):
                comps.append((ANG[var],val,'whole fiber degenerate (an area vanishes or two coincide identically)')); continue
            for tag,G1,G2 in systems(Es0):
                g=sp.gcd(G1,G2)
                if sp.Poly(g,a,b).total_degree()>0:
                    for f,_ in sp.factor_list(g)[1]:
                        fp=sp.Poly(f,a,b)
                        if fp.total_degree()==0: continue
                        if fp.degree(a)==0 or fp.degree(b)==0:
                            vv=a if fp.degree(b)==0 else b
                            rr=rational_roots(f,vv) or []
                            if not rr: continue   # irreducible in one variable without rational root: no rational points
                            sub={vv:rr[0]}
                            Es1=[sp.expand(e.subs(sub)) for e in Es0]
                            deg= any(e==0 for e in Es1) or any(sp.expand(Es1[i]-Es1[j])==0 or sp.expand(Es1[i]+Es1[j])==0 for i in range(4) for j in range(i+1,4))
                            if not deg: comps.append((ANG[var],val,tag,f))
                        else:
                            # bivariate common factor: check degeneracy on it if linear in one var
                            if fp.degree(a)==1 or fp.degree(b)==1:
                                vv,ov=(a,b) if fp.degree(a)==1 else (b,a)
                                c=sp.Poly(f,vv).all_coeffs(); sol={vv:sp.cancel(-c[1]/c[0])}
                                Es1=[sp.numer(sp.together(e.subs(sol))) for e in Es0]
                                deg= any(sp.expand(e)==0 for e in Es1) or any(sp.expand(Es1[i]**2-Es1[j]**2)==0 for i in range(4) for j in range(i+1,4))
                                if not deg: comps.append((ANG[var],val,tag,f))
                            else: comps.append((ANG[var],val,tag,f))
                    G1,G2=sp.cancel(G1/g),sp.cancel(G2/g)
                R=sp.resultant(G1,G2,b)
                if R==0: comps.append((ANG[var],val,tag,'zero resultant after gcd')); continue
                for a0 in set(rational_roots(R,a) or []):
                    h=sp.gcd(sp.Poly(G1.subs(a,a0),b),sp.Poly(G2.subs(a,a0),b))
                    for b0 in set(rational_roots(h.as_expr(),b) or []):
                        vals=[sp.Rational(e.subs({a:a0,b:b0})) for e in Es0]; ab=[abs(x) for x in vals]
                        if 0 not in ab and len(set(ab))==4: sols.append((ANG[var],val,a0,b0,vals))
    return sols,comps

if __name__=="__main__":
    name,mode=sys.argv[1],sys.argv[2]; t0=time.time(); lines=[]
    if mode=='curve':
        out=run(name)
        lines.append(f"=== {name} [curves, {out['systems']} systems, {time.time()-t0:.0f}s]  degenerate rational components verified: {out['deg_comp']}")
        for k,r in out['g1'].items():
            lines.append(f"  genus1 Y^2={sp.factor(sp.sympify(k))}: rank {r['rank']}, tors {r['torsion']}, pts {r['npts']} -> {'COMPLETE' if r['complete'] else 'INCOMPLETE'} (x{r['count']}, M={r['M']})")
        for tag,d,Mstr in out['g2']: lines.append(f"  genus{d['genus']} Y^2={sp.factor(sp.sympify(d['D']))}: pts found {d['npts']} (tag {tag}, M={Mstr})")
        lines.append(f"  genus0 (infinite families?): {out['g0']}")
        lines.append(f"  unresolved: {out['unres']}")
        lines.append(f"  flags: {out['flags']}   torsion fibers appearing as components: {sorted(out['univ'],key=str)}")
        lines.append(f"  NONDEGENERATE curve sols: {out['sols']}")
    else:
        fs,fc=fibers(name)
        lines.append(f"=== {name} [fibers, {time.time()-t0:.0f}s] non-degenerate components: {fc}")
        lines.append(f"  NONDEGENERATE fiber sols: {fs}")
    txt="\n".join(lines); print(txt); open('/tmp/tp/results3.log','a').write(txt+"\n")
