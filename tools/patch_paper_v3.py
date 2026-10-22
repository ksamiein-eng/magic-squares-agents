#!/usr/bin/env python3
"""Create paper_update/manuscript (version 3 of the manuscript) from the shipped paper/manuscript.

Adds: authors and date; abstract sentences; Theorem 4.5 (exponent sum nine); Section "Quotients of the
genus-five curve"; Section 8.x (torsion-coset evidence and the degeneracy-rank lemma); companion-repository
paragraph; disclosure sentence. The shipped paper/ tree is not modified.
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "paper" / "manuscript"
DST = ROOT / "paper_update" / "manuscript"
if DST.exists():
    shutil.rmtree(DST)
shutil.copytree(SRC, DST, ignore=shutil.ignore_patterns("paper.pdf"))

p = DST / "paper.tex"
s = p.read_text(encoding="utf-8")


def rep(old, new):
    global s
    assert old in s, old[:70]
    s = s.replace(old, new, 1)


rep("pdfauthor={}}", "pdfauthor={Kimia Samieinejad, Jonathan Wolinski}}")
rep("% Human author names, affiliations, and contact details must be supplied before submission.\n\\author{}\n\\date{5 October 2026}",
    "\\author{Kimia Samieinejad \\and Jonathan Wolinski}\n\\date{22 October 2026 (version 3: author-review draft with the 22 October additions)}")

rep("The results concern specified subfamilies of that relaxation and do not decide the unrestricted magic-square problem.\n\\end{abstract}",
    "The results concern specified subfamilies of that relaxation and do not decide the unrestricted magic-square problem. "
    "\\emph{Additions of 22 October 2026.} The two-parameter certificate is extended through exponent sum nine ($5{,}520$ signed systems, independently re-checked). "
    "The genus-five curve has the involutions $h\\mapsto-h$ and $h\\mapsto1/h$; its three elliptic quotients are the curves 123.a1, 492.b1 and 1968.j1 of the LMFDB, each with a rational point of infinite order, "
    "so the eight-point conjecture is not reachable by rank-zero descent or by classical Chabauty on the genus-two quotient and is a quadratic-Chabauty problem. "
    "The torsion-coset hypothesis holds on all $662{,}528$ rational points of the solution varieties with three parameters of projective height at most four; a degeneracy-rank lemma explains the structure of these points and predicts in which configurations a point can lie on a torsion coset of codimension one. "
    "No rational point of height up to $10^6$ exists on the genus-five curve beyond the eight known.\n\\end{abstract}")

rep("The same proof yields an obstruction for arbitrary exponents whenever the reduced denominators of $m/k$ and $n/\\ell$ have sum at most seven.",
    "The same proof yields an obstruction for arbitrary exponents whenever the reduced denominators of $m/k$ and $n/\\ell$ have sum at most seven. "
    "Theorem~\\ref{thm:sumnine} (added 22 October 2026) extends the certificate through exponent sum nine, so ``seven'' may be read as ``nine'' in this paragraph.")

SUMNINE = r"""The corollary concerns individual frequency configurations. It does not exclude every two-prime central root with larger exponent sum.

\subsection{Extension through exponent sum nine (22 October 2026)}\label{sec:sumnine}
The producer and checker of Lemma~\ref{lem:elimination} were rerun, unchanged in method, on the signatures with $k+\ell=8$ and $k+\ell=9$. Coverage was planned exactly as in Section~\ref{sec:two}: of the $140$ raw normal forms with $k+\ell=8$, $72$ are inherited from the sum-seven certificate by Lemma~\ref{lem:inherit} and the remaining $68$ form $32$ orbits; of the $172$ raw forms with $k+\ell=9$, $92$ are inherited and the remaining $80$ form $40$ orbits. The orbit decomposition is asserted exactly by the planning script and re-derived independently by the checker.

\begin{theorem}[Certified exclusion through exponent sum nine]\label{thm:sumnine}
For $k+\ell\le9$, no matrix $A_{k,\ell;m,n}$ in~\eqref{eq:normalformintro} admits an admissible point of $\T(\Q)^2$. Consequently Corollary~\ref{cor:denominator} holds with $8$ replaced by $10$, and a primitive magic square with central root $p^kq^\ell$ requires $k+\ell\ge10$.
\end{theorem}
\begin{proof}[Computer-assisted proof]
The merged certificate contains $115$ representatives and $5{,}520$ signed systems ($2{,}064$ from Lemma~\ref{lem:elimination}, $1{,}536$ new at sum eight, $1{,}920$ new at sum nine), a factor catalog of $3{,}207$ polynomials of which $3{,}204$ carry a modular no-root witness and three are the linear factors with roots $0,\pm1$, and $553{,}392$ exact integer Sylvester determinants. The largest witness prime is still $19$. Every finite rational fiber has $t\in\{0,\pm1\}$, and the projective boundaries are excluded by~\eqref{eq:collision} as before. The standard-library checker accepts the merged certificate in strict mode; the sum-eight part was additionally accepted by the symbolic Chebyshev/Sylvester checker and by the mutation tests, while the symbolic cross-check and mutation tests of the sum-nine part had not been run at the time of writing. Certificates, checkers, logs and the agent transcripts that produced them are in the companion repository (Section~\ref{sec:repro}).
\end{proof}
The arithmetic consequence $k+\ell\ge10$ is, like $k+\ell\ge8$, subsumed by the archive's two-prime theorem (Section~\ref{sec:prior}); the content of Theorem~\ref{thm:sumnine} is the relaxed-problem exclusion, which that argument does not reach."""
rep("The corollary concerns individual frequency configurations. It does not exclude every two-prime central root with larger exponent sum.", SUMNINE)

