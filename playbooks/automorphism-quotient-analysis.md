# Playbook: automorphism and quotient analysis

**Applies when** the ledger entry is "the known rational points of curve X are all of X(Q)" and the
paper has not written down the automorphism group of X.

**Inputs.** The curve's equation; the known points; a CAS for identities (SymPy suffices); access
to the LMFDB for elliptic-curve identification.

**Steps.**
1. Look at the polynomial: even, palindromic, or both ⇒ involutions h → −h, h → 1/h. Write the
   invariant functions and the quotient equations; verify every identity symbolically.
2. Descend until elliptic curves appear (genus 2 bielliptic ⇒ two elliptic quotients). Put each
   in integral Weierstrass form by moving a rational root to infinity.
3. Map the known points down. Test them for torsion by exact point arithmetic: on an integral
   model a torsion point has integer coordinates (Nagell–Lutz), so one non-integral multiple
   proves infinite order and hence rank ≥ 1. This step is PROVED, not quoted.
4. Identify each curve in the LMFDB by j-invariant, then confirm the isomorphism exactly by
   c₄/c₆ scaling (a twist has the same j and is a different curve: this bit the first attempt).
   Quote the database rank as DATABASE-QUOTED.
5. Decide the method: any rank-0 quotient ⇒ elementary closure (pull back a finite set). All
   quotients rank ≥ 1 ⇒ classical Chabauty needs rank Jac < genus on some quotient; otherwise
   quadratic Chabauty (bielliptic genus 2 of rank 2 is the Balakrishnan–Dogra case) or elliptic
   Chabauty over the field where the cover splits.
6. State the independence argument when adding ranks (distinct j-invariants and conductors ⇒
   pairwise non-isogenous ⇒ ranks add in the Jacobian).

**Acceptance.** Every identity verified in a CAS; every rank ≥ 1 witnessed exactly; every database
fact tagged; the method decision written as a Chabauty-readiness memo with the concrete inputs.

**Best tag.** PROVED for the obstruction or (with a rank-0 quotient) for closure; the route itself
stays CONJECTURAL until computed.

**Failure modes.** Twist confusion; using Nagell–Lutz on a non-integral model; adding ranks of
isogenous curves; forgetting that a point on a quotient need not lift.
