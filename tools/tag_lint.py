#!/usr/bin/env python3
"""Evidence-tag linter: the mechanical contract between agents and the write-up.

Checks
  1. ledger/attacks.json: every attack has a tag from the allowed set, at least one evidence file
     that exists, and at least one verifier; MACHINE-VERIFIED attacks must name a stage of
     verify_findings.py or verify_paper_plus.py that passed in the latest report.
  2. docs/RESULTS.md: every paragraph under "## Findings" carries at least one bracketed tag; every
     tag is in the allowed set; every backticked path mentioned next to a tag exists.
  3. README findings table: every row has a tag column value from the allowed set.
Exit 1 on any violation. Run: python tools/tag_lint.py
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAGS = {"PROVED", "MACHINE-VERIFIED", "DATABASE-QUOTED", "SEARCH-EVIDENCE", "CONJECTURAL", "UNSUPPORTED", "referee"}
problems = []


def passed_stages():
    names = set()
    for f in ("verify_findings_latest.json", "verify_paper_plus_latest.json"):
        p = ROOT / "results" / f
        if p.exists():
            for s in json.loads(p.read_text()).get("stages", []):
                if s.get("passed"):
                    names.add(s["stage"])
    return names


def check_ledger():
    stages = passed_stages()
    att = json.loads((ROOT / "ledger" / "attacks.json").read_text(encoding="utf-8"))
    for a in att["attacks"]:
        tags = {t.strip() for t in re.split(r"[;(),]", a.get("tag", "")) if t.strip() in TAGS}
        if not tags:
            problems.append(f"ledger {a['id']}: no allowed tag in {a.get('tag')!r}")
        ev = a.get("evidence", [])
        if not ev or not all((ROOT / e).exists() for e in ev):
            problems.append(f"ledger {a['id']}: missing evidence file(s) {ev}")
        if a.get("tag") != "referee" and not a.get("verified_by"):
            problems.append(f"ledger {a['id']}: no verifier")
        if "MACHINE-VERIFIED" in tags:
            st = [v.split(":", 1)[1] for v in a.get("verified_by", []) if v.startswith("verify_")]
            if not any(s in stages for s in st):
                problems.append(f"ledger {a['id']}: MACHINE-VERIFIED but no passing stage among {st} (passed: {sorted(stages)})")


def check_results_md():
    txt = (ROOT / "docs" / "RESULTS.md").read_text(encoding="utf-8")
    m = re.search(r"## Findings(.*?)\n## ", txt, re.S)
    if not m:
        problems.append("RESULTS.md: no Findings section"); return
    for para in [p for p in m.group(1).split("\n\n") if p.strip() and not p.strip().startswith("|")]:
        tags = re.findall(r"\[([A-Z-]+)(?:[ :,][^\]]*)?\]", para)
        tags = [t for t in tags if t in TAGS]
        if not tags:
            problems.append("RESULTS.md: untagged finding paragraph: " + para.strip()[:80].replace("\n", " "))
    for t in re.findall(r"\[([A-Z][A-Z-]+)", txt):
        if t.isupper() and t not in TAGS and "-" in t:
            problems.append(f"RESULTS.md: unknown tag {t}")
    for path in re.findall(r"`((?:agents|results|paper_mcp|docs)/[^`]+)`", m.group(1)):
        if not (ROOT / path).exists():
            problems.append(f"RESULTS.md: evidence path does not exist: {path}")


def check_readme():
    txt = (ROOT / "README.md").read_text(encoding="utf-8")
    m = re.search(r"\| Target in the paper \|.*?\n\n", txt, re.S)
    if not m:
        problems.append("README: findings table not found"); return
    for row in m.group(0).splitlines()[2:]:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if len(cells) >= 4 and not any(t in cells[3] for t in TAGS):
            problems.append("README: row without tag: " + cells[0][:50])


check_ledger(); check_results_md(); check_readme()
if problems:
    print("TAG LINT FAILED"); [print(" -", p) for p in problems]; sys.exit(1)
print("TAG LINT PASSED: ledger, docs/RESULTS.md findings and README table all carry valid tags with existing evidence")