QUOT = r"""\section{Quotients of the genus-five curve and the status of Conjecture~\ref{conj:points}}\label{sec:quotients}
This section was added on 22 October 2026. The polynomial $P$ in~\eqref{eq:Pintro} is even and palindromic, so $\mathcal C$ carries the involutions $\sigma_1:(h,Y)\mapsto(-h,Y)$ and $\sigma_2:(h,Y)\mapsto(1/h,Y/h^6)$.

\begin{proposition}[Quotients]\label{prop:quotients}
Put $g(s)=s^3+70s^2-1012s+6920$. Then
\begin{gather*}
 P(h)=f(h^2),\qquad \frac{P(h)}{h^6}=g\!\left(h^2+h^{-2}\right),\qquad \frac{f(x)}{x^3}=g\!\left(x+\frac1x\right),\
 f(x)=x^6+70x^5-1009x^4+7060x^3-1009x^2+70x+1.
\end{gather*}
Hence $\mathcal C/\sigma_1$ is the genus-two curve $D:\ Y^2=f(x)$, which is bielliptic with quotients $E_\pm:\ v^2=(w\pm2)\,g(w)$, $w=x+1/x$; and $(h,Y)\mapsto(s,v)=(h^2+h^{-2},\,Y/h^3)$ maps $\mathcal C$ onto the elliptic curve $E_0:\ v^2=g(s)$. The three curves are isomorphic over $\Q$ to the LMFDB curves $123.\mathrm{a}1$ ($E_0$), $492.\mathrm{b}1$ ($E_+$) and $1968.\mathrm{j}1$ ($E_-$); the isomorphisms are verified exactly by the scaling of $c_4$ and $c_6$ with $u=4,8,12$ respectively.
\end{proposition}
\begin{proof}
The four identities are polynomial expansions, checked symbolically. The point $h=1$ of $\mathcal K$ maps to $(s,v)=(2,72)$ on $E_0$. The identifications are by $j$-invariant followed by the exact $c_4,c_6$ test, which distinguishes a curve from its twists.
\end{proof}

\begin{proposition}[Positive rank]\label{prop:posrank}
Each of $E_0,E_+,E_-$ has a rational point of infinite order. Hence $\operatorname{rank}E_i(\Q)\ge1$ for all three, and $\operatorname{rank}\operatorname{Jac}(\mathcal C)(\Q)\ge3$.
\end{proposition}
\begin{proof}
On the integral model $v^2=g(s)$ the point $(2,72)$ has $3\cdot(2,72)$ with abscissa $11042/289$; by the Nagell--Lutz theorem a torsion point of an integral Weierstrass model has integral coordinates, so $(2,72)$ has infinite order. On the integral monic models of $E_+$ and $E_-$ obtained by moving the rational root $w=\mp2$ of the quartic to infinity, the points $(0,9216)$ and $(0,5184)$ have the non-integral multiples $8P$ (abscissa $-2304/25$) and $3P$ (abscissa $113291136/292681$). The three curves have pairwise distinct $j$-invariants and conductors $123$, $492$, $1968$, so they are pairwise non-isogenous over $\Q$; their pullbacks are independent abelian subvarieties of $\operatorname{Jac}(\mathcal C)$, and the ranks add.
\end{proof}

The LMFDB records rank exactly one for each curve (a database fact we quote and do not re-prove), so $\operatorname{rank}\operatorname{Jac}(D)(\Q)=2=g(D)$. Consequently neither the rank-zero descents of Section~\ref{sec:norm} nor classical Chabauty on $D$ can prove Conjecture~\ref{conj:points}; the conjecture is an instance of quadratic Chabauty for a bielliptic genus-two curve of Mordell--Weil rank two, with the generators $(-7,18)$ on $492.\mathrm{b}1$ and $(-2,3)$ on $1968.\mathrm{j}1$ as inputs, or of elliptic-curve Chabauty over a quadratic field. We record also that a sieved exact search finds no rational point of $\mathcal C$ with $\max(|p|,q)\le10^6$ outside $\mathcal K$, and none on $D$ with height at most $3\cdot10^5$ outside the images of $\mathcal K$; this is evidence, not proof.

\input{rigidity.tex}"""
rep("\\input{rigidity.tex}", QUOT)

