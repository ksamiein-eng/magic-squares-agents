#!/usr/bin/env python3
"""The paper's verification suite, plus the stages the agents added (the "absorb" step).

Runs paper/verify_paper.py's own JOBS (and FOUR_PRIME_JOBS unless --skip-four-prime) through the
paper's own task() in temporary copies, then the overlay stages in paper_overlay/stages.json,
numbered after the paper's. One report, in the paper's report format, under
results/verification_runs/plus_<timestamp>/. paper/ is never modified.

    python verify_paper_plus.py --skip-four-prime        # 9 paper stages + overlay (~10 min)
    python verify_paper_plus.py --overlay-only           # just the agents' stages (~4 min)
"""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys, tempfile, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "paper"))
import verify_paper  # noqa: E402  (the paper's own runner)


def overlay_task(stage: dict, out: Path) -> dict:
    t0 = time.perf_counter()
    log = out / "logs" / (stage["name"] + ".log")
    with tempfile.TemporaryDirectory(prefix="rc-overlay-") as tmp:
        dst = Path(tmp) / Path(stage["dir"]).name
        shutil.copytree(ROOT / stage["dir"], dst, ignore=shutil.ignore_patterns("__pycache__", "results", "*.log"))
        (dst / "results").mkdir(exist_ok=True)
        for f in stage.get("copy_results", []):
            shutil.copy2(ROOT / stage["dir"] / "results" / f, dst / "results" / f)
        with log.open("w", encoding="utf-8") as fh:
            done = subprocess.run([sys.executable] + stage["command"], cwd=dst, stdout=fh, stderr=subprocess.STDOUT)
    txt = log.read_text(encoding="utf-8", errors="replace")
    import re
    accepted = stage["accept"] in txt and not (stage.get("reject") and re.search(stage["reject"], txt))
    return {"stage": stage["name"], "passed": done.returncode == 0 and accepted, "returncode": done.returncode,
            "seconds": round(time.perf_counter() - t0, 3), "log": str(log.relative_to(out)), "certifies": stage.get("certifies"), "ledger": stage.get("ledger")}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip-four-prime", action="store_true")
    ap.add_argument("--overlay-only", action="store_true")
    a = ap.parse_args()
    out = ROOT / "results" / "verification_runs" / ("plus_" + time.strftime("%Y%m%dT%H%M%S"))
    (out / "logs").mkdir(parents=True)
    results = []
    if not a.overlay_only:
        jobs = list(verify_paper.JOBS) + ([] if a.skip_four_prime else list(verify_paper.FOUR_PRIME_JOBS))
        for job in jobs:
            r = verify_paper.task(job, out)
            r["origin"] = "paper"
            results.append(r)
            print(json.dumps({k: r[k] for k in ("stage", "passed", "seconds")}), flush=True)
    overlay = json.loads((ROOT / "paper_overlay" / "stages.json").read_text(encoding="utf-8"))
    for st in overlay["stages"]:
        r = overlay_task(st, out)
        r["origin"] = "agents"
        results.append(r)
        print(json.dumps({k: r[k] for k in ("stage", "passed", "seconds")}), flush=True)
    for i, r in enumerate(results, 1):
        r["number"] = i if not a.overlay_only else 16 + i
    report = {"suite": "paper 16 stages + agent overlay", "paper_stages": sum(r["origin"] == "paper" for r in results),
              "overlay_stages": sum(r["origin"] == "agents" for r in results), "all_passed": all(r["passed"] for r in results),
              "isolation": "Each stage runs in its own temporary copy. Shipped proof files are not modified.", "stages": results}
    (out / "report.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    shutil.copy(out / "report.json", ROOT / "results" / "verify_paper_plus_latest.json")
    print(json.dumps({"all_passed": report["all_passed"], "paper_stages": report["paper_stages"], "overlay_stages": report["overlay_stages"], "report": str(out / "report.json")}))
    sys.exit(0 if report["all_passed"] else 1)


if __name__ == "__main__":
    main()
