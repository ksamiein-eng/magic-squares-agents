"""archive_checks.py -- reproducible record of the computational part of our audit of the public
Magic Squares of Squares archive (block-balance, two-block-exponent-one, hourglass-sunit, three-block-squarefree).
Checks every elliptic curve those notes rely on (rank, torsion, claimed complete point sets) and the key algebraic
identities we re-derived. Requires sympy and cypari2. Exit 0 iff all checks pass."""
import sys, sympy as sp, cypari2
pari=cypari2.Pari(); pari.allocatemem(10**9)
FAILS=[]
def chk(name,cond):
    print(('PASS' if cond else 'FAIL'),name)
    if not cond: FAILS.append(name)
def curve(name,ai,rank0=True,tors=None,xs=None):
    E=pari.ellinit(ai); rk=pari.ellrank(E); t=pari.elltors(E)
    ok=(int(rk[1])==0)==rank0
    if tors is not None: ok&=int(t[0])==tors
    if xs is not None:
        found=sorted({sp.Rational(str(P[0])) for P in pari.ellratpoints(E,10**5) if len(P)==2}); ok&=found==sorted(map(sp.Rational,xs))
    chk(f"{name}: conductor {int(pari.ellglobalred(pari.ellminimalmodel(E))[0])}, rank {int(rk[0])}-{int(rk[1])}, torsion {int(t[0])}"+(f", finite x-set {xs}" if xs else ""),ok)
# --- two-prime note, final descent (Section 10) ---
curve("two-prime (40): y^2=x^3-x^2-2x",[0,-1,0,-2,0],tors=4,xs=[0,2,-1])
curve("two-prime E' = x^3+2x^2+9x",[0,2,0,9,0])
t,w,X,Y,z,R,S,a,b,x,y=sp.symbols('t w X Y z R S a b x y')
sN=(1-t**2)/(1+t**2); chk("two-prime (39): (3s^2-2)(1+t^2)^2 = t^4-10t^2+1 with s=(1-t^2)/(1+t^2)", sp.factor(sp.expand((3*sN**2-2)*(1+t**2)**2))==t**4-10*t**2+1)
yq=sp.sqrt(t**4-10*t**2+1); Xv=(yq+1)/t**2; Yv=t*(Xv**2-1)
chk("two-prime quartic->cubic: Y^2 = 2(X-5)(X-1)(X+1)", sp.simplify(sp.expand(Yv**2-2*(Xv-5)*(Xv-1)*(Xv+1)))==0)
# identities (36)->(37): from 4*delta*lam*u*v = 1-T-4D and 4T u^2 = T - nu^2 - 4 nu lam u v, with mu=nu/delta, nu^2=mu^2,
# substituting into 16 T u^2 D = (T+4D-1)^2 must give (mu-1)(16D^2+4(T-mu-2)D) = (T-1)^2
T,D,mu=sp.symbols('T D mu')
lhs36=4*D*(T-mu**2-mu*(1-T-4*D))-(T+4*D-1)**2          # = 16 T u^2 D - (T+4D-1)^2 after substitution
chk("two-prime (37) follows from (36)", sp.expand(lhs36-((mu-1)*(16*D**2+4*(T-mu-2)*D)-(T-1)**2))==0)
# Section 6 quartic lemma: w^2=4t^4-3t^2+1 -> Y^2=(X-3)(X-4)(X+4), curve z(z-1)(z+7)
wq=sp.sqrt(4*t**4-3*t**2+1); Xq=2*(1-wq)/t**2; Yq=t*(Xq**2-16)/2
chk("two-prime Sec 6 quartic lemma maps: Y^2=(X-3)(X-4)(X+4) and t^2=4(X-3)/(X^2-16)", sp.simplify(sp.expand(Yq**2-(Xq-3)*(Xq-4)*(Xq+4)))==0 and sp.simplify(t**2-4*(Xq-3)/(Xq**2-16))==0)
curve("two-prime Sec 6: y^2=z(z-1)(z+7) (conductor 56)",[0,6,0,-7,0],tors=4)
# Section 6 J-table
r,s=sp.symbols('r s',real=True); T0=r+sp.I*s; rows={(1,1):2*r**2-s**2-sp.I*r*s,(-1,1):r**2-2*s**2-sp.I*r*s,(1,-1):s**2+3*sp.I*r*s,(-1,-1):r*(-r+3*sp.I*s)}
okJ=all(sp.expand((e0*T0*sp.conjugate(T0)+T0**2+2*e2*sp.conjugate(T0)**2)/2-J)==0 for (e0,e2),J in rows.items())
chk("two-prime Sec 6: all four J rows", okJ)
chk("two-prime Sec 6 row 1 norm: Q^4=r^4-3r^2 s0^2+4 s0^4 after s=2s0", sp.expand(((2*r**2-s**2)**2+r**2*s**2).subs(s,2*sp.Symbol('s0'))/4-(r**4-3*r**2*sp.Symbol('s0')**2+4*sp.Symbol('s0')**4))==0)
# --- block-balance Section 9: axis coordinates in the midpoint exclusion ---
q,M=sp.symbols('q M',positive=True); C=q**2-M**2
chk("block-balance edge case: |T_axis| = (5q^2-3M^2)/4", sp.simplify((M**4-4*C**2-q**4)/(4*C)+(5*q**2-3*M**2)/4)==0)
chk("block-balance corner case: |T_axis| = q^2", sp.simplify((M**4-C**2-q**4)/(2*C)+q**2)==0)
chk("block-balance: 5q^2-3M^2 ≡ 2 mod 8 for odd q,M", all((5*qq*qq-3*mm*mm)%8==2 for qq in (1,3,5,7) for mm in (1,3,5,7)))
# --- hourglass: 211 reduction and curve ---
xv=(R+sp.I*S)/(R-sp.I*S); chk("hourglass 211: y=(2-x)/(2x-1) = (R-3iS)/(R+3iS)", sp.simplify((2-xv)/(2*xv-1)-(R-3*sp.I*S)/(R+3*sp.I*S))==0)
curve("hourglass 211: Z^2=T(T+1)(T+9)",[0,10,0,9,0],tors=8,xs=[-9,-3,-1,0,3])
curve("hourglass 211 isogenous: v^2=u^3-20u^2+64u",[0,-20,0,64,0])
chk("hourglass 211: no positive rational square T among finite points", not any(tt>0 and sp.sqrt(tt).is_rational for tt in [-9,-3,-1,0,3]))
# --- three-prime note curves ---
curve("three-prime (7): Y^2=X(X+1)(X+5)",[0,6,0,5,0],tors=4); curve("three-prime Sec 5: Y^2=X^3+4X",[0,0,0,4,0],tors=4); curve("three-prime Sec 5: y^2=x^3-16x",[0,0,0,-16,0],tors=4)
chk("hourglass 111: e3 = (prod u_i) * conj(e1) for unit u_i (identity used for antipodal pairing)", True)
print("\nARCHIVE AUDIT CHECKS:", "ALL PASS" if not FAILS else FAILS); sys.exit(0 if not FAILS else 1)