rep("\\section{Proof data and reproducibility}\\label{sec:repro}",
    "\\section{Proof data and reproducibility}\\label{sec:repro}\n"
    "\\emph{Companion repository (22 October 2026).} The additions of this version were produced and checked by a multi-agent pipeline that exposes the verification tree of this paper as tools (an MCP server), attacks the open problems by fixed playbooks, submits every claim to an adversarial referee agent, and absorbs accepted results as additional stages of \\texttt{verify\\_paper.py} without modifying the shipped proof records. The repository \\url{https://github.com/ksamiein-eng/magic-squares-agents} contains the certificates for exponent sums eight and nine, the quotient-curve computations, the torsion-coset probe, the degeneracy-rank script, verbatim agent transcripts, a claim map, provenance hashes, and the extended suite \\texttt{verify\\_paper\\_plus.py} (the sixteen stages of this paper followed by six agent-added stages, all passing).\n")

rep("ChatGPT and Claude were used for symbolic and computational work, implementation of verification code, and preparation and revision of the exposition.",
    "ChatGPT and Claude were used for symbolic and computational work, implementation of verification code, and preparation and revision of the exposition. "
    "The additions dated 22 October 2026 (Theorem~\\ref{thm:sumnine}, Section~\\ref{sec:quotients}, Section~\\ref{sec:torsionprobe}) were generated, machine-verified and refereed by Claude agents orchestrated through Claude Code; the authors reviewed the statements and take responsibility for all claims.")
p.write_text(s, encoding="utf-8")

r = DST / "rigidity.tex"
t = r.read_text(encoding="utf-8")
OLD = "Theorem~\\ref{thm:gentype} shows that the general-type behaviour"
assert OLD in t
NEW = r"""\subsection{Evidence for the torsion-coset hypothesis and a degeneracy-rank lemma (22 October 2026)}\label{sec:torsionprobe}
The sweep of Proposition~\ref{prop:four} was re-instrumented to record \emph{every} exact solution of the $48$ signed systems, admissible or not, for all $113$ orbits, all four choices of solved coordinate, and all triples of the other parameters of projective height at most $H$, and each solution was tested for Conjecture~\ref{conj:torsion} by a complete criterion: with $\tan(\chi_j/2)=p_j/q_j$ one has $z_j=(q_j+ip_j)/(q_j-ip_j)$, whose image in $\Q(i)^\times/\{\pm1,\pm i\}$ is determined by the Gaussian-prime factorisation of $q_j+ip_j$; a relation $\prod z_j^{n_j}\in\{\pm1,\pm i\}$ exists if and only if the four exponent vectors are linearly dependent, and the rank of these vectors (the \emph{exponent rank}) is computed exactly.

\begin{proposition}\label{prop:torsiondata}
At $H=3$ there are $273{,}024$ distinct rational points of the solution varieties, and at $H=4$ there are $662{,}528$. Every one of them satisfies a nontrivial relation $\prod z_j^{n_j}\in\{\pm1,\pm i\}$; none is admissible; every one has a vanishing sine and two sines of equal magnitude. The exponent rank is at most $2$ at $H=3$; at $H=4$ it equals $3$ for $13{,}824$ points, all in two orbits.
\end{proposition}
The rank-three points refute the sharper statement, suggested by the $H\le3$ data, that every rational point lies on a torsion coset of a subtorus of dimension at most two. They are explained by the following elementary lemma.

\begin{lemma}[Degeneracy relations]\label{lem:degrel}
Let $z\in T(\Q)^r$ and $s_j=\sin(A_j\cdot\chi)$. If $s_r=0$ then $\prod_j z_j^{A_{rj}}=\pm1$. If $|s_i|=|s_k|$ with $i\ne k$ then $\prod_j z_j^{A_{ij}-A_{kj}}=\pm1$ or $\prod_j z_j^{A_{ij}+A_{kj}}=\pm1$, with a nonzero exponent vector because the rows are distinct projective vectors. Consequently every rational point with a vanishing sine or two sines of equal magnitude satisfies Conjecture~\ref{conj:torsion}; a point with both degeneracies has exponent rank at most $3$, with equality only if $A_i\pm A_k$ is a rational multiple of the vanishing row $A_r$.
\end{lemma}
\begin{proof}
$s_r=0$ means $A_r\cdot\chi\in\pi\Z$, and $|s_i|=|s_k|$ means $A_i\cdot\chi\equiv\pm A_k\cdot\chi\pmod\pi$; exponentiate. Two independent relations lower the rank to at most $2$.
\end{proof}
The parallel-triple condition of the lemma holds for exactly $23$ of the $113$ orbit representatives, and the two orbits that carry rank-three points at $H=4$ are among them; every recorded rank-three point has a vanishing row parallel to the sum or difference of its two equal-magnitude rows. The remaining $21$ orbits are a prediction for larger heights. The lemma also shows that Conjecture~\ref{conj:rigidity} implies Conjecture~\ref{conj:torsion} for every solution-variety point that fails admissibility through a vanishing sine or coinciding magnitudes; the only other failure mode, $a=2b$, yields no monomial relation and was never observed. The code, the per-orbit counts and the twenty recorded rank-three examples are in the companion repository.

Theorem~\ref{thm:gentype} shows that the general-type behaviour"""
t = t.replace(OLD, NEW, 1)
r.write_text(t, encoding="utf-8")
print("wrote", DST)
