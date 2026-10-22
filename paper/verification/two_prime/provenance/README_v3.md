# Magic squares of squares: verified core, version 3

This release completes exponent pairs (4,1) and (3,2), adding 288 new signed
systems to the 240 checked in version 2. For a primitive 3-by-3 magic square
of nine distinct positive integer squares with central root y = p^k q^l,
where p and q are distinct primes, the supported conclusion is k+l >= 6.
The central entry is y^2, not y.

## Read first

`verified_core.pdf` is the 18-page working manuscript; `verified_core.tex` is
its editable LaTeX source. Section 7 contains the six new calculations and
proofs. Corollary 7.5 gives a compact exclusion criterion for arbitrary
exponents, using the reduced denominators of m/k and n/l.

The original full manuscript's exponent-sum-seven claim, remaining
three-prime closures, genus classifications, elliptic ranks, saturation, and
large canonical-height bounds are NOT certified by this release. No
first-in-literature claim is made. These are checked computer-assisted
proofs of the specified range, not a formal proof-assistant development.

## Verify with Python's standard library

From this directory, with Python 3.10 or newer:

```bash
python verify_degree5_stdlib.py
```

The self-contained checker reads `results/certificate_degree5.json`. It does
not import the producer or require SymPy, Sage, PARI, Magma, network access,
or hidden temporary files. It reconstructs the sine numerators; checks all
48 signed row spaces against 192 unrestricted signed assignments; checks
resultant and factor-product identities; verifies every modular no-root
witness; and excludes the finite fibers and projective boundaries.

All 40 raw full-depth normal forms through exponent sum five are covered:
six parallelograms, 22 symmetry-equivalent direct-certificate routes, and
twelve explicit circle-power pullbacks. The certificate has 528 systems and
274 catalog entries: three linear factors and 271 nonlinear factors with
no rational root. Witness primes are 3, 5, 7, 11, and 13.

The checker proves a degree bound D before checking each determinant at D+1
integer values. There are 18,480 exact integer determinant checks. This is
a polynomial identity proof, not random evaluation or a finite-height search.
Every possible finite rational t is 0 or +/-1 (the old (2,2) rows need only
0). Each allowed fiber is degenerate; both projective boundaries are also
excluded.

Corruption tests and arithmetic regressions:

```bash
python test_degree5_verifier.py
```

## Separate symbolic checking and optional regeneration

With the pinned version in `requirements.txt` (SymPy 1.14.0):

```bash
python crosscheck_degree5_sympy.py
python check_foundation.py
# Optional certificate discovery/regeneration:
python build_degree5_certificate.py
python verify_degree5_stdlib.py
```

The symbolic checker independently reconstructs the sine formulas using
Chebyshev polynomials and computes Sylvester determinants directly over
ZZ[t]. It also verifies all finite-fiber and projective degeneracy identities,
and proves normal-form coverage via coordinate gcd normalization. It does
not call a resultant, factorization, or rational-root solver for acceptance.
The producer DOES use SymPy factorization to discover the proof data. Its
summary says GENERATED_NOT_YET_INDEPENDENTLY_VERIFIED because that file
records generation only; the subsequent verification files record PASS.

## Proof objects and results

- `results/certificate_degree5.json`: complete combined certificate.
- `results/verification_degree5_stdlib.json`: complete verification record,
  including all finite-fiber, boundary, and normal-form witnesses.
- `results/crosscheck_degree5_sympy.json`: separate symbolic check.
- `results/degree5_release_summary.json`: concise scope and result summary.
- `results/degree5_factor_catalog.md`: every factor and modular witness.
- `results/degree5_systems.csv`: all 528 assignment/factor records.
- `results/baseline_preservation_v3.json`: exact preservation of the old five
  cases and the old factor-catalog prefix in the new certificate.
- `results/degree5_mutation_tests.json`: ten corrupted-certificate rejections,
  an unsupported-fiber rejection, and 180 Bareiss/Leibniz determinant tests.
- `results/next_sum6_plan.json`: proposed coverage ONLY; those 672 systems
  have NOT been eliminated in this release.
- `results/clean_extraction_verification_v3.json`: clean-extraction check.

The old degree-four and (2,1) certificates, scripts, and logs are retained as
baseline evidence. `results/next_sum5_plan.json` is the historical v2 plan,
now completed by this release; it is not the current completion status.
Likewise, `results/configurations_2prime_sum7.json` records enumeration only,
not an exclusion of those systems. Historical manifests and notes in
`provenance/` describe the prior release, not the current one.

## Integrity and proof boundary

```bash
sha256sum -c SHA256SUMS
```

This checks current release files. `INPUT_SHA256SUMS` identifies the supplied
v2 artifacts; those input hashes are provenance, not paths expected inside
this directory. The original user attachments remain unchanged.

The written integral dictionary, primitive full-depth argument, signed-system
lemma, real-angle theorem, and forward circle-power lemma justify the
arithmetic reduction. A passing checksum is not a mathematical proof; the
proof consists of those arguments and the checked polynomial identities.
Python and the checker implementations remain within the software trust
boundary. A completed rational-point classification of the genus-two covers
is not asserted here.

Full mathematical attribution is in the manuscript. The producer's polynomial
operations are documented at https://docs.sympy.org/latest/modules/polys/reference.html.
