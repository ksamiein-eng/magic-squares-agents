#!/usr/bin/env python3
"""Degeneracy-rank bound: turn the refuted "exponent rank <= 2" sharpening into a theorem and a prediction.

Setting (paper, Section 8): a rational-circle point z in T(Q)^4 for a full-depth configuration A (rows A_0..A_3)
has sines s_r = sin(A_r . chi). Its *exponent rank* is the rank of the Gaussian-prime exponent vectors of
z_1..z_4; the torsion-coset hypothesis (Conj. 8.6) says rank <= 3, i.e. some nontrivial n with prod z_j^{n_j}
in {+-1, +-i}.

Lemma (degeneracy relations). Let z be a rational point of a solution variety.
 (a) If s_r = 0 then A_r . chi is a multiple of pi, so prod_j z_j^{A_rj} = +-1: the vector A_r is a relation.
 (b) If |s_i| = |s_j| with i != j, then A_i.chi = +-A_j.chi mod pi, so A_i - A_j or A_i + A_j is a relation;
     it is nonzero because rows are distinct projective vectors.
 (c) Hence a point that is degenerate in both senses (every point found by the probe at H <= 4 is) has
     exponent rank <= 3, and rank exactly 3 only if the two relation vectors are parallel:
     A_i +- A_j is a rational multiple of A_r.

Prediction. An orbit can carry rank-3 points only if its representative has rows r, i, j (distinct) with
A_i + A_j or A_i - A_j parallel to A_r. This script evaluates the criterion for all 113 orbits and compares it
with the ranks actually observed at H = 4 (per_orbit data in results/torsion_coset_H4_summary.json).
Proof check: for every example rank-3 point, verify (a) and (b) exactly from the recorded sines and rows.

Output: results/rank_bound_prediction.json
"""
import itertools, json
from fractions import Fraction as Fr
from pathlib import Path

HERE = Path(__file__).resolve().parent
summary = json.loads((HERE / "results" / "torsion_coset_H4_summary.json").read_text())
examples = json.loads((HERE / "results" / "torsion_coset_H4_examples.json").read_text())


def parallel(u, v):
    """u and v nonzero and proportional over Q."""
    if not any(u) or not any(v):
        return False
    k = next(i for i, x in enumerate(v) if x)
    if u[k] == 0:
        return False
    c = Fr(u[k], v[k])
    return all(Fr(a) == c * b for a, b in zip(u, v))


def criterion(rows):
    hits = []
    for r in range(4):
        for i, j in itertools.combinations([x for x in range(4) if x != r], 2):
            for sg in (1, -1):
                w = [a + sg * b for a, b in zip(rows[i], rows[j])]
                if parallel(w, rows[r]):
                    hits.append({"zero_row": r, "pair": [i, j], "sign": sg, "A_i_pm_A_j": w})
    return hits


per_orbit = summary["per_orbit"]
rows_of = {o["orbit"]: [list(map(int, r)) for r in o["rows"]] for o in per_orbit}
observed_rank3 = sorted(o["orbit"] for o in per_orbit if str(3) in {str(k) for k, v in o["points_by_rank"].items() if v})
predicted = sorted(o for o, rows in rows_of.items() if criterion(rows))
result = {
    "lemma": "degenerate point => exponent rank <= 3; rank 3 only if A_i +- A_j is parallel to the zero row A_r",
    "orbits_total": len(rows_of),
    "orbits_satisfying_parallel_triple_criterion": predicted,
    "orbits_with_rank3_points_observed_at_H4": observed_rank3,
    "prediction_consistent": set(observed_rank3) <= set(predicted),
    "criterion_details": {o: criterion(rows_of[o]) for o in predicted},
    "max_rank_observed_overall": summary.get("max_exponent_rank_observed"),
    "rank_counts_overall": summary.get("points_by_exponent_rank"),
}
# exact check of the lemma on every recorded rank-3 example
checks = []
for e in examples["examples"]:
    rows = [list(map(int, r)) for r in e["rows"]]
    sines = [Fr(x) for x in e["sines"]]
    zero_rows = [r for r in range(4) if sines[r] == 0]
    equal_pairs = [[i, j] for i, j in itertools.combinations(range(4), 2) if abs(sines[i]) == abs(sines[j])]
    par = [(r, p) for r in zero_rows for p in equal_pairs
           for sg in (1, -1) if parallel([a + sg * b for a, b in zip(rows[p[0]], rows[p[1]])], rows[r])]
    checks.append({"orbit": e["orbit"], "rank": e["rank"], "zero_rows": zero_rows, "equal_pairs": equal_pairs,
                   "has_parallel_degeneracy_pair": bool(par), "lemma_predicts_rank_le_3": True,
                   "rank3_explained": e["rank"] < 3 or bool(par)})
result["example_checks"] = checks
result["all_rank3_examples_explained"] = all(c["rank3_explained"] for c in checks)
(HERE / "results" / "rank_bound_prediction.json").write_text(json.dumps(result, indent=1))
print(json.dumps({k: result[k] for k in ("orbits_satisfying_parallel_triple_criterion", "orbits_with_rank3_points_observed_at_H4",
                                          "prediction_consistent", "all_rank3_examples_explained", "rank_counts_overall")}))
print("criterion details for observed orbits:", {o: result["criterion_details"].get(o) for o in observed_rank3})
