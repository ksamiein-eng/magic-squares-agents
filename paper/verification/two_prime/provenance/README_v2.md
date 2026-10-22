# Magic squares of squares: verified core, version 2

This release extends the previously certified (2,1) case to (3,1) and (2,2).
For a primitive 3-by-3 magic square of nine distinct positive integer squares
with central root y = p^k q^l, p and q distinct primes, the supported conclusion
is now k+l >= 5. Here the actual central entry is y^2.

## Read first

`verified_core.pdf` is the 15-page working manuscript; `verified_core.tex` is its
editable LaTeX source. Section 6 contains the new proofs and Section 6.4 gives
uniform pruning rules for later exponent pairs. The earlier full manuscript's
claims about exponent sums through seven, other three-prime closures, and
large canonical-height bounds are NOT certified by this release.

No first-in-literature claim is made. A checked computational theorem, a
shorter proof, and a historically novel theorem are different claims.

## Verify without third-party packages

From this directory, with Python 3.10 or newer:

```bash
python verify_degree4_stdlib.py
```

The checker is self-contained and reads `results/certificate_degree4.json`.
It uses only Python's standard library. No Sage, PARI, Magma, network access,
hidden temporary file, numerical root approximation, or factorization package
is needed. It does not import the producer.

The checker reconstructs every sine numerator, checks 48 signed row spaces
against 192 unrestricted signed assignments, verifies every resultant and
factor-product identity, checks modular no-root witnesses, and verifies the
finite fibers and the two projective boundary lines. It derives coverage of
all 18 raw full-depth configurations of (1,1), (2,1), (3,1), (2,2).

Determinant identities are checked at D+1 exact integer values AFTER proving
both sides have degree at most D. This is an exact identity test, not a bounded
search or a random-evaluation heuristic. There are 6,096 integer determinant
evaluations, 240 systems, and 130 non-linear no-root catalog entries. The
witness primes are 3, 5, 7, and 11. Four representatives (192 systems) are new;
the other 48 systems reverify the (2,1) baseline.

For corruption guards and small arithmetic regressions:

```bash
python test_degree4_verifier.py
```

## Independent symbolic cross-check and optional regeneration

With the pinned SymPy version from `requirements.txt`:

```bash
python crosscheck_degree4_sympy.py
python check_foundation.py
# Optional discovery/regeneration:
python build_degree4_certificate.py
python verify_degree4_stdlib.py
```

The symbolic checker reconstructs the sine formulas using Chebyshev
polynomials and computes the Sylvester determinants symbolically over ZZ[t].
It does not call a resultant, factorization, or rational-root routine for
acceptance. The producer does use SymPy factorization to discover a proof
object. Its generation summary deliberately reports only the generation
phase; the independent verification logs report acceptance.

## Proof data

- `results/certificate_degree4.json`: all five representatives, 240 systems,
  original and reduced polynomials, removed factors, resultants, factor
  references, and modular witnesses.
- `results/verification_degree4_stdlib.json`: complete successful verification,
  including derived finite-fiber, boundary, and normal-form coverage records.
- `results/crosscheck_degree4_sympy.json`: successful symbolic cross-check.
- `results/degree4_factor_catalog.md`: all 133 factors (130 non-linear and three
  linear), exact coefficient encodings, and modular residues.
- `results/degree4_systems.csv`: every system and its factor references.
- `results/degree4_mutation_tests.json`: rejection of ten altered certificates
  and one unsupported finite-fiber claim, plus 180 Bareiss/Leibniz regressions.
- `results/next_sum5_plan.json`: coverage plan only; no sum-five exclusion is
  claimed. It leaves six representatives to compute.
- `results/clean_extraction_verification.json`: successful verification from a
  newly extracted release archive.

The previous (2,1) producer, two verifiers, catalog, and logs are retained as
baseline evidence. `results/configurations_2prime_sum7.json` gives configuration
counts only; it is NOT a solution of those systems.

## Proof boundary

The written integral dictionary, primitive full-depth lemma, signed-system
lemma, real-angle theorem, and one-way circle-power lemma explain why the
checked polynomial identities imply the stated arithmetic exclusions. The
checker is not a formal proof-assistant development: Python and the checker
implementation remain within the software trust boundary. No complete
rational-point classification of the genus-two covers is asserted.

Use `sha256sum -c SHA256SUMS` to check release-file integrity. Input hashes in
`INPUT_SHA256SUMS` identify the prior uploaded v1 artifacts; they are provenance
records, not files expected to live inside this release directory.

The producer uses the polynomial operations documented in the official SymPy
1.14 reference: https://docs.sympy.org/latest/modules/polys/reference.html.
Full mathematical references and attribution are in the manuscript.
