"""linrel_exact.py <ORBIT>... : exact proof (Lemma 5.4) that each linear-relation component is degenerate.
Self-contained: over K=Q(t)[u]/(F) compute gcd_{K[v]}(G1,G2); if it has degree 1 with root r, substitute v=r into
every area polynomial E(m) and reduce mod F -- a line whose area reduces to 0 vanishes identically on the component.
Exceptional points (where a Euclidean leading coefficient's norm vanishes) are checked individually."""
import sys, json
src=open('/tmp/tp/pipe3.py').read(); exec(src[:src.index('if __name__')])
DOM=sp.QQ.frac_field(t); VAR={'x':t,'z':u,'w':v}
def verify(name):
    path=f'/tmp/tp/certs/{name}.json'; r=json.load(open(path)); Es=[E(m) for m in CONF[name]]
    sysmap={tuple(tag):(G1,G2) for tag,G1,G2 in systems(Es)}; out=[]
    for s in r['systems']:
        for fr in s['factors']:
            if fr.get('type')!='linear_in_circle_point' or not str(fr.get('status','')).startswith('NO FINITE'): continue
            if not fr['quotients'] or fr['quotients'][0].get('curve_kind') not in ('genus0','genus0-const-square'): continue
            assert VAR[s['projection']['eliminated']]==v, "assumes eliminated variable is w"
            F=sp.sympify(fr['poly'],locals={'t':t,'u':u,'v':v}); G1,G2=sysmap[tuple(s['tag'])]
            FP=sp.Poly(F,u,domain=DOM)
            if not FP.is_irreducible: fr['exact_verification']={'verdict':'F reducible over Q(t) -- MANUAL'}; continue
            def red(a): return sp.Poly(sp.together(a),u,domain=DOM).rem(FP)
            def inv(a):
                s_,_,h=a.gcdex(FP); assert h.degree()==0; return (s_*(1/h.LC())).rem(FP)
            denoms=[]
            def kpoly(G):
                cs=[red(c) for c in sp.Poly(G,v).all_coeffs()]
                while cs and cs[0].is_zero: cs=cs[1:]
                return cs
            def kmod(A,B):
                A=list(A); lb=inv(B[0]); denoms.append(B[0])
                while len(A)>=len(B) and A:
                    q=(A[0]*lb).rem(FP)
                    for i,b in enumerate(B): A[i]=(A[i]-q*b).rem(FP)
                    while A and A[0].is_zero: A=A[1:]
                    if len(A)<len(B): break
                return A
            P1,P2=kpoly(G1),kpoly(G2)
            while P2: P1,P2=P2,kmod(P1,P2)
            H=P1; dg=len(H)-1
            rec={'field':'K=Q(t)[u]/(F), F irreducible over Q(t)','gcd_degree_in_v':dg}
            zero_lines=[]
            if dg==1:
                root=(-H[1]*inv(H[0])).rem(FP); rec['gcd_root_v']=str(root.as_expr())
                # substitute v=root into each area polynomial, reduce mod F
                for i,m in enumerate(CONF[name]):
                    cs=[red(c) for c in sp.Poly(Es[i],v).all_coeffs()]
                    val=red(0)
                    for c in cs: val=(val*root+c).rem(FP)
                    if val.is_zero: zero_lines.append({'index':i,'vector':list(m)})
                rec['lines_vanishing_identically']=zero_lines
            # exceptional t: norms of Euclidean denominators, gcd leading coeff, and F's leading coeff in u
            excT=set()
            for d in denoms+([H[0]] if H else [])+[sp.Poly(sp.Poly(F,u).LC(),u,domain=DOM)]:
                if d.is_zero: continue
                N=sp.resultant(sp.Poly(d.as_expr(),u),sp.Poly(F,u)).as_expr() if sp.Poly(d.as_expr(),u).degree()>0 else d.as_expr()
                N=sp.expand(sp.numer(sp.together(N)))
                if N.free_symbols: excT|=set(rational_roots(N,t) or [])
            excl=[]
            for t0 in excT:
                for u0 in set(rational_roots(sp.expand(F.subs(t,t0)),u) or []):
                    h=sp.gcd(sp.Poly(G1.subs({t:t0,u:u0}),v),sp.Poly(G2.subs({t:t0,u:u0}),v))
                    if h.degree()<=0: continue
                    for v1 in set(rational_roots(h.as_expr(),v) or []):
                        vals=[sp.Rational(e.subs({t:t0,u:u0,v:v1})) for e in Es]; ab=[abs(x) for x in vals]
                        excl.append({'point':[str(t0),str(u0),str(v1)],'areas':[str(x) for x in vals],'degenerate':(0 in ab or len(set(ab))<4)})
            rec['exceptional_t']=[str(x) for x in sorted(excT)]; rec['exceptional_rational_points']=excl
            rec['verdict']='PROVED degenerate' if (dg==1 and zero_lines and all(e['degenerate'] for e in excl)) else 'INCOMPLETE'
            fr['exact_verification']=rec; out.append((s['tag'],dg,[z['vector'] for z in zero_lines],len(excT),len(excl),rec['verdict']))
    json.dump(r,open(path,'w'),indent=1,default=str); return out
if __name__=="__main__":
    for name in sys.argv[1:]:
        res=verify(name); print(f"{name}: {len(res)} linear-relation components")
        for tag,dg,zl,nt,nx,verd in res: print(f"   {tag} gcd deg {dg} vanishing line {zl} exc-t {nt} pts {nx}  {verd}")
