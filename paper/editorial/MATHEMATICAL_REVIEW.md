# Mathematical proofread and appendix revision

**Review date:** 5 October 2026  
**Input:** `magic_squares_research_paper_revised.tex` and the matching revised submission package.  
**Scope:** the focused research article, not the superseded 20-page draft or the separate 43-page research record.

## Assessment

The complete focused source was read, including its abstract, introduction, definitions, proofs, unnumbered displays, tables, appendices, and bibliography. The two main proof chains were reviewed separately from their success logs. The existing eight-stage verification suite was rerun before editing. An additional checker now verifies the expanded appendix tables, a complete worked Sylvester determinant, the coordinate-gcd coverage reduction, the finite-group stabilizer convention, prime-by-prime torsion bounds, a short squarefreeness witness, and the explicit reconstruction collision table.

No new counterexample or result-level failure was found in either main theorem. Several statements needed mathematical precision or clearer attribution of what a calculation proves. Those changes are listed below. Theorems 1.1 and 1.2 retain their stated scope; no new exponent range or whole-orbit exclusion has been added.

This is an exact computational and mathematical review, not a proof-assistant formalization, independent human peer review, or a historical-novelty certificate. Conjecture 7.3 remains unproved. External references were checked to the extent recorded in the citation-audit addendum; a metadata or abstract check is not described as reading a complete source.

## Changes to the main argument

1. **Order of quantifiers in Lemma 2.5.** The assertion is now: for *each* center prime, at least three lines are full-depth. Those three lines may depend on the prime. A common triple for every prime is not claimed. The original proof already argued one prime at a time.
2. **The forty D1 exclusions.** The abstract and introduction now distinguish the sixteen immediate zero-offset cases from the twenty-four cases excluded using three elliptic descents. It was imprecise to attribute all forty to the descents.
3. **Integer domains.** The normal-form bounds and deficiencies are explicitly integers; the Gaussian indexing vectors are explicitly in the integer lattice. The fixed factorization has distinct primes congruent to one modulo four and positive exponents.
4. **Offset terminology.** The introduction now defines an offset using the larger entry of an opposite pair. It does not imply that both entries of a pair lie above the center. The factor `2pq` is still four times ordinary triangle area.
5. **Gaussian legs.** The absolute real and imaginary parts of the representative are specified as the triangle legs. Units and conjugation account for signs and leg interchange.
6. **Projective circle coverage.** The inverse parameter `Im(z)/(1+Re(z))` and the exceptional point `z=-1` are explicit. No rational point is silently excluded by an affine half-angle chart.
7. **Kernel normalization.** The cross-product divisor and kernel vector have a fixed record normalization; coprimality is stated over `Q[r]`. Polynomial gcd one implies that the three kernel entries do not vanish together at an unhandled parameter.
8. **Descent conventions.** The descent map at an ordinary point is its x-coordinate modulo rational squares. The primitive covering equation now explicitly requires `gcd(U,V)=1`.
9. **Torsion reduction.** The order-four bound is explained prime by prime, using prime-to-p injectivity only. The argument does not assume full torsion injectivity at a prime dividing the torsion order.
10. **Squarefreeness and infinity.** A coprime factorization modulo five supplies a short check of the genus-five polynomial's squarefreeness. An explicit smooth infinity chart distinguishes the two points at infinity from the single base parameter value.
11. **Converse nondegeneracy.** Every pairwise sum and difference of the four reconstructed offsets is now displayed. The proof checks that an extra curve point gives a genuinely admissible sine configuration, not just a solution of the linear relations.
12. **Proof data.** The appendix explains polynomial encodings, assignment tuples, local record-number conventions, removed components, and a complete worked elimination. A reader need not interpret a pass flag as a proof.

The generative-AI disclosure is unchanged from the user's revised version. No author, affiliation, reviewer, publication DOI, or new novelty claim was supplied.

## Result-by-result review

The labels below refer to the revised article. A successful computation is used only for the finite assertion it actually checks; general implications have written proofs.

