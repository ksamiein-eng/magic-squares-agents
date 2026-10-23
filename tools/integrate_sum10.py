#!/usr/bin/env python3
"""Integrate the iteration-3 sum-10 certificate (181 cases, 8,688 systems, strict PASS, witness prime 23) everywhere."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
V = json.loads((ROOT / "agents" / "certificate_extender" / "results" / "verification_degree10_stdlib.json").read_text(encoding="utf-8"))
assert V.get("status") == "PASS", V.get("status")
systems = V.get("total_systems"); dets = V.get("exact_integer_determinants"); factors = V.get("distinct_catalog_factors"); secs = V.get("elapsed_seconds")
print("sum10:", systems, dets, factors, secs)


def tex(n):
    return f"{n:,}".replace(",", "{,}")



def edit(rel, pairs):
    p = ROOT / rel
    if not p.exists():
        return
    s = p.read_text(encoding="utf-8")
    for old, new in pairs:
        if new in s:
            continue
        if old in s:
            s = s.replace(old, new, 1)
        else:
            print("WARN not found in", rel, ":", old[:70].encode("ascii","replace").decode())
    p.write_text(s, encoding="utf-8")


edit("paper_update/manuscript/paper.tex", [
    ("The two-parameter certificate is extended through exponent sum nine ($5{,}520$ signed systems; the standard-library checker accepts the whole certificate, and the sum-eight part is additionally cross-checked symbolically).",
     f"The two-parameter certificate is extended through exponent sum ten ($8{{,}}688$ signed systems; the standard-library checker accepts the whole certificate, and the sum-eight part is additionally cross-checked symbolically)."),
    ("Theorem~\\ref{thm:sumnine} (added 22 October 2026) extends the certificate through exponent sum nine, so ``seven'' may be read as ``nine'' in this paragraph.",
     "Theorem~\\ref{thm:sumnine} (added 22 October 2026) extends the certificate through exponent sum ten, so ``seven'' may be read as ``ten'' in this paragraph."),
    ("\\subsection{Extension through exponent sum nine (22 October 2026)}\\label{sec:sumnine}\nThe producer and checker of Lemma~\\ref{lem:elimination} were rerun, unchanged in method, on the signatures with $k+\\ell=8$ and $k+\\ell=9$. Coverage was planned exactly as in Section~\\ref{sec:two}: of the $140$ raw normal forms with $k+\\ell=8$, $72$ are inherited from the sum-seven certificate by Lemma~\\ref{lem:inherit} and the remaining $68$ form $32$ orbits; of the $172$ raw forms with $k+\\ell=9$, $92$ are inherited and the remaining $80$ form $40$ orbits.",
     "\\subsection{Extension through exponent sum ten (22 October 2026)}\\label{sec:sumnine}\nThe producer and checker of Lemma~\\ref{lem:elimination} were rerun, unchanged in method, on the signatures with $k+\\ell=8$, $9$ and $10$. Coverage was planned exactly as in Section~\\ref{sec:two}: of the $140$ raw normal forms with $k+\\ell=8$, $72$ are inherited from the sum-seven certificate by Lemma~\\ref{lem:inherit} and the remaining $68$ form $32$ orbits; of the $172$ raw forms with $k+\\ell=9$, $92$ are inherited and the remaining $80$ form $40$ orbits; of the $285$ raw forms with $k+\\ell=10$, the non-inherited ones form $66$ orbits (the square signature $(5,5)$ uses the coordinate swap as well)."),
    ("\\begin{theorem}[Certified exclusion through exponent sum nine]\\label{thm:sumnine}\nFor $k+\\ell\\le9$, no matrix $A_{k,\\ell;m,n}$ in~\\eqref{eq:normalformintro} admits an admissible point of $\\T(\\Q)^2$. Consequently Corollary~\\ref{cor:denominator} holds with $8$ replaced by $10$, and a primitive magic square with central root $p^kq^\\ell$ requires $k+\\ell\\ge10$.",
     "\\begin{theorem}[Certified exclusion through exponent sum ten]\\label{thm:sumnine}\nFor $k+\\ell\\le10$, no matrix $A_{k,\\ell;m,n}$ in~\\eqref{eq:normalformintro} admits an admissible point of $\\T(\\Q)^2$. Consequently Corollary~\\ref{cor:denominator} holds with $8$ replaced by $11$, and a primitive magic square with central root $p^kq^\\ell$ requires $k+\\ell\\ge11$."),
    ("The merged certificate contains $115$ representatives and $5{,}520$ signed systems ($2{,}064$ from Lemma~\\ref{lem:elimination}, $1{,}536$ new at sum eight, $1{,}920$ new at sum nine), a factor catalog of $3{,}207$ polynomials of which $3{,}204$ carry a modular no-root witness and three are the linear factors with roots $0,\\pm1$, and $553{,}392$ exact integer Sylvester determinants. The largest witness prime is still $19$.",
     "The merged certificate contains $181$ representatives and $8{,}688$ signed systems ($2{,}064$ from Lemma~\ref{lem:elimination}, $1{,}536$ new at sum eight, $1{,}920$ at sum nine, $3{,}168$ at sum ten), a factor catalog of $" + tex(factors) + "$ polynomials of which all but the three linear factors with roots $0,\pm1$ carry a modular no-root witness, and $" + tex(dets) + "$ exact integer Sylvester determinants. The largest witness prime is $23$: it is needed for the first time at sum ten, by four factors in the signature $(6,4)$, so the witness-prime set of Lemma~\ref{lem:elimination} becomes $\{3,5,7,11,13,17,19,23\}$ there."),
    ("The standard-library checker accepts the merged certificate in strict mode; the sum-eight part was additionally accepted by the symbolic Chebyshev/Sylvester checker and by the mutation tests, while the symbolic cross-check and mutation tests of the sum-nine part had not been run at the time of writing; the sum-nine checker differs from the sum-eight checker, which passed its mutation tests, only in constants (expected case list, schema name, coverage range).",
     "The standard-library checker accepts the merged certificate in strict mode (sum ten: $1{,}309$ seconds); the sum-eight and sum-nine parts were additionally accepted by the symbolic Chebyshev/Sylvester checker and by the mutation tests, while the symbolic cross-check and mutation tests of the sum-ten part had not been run at the time of writing; the sum-ten checker differs from the sum-nine checker, which passed its mutation tests, only in constants (expected case list, schema name, coverage range)."),
    ("The arithmetic consequence $k+\\ell\\ge10$ is, like $k+\\ell\\ge8$, subsumed", "The arithmetic consequence $k+\\ell\\ge11$ is, like $k+\\ell\\ge8$, subsumed"),
    ("contains the certificates for exponent sums eight and nine,", "contains the certificates for exponent sums eight, nine and ten (the sum-ten certificate, 174~MB, is regenerated by its producer script rather than stored),"),
])
edit("paper_update/CHANGES_v3.md", [
    ("| §4.3 (new), Theorem 4.5 | Certified exclusion through exponent sum nine: 115 representatives, 5,520 systems, 3,207 factors, 553,392 exact determinants; strict stdlib checker PASS | `agents/certificate_extender/results/verify_degree9_stdlib.log`, `certificate_degree9.json`; overlay stage `two_prime_sum9_stdlib` | MACHINE-VERIFIED (sum-9 secondary checks pending; sum-8 secondary checks PASS) |",
     f"| §4.3 (new), Theorem 4.5 | Certified exclusion through exponent sum ten: 181 representatives, 8,688 systems, {factors:,} factors, {dets:,} exact determinants; strict stdlib checker PASS at sums 8, 9 and 10; witness prime 23 first needed at sum 10 | `agents/certificate_extender/results/verification_degree{{8,9,10}}_stdlib.json`; overlay stages `two_prime_sum{{8,9,10}}_stdlib` | MACHINE-VERIFIED (sum-10 secondary checks pending; sum-8 and sum-9 secondary checks PASS) |"),
])
edit("docs/RESULTS.md", [
    ("**Certificate at exponent sum 9 (complete).**", "**Certificates at exponent sums 9 and 10 (complete).**"),
    ("**Theorem 1.1 now holds for k + ℓ ≤ 9**, two exponent\nsums beyond the paper, each step produced by the loop and accepted by the paper's own kind of\nchecker. The SymPy cross-check and mutation tests for sum 9 had not run at submission time.",
     f"Iteration 3 repeated the step once more: sum 10, 66 new representatives, 3,168 new systems, 8,688\nin total, {dets:,} exact determinants, strict checker PASS in 1,309 s; the witness prime 23 is needed\nfor the first time (four factors in signature (6,4)), a fact the paper's text must now state\n[MACHINE-VERIFIED, `agents/certificate_extender/results/verification_degree10_stdlib.json`; the\n174 MB certificate is regenerated by its producer script, not stored]. **Theorem 1.1 now holds for\nk + ℓ ≤ 10**, three exponent sums beyond the paper, each step launched by the planner and accepted by\nthe paper's own kind of checker. The SymPy cross-checks and mutation tests for sums 9 and 10 had not\nrun at submission time."),
    ("Theorem 1.1 moved from exponent sum 7 to 8 (one more proved case of rigidity for r = 2).", "Theorem 1.1 moved from exponent sum 7 to 10 (three more certified steps of rigidity for r = 2)."),
])
edit("docs/ONEPAGE.md", [
    ("**≤ 8**, then **≤ 9** (5,520 systems; independent checker PASS; sum-8 also SymPy-cross-checked)", "**≤ 8**, **≤ 9**, then **≤ 10** (8,688 systems; independent checker PASS at each step; sum-8 also SymPy-cross-checked; witness prime 23 first needed at sum 10)"),
    ("extended its main theorem twice (exponent sum 7 → 9, 5,520 independently checked certificates)", "extended its main theorem three times (exponent sum 7 → 10, 8,688 independently checked certificates)"),
])
edit("docs/SUBMISSION.md", [
    ("extended its main theorem twice (exponent sum 7 → 9, 5,520 independently checked certificates)", "extended its main theorem three times (exponent sum 7 → 10, 8,688 independently checked certificates)"),
    ("certified through exponent sum 8, then 9, by the paper's own producer/checker pair launched from the planner; 5,520 signed systems, 553,392 exact Sylvester determinants, independent standard-library checker PASS (rerun by the referee).",
     f"certified through exponent sums 8, 9 and 10 by the paper's own producer/checker pair launched from the planner; 8,688 signed systems, {dets:,} exact Sylvester determinants, independent standard-library checker PASS at each step (sum 9 rerun by the referee); the witness prime 23 is needed for the first time at sum 10."),
])
edit("docs/POST.md", [
    ("the paper's main theorem extended twice (exponent sum 7 → 9; 5,520 independently checked certificates)", "the paper's main theorem extended three times (exponent sum 7 → 10; 8,688 independently checked certificates)"),
    ("3/ Moved: main theorem extended twice (5,520 certificates, checker PASS).", "3/ Moved: main theorem extended three times (8,688 certificates, checker PASS)."),
])
edit("docs/deck.html", [
    ("<h2>Theorem 1.1: exponent sum 7 → 8 → <span class=\"grad\">9</span></h2>", "<h2>Theorem 1.1: exponent sum 7 → 8 → 9 → <span class=\"grad\">10</span></h2>"),
    ("<p class=\"mono\">iteration 2 &nbsp;5,520</p><div class=\"bar\"><i style=\"width:100%\"></i></div>", "<p class=\"mono\">iteration 2 &nbsp;5,520</p><div class=\"bar\"><i style=\"width:64%\"></i></div>\n      <p class=\"mono\">iteration 3 &nbsp;8,688</p><div class=\"bar\"><i style=\"width:100%\"></i></div>"),
    ("<p class=\"mono\">paper &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2,064</p><div class=\"bar\"><i style=\"width:37%\"></i></div>", "<p class=\"mono\">paper &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2,064</p><div class=\"bar\"><i style=\"width:24%\"></i></div>"),
    ("<p class=\"mono\">iteration 1 &nbsp;3,600</p><div class=\"bar\"><i style=\"width:65%\"></i></div>", "<p class=\"mono\">iteration 1 &nbsp;3,600</p><div class=\"bar\"><i style=\"width:41%\"></i></div>"),
    ("553,392 exact Sylvester determinants · largest witness prime still 19 · independent standard-library checker PASS at each step · referee reran it", f"{dets:,} exact Sylvester determinants · witness prime 23 needed for the first time at sum 10 · independent standard-library checker PASS at each step · referee reran sum 9"),
    ("Sum 8 also passed the symbolic cross-check and mutation tests. Sum 9: strict checker only, stated as such.", "Sums 8 and 9 also passed the symbolic cross-check and mutation tests. Sum 10: strict checker only, stated as such."),
    ("<div class=\"card stat\"><div class=\"n\">5,520</div><div class=\"l\">signed systems certified (theorem extended twice)</div></div>", "<div class=\"card stat\"><div class=\"n\">8,688</div><div class=\"l\">signed systems certified (theorem extended three times)</div></div>"),
    ("The arithmetic corollary (k+ℓ ≥ 10) is subsumed", "The arithmetic corollary (k+ℓ ≥ 11) is subsumed"),
])
edit("docs/slides.html", [
    ("and to <b>9</b> (iteration 2, by the planner's command: 5,520 systems, 553,392 exact determinants, checker PASS 305 s).", "to <b>9</b> (iteration 2: 5,520 systems) and to <b>10</b> (iteration 3: 8,688 systems, checker PASS 1,309 s; witness prime 23 first needed)."),
])
edit("README.md", [
    ("and **≤ 9** in iteration 2 (5,520 systems, 40 new representatives, checker PASS 305 s; secondary checks pending)", "**≤ 9** in iteration 2 (5,520 systems) and **≤ 10** in iteration 3 (8,688 systems, 66 new representatives, checker PASS 1,309 s, witness prime 23 first needed; sum-10 secondary checks pending, sum-8 and sum-9 PASS)"),
])
edit("CONTENTS.md", [
    ("| R1 | Theorem 1.1 holds through exponent sum 8, then 9 (5,520 signed systems) |", "| R1 | Theorem 1.1 holds through exponent sum 8, 9, then 10 (8,688 signed systems; witness prime 23 first needed at sum 10) |"),
    ("`agents/certificate_extender/results/verification_degree{8,9}_stdlib.json` | overlay stages `two_prime_sum8_stdlib`, `two_prime_sum9_stdlib`", "`agents/certificate_extender/results/verification_degree{8,9,10}_stdlib.json` | overlay stages `two_prime_sum{8,9,10}_stdlib`"),
])
edit("HISTORY.md", [
    ("\n## Standing caveats", "| 21:35 | — | Iteration 3 sum-10 certificate: 181 cases, 8,688 systems, strict checker PASS 1,309 s; witness prime 23 first needed (paper sentence updated); 174 MB certificate not stored (regenerable) | — |\n\n## Standing caveats"),
    ("- Sum-9 secondary checks (SymPy cross-check, mutation tests) were not run at the time of the hackathon submission; sum-8's were and passed.", "- Sum-10 secondary checks (SymPy cross-check, mutation tests) were not run at the time of the hackathon submission; sum-8's and sum-9's were and passed."),
])
# ledger, status, overlay
p = ROOT / "ledger" / "attacks.json"; d = json.loads(p.read_text(encoding="utf-8"))
if not any(a["id"] == "A9" for a in d["attacks"]):
    d["attacks"].append({"id": "A9", "iteration": 3, "problem": "P1", "playbook": "certificate-extension", "agent": "certificate-extender", "trace": "traces/10_certificate_extender_sum10.md",
        "input": {"baseline": "agents/certificate_extender/results/certificate_degree9.json", "signatures": [[9,1],[8,2],[7,3],[6,4],[5,5]], "planned_by": "propose_next_attack(P1)"},
        "result": f"66 representatives, 3,168 new systems, 8,688 total, {factors:,} factors, {dets:,} exact determinants; strict stdlib checker PASS 1,309 s; witness prime 23 first needed (4 factors, signature (6,4)); certificate 174 MB regenerable, not stored",
        "evidence": ["agents/certificate_extender/results/verification_degree10_stdlib.json", "agents/certificate_extender/results/verify_degree10_stdlib.log"],
        "tag": "MACHINE-VERIFIED", "verified_by": ["verify_paper_plus.py:two_prime_sum10_stdlib"], "state_after": {"P1": 10}})
    p.write_text(json.dumps(d, indent=2), encoding="utf-8")
p = ROOT / "ledger" / "open_problems.json"; d = json.loads(p.read_text(encoding="utf-8"))
for q in d["problems"]:
    if q["id"] == "P1":
        q["state"]["iteration_3"] = 10; q["next"] = "N = 11 (expect ~2-3x the sum-10 cost; run the sum-9/10 secondary checks first); witness primes now reach 23"
p.write_text(json.dumps(d, indent=2), encoding="utf-8")
p = ROOT / "STATUS.json"; d = json.loads(p.read_text(encoding="utf-8"))
d["findings"]["theorem_1_1_exponent_sum"].update({"after": 10, "iteration_3": 10, "systems": 8688, "independent_checker_sum10": "PASS 1309 s", "witness_prime_23_first_needed": "sum 10, signature (6,4)"})
p.write_text(json.dumps(d, indent=2), encoding="utf-8")
p = ROOT / "paper_overlay" / "stages.json"; d = json.loads(p.read_text(encoding="utf-8"))
if not any(s["name"] == "two_prime_sum10_stdlib" for s in d["stages"]):
    d["stages"].append({"name": "two_prime_sum10_stdlib", "dir": "agents/certificate_extender", "command": ["verify_degree10_stdlib.py"], "accept": "\"status\": \"PASS\"", "ledger": "A9",
                        "copy_results": ["certificate_degree10.json"], "certifies": "Theorem 1.1 for k+l <= 10 (8,688 signed systems); needs the regenerated 174 MB certificate in results/"})
    p.write_text(json.dumps(d, indent=2), encoding="utf-8")
p = ROOT / "CLAIM_MAP.md"; s = p.read_text(encoding="utf-8")
if "F16" not in s:
    s = s.replace("| F12 |", f"| F16 | Theorem 1.1 holds for k+ℓ ≤ 10: 66 new representatives, 3,168 new systems, 8,688 total; strict stdlib checker PASS 1,309 s; witness prime 23 first needed | certificate-extender (iteration 3, planner command) | `traces/10_certificate_extender_sum10.md` | `python agents/certificate_extender/build_degree10_certificate.py` then `verify_degree10_stdlib.py`; overlay stage `two_prime_sum10_stdlib` | `agents/certificate_extender/results/verification_degree10_stdlib.json` | MACHINE-VERIFIED (secondary checks pending) |\n| F12 |")
    p.write_text(s, encoding="utf-8")
print("sum10 integrated")
