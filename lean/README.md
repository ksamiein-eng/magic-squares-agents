# Lean formalization: status and candidates

Nothing in this repository is formalized in Lean today. This directory exists so that the fact is explicit,
in the way `openai/math` states which of its results carry Lean proofs (about 42% at release) and which do not.

`formalization.yaml` lists every top-line result with its precise statement, the Mathlib dependencies a
formalization would need, an estimated difficulty, and a priority. The two elementary results produced on
22 October 2026 (the trichotomy on a signed system and the degeneracy relations) are low-difficulty targets
and are the natural first formalizations; the certificate theorem needs a verified checker rather than a
verified certificate.

Playbook: `playbooks/formalize-in-lean.md`.
