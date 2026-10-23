import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Rigidity Lab dashboard")


@app.cell
def _():
    import json
    from pathlib import Path
    import marimo as mo

    ROOT = Path(__file__).resolve().parents[1] if "__file__" in globals() else Path.cwd()
    if not (ROOT / "ledger").exists():
        ROOT = Path.cwd()
    return ROOT, json, mo


@app.cell
def _(ROOT, json, mo):
    problems = json.loads((ROOT / "ledger" / "open_problems.json").read_text(encoding="utf-8"))["problems"]
    attacks = json.loads((ROOT / "ledger" / "attacks.json").read_text(encoding="utf-8"))["attacks"]
    mo.md(f"""
# Rigidity Lab: the ledger, live

A marimo notebook over the repository's own state files. **{len(problems)} open targets**, **{len(attacks)} attack runs**
(including referee passes). Every number below is read from `ledger/`, `results/` and `agents/*/results/`; nothing is typed in.
""")
    return attacks, problems


@app.cell
def _(mo, problems):
    prob_rows = [{"id": p["id"], "type": p["type"], "statement": p["statement"][:110] + ("…" if len(p["statement"]) > 110 else ""),
             "state": "; ".join(f"{k}: {v}" for k, v in p["state"].items())[:160], "best tag": p["best_tag_attainable"][:40]} for p in problems]
    mo.vstack([mo.md("## Open problems (typed; the type names the playbook)"), mo.ui.table(prob_rows, selection=None)])
    return


@app.cell
def _(attacks, mo):
    attack_rows = [{"id": a["id"], "iter": a["iteration"], "problem": a["problem"], "playbook": a["playbook"], "tag": a["tag"][:48], "result": a["result"][:140]} for a in attacks]
    mo.vstack([mo.md("## Attack runs and referee passes"), mo.ui.table(attack_rows, selection=None)])
    return


@app.cell
def _(ROOT, json, mo):
    data = []
    for H in (2, 3, 4, 5):
        tp = ROOT / "agents" / "torsion_coset_probe" / "results" / f"torsion_coset_H{H}_summary.json"
        if tp.exists():
            s = json.loads(tp.read_text(encoding="utf-8"))
            cls = s.get("points_by_class", {})
            total = sum(cls.values()) if cls else s.get("totals", {}).get("points", 0)
            data.append({"H": H, "points": total, "off_torsion_coset": cls.get("NOT_on_torsion_coset", 0),
                         "admissible": (s.get("admissible_points") or 0) if not isinstance(s.get("admissible_points"), list) else len(s["admissible_points"]),
                         "max_rank": s.get("max_exponent_rank_observed")})
    mo.vstack([mo.md("## Torsion-coset probe by height (Conjecture 8.6)"), mo.ui.table(data, selection=None),
               mo.md("Zero exceptions at every height; the exponent-rank maximum rose from 2 to 3 at H = 4, which refuted a candidate sharpening and produced the degeneracy-rank lemma.")])
    return


@app.cell
def _(ROOT, json, mo):
    rep = ROOT / "results" / "verify_paper_plus_latest.json"
    if rep.exists():
        r = json.loads(rep.read_text(encoding="utf-8"))
        stage_rows = [{"stage": st["stage"], "passed": st["passed"], "seconds": st["seconds"], "certifies": st.get("certifies", "")} for st in r["stages"]]
        out = mo.vstack([mo.md(f"## Agent-added verification stages (overlay on the paper's suite): all passed = **{r['all_passed']}**"), mo.ui.table(stage_rows, selection=None)])
    else:
        out = mo.md("Run `python verify_paper_plus.py --overlay-only` to populate this section.")
    out
    return


@app.cell
def _(ROOT, json, mo):
    cert = {}
    for n in (8, 9):
        cp = ROOT / "agents" / "certificate_extender" / "results" / f"verification_degree{n}_stdlib.json"
        if cp.exists():
            d = json.loads(cp.read_text(encoding="utf-8"))
            cert[n] = {"sum": n, "status": d.get("status"), "systems": d.get("total_systems") or d.get("systems_checked"), "determinants": d.get("exact_integer_determinants"), "seconds": d.get("elapsed_seconds")}
    mo.vstack([mo.md("## Two-prime certificate (Theorem 1.1) by exponent sum"), mo.ui.table(list(cert.values()), selection=None)])
    return


if __name__ == "__main__":
    app.run()
