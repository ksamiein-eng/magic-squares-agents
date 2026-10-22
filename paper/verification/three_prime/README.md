# Three-prime certificate audit and closure of F-2

This is a verification supplement to the supplied magic-squares manuscript, not a
certification of the entire paper. The original 38-file archive is preserved under
`input/` and is never imported or executed by the audit. The PDF and its LaTeX
source are in `paper/`.

## Main outcomes

All 17 orbit certificate files use the corrected area-angle inputs. All 816 signed
systems and their projection factor supports check. Five distinct orbits are
closed: A, E1, E3=E4, F-1=F-3, and F-2. F-2 is closed through the actual recorded
rank-zero quotient route, contrary to the revised manuscript's unresolved
conductor-216 exception. This does not assert that a separate conductor-216 curve
has rank zero.

All eight supplied rank-one sieve residue sets are reproduced. These are subgroup
congruence statements, not certifications of full positive-rank bases or global
canonical-height bounds. All 16 Chabauty point/model pairs are repaired, with
explicit coordinate maps and non-torsion witnesses (rank at least one, not an upper bound or full basis). The supplied drivers contain bounded searches and
commented-out Chabauty calls; no quadratic Chabauty computation was executed.

Ten distinct orbits remain unresolved as full rational-point problems:
B1, B2, C, D1, D2, D3, D4, E2, F+1, F+2. Partial components may be closed even when
their entire orbit is unresolved. The positive-rank basis saturation, rank-two
sieves, and nonlinear smooth-model genus claims remain unverified. The prior
verified core's two-prime bound is unchanged; this release does not certify the
exponent-sum-seven stage.

## Reproduce

Use Python 3.11 or later with SymPy 1.14.0 (the audit ran with Python 3.13.5).
Do not use `python -O`: assertions are part of the acceptance checks.

```sh
python run_audit.py
python test_audit.py
```

An already-extracted copy of the original archive can be used instead:

```sh
python run_audit.py /absolute/path/containing/repro/and/chabauty_inputs
```

The run writes logs and regenerates the audit JSON outputs in the package root.
The input files remain unchanged. The scripts do not need PARI, Sage, Magma,
network access, or an absolute temporary path from the original author's machine.

The small rank-zero certificates can be checked with Python's standard library
alone:

```sh
python verify_rank_zero.py rank_zero_certificate.json
```

The rank-zero generator is optional; normal verification reads and checks the
supplied finite certificate. The classical 2-isogeny descent theorem and the
binary-quartic Jacobian formula used by the proof are stated and cited in the PDF.

## Files and proof boundaries

- `audit_status.json`: combined outcome and precise unresolved scope.
- `projection_audit.json`: 68 numerator checks, 816 systems, factor multiplicities,
  removed-branch witnesses, and complete orbit coverage.
- `quotient_audit.json`: all 600 reconstructed line/discriminant records and
  square-class reductions.
- `component_audit.json`: 532 exact generic component calculations, Bezout
  identities, degeneracy witnesses and exceptions; 16 special linear relations.
- `fiber_audit.json`: 153 finite special fibers, including 3,696 bivariate systems.
- `rank_zero_certificate.json`: seven rank-zero 2-isogeny descent certificates and
  rational torsion upper bounds.
- `rankzero_quotient_audit.json`: complete point counts for 108 direct genus-one
  records and three auxiliary even quotients.
- `lift_audit.json`: 244 complete finite-quotient lifting checks and a status for
  every recorded factor entry. The five orbit closures require *all* upstream
  checks, not this file alone.
- `sieve_audit.json`: exact finite-field constraints and CRT intersections for
  eight rank-one subgroup sieves.
- `chabauty_inputs_corrected.json`: model-compatible points and maps; rank and full
  generation remain reported, not certified. Not a Chabauty result.
- `chabauty_audit.json`: original incorrect pairs and all 16 exact repairs.
- `manuscript_patch.md`: precise changes needed in the full manuscript.
- `real_angle_lemma.md`: the elementary boundary obstruction used by the audit.
- `input_integrity.json`: original ZIP digest and internal manifest comparison.

The original manifest references 30 files; all are present, 29 hashes match, and
only `repro/paper/paper.md` differs from the historical hash. A separate release
manifest protects this audit package. A hash proves byte identity, not mathematical
correctness. Run the checks to verify the mathematical calculations.

## Software trust

This is a computer-assisted proof, not a proof-assistant formalization. The full
pipeline depends on Python and SymPy's exact polynomial arithmetic, factorization,
and rational-root routines. Only the rank-zero descent and rank-one finite-field
sieve layers are standard-library-only. Eleven deliberate certificate corruptions
are rejected by the included tests. These tests do not replace the written proofs.

## Typeset the supplement

```sh
cd paper
pdflatex -interaction=nonstopmode -halt-on-error three_prime_audit.tex
pdflatex -interaction=nonstopmode -halt-on-error three_prime_audit.tex
```

No historical-novelty claim is made. No unsupported broader manuscript claim is
restored by this release.
