"""Reproduce all checks without importing or executing the uploaded pipeline.

Requires Python 3.11+ and SymPy 1.14.0. The 2-isogeny and sieve checks themselves
use only the Python standard library. Run from any directory; inputs are resolved
relative to this file unless an explicit archive extraction directory is given.
"""
from pathlib import Path
import json
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent


def main() -> None:
    if not __debug__:
        raise RuntimeError("Do not disable assertions: -O is not supported.")
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / "input"
    if not (root / "repro/certs/F-2.json").is_file():
        raise FileNotFoundError("Expected input/repro/certs/F-2.json")
    logs = HERE / "logs"
    logs.mkdir(exist_ok=True)
    runs = [
        ("audit_inputs.py", "projection_audit.json"),
        ("audit_quotients.py", "quotient_audit.json"),
        ("audit_components.py", "component_audit.json"),
        ("audit_fibers.py", "fiber_audit.json"),
        ("verify_rank_zero.py", "rank_zero_certificate.json"),
        ("audit_rankzero_quotients.py", "rankzero_quotient_audit.json"),
        ("audit_lifts.py", "lift_audit.json"),
        ("rebuild_sieves.py", "sieve_audit.json"),
        ("audit_chabauty.py", "chabauty_audit.json"),
    ]
    record = []
    for script, output in runs:
        args = [sys.executable, str(HERE / script)]
        if script != "verify_rank_zero.py":
            args.append(str(root))
        args.append(str(HERE / output))
        started = time.monotonic()
        completed = subprocess.run(args, text=True, capture_output=True, cwd=HERE)
        (logs / (Path(script).stem + ".log")).write_text(completed.stdout + completed.stderr)
        if completed.returncode:
            raise RuntimeError(f"{script} failed; inspect logs/{Path(script).stem}.log")
        record.append({"script": script, "seconds": round(time.monotonic() - started, 3), "passed": True})
        print(script, "PASS", flush=True)
    load = lambda name: json.loads((HERE / name).read_text())
    p, q, c, f, l, s, h = map(load, [
        "projection_audit.json", "quotient_audit.json", "component_audit.json", "fiber_audit.json",
        "lift_audit.json", "sieve_audit.json", "chabauty_audit.json"])
    assert p["passed"] and p["counts"]["records"] == 17
    assert p["counts"]["signed_systems"] == 816 and p["counts"]["distinct_orbits"] == 15
    assert q["passed_identity_checks"] and q["total_quotient_records"] == 600
    assert c["generic_components"] == 532 and c["linear_relation_components"] == 16
    assert c["all_exceptional_values_are_audited_torsion_fibers"]
    assert f["passed"] == f["fibers"] == 153 and not f["unresolved_fibers"]
    assert not l["failed_lifting_entries"] and l["finite_quotient_factor_entries_lifted"] == 244
    closed = sorted(k for k, v in l["orbits"].items() if v["closed_given_verified_upstream_checks"])
    assert closed == sorted(["A", "E1", "E3", "E4", "F-1", "F-2", "F-3"])
    assert s["all_match"] and len(s["rows"]) == 8
    assert h["points_checked"] == h["invalid_uploaded_point_model_pairs"] == 16
    (HERE / "chabauty_inputs_corrected.json").write_text(json.dumps(h["corrected_inputs"], indent=2))
    status = {
        "scope": "Audit of the supplied three-prime certificates, not certification of the entire manuscript.",
        "closed_labels": closed,
        "closed_distinct_orbits": ["A", "E1", "E3=E4", "F-1=F-3", "F-2"],
        "unresolved_distinct_orbits": ["B1", "B2", "C", "D1", "D2", "D3", "D4", "E2", "F+1", "F+2"],
        "counts": {**p["counts"], "quotient_records": 600, "generic_components": 532,
                   "linear_relation_components": 16, "finite_special_fibers": 153,
                   "fiber_equation_systems": f["systems"], "finite_quotient_factors_lifted": 244,
                   "rank_zero_models_proved": 7, "complete_direct_genus_one_records": 108,
                   "complete_auxiliary_even_quotients": 3, "rank_one_sieves_matched": 8,
                   "Chabauty_point_model_pairs_repaired": 16},
        "not_certified": ["Positive rank upper bounds", "Global saturation of positive-rank bases",
                          "Rank-two sieve and large canonical-height lower bounds",
                          "Nonlinear smooth-model genera", "Any completed quadratic Chabauty run",
                          "Full two-prime exponent-sum-seven theorem", "Historical priority"],
        "runs": record,
        "software_trust": "Python, SymPy exact polynomial routines, and the audit implementations; not a formal proof assistant."
    }
    (HERE / "audit_status.json").write_text(json.dumps(status, indent=2))
    print("All acceptance conditions passed; five distinct three-prime orbits closed.")


if __name__ == "__main__":
    main()
