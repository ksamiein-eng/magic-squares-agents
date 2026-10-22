# Integration instructions for the full manuscript

Use this with the verified core v4. Do not globally replace the paper's unresolved
three-prime claims by "certified": the status changes below are narrower.

## 1. Inputs and parametrization

Keep the area-angle definition `exp(i chi_j)=(pi_j/conj(pi_j))^2=pi_j^4/ell_j^2`.
Replace the incomplete Gaussian representative in Section 2.3 by

\[
z_m=\prod_j\pi_j^{k_j+m_j}\bar\pi_j^{k_j-m_j},\qquad
z_m\bar z_m=y^2,\qquad \delta_m=|\operatorname{Im}(z_m^2)|.
\]

State that the finite counts concern integral triangles at fixed integral y.
Use "offset" for 2pq: it is four times the ordinary triangle area.

The actual 17 certificate inputs agree with the corrected 2|m| numerator. Delete
any claim that a doubled-angle pullback is birational or preserves all genera and
Jacobians. The input identity is now checked against the historical certificate
files themselves, not only a function in the old verifier.

## 2. Three-prime closure ledger: change F-2 to Closed

Replace the F-2 ledger row and its rank-one exception in Theorem D by:

> Orbit F-2 is closed for the rational-circle relaxation. Its 48 signed systems
> give 108 univariate factor entries, 96 generically degenerate component entries,
> and 24 remaining genus-three quotient entries. The last group consists of two
> reciprocal octics. Their even quotients have rank-zero Jacobian
> `Y^2=X^3-24003 X+1296702` and exactly twelve rational points each. The only square
> quotient parameters are zero and infinity, whose complete lifts to the original
> systems are degenerate. All generic exceptions and projective boundaries are
> included in the audit.

Cite the supplement's Proposition 5.1 and Theorem 5.2 together with the reproduction
package. Do not say that the separately named conductor-216 curve is rank zero.
Its possible appearance in another quotient route does not negate the complete
rank-zero route proved here.

Five distinct orbit closures are independently established: A, E1, E3=E4,
F-1=F-3, and F-2. There are 17 labels but only 15 orbits. The ten other entire
orbits remain unresolved in this audit, even where particular components close.

## 3. Explain the status of the verified sieve sets correctly

All eight rank-one subgroup residue lists in `sieves_cubic.json` match an
independent finite-field/CRT computation. State this as a verified congruence
statement for points nG on the specified original model. A global height theorem
still needs proven full generation, torsion conventions, the exact coordinate
function, complete orbit-to-curve maps, and rigorous canonical-height bounds.

Do not claim that `sieves_rank2.json` is supplied: it is absent from this archive.
Do not use the corrected Hermite coefficient as a substitute for verifying the
height lower bound on which the index estimate relies. Remove the old unconditional
uniform numerical height floor until its remaining proof obligations are met.

## 4. Replace the Chabauty handoff

Use `chabauty_inputs_corrected.json` and its explicit maps. All 16 uploaded
point/model pairs were inconsistent because the points were in the original
Weierstrass coordinates. The corrected points are proved on-curve, but are not
newly certified full Mordell-Weil generators.

The supplied Sage and Magma files only perform bounded point searches. The actual
quadratic-Chabauty call is commented out. Replace "ready-to-run Chabauty proof" by
"input preparation; a genuine complete Chabauty computation remains to be done."

## 5. Genus and novelty claims

For nonlinear components, retain the explicit equations as research inputs, but
label their smooth-model genera and the resulting Faltings-finiteness conclusions
as unverified until the required lower bounds and geometric conditions are proved.
Factoring over Q does not alone prove geometric irreducibility.

Replace the inference that positive-rank quotients show that relaxed nonexistence
cannot hold by:

> Positive-rank quotients show that the particular rank-zero quotient argument
> used so far does not settle these components. They do not show that any
> nondegenerate rational point lifts to the original equations.

The relaxed Theorem A is not established by the genuine-prime valuation proof;
retain only its proved integral prime-power conclusion unless a separate rational-
circle theorem is supplied. Historical novelty remains a theorem-by-theorem
comparison, not an inference from this audit.

## 6. Two-prime scope and archive provenance

The separate verified core v4 excludes exponent sums through six, hence gives
k+l >= 7. This audit of three-prime certificates does not certify the larger
sum-seven claim merely because `twoprime.py` has now been uploaded. Its complete
exceptional-component and projective-boundary proof still needs verification in
the established format.

Update the manuscript hash in a new release manifest. Preserve the historical
manifest unchanged as provenance: all its paths exist, but paper/paper.md has
changed since its recorded hash.
