#!/usr/bin/env python3
"""Check a repository against STANDARD.md (v0.1): ten requirements, PASS/FAIL each, report to results/standard_check.json.

It checks that the artefacts exist and have the right shape; it does not judge the mathematics.
Run from anywhere: python tools/standard_check.py [repo-root]
"""
import hashlib, json, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
TAGS = {"PROVED", "MACHINE-VERIFIED", "DATABASE-QUOTED", "SEARCH-EVIDENCE", "CONJECTURAL"}
out = []


def req(rid, title, ok, detail):
    out.append({"id": rid, "title": title, "passed": bool(ok), "detail": detail})
    print(f"{rid:>3}  {'PASS' if ok else 'FAIL'}  {title}: {detail}")


def exists(*parts):
    return (ROOT.joinpath(*parts)).exists()


# R1 tagged claims
try:
    att = json.loads((ROOT / "ledger" / "attacks.json").read_text(encoding="utf-8"))["attacks"]
    untagged = [a["id"] for a in att if a.get("tag") != "referee" and not any(t in a.get("tag", "") for t in TAGS)]
    lint = subprocess.run([sys.executable, str(ROOT / "tools" / "tag_lint.py")], capture_output=True, text=True, cwd=ROOT)
    req("R1", "tagged claims", not untagged and lint.returncode == 0, f"{len(att)} ledger entries, untagged: {untagged or 'none'}; tag_lint {'passed' if lint.returncode == 0 else 'FAILED'}")
except Exception as e:
    req("R1", "tagged claims", False, repr(e))

# R2 producer/checker separation: checker reports present, checkers do not import producers
reports = sorted((ROOT / "agents" / "certificate_extender" / "results").glob("verification_degree*_stdlib.json")) if exists("agents") else []
checkers = sorted((ROOT / "agents" / "certificate_extender").glob("verify_degree*_stdlib.py")) if exists("agents") else []
imports_producer = [c.name for c in checkers if re.search(r"import\s+build_degree|from\s+build_degree", c.read_text(encoding="utf-8", errors="ignore"))]
req("R2", "producer/checker separation", bool(reports) and not imports_producer, f"{len(reports)} checker reports; checkers importing a producer: {imports_producer or 'none'}")

# R3 fresh referee
verdicts = sorted((ROOT / "results").glob("skeptic_verdict*.md"))
reran = all(re.search(r"rerun|reran|re-run|re-ran|rerunning", v.read_text(encoding="utf-8", errors="ignore"), re.I) for v in verdicts)
req("R3", "fresh referee with reruns", bool(verdicts) and reran, f"{len(verdicts)} verdict file(s); each names reruns: {reran}")

# R4 one-command reproduction
latest = [ROOT / "results" / n for n in ("verify_findings_latest.json", "verify_paper_plus_latest.json")]
ok4, det = True, []
for p in latest:
    if p.exists():
        r = json.loads(p.read_text(encoding="utf-8"))
        st = r.get("stages", [])
        ok4 &= all(s.get("passed") for s in st)
        det.append(f"{p.name}: {sum(1 for s in st if s.get('passed'))}/{len(st)} stages pass")
    else:
        ok4 = False; det.append(f"{p.name}: missing")
req("R4", "one-command reproduction", ok4 and exists("verify_findings.py"), "; ".join(det))

# R5 original suite untouched: hashes in paper/SHA256SUMS match
ok5, mism, n = True, [], 0
sums = ROOT / "paper" / "SHA256SUMS"
if sums.exists():
    for line in sums.read_text(encoding="utf-8").splitlines():
        parts = line.split(None, 1)
        if len(parts) != 2:
            continue
        h, rel = parts
        f = ROOT / "paper" / rel.strip().lstrip("*")
        if f.exists():
            n += 1
            if hashlib.sha256(f.read_bytes()).hexdigest() != h:
                mism.append(rel)
    ok5 = n > 0 and not mism
else:
    ok5 = False
req("R5", "paper's suite is the source of truth (original hashes unchanged, overlay registered)", ok5 and exists("paper_overlay", "stages.json"), f"{n} hashed files checked, mismatches: {mism[:3] or 'none'}; overlay: {exists('paper_overlay', 'stages.json')}")

# R6 verbatim traces hashed in provenance
try:
    prov = json.loads((ROOT / "PROVENANCE.json").read_text(encoding="utf-8"))
    runs = prov.get("agent_runs", [])
    missing = [r["trace"] for r in runs if not (ROOT / r["trace"]).exists()]
    stale = []
    for r in runs:
        p = ROOT / r["trace"]
        if p.exists() and hashlib.sha256(p.read_bytes()).hexdigest() != r.get("trace_sha256"):
            stale.append(r["trace"])
    traces = sorted((ROOT / "traces").glob("*.md"))
    unlisted = [t.name for t in traces if t.name != "README.md" and not any(r["trace"].endswith(t.name) for r in runs)]
    req("R6", "verbatim traces with hashes", bool(runs) and not missing and not stale and not unlisted, f"{len(runs)} runs in provenance; missing {missing or 'none'}; stale hashes {stale or 'none'}; traces not in provenance {unlisted or 'none'}")
except Exception as e:
    req("R6", "verbatim traces with hashes", False, repr(e))

# R7 claim map complete rows
cm = ROOT / "CLAIM_MAP.md"
rows = [l for l in cm.read_text(encoding="utf-8").splitlines() if l.startswith("| F")] if cm.exists() else []
incomplete = [l.split("|")[1].strip() for l in rows if any(c.strip() == "" for c in l.strip().strip("|").split("|"))]
req("R7", "claim map", bool(rows) and not incomplete, f"{len(rows)} claims; rows with empty cells: {incomplete or 'none'}")

# R8 history with corrections
hist = (ROOT / "HISTORY.md").read_text(encoding="utf-8") if exists("HISTORY.md") else ""
corr = len(re.findall(r"refuted|corrected|correction|downgraded|fixed", hist, re.I))
req("R8", "versioned history with corrections", bool(hist) and corr >= 1, f"history present; correction mentions: {corr}")

# R9 formalization status
fy = ROOT / "lean" / "formalization.yaml"
txt = fy.read_text(encoding="utf-8") if fy.exists() else ""
statuses = re.findall(r"^\s*status:\s*(\S+)", txt, re.M)
req("R9", "formalization status per result", bool(statuses), f"{len(statuses)} entries with status: {sorted(set(statuses))}")

# R10 disclosure, licences, citation
tex = ""
for cand in (ROOT / "paper_update" / "manuscript" / "paper.tex", ROOT / "paper" / "manuscript" / "paper.tex"):
    if cand.exists():
        tex = cand.read_text(encoding="utf-8", errors="ignore"); break
disclosed = bool(re.search(r"Claude|ChatGPT|language model|AI agents?|LLM", tex))
req("R10", "disclosure, licence, citation", disclosed and exists("LICENSE") and exists("CITATION.cff"), f"disclosure in manuscript: {disclosed}; LICENSE: {exists('LICENSE')}; CITATION.cff: {exists('CITATION.cff')}")

passed = sum(r["passed"] for r in out)
report = {"standard": "STANDARD.md v0.1", "checked": time.strftime("%Y-%m-%dT%H:%M:%S"), "passed": passed, "total": len(out), "requirements": out}
(ROOT / "results").mkdir(exist_ok=True)
(ROOT / "results" / "standard_check.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
print(f"\n{passed}/{len(out)} requirements pass -> results/standard_check.json")
sys.exit(0 if passed == len(out) else 1)