| Result | Review and evidence | Disposition |
|---|---|---|
| Theorem 1.1 | Followed integer-square source through full-depth restrictions, complete normal-form coverage, all signed assignments, exact resultants, modular witnesses, and all finite/projective boundary fibers. Both existing implementations rerun. | Retained; exponent sum at most seven only. |
| Theorem 1.2 | Checked the D1 kernel reduction, both square conditions, complete quartic exclusions, conic parametrization and inverse, genus-five pullback, rational reconstruction, and all nondegeneracy exceptions. | Retained as an existence equivalence, not a bijection or a complete point list. |
| Lemma 2.1 | Recomputed eight magic sums and all 36 pairwise entry differences. Their eight distinct linear zero sets match the displayed degeneracy polynomial. | Retained. |
| Proposition 2.2 | Checked parity, integer legs, the AP identities, reverse construction, unequal legs, positivity, and distinct offsets. | Retained for a fixed positive integer center root. |
| Lemma 2.3 | Modulo-four and nonsquare-minus-one arguments force a common root divisor at every prohibited center prime. | Retained with primitive-root hypothesis. |
| Proposition 2.4 | Reviewed Gaussian unique factorization, units/conjugation, the axis exception, pairwise indexing, common leg divisors, and the finite count. | Lattice and prime domains made explicit. |
| Lemma 2.5 | Checked coprimality with a primitive hypotenuse, both valuation cases, the odd-prime minimum argument, and primitivity forcing the minimum to be zero. | Quantifier order clarified. |
| Corollary 2.6 | There is one full-depth projective triangle for a prime-power root; three distinct ones are necessary. | Retained as an arithmetic statement. |
| Lemma 2.7 | Two size-at-least-three full-depth subsets of four lines meet in at least two; only two fully extremal projective vectors exist. The deficiencies cannot coincide. | Retained. |
| Lemma 3.1 | Reviewed the half-sum/half-difference argument with arbitrary sine signs. Compared the 48 row spaces with all 192 fully signed assignments. | Retained. |
| Theorem 3.2 | Recomputed both trigonometric identities and all six residual polynomials; verified each nonvanishing condition under a>b>0 and a!=2b. | Retained over real angles. |
| Corollary 3.3 | Substitution of frequency linear forms gives the real-circle obstruction; the semiprime normal form is exactly a parallelogram. | Retained; Brown's arithmetic antecedent remains credited. |
| Lemma 4.1 | Forward integer circle powers preserve rational points and the actual sine magnitudes; all stated sign/permutation operations are reversible. | Retained without rational surjectivity assumption. |
| Lemma 4.2 | Reran 2,064 equation-pair certificates: exact division, nonzero determinant, complete factor products, rational-root exclusions, and degree-bounded determinant identity checks. | Retained; removed t=0 branches handled separately. |
| Corollary 4.3 | Coordinate-gcd reduction maps every original solution forward to the reduced rational-circle configuration. | Retained; does not exclude all large signatures. |
| Proposition 5.1 | Independently enumerated 13 projective vectors, 715 four-subsets, 177 admissible sets and 15 disjoint orbits. Stabilizers checked in the full order-48 group. | Retained as combinatorics, not a rational-point classification. |
| Lemma 5.2 | All four signed frequency identities and determinants checked. Unimodular inverse distinguished from determinant-two forward maps. | Retained. |
| Lemma 6.1 | All 48 relation matrices, kernel products, divisors and two norms rechecked; counts and exceptional factors match. | Retained with explicit normalization convention. |
| Proposition 6.2 | Complete signed-squareclass candidate sets, real obstructions, both primitive local charts, rank formula, good-prime counts, torsion bound and exhibited points checked. | Retained; complete quartic lists do not rely on a finite-height search. |
| Corollary 6.3 | Sixteen zero-offset cases plus 24 quartic exclusions leave eight records, with reciprocal residual pairs correctly rescaled. | Retained; count attribution corrected. |
| Lemma 7.1 | Expanded factor and pullback identities; independently checked squarefreeness modulo five; applied Riemann-Hurwitz and explicit smooth infinity chart. | Retained; eight points only over specified base parameters. |
| Corollary 7.2 | It is conditional on C(Q)=K. The exact D1 equivalence and the three forward transfer maps give the conclusion. | Conditional form retained. |
| Conjecture 7.3 | No completeness proof is present; no verified result uses it. | Explicitly unproved. |

