# Reproducibility bundle — magic squares of squares paper

Recovered and re-verified 2026-10-01 after the working container was reset. Everything here is
durable (outputs folder). Run order:

1. `python3 verify_all.py`  — independent re-verification of every load-bearing claim (24 checks,
   written fresh, not derived from the pipeline). All PASS as of 2026-10-01.
2. `python3 certify.py <ORBIT>...` — regenerates the per-system certificate `certs/<ORBIT>.json`
   (Appendix A format). Uses the parametrization t_j = tan(chi_j/2), exponent 2|m_j| — this IS the correct area-angle
   relaxation (Appendix B). A '4|m_j|' variant tried earlier is a degree-2 COVER (T=2t/(1-t^2) is not
   birational) and is retired; nothing depends on it.
3. `python3 section81.py` — derives the four linear ell of Section 8.1.

## Pipeline (recovered verbatim from the session transcript, patches applied in order)
- `setup.py`   — E(m) area polynomials, the 17 configuration labels (= 15 orbits), the 48 systems.
- `pipe3.py`   — projection / factorization / linearization / quotient (valid_Bs) / point-lifting.
- `certify.py` — certificate writer (reconstructed from this session's record).
- `gamma.py`, `fplus.py` — Gamma-curve genera for the nonlinear orbits D2, D4, F+1, F+2.
- `twoprime.py` — Theorem C elimination.

## Certificate status
Regenerated and matching original counts exactly: ALL 17/17 (completed 2026-10-01).
  A B1 B2 C D1 D2 D3 D4 E1 E2 E3 E4 F+1 F+2 F-1 F-2 F-3
Duplicates confirming the 15-orbit classification: E3 == E4, F-1 == F-3 (identical counts).

4. `python3 linrel_exact.py F-1 F-3` — Lemma 5.4: exact function-field proof that all 16 linear-relation
   components are degenerate (self-contained: vanishing line read off the gcd root). DONE 2026-10-01, 16/16 PROVED.

## Also to re-run (scripts to be reconstructed from the session record)
- sieve certificates (sieves_cubic.json exists in ../chabauty_inputs; rank-2 sieve record to regenerate).
- saturate.py : full saturation table (verify_all.py covers E_A..E_D).

Chabauty inputs for the six bounded orbits are in `../chabauty_inputs/`.

## Regenerating the typeset manuscript
`paper/paper.md` is the manuscript source (formulas as LaTeX in code spans, mirroring the shared doc);
`paper/md2tex.py` converts it with pandoc using `paper/template.tex`; then run pdflatex twice.
Last regenerated 2026-10-01 after the external audit (20 pages): real-angle Theorem B, E1 closed a priori,
E_B/E_C resolved as quotients of one genus-2 curve, f(1)=8f(0) criterion, corrected sieve bound and Hermite
constant, corrected Appendix B (cover, not birational), novelty rewritten, Auel-Singer/Weisenberg/Cain cited. The shared doc remains the editable master.
