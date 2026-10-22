"""Section 8.1: derive the common form 2(1+c)(1+c(1-c)ell(c))=square for the sieve curves,
extract the four linear ell, and confirm E_A is the quartic exception. Exact, symbolic."""
import sympy as sp
from fractions import Fraction
from math import isqrt
c, s = sp.symbols('c s')
CUBICS = {'E_A':(1,-5,19,9),'E_B':(1,11,-5,1),'E_C':(1,-5,11,1),'E_D':(25,-29,11,1),'E_E':(25,-61,43,1)}
def squarefree(k):
    k=int(k); out=1
    for p,e in sp.factorint(abs(k)).items(): out*=p**(e%2)
    return out*(1 if k>0 else -1)
def analyze(name,co):
    a,b,cc,d=co; f=a*s**3+b*s**2+cc*s+d
    g=sp.expand(sp.cancel((1+c)**3*f.subs(s,(1-c)/(1+c))))
    m,n,K=sp.symbols('m n K'); target=sp.expand(K*(1+c*(1-c)*(m*c+n)))
    sol=sp.solve(sp.Poly(sp.expand(g-target),c).coeffs(),[K,m,n],dict=True)
    if sol:
        S=sol[0]; Kv,ell=S[K],sp.factor(S[m]*c+S[n])
        return ('fit',Kv,squarefree(Kv),ell)
    return ('exception',None,None,None)
if __name__=="__main__":
    for name,co in CUBICS.items():
        kind,K,sf,ell=analyze(name,co)
        if kind=='fit': print(f"{name}: condition 2(1+c)(1+c(1-c)*ell)=square, squarefree(K)={sf}, ell={ell}")
        else: print(f"{name}: QUARTIC EXCEPTION (no linear ell)")
    # false-simplification check
    def issqQ(fr): fr=Fraction(fr); return isqrt(fr.numerator)**2==fr.numerator and isqrt(fr.denominator)**2==fr.denominator
    print("\n2(1+cos) at rational angles (should NOT be squares):",
          [(f"{p}/{r}",str(2*(1+Fraction(p,r))),issqQ(2*(1+Fraction(p,r)))) for p,r in [(3,5),(5,13),(8,17)]])
