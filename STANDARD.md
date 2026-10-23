# A verification standard for AI-assisted mathematics (v0.1)

**Purpose.** Let a reader, a referee or another agent decide in minutes what each claim in an
AI-assisted paper rests on, re-run it, and see every correction. The standard is a checklist of
ten requirements and a machine check (`tools/standard_check.py`) that a repository either passes
or fails. It was extracted from this repository's practice and is written to be reused by any
paper, on any problem, with any model.

The underlying principle: **a result is worth exactly its evidence, and the evidence must be
legible without trusting the author or the model.**

## The ten requirements

| # | Requirement | What counts | Where it lives here |
|---|---|---|---|
| R1 | **Tagged claims.** Every mathematical claim carries one tag from a fixed vocabulary: PROVED (written argument, checkable by a reader), MACHINE-VERIFIED (an independent checker, distinct from the producer, accepted it in this repository), DATABASE-QUOTED (a fact taken from a database or the literature and not re-proved), SEARCH-EVIDENCE (a bounded computation that found nothing), CONJECTURAL. | No untagged claim in the report, the README or the ledger; tags never upgraded without new evidence. | `ledger/attacks.json`, `docs/RESULTS.md`, `README.md` |
| R2 | **Producer / checker separation.** Anything tagged MACHINE-VERIFIED was accepted by a checker that shares no code with the producer, ideally standard-library only, and the checker's report is committed. | Checker report file present; the producer is not imported by the checker. | `agents/certificate_extender/verify_degree*_stdlib.py`, `results/verification_degree*_stdlib.json` |
| R3 | **Fresh referee.** A reviewer distinct from every producer re-runs at least one computation per result, assigns the tags, and records a verdict table with the corrections it demanded. | Verdict file(s) present, each naming what was rerun. | `results/skeptic_verdict*.md` |
| R4 | **One-command reproduction.** A single command re-runs every machine-checkable claim and writes a report with per-stage pass/fail. | The latest report exists and all stages pass, or the failures are listed in the status file. | `verify_findings.py`, `verify_paper_plus.py`, `results/*_latest.json` |
| R5 | **The paper's own suite is the source of truth.** New results are added as stages of the paper's existing verification suite, never by editing the paper's shipped proof records. | The original tree is byte-identical (hashes); the overlay lists added stages. | `paper/SHA256SUMS`, `paper_overlay/stages.json` |
| R6 | **Verbatim traces.** The full transcript of every AI run that produced a claim is published, with a hash, unedited except for personal data. | One trace per agent run, listed with hashes in the provenance file. | `traces/`, `PROVENANCE.json` |
| R7 | **Claim map.** Each claim is linked to the trace turn that produced it, the command that re-checks it, and the evidence file. | A table with one row per claim and no empty cells. | `CLAIM_MAP.md` |
| R8 | **Versioned history with corrections.** Every release and every correction is recorded; corrected statements are not silently overwritten. | A history file whose rows include the corrections, including the model's own refuted guesses. | `HISTORY.md` |
| R9 | **Formalization status stated.** For every top-line result, whether it is formalized in a proof assistant, and if not, the exact candidate statement and expected difficulty. | A catalogue with a `status` field per result; "0% formalized" is an acceptable, explicit answer. | `lean/formalization.yaml` |
| R10 | **Disclosure, licence, citation.** The role of AI systems is stated in the paper; authors take responsibility; licences for code and text are explicit; a citation file exists. | Disclosure sentence in the manuscript; LICENSE files; CITATION.cff. | `paper_update/manuscript/paper.tex`, `LICENSE`, `LICENSE-PAPER`, `CITATION.cff` |

Two consequences of the standard that matter for trust:

* A claim can only move *down* the tag ladder without new work (the referee's job), and only *up*
  with a new artefact (a checker report, a written proof, a formal proof). The ladder makes the
  difference between "the model says" and "a reader can check" visible in every sentence.
* Failures are first-class. A refuted guess, a wrong overflow guard, a database rank used as a
  proof: each is recorded in the history and in the referee's table, because a standard that
  only records successes cannot be trusted on the successes either.

## Machine check

```bash
python tools/standard_check.py          # prints one line per requirement, PASS/FAIL, and writes results/standard_check.json
```

The checker verifies the presence and shape of each artefact (R1 vocabulary, R2 checker reports,
R3 verdict files, R4 latest reports all passing, R5 original hashes unchanged, R6 traces hashed in
the provenance, R7 claim-map rows complete, R8 history rows with corrections, R9 catalogue with
status fields, R10 disclosure, licences and citation). It cannot judge mathematics; it judges
whether the mathematics is checkable.

## How to adopt it for your paper

1. Keep your paper and its verification code in `paper/` with a hash list; never edit them from an agent.
2. Create `ledger/open_problems.json` with your open targets, each typed; pick a playbook per type (`playbooks/`).
3. Run agents in exclusive directories; export every transcript with `tools/export_traces.py`.
4. Have a fresh agent (or a person) write the verdict table and assign tags; run `tools/tag_lint.py`.
5. Register accepted results as overlay stages; run `verify_paper_plus.py`; regenerate `PROVENANCE.json`.
6. State formalization status per result in `lean/formalization.yaml`; record every correction in `HISTORY.md`.
7. Run `tools/standard_check.py` and ship its report with the paper.

Version 0.1, 22 October 2026. Proposed by Kimia Samieinejad and Jonathan Wolinski. Comments and
counter-examples welcome in the repository's issues.
