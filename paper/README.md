# Rational-circle obstructions and a genus-five reduction

This package contains a focused article and the proof records supporting it. The main manuscript is `manuscript/paper.pdf`; the editable source is `manuscript/paper.tex`. This is an author-review draft, not a claim of independent human peer review or a final historical-priority assessment.

## Mathematical scope

The article proves the exclusion of the specified two-parameter rational-circle normal forms through exponent sum seven, and the exact equivalence between admissibility of the D1 configuration and an additional rational point on the displayed genus-five curve. It gives explicit integer-torus transfers. The conjecture that the eight known genus-five points are complete is **not** assumed or proved. The paper does not solve the unrestricted magic-square problem.

The broader 43-page research record is retained under `research_record/`. Its nonlinear genus calculations, auxiliary orbit closures, and elliptic height results were not silently erased; they were left outside the main article to give the submission a coherent scope. The full verification trees are retained for traceability.

## Read and edit

- `manuscript/paper.tex`: main text and proofs.
- `manuscript/references.bib`: portable BibTeX bibliography.
- `manuscript/references.tex`: the same bibliography in directly compilable form.
- `editorial/references.json`: bibliographic metadata and the scope of the source checks.
- `editorial/CITATION_AUDIT.md`: what was checked and what remains uncertain.
- `editorial/CLAIM_MAP.md`: main claims and their proof dependencies.
- `editorial/MATHEMATICAL_REVIEW.md`: result-by-result and equation-by-equation proofread.
- `editorial/PROOFREAD_CHANGES.json`: substantive source edits.
- `review_math.py`: exact appendix tables and additional mathematical checks.
- `editorial/EDITORIAL_NOTES.md`: selection decisions and remaining submission tasks.

The TeX source uses `references.tex`, so building does not need BibTeX. To switch to a journal's bibliography style, replace that input by the journal's bibliography commands and use `references.bib`. No font files are bundled.

## Reproduce the focused article

Python 3.11 or later is expected. Install the pinned symbolic dependency:

```sh
python -m pip install -r requirements.txt
python check_paper.py
python verify_paper.py
```

`verify_paper.py` runs nine stages, including the two different two-prime checking implementations, D1 arithmetic and symbolic checks, corruption tests, and a separate torus row-space check. Every stage uses an independent temporary copy; shipped proof records are not modified. Do not disable assertions with `python -O`.

The certificate acceptance commands with no third-party packages are:

```sh
cd verification/two_prime
python verify_degree7_stdlib.py
cd ../d1_norm
python verify_d1_stdlib.py
```

These smaller commands are not a substitute for the full focused suite. Some old standalone verifiers write reports in their working directory; the root wrapper avoids this by using temporary copies.

`verification_runs/prior_full_suite/report.json` records the rerun of all 24 stages of the preceding research package before the rewrite. That run is not confused with the eight-stage suite shipped with the input. The current focused-paper suite has nine stages. The author should review the mathematical implications, not only the success flags.

## Build the PDF

A TeX installation with `pdflatex`, Latin Modern, AMS math packages, `mathtools`, `booktabs`, `array`, `longtable`, `microtype`, `geometry`, `xurl`, `hyperref`, and `fancyhdr` is sufficient:

```sh
python build_paper.py
```

The build runs three passes and writes `manuscript/paper.pdf`. It rejects unresolved references and overfull boxes. It does not perform optical layout review; the delivered version was rendered and inspected separately.

## Integrity, attribution, and responsibility

`SHA256SUMS` records the shipped bytes. A matching hash is evidence of byte identity, not mathematical truth. The bibliography credits the common-hypotenuse formulation, the circle-group relaxation, prime-signature organization, Gaussian approaches, and the overlapping valuation argument to the relevant sources. In particular, Houston's 2016 P4/W1 formulation is included; the relaxation itself is not advertised as new.

The article retains the requested disclosure of ChatGPT and Claude use for symbolic/computational work, verification code, and exposition. It does not characterize that work as grammar-only assistance, and it does not invent human review, funding, affiliations, or author identities. Before submission, the human author(s) must supply the author information, take responsibility for all claims, choose the dissemination license and journal, and create the stable public archive reference for the exact companion release. No repository DOI has been fabricated.

## Mathematical proofread, 5 October 2026

The main results are unchanged. The appendices now include a complete worked elimination, all 43 direct cases, full-group stabilizer conventions, explicit local descent and torsion arguments, and the D1 exceptional-point checks. The original verification tree is byte-for-byte unchanged; the added ninth stage verifies the new appendix material. `review_math.py --write-tables` deliberately regenerates five tables; ordinary verification rejects a mismatch instead of rewriting them.


## Added 7 October 2026: Section 8 (rational-circle rigidity)

`manuscript/rigidity.tex` states the rigidity conjecture, Proposition 8.2 (complete four-parameter search at projective heights 3 and 4 — 0 and infinity included, free-angle families decided exactly — zero admissible points) and Theorem 8.3 (all 48 Hadamard solution surfaces are of general type, p_g=11, q=0, K^2=32). Verification lives in `verification/four_prime/`:

- `r4search.py H [START END]` — the exhaustive sweep (checkpoints in `results/`); `results/r4_H3_final.json`, `r4_H4_final.json` are the completed projective sweeps. `r4_H5_affine_legacy.json` is an earlier finite-chart sweep that omitted 0/infinity and the free-angle branch; it is kept for the record and not relied on.
- `verify_hadamard_types.py {I,II,III,IV,all}` — asserts every branch-geometry hypothesis of Theorem 8.3 (bidegrees, reducedness, nodes only, no triple points, nodes off the other divisor, transversal or simple tangency).
- `general_type_check.py` — the Q(i)-splitting for type I and the two independent invariant computations.
- `branchcheck.py`, `branchfine.py` — exploratory classification scripts (not part of the acceptance path).

`python verify_paper.py` now runs 15 stages; `--skip-four-prime` runs the original nine. **Section 8 has not yet had an independent second audit.**

**Referee pass, 8 October 2026.** A line-by-line review of Section 8 and its code found one real completeness gap (the free-angle branch of the sweep, now handled exactly) and six statement-level corrections; see `STATUS.json` → `referee_pass_8_october`.

**Second referee pass, 13 October 2026.** Fixed an impossible intersection count in the proof of Theorem 8.3 (type II: 16 tangencies, no transversal points) and the 'finite map' wording (torus isogeny → generically finite rational map); added the weak form of the conjecture and the torsion-coset hypothesis (Conjectures 8.5, 8.6). See `STATUS.json`.

**Archive audit (13 October 2026).** `verification/archive_audit/archive_checks.py` reproduces the computational part of our audit of the public Magic Squares of Squares archive (every elliptic curve the block-balance, two-prime, hourglass and three-prime notes rely on, with ranks, torsion and claimed point sets, plus the key identities). It is stage 16 of `verify_paper.py`. The abstract, the remark after Theorem 1.1, Section 8 and Conjecture 7.3 were reframed accordingly; see `STATUS.json`.
