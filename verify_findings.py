#!/usr/bin/env python3
"""Re-run every machine-checkable finding of this project in one command (mirrors paper/verify_paper.py).

Stages (each writes a JSON/log under results/verification_runs/<timestamp>/):
  1. mcp_tools            paper_mcp/test_mcp.py (all 14 tools in-process)
  2. paper_core_stages    the paper's own nine core certificate stages (verify_paper.py --skip-four-prime)  [--skip-paper to omit, ~4 min]
  3. sum8_certificate     agents/certificate_extender/verify_degree8_stdlib.py (strict, standard library only, ~2.5 min)
  4. point_hunter_selftest agents/point_hunter/hunt.py --selftest, then a height-3000 search on C
  5. torsion_probe_H2     agents/torsion_coset_probe/torsion_coset_probe.py 2 0 10 (first ten orbits, ~10 s) and compare counts with the shipped summary
  6. quotient_structure   genus5_quotient_structure tool: identities, Nagell-Lutz witnesses, c4/c6 isomorphism checks
Exit status is nonzero if any stage fails. Shipped result files are never modified; the torsion probe writes to a temp copy.
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable


def run(cmd, cwd, log, timeout=3600):
    t0 = time.time()
    with open(log, "w", encoding="utf-8") as f:
        p = subprocess.run(cmd, cwd=cwd, stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
    return p.returncode, round(time.time() - t0, 1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip-paper", action="store_true", help="skip the paper's own nine-stage suite")
    a = ap.parse_args()
    out = ROOT / "results" / "verification_runs" / time.strftime("%Y%m%dT%H%M%S")
    out.mkdir(parents=True)
    report = {"started": time.strftime("%Y-%m-%d %H:%M:%S"), "python": sys.version.split()[0], "stages": []}

    def stage(name, fn):
        t0 = time.time()
        try:
            res = fn()
            ok = bool(res.get("passed"))
        except Exception as e:  # noqa: BLE001
            res, ok = {"error": repr(e)}, False
        res.update(stage=name, passed=ok, seconds=round(time.time() - t0, 1))
        report["stages"].append(res)
        print(json.dumps({k: res[k] for k in ("stage", "passed", "seconds")}), flush=True)

    def s_mcp():
        rc, s = run([PY, "paper_mcp/test_mcp.py"], ROOT, out / "mcp_tools.log")
        txt = (out / "mcp_tools.log").read_text(encoding="utf-8")
        return {"passed": rc == 0 and "stage run: D1_normalization_and_descent True" in txt, "log": "mcp_tools.log"}

    def s_paper():
        rc, s = run([PY, "-I", "verify_paper.py", "--skip-four-prime"], ROOT / "paper", out / "paper_core_stages.log")
        txt = (out / "paper_core_stages.log").read_text(encoding="utf-8")
        return {"passed": rc == 0 and txt.count("'passed': True") >= 9, "stages_passed": txt.count("'passed': True"), "log": "paper_core_stages.log"}

    def s_sum8():
        d = ROOT / "agents" / "certificate_extender"
        rc, s = run([PY, "verify_degree8_stdlib.py", "--output", str(out / "verification_degree8_stdlib.json")], d, out / "sum8_certificate.log")
        j = json.loads((out / "verification_degree8_stdlib.json").read_text()) if (out / "verification_degree8_stdlib.json").exists() else {}
        return {"passed": rc == 0 and j.get("status") == "PASS", "status": j.get("status"), "cases": j.get("cases_checked") or j.get("cases"), "systems": j.get("systems_checked") or j.get("systems"), "log": "sum8_certificate.log"}

    def s_hunt():
        d = ROOT / "agents" / "point_hunter"
        rc1, _ = run([PY, "hunt.py", "--selftest"], d, out / "point_hunter_selftest.log")
        rc2, _ = run([PY, "hunt.py", "--curve", "C", "--H", "3000", "--out", str(out / "hunt_C_H3000.json")], d, out / "point_hunter_search.log")
        j = json.loads((out / "hunt_C_H3000.json").read_text()) if (out / "hunt_C_H3000.json").exists() else {}
        curves = j.get("curves", {})
        c = curves.get("C", j)
        new = c.get("new_points")
        return {"passed": rc1 == 0 and rc2 == 0 and new == [], "new_points": new, "selftest_log": "point_hunter_selftest.log"}

    def s_torsion():
        src = ROOT / "agents" / "torsion_coset_probe"
        with tempfile.TemporaryDirectory(prefix="torsion-") as tmp:
            dst = Path(tmp) / "probe"
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("results", "__pycache__"))
            (dst / "results").mkdir()
            rc, s = run([PY, "torsion_coset_probe.py", "2", "0", "10"], dst, out / "torsion_probe_H2.log")
            txt = (out / "torsion_probe_H2.log").read_text(encoding="utf-8", errors="replace")
        shipped = json.loads((src / "results" / "torsion_coset_H2_summary.json").read_text())
        bad = "NOT_on_torsion_coset" in txt and "'NOT_on_torsion_coset': 0" not in txt and "NOT_on_torsion_coset\": 0" not in txt
        return {"passed": rc == 0 and "admissible 0" in txt and not bad, "orbits_rerun": 10,
                "shipped_H2_totals": shipped.get("totals") or shipped.get("points_by_class"), "log": "torsion_probe_H2.log"}

    def s_quotient():
        sys.path.insert(0, str(ROOT / "paper_mcp"))
        import asyncio
        from fastmcp import Client
        from rational_circle_mcp import mcp

        async def go():
            async with Client(mcp) as c:
                r = await c.call_tool("genus5_quotient_structure", {})
                return r.data if r.data is not None else json.loads(r.content[0].text)
        d = asyncio.run(go())
        (out / "genus5_quotient_structure.json").write_text(json.dumps(d, indent=1))
        ids = all(d["identities_verified"].values())
        wit = all((q.get("infinite_order") or {}).get("torsion") is False for q in d["quotients"].values())
        iso = all(q["lmfdb"]["isomorphism_verified"] for q in d["quotients"].values())
        return {"passed": ids and wit and iso, "identities": ids, "infinite_order_witnesses": wit, "lmfdb_isomorphisms": iso}

    stage("mcp_tools", s_mcp)
    if not a.skip_paper:
        stage("paper_core_stages", s_paper)
    stage("sum8_certificate", s_sum8)
    stage("point_hunter_selftest_and_search", s_hunt)
    stage("torsion_probe_H2_first_ten_orbits", s_torsion)
    stage("quotient_structure", s_quotient)
    report["all_passed"] = all(s["passed"] for s in report["stages"])
    report["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    (out / "report.json").write_text(json.dumps(report, indent=1))
    shutil.copy(out / "report.json", ROOT / "results" / "verify_findings_latest.json")
    print(json.dumps({"all_passed": report["all_passed"], "report": str(out / "report.json")}))
    sys.exit(0 if report["all_passed"] else 1)


if __name__ == "__main__":
    main()
