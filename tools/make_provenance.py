#!/usr/bin/env python3
"""Write PROVENANCE.json and SHA256SUMS for the project (mirrors paper/editorial/PROVENANCE.json and paper/SHA256SUMS).

Records: every agent run (id, role, model, time span, turns, tool calls, transcript hash), every result
file (path, sha256, bytes), the environment, and the latest verify_findings report.
"""
import hashlib, json, re, subprocess, sys, time, platform
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACES = {
    "00_coordinator.md": {"role": "coordinator (main Claude Code session; also quotient-geometer role)", "agent_id": "e4ab3fed-fe0c-4e63-8ea3-c5514030f294"},
    "01_certificate_extender.md": {"role": "certificate-extender", "agent_id": "a4ed7d04f5fadf220"},
    "02_torsion_coset_prober.md": {"role": "torsion-coset-prober", "agent_id": "a60b808fcc39d0856"},
    "03_point_hunter.md": {"role": "point-hunter", "agent_id": "a1fc4e0f3191ca149"},
    "04_skeptic.md": {"role": "skeptic (referee)", "agent_id": "a86acff213db9b8f2"},
    "06_torsion_coset_prober_H4.md": {"role": "torsion-coset-prober (iteration 2, H=4)", "agent_id": "a004fb926ffeb19e4"},
    "07_certificate_extender_sum9.md": {"role": "certificate-extender (iteration 2, exponent sum 9)", "agent_id": "a33ab313a80618bd9"},
    "05_agent_sdk_docs_lookup.md": {"role": "claude-code-guide (documentation lookup for orchestrator/run_attack.py)", "agent_id": "a547588d0c9123d72"},
}
RESULT_GLOBS = ["results/*.json", "results/*.md", "results/*.log", "agents/*/REPORT*.md", "ledger/*.json", "playbooks/*.md", "paper_overlay/*.json", "agents/*/results/*.json",
                "agents/*/*.py", "paper_mcp/*.py", "traces/*.md", "docs/RESULTS.md", "CLAIM_MAP.md", "STATUS.json"]
IGNORE = re.compile(r"torsion_coset_H\d\.json$|certificate_degree7\.json$|degree8_part_.*\.json$|tmp_.*\.json$")


def sha(p: Path):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    agents = []
    for name, meta in TRACES.items():
        p = ROOT / "traces" / name
        if not p.exists():
            continue
        txt = p.read_text(encoding="utf-8")
        m = re.search(r"Span: (\S+) → (\S+)\. Assistant turns: (\d+)\. Tool calls: (\d+)\. Model\(s\): (.*)\.", txt)
        agents.append({**meta, "trace": f"traces/{name}", "trace_sha256": sha(p),
                       "span_utc": [m.group(1), m.group(2)] if m else None,
                       "assistant_turns": int(m.group(3)) if m else None, "tool_calls": int(m.group(4)) if m else None,
                       "models": m.group(5) if m else None})
    files = []
    for g in RESULT_GLOBS:
        for p in sorted(ROOT.glob(g)):
            if p.is_file() and not IGNORE.search(p.name) and p.name not in ("PROVENANCE.json", "SHA256SUMS"):
                files.append({"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p), "bytes": p.stat().st_size})
    latest = ROOT / "results" / "verify_findings_latest.json"
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    prov = {
        "project": "Rigidity Lab (magic-squares-agents)", "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "git_head_at_generation": git or None,
        "environment": {"os": platform.platform(), "python": sys.version.split()[0],
                        "host_agent": "Claude Code (desktop), coordinator model claude-fable-5-1; specialists inherit unless stated in their trace header"},
        "inputs": {"paper_package": "paper/ (SHA256SUMS inside; 251 verification files, byte-identical to the author's release)",
                   "paper2agent": "https://github.com/jmiao24/Paper2Agent (skill read at build time; pipeline mirrored, not executed)",
                   "lmfdb": "https://www.lmfdb.org (curve identifications 123.a1, 492.b1, 1968.j1; ranks quoted)"},
        "agent_runs": agents,
        "verification": json.loads(latest.read_text()) if latest.exists() else "verify_findings.py not yet run",
        "result_files": files,
        "policy": "paper/ is read-only; every finding carries an evidence tag from results/skeptic_verdict.md; a matching hash is evidence of byte identity, not of mathematical truth (same wording as the paper's SHA256SUMS policy)",
    }
    (ROOT / "PROVENANCE.json").write_text(json.dumps(prov, indent=1), encoding="utf-8")
    with open(ROOT / "SHA256SUMS", "w", encoding="utf-8") as f:
        for r in files:
            f.write(f"{r['sha256']}  {r['path']}\n")
    print(f"PROVENANCE.json: {len(agents)} agent runs, {len(files)} files hashed; verification: {'present' if latest.exists() else 'missing'}")


if __name__ == "__main__":
    main()
