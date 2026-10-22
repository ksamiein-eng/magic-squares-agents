"""verify_all.py -- independent re-verification of every load-bearing claim in the paper.
Written fresh (not derived from the pipeline) so it is a genuine check. Requires sympy, cypari2.
Run: python3 verify_all.py    All lines should print PASS."""
import sympy as sp, itertools, random, math
from fractions import Fraction; from math import isqrt
import cypari2; pari=cypari2.Pari(); pari.allocatemem(2*10**9)
FAILS=[]
def check(name,cond,info=''):
    print(('PASS' if cond else 'FAIL'),name,info)
    if not cond: FAILS.append(name)
# 1. Pullback identity (justifies Sections 6-8 under the corrected area-angle parametrization)
t,u,v=sp.symbols('t u v',real=True)
def mkE(ef):
    def Zp(var,k): return (1+sp.I*var)**(ef*k) if k>=0 else (1-sp.I*var)**(ef*(-k))
    def E(m,vs):
        val=sp.im(sp.expand(sp.prod([Zp(vs[i],m[i]) for i in range(3)])))
        for i,mm in enumerate(m):
            if mm==0: val=val*(1+vs[i]**2)**(ef//2)
        return sp.expand(val)
    return E
Eo,Ec=mkE(2),mkE(4); random.seed(11); ok=True
vecs=[(1,1,1),(1,1,-1),(1,-1,1),(1,-1,-1),(0,1,1),(0,1,-1),(1,0,1),(1,0,-1),(1,1,0),(1,-1,0),(1,0,0),(0,1,0),(0,0,1)]
for m in vecs:
    Ecm,Eom=Ec(m,[t,u,v]),Eo(m,[t,u,v])
    for _ in range(4):
        tv,uv,vv=[sp.Rational(random.randint(-9,9),random.randint(2,7)) for _ in range(3)]
        if any(x**2==1 for x in (tv,uv,vv)): continue
        Dt,Du,Dv=[2*x/(1-x**2) for x in (tv,uv,vv)]
        ok&= sp.nsimplify(Ecm.subs({t:tv,u:uv,v:vv})-((tv**2-1)*(uv**2-1)*(vv**2-1))**2*Eom.subs({t:Dt,u:Du,v:Dv}))==0
check('1 pullback identity E_c=(t^2-1)^2(u^2-1)^2(v^2-1)^2 E_o(D(t),D(u),D(v))',ok)
# 2. 15 orbits
def canon(w):
    for x in w:
        if x!=0: return tuple(w) if x>0 else tuple(-y for y in w)
P=sorted({canon(w) for w in itertools.product((-1,0,1),repeat=3) if any(w)})
adm=[frozenset(S) for S in itertools.combinations(P,4) if all(sum(abs(m[i])==1 for m in S)>=3 for i in range(3))]
G=[(sg,pm) for sg in itertools.product((1,-1),repeat=3) for pm in itertools.permutations(range(3))]
act=lambda g,w: canon([g[0][i]*w[g[1][i]] for i in range(3)])
orbits=[];seen=set()
for S in adm:
    if S in seen: continue
    orb={frozenset(act(g,w) for w in S) for g in G}; seen|=orb; orbits.append(orb)
check('2 Lemma 5.1: 13 vectors, 177 admissible 4-sets, 15 orbits',(len(P),len(adm),len(orbits))==(13,177,15))
# 3. Hill gap witness
def al(s1,s2,s3): k=Fraction(s2-s1,s3-s2); return k*(k+1)/(k-1)
def sq(fr): return isqrt(fr.numerator)**2==fr.numerator and isqrt(fr.denominator)**2==fr.denominator
aps=[(2,58,82),(46,74,94),(97,113,127)]
a1,a2=al(*aps[0]),al(*aps[1])
check('3 Hill witness: D=3360 common, alpha2/alpha1 square but numerator-split not',
      all(s2*s2-s1*s1==3360==s3*s3-s2*s2 for s1,s2,s3 in aps) and sq(a2/a1) and not sq(Fraction(a2.numerator,a1.numerator)))
# 4. Valuation lemma / Theorem A mechanism
def tri(y): return [(p,2*p*isqrt(y*y-p*p)) for p in range(1,y) if isqrt(y*y-p*p)**2==y*y-p*p and p<isqrt(y*y-p*p)]
def vl(n,l):
    c=0
    while n%l==0: n//=l; c+=1
    return c
T=tri(125); vals=[vl(a,5) for _,a in T]
check('4 valuation lemma on y=5^3: 3 triangles, v_5(2pq) pairwise distinct',len(T)==3 and len(set(vals))==3)
# 5. Curve zoo
s=pari('s'); Y=pari('Y')
CUR={'E_A':(1,-5,19,9),'E_B':(1,11,-5,1),'E_C':(1,-5,11,1),'E_D':(25,-29,11,1),'E_E':(25,-61,43,1)}
claimed={'E_A':(1968,1),'E_B':(352,1),'E_C':(352,1),'E_D':(1840,1),'E_E':(13280,2)}
for name,(a,b,c,d) in CUR.items():
    E=pari.ellinit([0,b,0,a*c,a*a*d]); Em=pari.ellminimalmodel(E); rk=pari.ellrank(E)
    N=int(pari.ellglobalred(Em)[0]); check(f'5 {name} conductor={N} rank={int(rk[0])}',N==claimed[name][0] and int(rk[0])==int(rk[1])==claimed[name][1])
EB=pari.ellminimalmodel(pari.ellinit([0,11,0,-5,1])); EC=pari.ellminimalmodel(pari.ellinit([0,-5,0,11,1]))
check('5 E_B,E_C non-isogenous (a_p differ)',any(pari.ellap(EB,p)!=pari.ellap(EC,p) for p in [3,5,7,13,17,19,23]))
# 6. Prop 7.3
for name,(a,b,c,d) in CUR.items():
    if name=='E_E': continue
    f=a*s**3+b*s**2+c*s+d; rk=pari.ellrank(pari.ellinit(pari.ellfromeqn(Y**2-s*f)))
    check(f"6 Prop 7.3 {name}: E' rank 1 (rank J(C)=2=g)",int(rk[0])==int(rk[1])==1)
# 7. Saturation
for name in ['E_A','E_B','E_C','E_D']:
    a,b,c,d=CUR[name]; E=pari.ellinit([0,b,0,a*c,a*a*d]); Em=pari.ellminimalmodel(E)
    rk=pari.ellrank(E); g=pari.ellsaturation(E,rk[3],1000); hG=float(pari.ellheight(E,g[0]))
    hj=math.log(max(abs(int(pari.numerator(Em.j()))),abs(int(pari.denominator(Em.j()))))); hD=math.log(abs(int(Em.disc())))
    H=int(math.exp(0.02+0.25*hj+hD/6+1.946+0.7))+1
    pts=pari.ellratpoints(Em,H); minh=min([float(pari.ellheight(Em,P)) for P in pts if float(pari.ellheight(Em,P))>1e-9] or [9e9])
    sat=pari.ellsaturation(E,g,int(math.sqrt(hG/0.02))+2)
    check(f'7 saturation {name}: lambda1>=0.02 and generator saturated',minh>=0.02 and abs(float(pari.ellheight(E,sat[0]))-hG)<1e-8)
# 8. Section 8.1
c=sp.symbols('c'); ss=sp.symbols('ss')
want={'E_B':-2*(c+1),'E_C':2*(c+1),'E_D':4*(2*c-1),'E_E':4*(4*c+1)}
for name,(a,b,cc,d) in CUR.items():
    f=a*ss**3+b*ss**2+cc*ss+d; g=sp.expand(sp.cancel((1+c)**3*f.subs(ss,(1-c)/(1+c))))
    m,n,K=sp.symbols('m n K'); sol=sp.solve(sp.Poly(sp.expand(g-K*(1+c*(1-c)*(m*c+n))),c).coeffs(),[K,m,n],dict=True)
    if name=='E_A': check('8 Sec 8.1 E_A is the quartic exception',not sol)
    else: check(f'8 Sec 8.1 {name} ell={sp.factor(want[name])}', bool(sol) and sp.expand(sol[0][m]*c+sol[0][n]-want[name])==0 and sol[0][K]==8)
check('8 Sec 8.1: 2(1+cos) NOT a square at (3,4,5) [draft error fixed]',not sq(2*(1+Fraction(3,5))))
exec('')

# 9. F-2 has a rank-1 even-quotient (conductor 216) -> not closed by rank-0 (the proofread correction)
try:
    import sympy as _sp
    _x=pari('x'); _f=1024*_x**4+77824*_x**3+30720*_x**2-36864*_x+9216
    _E=pari.ellinit(pari.ellfromeqn(pari('y^2')-_f)); _Em=pari.ellminimalmodel(_E); _rk=pari.ellrank(_E)
    check('9 F-2 E_{F2}: conductor 216, rank 1 (ledger correction)', int(pari.ellglobalred(_Em)[0])==216 and int(_rk[0])==int(_rk[1])==1)
except Exception as _e:
    check('9 F-2 E_{F2} check ran', False, str(_e))

print('\nRESULT:','ALL PASS' if not FAILS else f'FAILURES: {FAILS}')
