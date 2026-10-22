#!/usr/bin/env python3
"""Assemble the version-4 manuscript from the preserved version-3 core.
Requires the successful release verification records; does not rerun them.
"""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parent

def main():
    for name in ['verification_degree6_stdlib.json','crosscheck_degree6_sympy.json']:
        if json.loads((ROOT/'results'/name).read_text())['status']!='PASS':
            raise RuntimeError('Missing successful verification: '+name)
    s=(ROOT/'provenance'/'verified_core_v3.tex').read_text()
    s=s.replace('Working draft v3','Working draft v4')
    s=s.replace('two-prime exclusions through exponent sum five}', 'two-prime exclusions through exponent sum six}')
    begin=s.index('\\begin{abstract}')
    end=s.index('\\end{abstract}',begin)+len('\\end{abstract}')
    abstract=r'''\begin{abstract}
We give a self-contained integral common-hypotenuse formulation, the correct Gaussian area-angle parametrization, and a valuation argument excluding every prime-power center. A real-angle identity proves the semiprime exclusion and closes the three-prime configuration E1. We certify all two-prime exponent pairs of sum at most six, adding $(5,1)$, $(4,2)$, and $(3,3)$ to the previous cases. Thus a primitive magic square of nine distinct positive integer squares with central root $y=p^kq^l$, for distinct primes, must have $k+l\ge7$. The combined proof data contain 1,200 signed systems and 662 non-linear factors excluded by explicit modular no-root witnesses. Two separate implementations verify the algebra, complete normal-form coverage, finite fibers, and projective boundaries. Circle-power inheritance gives a necessary lower bound of seven for the sum of the reduced deficiency denominators at arbitrary exponents. We retain an explicit complementary-quotient relation for two specified elliptic models. Larger exponent ranges, other three-prime closures, elliptic ranks, saturation, and height bounds remain uncertified here. No first-in-literature claim is made.
\end{abstract}'''
    s=s[:begin]+abstract+s[end:]
    s=s.replace(r'\begin{corollary}[Current certified two-prime lower bound]\label{cor:bound}',r'\begin{corollary}[Certified bound through exponent sum five]\label{cor:bound5}')
    s=s.replace(r'\label{cor:reduced}',r'\label{cor:reduced5}').replace(r'\label{eq:gcdcriterion}',r'\label{eq:gcdcriterion5}')
    anchor=r'\section{Two elliptic models with one common genus-two cover}'
    s=s.replace(anchor,(ROOT/'section_degree6.tex').read_text()+'\n'+anchor)
    start=s.index(r'\section{Verification record and remaining priorities}')
    end=s.index(r'\appendix',start)
    status=r'''\section{Verification record and remaining priorities}\label{sec:status}
The producer and foundation checks were run with Python and SymPy 1.14.0. The degree-six standard-library verifier passed all 1,200 systems, as did the separate Chebyshev/direct-symbolic-determinant cross-check. Both verify finite fibers and projective boundaries. Normal-form coverage is checked by explicit power-map routes and independently by coordinate gcd reduction. The complete version-3 certificate was reverified before extension, and its eleven representative records and catalog prefix are preserved exactly. None of these computations requires PARI, Sage, Magma, a network connection, or a hidden temporary file.

\paragraph{Proved in this core.}
The fixed-center integral dictionary, Gaussian parametrization and count, local valuation and full-depth statements, all prime-power exclusions, the real-angle parallelogram obstruction, semiprime exclusion, and E1 closure have written proofs. All two-prime exponent pairs of sum at most six have complete normal-form coverage and either an elementary proof or exact algebraic certificates checked by two implementations. Harmonic inheritance gives the updated reduced-denominator obstruction of Corollary~\ref{cor:reduced}. The specified $E_B/E_C$ cover relation has an explicit proof.

\paragraph{Finite regressions, separately identified.}
The foundation program again passed all 16 check groups. It checks all 3,000 integral nondegenerate triangles for 1,074 admissible $y\le10000$, including $y=1$ with no triangle. Euclidean and Gaussian generation agree, and all offset and valuation identities pass. This is a regression test, not a search bound for magic squares. The three-prime combinatorial counts $13/177/15$ are reproduced. Counts for the remaining three-prime orbits do not constitute their rational-point classifications.

\paragraph{Next exact computation.}
Exponent sum seven consists of $(6,1)$, $(5,2)$, and $(4,3)$. The updated reduced-denominator obstruction excludes 37 of the 73 raw normal forms. The remaining 36 form eighteen representative classes, requiring 864 proposed signed systems: two for $(6,1)$, eight for $(5,2)$, and eight for $(4,3)$. The coverage plan \path{results/next_sum7_plan.json} verifies this reduction, but these systems have \emph{not} been eliminated here. A future exclusion certificate must include every removed component, finite rational fiber, and projective boundary. Failure to classify a factor or shared component must remain unresolved. Completing that stage would independently recover the original manuscript's numerical exponent-sum-seven range; it would not certify its other claims.

\paragraph{After that.}
For each surviving three-prime component, supply its defining equations, rational maps to any quotient, inverse-lift conditions, and a rigorous smooth-model genus calculation. Only then do elliptic ranks, globally justified saturation, and a corrected Mordell--Weil height argument have the needed input. Quadratic Chabauty addresses particular validated curves; it does not replace these upstream obligations. No other three-prime closure or large canonical-height bound is retained here.

\paragraph{Literature and attribution.}
The common-hypotenuse dictionary and original semiprime exclusion are credited to Brown; prime-signature organization is not claimed as new. The bielliptic construction is standard. This repair provides precise proofs, explicit maps, and reproducible proof objects for the stated range. No first-in-literature claim is made for the valuation lemma, the real-angle formulation, or the exclusions through exponent sum six. A theorem-by-theorem priority comparison remains separate from correctness verification.

'''
    s=s[:start]+status+s[end:]
    start=s.index(r'\section{Reproduction and proof boundary}')
    end=s.index(r'\begin{thebibliography}',start)
    reproduction=r'''\section{Reproduction and proof boundary}
Run from the bundle root:
\begin{verbatim}
# Standard-library certificate verification:
python verify_degree6_stdlib.py
# Independent symbolic check (requires SymPy 1.14.0):
python crosscheck_degree6_sympy.py
python test_degree6_verifier.py
python check_foundation.py
\end{verbatim}
Optional regeneration uses \path{build_degree6_certificate.py}; rerun both checkers afterward. The README gives the manuscript build commands. The file \path{plan_sum7.py} checks next-stage coverage only, not a new exclusion.

The combined verifier checks 95 raw normal forms through exponent sum six. Every rational finite fiber permitted by the verified factors, every removed $t=0$ branch, and both projective boundary lines are checked from the reconstructed numerators. The symbolic cross-check verifies those identities separately and checks normal forms after dividing out coordinate gcds.

The negative tests reject thirteen damaged certificates and one unsupported finite-fiber claim, including corruptions of newly added representatives. A forged higher-degree polynomial vanishing at the entire determinant evaluation grid is rejected by the independent degree bound. Fraction-free integer determinants agree with a separate Leibniz implementation on 180 small matrices. These tests are safeguards, not substitutes for the written mathematical arguments.

\path{results/certificate_degree6.json} contains all 1,200 systems, 665 catalog polynomials, and modular witnesses. Readable coefficient and assignment records appear in \path{results/degree6_factor_catalog.md} and \path{results/degree6_systems.csv}. Earlier certificates and their checkers are retained; their historical plan files are not current status reports. The producer uses SymPy's documented polynomial operations \cite{SymPy} for discovery. Acceptance checks integer identities and finite-field values without assuming irreducibility or using a rational-root solver.

Python and the checker implementations remain in the software trust boundary. This is not a formal proof-assistant development. The written arguments explain why the checked calculations imply the arithmetic exclusions. Input and release hashes, environment versions, and a clean-extraction verification record accompany the package. The original attachments remain unchanged. The broader three-prime and height claims are not reinstated.

'''
    s=s[:start]+reproduction+s[end:]
    (ROOT/'verified_core.tex').write_text(s)
    print('Wrote verified_core.tex')

if __name__=='__main__':main()