## Numbered-equation review

All 29 numbered equations in the revised article have been reviewed, including the two new appendix identities. Unnumbered supporting displays are covered by the result reviews and appendix checks above.

| Equations | Content and check |
|---|---|
| (1)-(2) | Four-offset admissibility and the integral two-parameter normal form. Distinctness restrictions and integer quantifiers are explicit. |
| (3)-(5) | D1 canonical sine system, exact genus-five polynomial, and eight specified projective points. No completeness inference. |
| (6) | Lucas degeneracy polynomial; all pairwise difference factors recomputed. |
| (7)-(9) | Gaussian norm representative, area-angle square, and offset identity `Im(Z_m^2)`. Squaring doubles the leg angle exactly once. |
| (10) | Complete signed role equations with arbitrary individual sine signs. |
| (11)-(12) | Product and sum-of-squares sine identities; six-case residual argument checked. |
| (13)-(14) | Projective rational-circle parametrization, inverse exception and homogeneous numerator. Denominator is positive on real projective points. |
| (15)-(16) | All four cleared-denominator sine numerators and universal collision identity. Reconstructed by separate implementations. |
| (17)-(18) | Explicit ordered frequency matrices and integer transfer matrices, including signs and determinants. |
| (19)-(20) | D1 linear matrix and both rational-square normalization conditions; first norm is nonzero for a unit-circle solution. |
| (21)-(22) | Classical 2-isogeny rank relation and primitive covering equation. Standard arithmetic premises remain cited; local exclusions independently checked. |
| (23)-(24) | Reciprocal residual square systems and conic parametrization with its rational inverse and exceptions. |
| (25)-(27) | Three reconstructed circles, polynomial norm identity and four signed offsets; all twelve pairwise comparisons checked. |
| (28) | New explicit four-by-four Sylvester determinant, factor product and complete modular no-root witness. |
| (29) | New modulo-five factorization; factors individually squarefree and pairwise coprime. |

## Appendix changes

**Appendix A** now gives the coordinate-gcd reduction, all raw/direct/system counts, all 43 directly certified representatives with their actual resultant degrees and rational-fiber sets, certificate conventions, and a complete worked elimination.

**Appendix B** now gives compact ordered vectors and explicitly states the order-two kernel of the full signed-permutation action. Stabilizer conventions and the distinction between classification and exclusion are explained.

**Appendix C** now derives the primitive covering equation, displays all relevant square classes and both local charts, lists the full square-residue sets modulo 16 and 64, and proves the torsion bounds primary component by primary component.

**Appendix D** now identifies every D1 normalization record, gives a worked kernel, treats rank-drop and projective exceptions, supplies a short squarefreeness witness, and lists all reconstruction collisions.

The new `review_math.py` regenerates five appendix tables from exact checked data and, in verification mode, requires the printed files to match. It is an additional check, not a substitute for the two original main-certificate acceptance implementations.

## What the review does not establish

It does not classify all rational points on the residual genus-five curve, solve the unrestricted magic-square problem, establish historical priority, audit all stronger claims in another archive, or provide independent human peer review. It does not enlarge the focused paper's theorem scope. The older research record is retained as provenance and is not silently reinstated as part of the focused article.

## Reproduction

From the package root:

```sh
python -m pip install -r requirements.txt
python verify_paper.py
```

This runs nine stages in separate temporary copies. The added `review_math.py` stage has eight check groups. The existing two-prime and D1 proof records are unchanged; an exact before/after hash comparison is included. All limitations in the citation audit remain explicit.
