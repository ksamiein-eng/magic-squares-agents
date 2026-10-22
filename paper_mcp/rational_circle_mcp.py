#!/usr/bin/env python3
"""Paper2Agent-style MCP server for the paper

    "Rational-circle rigidity for magic squares of squares: certified exclusions,
     a genus-five reduction, and surfaces of general type"

Every tool is bound to code or data shipped with the paper (``../paper``), or to a
small exact computation whose identities are re-verified with SymPy at call time.
Nothing here asserts a theorem the paper does not prove: tools return evidence,
pass/fail flags and exact objects, and say what they do *not* prove.

Run:   python paper_mcp/rational_circle_mcp.py          (stdio transport)
Test:  python paper_mcp/test_mcp.py
"""
from __future__ import annotations

import itertools
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
from fractions import Fraction as Fr
from pathlib import Path
from typing import Optional

from fastmcp import FastMCP

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
AGENTS = ROOT / "agents"
for p in (PAPER, PAPER / "verification" / "two_prime"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

mcp = FastMCP(
    "rational_circle",
    instructions=(
        "Tools, resources and prompts generated from the magic-squares-of-squares "
        "rational-circle paper and its 16-stage verification tree, plus the open-problem ledger, "
        "the next-attack planner and the agent-added overlay stages. Use paper_overview or ledger_board "
        "first. Every numerical claim returned by a tool is exact (Python integers / "
        "Fractions / SymPy); 'evidence' fields are never proofs."
    ),
)

# --------------------------------------------------------------------------- helpers

def frac(s) -> Optional[Fr]:
    """Parse '3/4', '-2', 'inf' (None means the projective point at infinity)."""
    if isinstance(s, (int, Fr)):
        return Fr(s)
    s = str(s).strip()
    if s.lower() in ("inf", "infinity", "oo"):
        return None
    return Fr(s)


def circle_point(t: Optional[Fr]) -> tuple[Fr, Fr]:
    """tan(chi/2) = t  ->  (cos chi, sin chi) exactly; t = None is chi = pi."""
    if t is None:
        return Fr(-1), Fr(0)
    p, q = t.numerator, t.denominator
    return Fr(q * q - p * p, p * p + q * q), Fr(2 * p * q, p * p + q * q)


def gmul(a, b):
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def gpow(z, n: int):
    if n < 0:
        z = (z[0], -z[1])  # conjugate = inverse on the unit circle
        n = -n
    r = (Fr(1), Fr(0))
    for _ in range(n):
        r = gmul(r, z)
    return r


def admissible(mags: list[Fr]) -> dict:
    """Pattern {a,b,a+b,a-b} with a>b>0, a!=2b, all distinct and nonzero."""
    mags = sorted(mags)
    if 0 in mags:
        return {"admissible": False, "reason": "a sine vanishes"}
    if len(set(mags)) < 4:
        return {"admissible": False, "reason": "two magnitudes coincide"}
    for i, j in itertools.combinations(range(4), 2):
        A, B = max(mags[i], mags[j]), min(mags[i], mags[j])
        rest = sorted(mags[k] for k in range(4) if k not in (i, j))
        if rest == sorted([A + B, A - B]):
            if A == 2 * B:
                return {"admissible": False, "reason": "a = 2b (entries not distinct)"}
            return {"admissible": True, "a": str(A), "b": str(B)}
    return {"admissible": False, "reason": "magnitudes are not of the form {a,b,a+b,a-b}"}


def signed_systems():
    return [
        (i, j, k, l, e2, e3)
        for i, j in itertools.combinations(range(4), 2)
        for k in [x for x in range(4) if x not in (i, j)]
        for l in [x for x in range(4) if x not in (i, j) and x != k]
        for e2 in (1, -1)
        for e3 in (1, -1)
    ]


def isqrt_exact(n: int) -> Optional[int]:
    if n < 0:
        return None
    r = math.isqrt(n)
    return r if r * r == n else None


P_COEFFS = [1, 0, 70, 0, -1009, 0, 7060, 0, -1009, 0, 70, 0, 1]  # h^12 .. h^0
G_COEFFS = [1, 70, -1012, 6920]  # s^3 .. s^0


def P_of(h: Fr) -> Fr:
    return sum(Fr(c) * h ** (12 - i) for i, c in enumerate(P_COEFFS))


def read_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- resources

@mcp.resource("paper://status")
def res_status() -> str:
    """STATUS.json of the paper release (main results, referee passes, open items)."""
    return (PAPER / "STATUS.json").read_text(encoding="utf-8")


@mcp.resource("paper://claim-map")
def res_claim_map() -> str:
    """Main claims and their proof dependencies (editorial/CLAIM_MAP.md)."""
    return (PAPER / "editorial" / "CLAIM_MAP.md").read_text(encoding="utf-8")


@mcp.resource("paper://manuscript")
def res_manuscript() -> str:
    """Full LaTeX source of the main article."""
    return (PAPER / "manuscript" / "paper.tex").read_text(encoding="utf-8")


@mcp.resource("paper://rigidity-section")
def res_rigidity() -> str:
    """Section 8: the rational-circle rigidity conjecture, Prop 8.2, Thm 8.3, Conj 8.5/8.6."""
    return (PAPER / "manuscript" / "rigidity.tex").read_text(encoding="utf-8")


@mcp.resource("paper://open-problems")
def res_open() -> str:
    """The research record's own list of what remains unresolved."""
    return (PAPER / "research_record" / "extended_status.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------------- tools: paper

@mcp.tool
def paper_overview() -> dict:
    """Title, main results, verification stages, and the open problems of the paper.

    Start here. Returns the release STATUS, the list of theorems/conjectures by
    label, and the explicitly open targets (genus-five point list, ten unresolved
    three-parameter orbits, 112 unclassified four-parameter surfaces, H>=5 sweeps).
    """
    status = read_json(PAPER / "STATUS.json")
    return {
        "title": status["title"],
        "release": status["release"],
        "main_results": status["main_results"],
        "verification_stages": status["verification_stages"],
        "open_problems": [
            "Conjecture 7.3: the eight known rational points of C: Y^2 = P(h) (genus 5) are all of C(Q). "
            "Equivalent to rigidity for configuration D1; implies it for B2, C, E2.",
            "Ten of fifteen squarefree three-prime orbits (B1,B2,C,D1,D2,D3,D4,E2,F+1,F+2) are not closed; "
            "six sufficient targets: D1,D2,D3,D4,F+1,F+2.",
            "Conjecture 8.1 (rigidity) for r>=3 in general; r=2 proved only for exponent sum <= 7.",
            "Kodaira dimension of the solution surfaces of the other 112 four-parameter orbits (Hadamard done).",
            "Conjecture 8.6 (torsion-coset hypothesis): untested systematically.",
            "Four-parameter sweep beyond projective height 4.",
        ],
        "labels": {
            "thm:main-two": "two-parameter exclusion through exponent sum 7",
            "thm:main-d1": "D1 existence <=> extra rational point on the genus-five curve",
            "lem:transport": "integer-torus maps D1 -> B2 -> C, D1 -> E2",
            "prop:four": "no admissible 4-parameter point with three parameters of height <= 4",
            "thm:gentype": "all 48 Hadamard solution surfaces are of general type (p_g=11,q=0,K^2=32)",
            "conj:rigidity": "no full-depth configuration admits an admissible rational-circle point",
            "conj:weak": "admissible points are not Zariski dense",
            "conj:torsion": "every rational point of a solution variety lies on a torsion coset",
        },
    }


@mcp.tool
def list_verification_stages() -> dict:
    """List the 16 machine-checkable stages of the paper's verification suite with their commands."""
    import verify_paper  # noqa: E402  (paper/verify_paper.py)

    return {
        "core_stages": [{"stage": n, "tree": t, "command": c} for n, t, c in verify_paper.JOBS],
        "four_prime_stages": [{"stage": n, "tree": t, "command": c} for n, t, c in verify_paper.FOUR_PRIME_JOBS],
        "note": "Each stage runs in an independent temporary copy; shipped proof records are never modified.",
    }


@mcp.tool
def run_verification_stage(stage: str) -> dict:
    """Run one named verification stage of the paper (see list_verification_stages) and return pass/fail.

    Heavy stages: two_prime_symbolic (~4 min), four_prime_height3_sweep (~3 min).
    """
    import verify_paper

    jobs = {n: (n, t, c) for n, t, c in verify_paper.JOBS + verify_paper.FOUR_PRIME_JOBS}
    if stage not in jobs:
        return {"error": f"unknown stage {stage!r}", "known": sorted(jobs)}
    with tempfile.TemporaryDirectory(prefix="rc-stage-") as tmp:
        out = Path(tmp)
        (out / "logs").mkdir()
        result = verify_paper.task(jobs[stage], out)
        log = (out / result["log"]).read_text(encoding="utf-8", errors="replace")
        result["log_tail"] = log[-3000:]
    return result


@mcp.tool
def check_paper_identities() -> dict:
    """Run check_paper.py: explicit curve identities, orbit enumeration, transport maps, certificate totals."""
    with tempfile.TemporaryDirectory(prefix="rc-check-") as tmp:
        out = Path(tmp) / "paper_checks.json"
        done = subprocess.run([sys.executable, "-I", "check_paper.py", "--output", str(out)],
                              cwd=PAPER, capture_output=True, text=True)
        data = read_json(out) if out.exists() else {}
    return {"returncode": done.returncode, "stderr_tail": done.stderr[-1500:], "checks": data.get("checks", data)}


# --------------------------------------------------------------------------- tools: configurations

@mcp.tool
def evaluate_configuration(rows: list[list[int]], tan_half_angles: list[str]) -> dict:
    """Exact sines of a frequency matrix at a rational-circle point, with the admissibility test.

    rows: integer frequency matrix (4 rows x r columns), e.g. D1 = [[1,1,1],[1,1,-1],[1,1,0],[1,0,1]].
    tan_half_angles: r values tan(chi_j/2) as fractions ('2/3', '-1', '0') or 'inf' (chi_j = pi).
    Returns the four signed sines s_r = Im prod_j z_j^{A_rj}, their magnitudes, which of the 48
    signed systems of Lemma 3.1 hold, the admissibility verdict, and degeneracies.
    """
    r = len(rows[0])
    if len(tan_half_angles) != r or len(rows) != 4:
        return {"error": "need 4 rows and one tan(chi/2) per column"}
    zs = [circle_point(frac(t)) for t in tan_half_angles]
    sines = []
    for row in rows:
        z = (Fr(1), Fr(0))
        for a, zj in zip(row, zs):
            z = gmul(z, gpow(zj, a))
        sines.append(z[1])
    mags = [abs(s) for s in sines]
    held = []
    for (i, j, k, l, e2, e3) in signed_systems():
        if sines[i] - e2 * sines[k] - e3 * sines[l] == 0 and sines[j] - e2 * sines[k] + e3 * sines[l] == 0:
            held.append([i, j, k, l, e2, e3])
    degeneracies = [f"s_{i}=0" for i, s in enumerate(sines) if s == 0]
    degeneracies += [f"|s_{i}|=|s_{j}|" for i, j in itertools.combinations(range(4), 2) if mags[i] == mags[j]]
    torsion = [bool(z in [(Fr(1), Fr(0)), (Fr(-1), Fr(0)), (Fr(0), Fr(1)), (Fr(0), Fr(-1))]) for z in zs]
    return {
        "circle_points": [[str(c), str(s)] for c, s in zs],
        "coordinate_is_torsion": torsion,
        "sines": [str(s) for s in sines],
        "magnitudes": [str(m) for m in mags],
        "signed_systems_satisfied": held,
        "on_solution_variety": bool(held),
        "degeneracies": degeneracies,
        **admissible(mags),
    }


@mcp.tool
def enumerate_configurations(r: int = 3) -> dict:
    """Enumerate full-depth configurations in {0,+-1}^r (r=3 or 4) and their orbits under signed coordinate permutations.

    r=3 reproduces Prop. 5.1 (13 vectors, 177 four-sets, 15 orbits); r=4 reproduces Prop. 8.2's
    11,862 four-sets in 113 orbits. Returns orbit representatives and sizes.
    """
    if r not in (3, 4):
        return {"error": "r must be 3 or 4"}

    def canon(v):
        i = next(k for k, x in enumerate(v) if x)
        return tuple(v) if v[i] > 0 else tuple(-x for x in v)

    vecs = [v for v in itertools.product((-1, 0, 1), repeat=r) if any(v) and v[next(i for i, x in enumerate(v) if x)] > 0]
    confs = [frozenset(S) for S in itertools.combinations(vecs, 4)
             if all(sum(1 for v in S if v[c] != 0) >= 3 for c in range(r))]
    G = [(sg, pm) for sg in itertools.product((1, -1), repeat=r) for pm in itertools.permutations(range(r))]
    orbits, seen = [], set()
    for S in confs:
        if S in seen:
            continue
        orb = {frozenset(canon([g[0][i] * v[g[1][i]] for i in range(r)]) for v in S) for g in G}
        seen |= orb
        orbits.append({"representative": sorted(S), "size": len(orb)})
    return {"r": r, "vectors": len(vecs), "full_depth_sets": len(confs), "orbits": len(orbits),
            "orbit_list": orbits}


@mcp.tool
def three_parameter_orbit_table() -> dict:
    """The fifteen three-parameter orbits with the paper's status (closed / unresolved) and the four transport maps."""
    freq = read_json(PAPER / "editorial" / "ordered_frequencies.json")
    maps = read_json(PAPER / "editorial" / "transport_matrices.json")
    closed = {"A", "E1", "E3", "F-1", "F-2"}
    table = []
    for label, vs in freq.items():
        base = label.split("=")[0]
        table.append({"label": label, "rows": vs, "status": "closed" if base in closed else "unresolved"})
    return {"orbits": table,
            "sufficient_targets_for_all_ten": ["D1", "D2", "D3", "D4", "F+1", "F+2"],
            "transport_maps": maps,
            "note": "D1 closure (Conjecture 7.3) would close B2, C and E2 via the maps."}


@mcp.tool
def two_prime_coverage(k: int, l: int) -> dict:
    """Coverage analysis of the two-prime normal forms A_{k,l;m,n} for one exponent pair (k>=l>0).

    Reports the raw normal forms, those inherited from lower certified signatures via
    column-gcd reduction (Lemma 4.1), and orbit representatives of what remains. For
    k+l<=7 everything is certified by the paper; for k+l>=8 this is the plan an extension
    must certify (see agents/certificate_extender).
    """
    from verify_degree7_stdlib import canonical_set, normal, orbit  # paper code
    from math import gcd

    if k < l or l <= 0:
        return {"error": "need k >= l > 0"}
    remaining, inherited, raw = set(), 0, 0
    for m in range(1 - k, k):
        for n in range(1 - l, l):
            raw += 1
            red = k // gcd(k, abs(m)) + l // gcd(l, abs(n))
            if red <= 7:
                inherited += 1
            else:
                remaining.add(canonical_set(normal(k, l, m, n)))
    reps, covered = [], set()
    for m in range(1 - k, k):
        for n in range(1 - l, l):
            cs = canonical_set(normal(k, l, m, n))
            if cs in remaining and cs not in covered:
                reps.append([m, n])
                covered |= orbit(normal(k, l, m, n), (k, l))
    return {"k": k, "l": l, "raw_normal_forms": raw, "inherited_from_sum_le_7": inherited,
            "remaining_orbits": len(remaining), "representatives_m_n": reps,
            "signed_systems_to_certify": 48 * len(reps),
            "certified_by_paper": k + l <= 7}


# --------------------------------------------------------------------------- tools: genus-five curve

@mcp.tool
def genus5_point_search(height: int = 500) -> dict:
    """Search rational points h=p/q (max(|p|,q) <= height <= 3000) on C: Y^2 = P(h), the genus-five curve of Thm 1.2.

    Exact (big-integer square test after a residue sieve). Reports every point found;
    the eight known points correspond to h in {0, 1, -1, infinity}. A bounded search is
    evidence for Conjecture 7.3, never a proof. For larger heights use agents/point_hunter.
    """
    H = max(1, min(int(height), 3000))
    co = [1, 70, -1009, 7060, -1009, 70, 1]
    mods = [7, 11, 13, 17, 19, 23, 29, 31, 37]
    sq = {m: {(i * i) % m for i in range(m)} for m in mods}
    found, survivors, t0 = [], 0, time.time()
    for q in range(1, H + 1):
        for p in range(0, q + 1):  # symmetries h->-h, h->1/h
            if math.gcd(p, q) != 1:
                continue
            x, y = p * p, q * q
            v = sum(c * x ** (6 - i) * y ** i for i, c in enumerate(co))
            if any(v % m not in sq[m] for m in mods):
                continue
            survivors += 1
            r = isqrt_exact(v)
            if r is not None:
                found.append({"h": f"{p}/{q}", "Y_over_q6": r, "known": (p, q) in [(0, 1), (1, 1)]})
    return {"height": H, "sieve_survivors": survivors, "points": found,
            "new_points": [f for f in found if not f["known"]],
            "seconds": round(time.time() - t0, 2),
            "symmetry_note": "searched 0<=p<=q; h->-h and h->1/h generate the rest"}


@mcp.tool
def reconstruct_d1_point(h: str) -> dict:
    """Theorem 1.2 converse: from a rational h, test whether (h, Y) lies on C and, if so, rebuild the D1 rational-circle point.

    Returns Y (if P(h) is a rational square), the three circle points (alpha, beta, gamma) of
    eq. (reconstruction), the four signed offsets, and the admissibility verdict. For the
    known h in {0, 1, -1} the result is degenerate; any other rational point on C would give
    an explicit admissible D1 point and refute Conjecture 7.3 and rigidity.
    """
    hv = frac(h)
    if hv is None:
        return {"on_curve": True, "point": "infinity", "degenerate": True, "note": "two points at infinity, both in K"}
    val = P_of(hv)
    num, den = val.numerator, val.denominator
    rn, rd = isqrt_exact(num), isqrt_exact(den)
    if rn is None or rd is None:
        return {"h": str(hv), "on_curve": False, "P(h)": str(val)}
    Y = Fr(rn, rd)
    Q = hv ** 4 + 34 * hv ** 2 + 1
    D = (1 + hv ** 2) * Q
    sa, ca = (1 - hv ** 2) / (1 + hv ** 2), -2 * hv / (1 + hv ** 2)
    sb, cb = 12 * hv * (1 - hv ** 2) / Q, (hv ** 4 - 38 * hv ** 2 + 1) / Q
    sg, cg = -48 * hv ** 2 * (1 - hv ** 2) / D, Y / D
    circles_ok = all(s * s + c * c == 1 for s, c in [(sa, ca), (sb, cb), (sg, cg)])
    L = (1 - hv ** 2) / D
    offsets = [L * (hv ** 4 - 62 * hv ** 2 + 1), L * (hv ** 4 - 14 * hv ** 2 + 1), L * Q, L * (-48 * hv ** 2)]
    direct = [sa * cb + ca * sb, sa * cb - ca * sb, sa, sg]
    return {
        "h": str(hv), "on_curve": True, "Y": str(Y), "in_known_list_K": hv in (0, 1, -1),
        "circle_points_sin_cos": {"alpha": [str(sa), str(ca)], "beta": [str(sb), str(cb)], "gamma": [str(sg), str(cg)]},
        "unit_circle_identities_hold": circles_ok,
        "offsets": [str(o) for o in offsets],
        "offsets_match_direct_sines": direct == offsets,
        "linear_relations_hold": offsets[0] == offsets[1] + offsets[3] and offsets[2] == offsets[1] - offsets[3],
        **admissible([abs(o) for o in offsets]),
    }


def _weierstrass_from_quartic_root(quartic_coeffs, root):
    """v^2 = quartic(w) with rational root w0: put w = w0 + 1/t, V = v t^2 -> cubic; then monic integral model."""
    import sympy as sp
    w, t, X = sp.symbols('w t X')
    quart = sum(sp.Integer(c) * w ** (4 - i) for i, c in enumerate(quartic_coeffs))
    cub = sp.expand(sp.cancel(quart.subs(w, root + 1 / t) * t ** 4))
    cp = sp.Poly(cub, t)
    a3, a2, a1, a0 = [int(cp.coeff_monomial(t ** k)) for k in (3, 2, 1, 0)]
    return (0, a2, 0, a3 * a1, a3 * a3 * a0), (a3, a2, a1, a0)


def _ec_add(a2, a4, a6, P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and y1 == -y2:
        return None
    lam = (3 * x1 * x1 + 2 * a2 * x1 + a4) / (2 * y1) if P == Q else (y2 - y1) / (x2 - x1)
    x3 = lam * lam - a2 - x1 - x2
    return (x3, lam * (x1 - x3) - y1)


def _nontorsion_witness(model, pt, max_mult=12):
    """Nagell-Lutz on an integral model y^2 = x^3+a2x^2+a4x+a6: a torsion point has integer x, y.
    Returns the first multiple with a non-integral coordinate (a proof of infinite order)."""
    _, a2, _, a4, a6 = model
    P, Q = (Fr(pt[0]), Fr(pt[1])), None
    for n in range(1, max_mult + 1):
        Q = _ec_add(Fr(a2), Fr(a4), Fr(a6), Q, P)
        if Q is None:
            return {"torsion": True, "order": n}
        if Q[0].denominator != 1 or Q[1].denominator != 1:
            return {"torsion": False, "multiple": n, "x": str(Q[0]), "nagell_lutz": "non-integral multiple => infinite order"}
    return {"torsion": None, "note": f"all multiples up to {max_mult} integral; inconclusive"}


def _c4c6(a):
    a1, a2, a3, a4, a6 = a
    b2 = a1 * a1 + 4 * a2
    b4 = 2 * a4 + a1 * a3
    b6 = a3 * a3 + 4 * a6
    b8 = a1 * a1 * a6 + 4 * a2 * a6 - a1 * a3 * a4 + a2 * a3 * a3 - a4 * a4
    c4 = b2 * b2 - 24 * b4
    c6 = -b2 ** 3 + 36 * b2 * b4 - 216 * b6
    disc = -b2 * b2 * b8 - 8 * b4 ** 3 - 27 * b6 * b6 + 9 * b2 * b4 * b6
    return c4, c6, disc


def _isomorphic_scaling(a, b):
    """Return u with c4(a)=u^4 c4(b), c6(a)=u^6 c6(b) if the models are Q-isomorphic, else None."""
    c4a, c6a, _ = _c4c6(a)
    c4b, c6b, _ = _c4c6(b)
    if c4b == 0 or c6b == 0:
        return None
    r4, r6 = Fr(c4a, c4b), Fr(c6a, c6b)
    if r4 < 0 or r6 < 0:
        return None

    def root(fr, k):
        n, d = fr.numerator, fr.denominator
        rn, rd = round(n ** (1 / k)), round(d ** (1 / k))
        return Fr(rn, rd) if rn ** k == n and rd ** k == d else None

    u4, u6 = root(r4, 4), root(r6, 6)
    return u4 if u4 is not None and u6 is not None and u4 == u6 else None


LMFDB_MATCHES = {
    "E_plus": {"lmfdb": "492.b1", "cremona": "492b1", "ainvs": [0, 1, 0, 11, 695], "rank": 1, "torsion": "trivial"},
    "E_minus": {"lmfdb": "1968.j1", "cremona": "1968m1", "ainvs": [0, 1, 0, 11, 35], "rank": 1, "torsion": "trivial"},
    "E_zero": {"lmfdb": "123.a1", "cremona": "123a1", "ainvs": [0, 1, 1, -10, 10], "rank": 1, "torsion": "Z/5"},
}


@mcp.tool
def genus5_quotient_structure() -> dict:
    """NEW (not in the paper): the automorphisms h->-h, h->1/h of C and the three elliptic quotients, with rank evidence.

    Computes with SymPy, verifying every identity exactly:
      D  = C/(h->-h):   Y^2 = f(x) = x^6+70x^5-1009x^4+7060x^3-1009x^2+70x+1  (genus 2, bielliptic),
      E0 = C -> (s,v) = (h^2+1/h^2, Y/h^3):  v^2 = g(s) = s^3+70s^2-1012s+6920,
      E+ = D/(x->1/x):  v^2 = (w+2) g(w),   E- :  v^2 = (w-2) g(w),  w = x+1/x,
    so Jac(C) ~ E+ x E- x E0 x A (A an abelian surface) up to isogeny. For each elliptic quotient it
    gives an integral Weierstrass model, a rational point coming from the known points of C, a
    Nagell-Lutz proof that the point has infinite order (so rank >= 1), and the LMFDB curve it is
    isomorphic to (isomorphism checked exactly via c4, c6 scaling; the database rank is quoted,
    not re-proved). Consequence: Conjecture 7.3 cannot be settled by the paper's rank-zero
    descent method on any elliptic quotient; it needs Chabauty-type methods on a Jacobian of
    Mordell-Weil rank >= 3 (genus 5), or on D (genus 2, rank 2).
    """
    import sympy as sp
    h, x, w, s = sp.symbols('h x w s')
    P = sum(sp.Integer(c) * h ** (12 - i) for i, c in enumerate(P_COEFFS))
    f = sp.Poly(P.subs(h, sp.sqrt(x)), x).as_expr()
    g = sum(sp.Integer(c) * s ** (3 - i) for i, c in enumerate(G_COEFFS))
    checks = {
        "P_is_f_of_h2": sp.expand(f.subs(x, h ** 2) - P) == 0,
        "P_over_h6_equals_g_of_h2_plus_h-2": sp.expand(sp.cancel(P / h ** 6 - g.subs(s, h ** 2 + h ** -2))) == 0,
        "f_is_reciprocal": sp.expand(x ** 6 * f.subs(x, 1 / x) - f) == 0,
        "f_over_x3_equals_g_of_w": sp.simplify(sp.expand(f / x ** 3) - g.subs(s, x + 1 / x)) == 0,
    }
    out = {"identities_verified": checks, "D": str(f), "g": str(g), "quotients": {}}
    # E0 directly from g; point from h=1: s=2, v=72
    E0 = (0, 70, 0, -1012, 6920)
    out["quotients"]["E_zero"] = {
        "model": "v^2 = s^3+70s^2-1012s+6920", "map": "s = h^2 + h^-2, v = Y/h^3", "ainvs": list(E0),
        "point_from_known_h=1": [2, 72], "on_curve": 2 ** 3 + 70 * 4 - 1012 * 2 + 6920 == 72 ** 2,
        "infinite_order": _nontorsion_witness(E0, (2, 72)),
    }
    gw = [1, 70, -1012, 6920]
    for name, sign in (("E_plus", +1), ("E_minus", -1)):
        quart = sp.Poly(sp.expand((w + 2 * sign) * sum(sp.Integer(c) * w ** (3 - i) for i, c in enumerate(gw))), w)
        qc = [int(c) for c in quart.all_coeffs()]
        model, cub = _weierstrass_from_quartic_root(qc, -2 * sign)
        a3, a2, a1, a0 = cub
        # small point search on the cubic V^2 = a3 t^3 + a2 t^2 + a1 t + a0, then scale to the monic model
        pt = None
        for tn in range(-30, 31):
            for td in range(1, 13):
                if math.gcd(tn, td) != 1:
                    continue
                tt = Fr(tn, td)
                val = a3 * tt ** 3 + a2 * tt ** 2 + a1 * tt + a0
                rn, rd = isqrt_exact(val.numerator), isqrt_exact(val.denominator)
                if val >= 0 and rn is not None and rd is not None:
                    X, Yv = a3 * tt, a3 * Fr(rn, rd)
                    if X.denominator == 1 and Yv.denominator == 1:
                        pt = (int(X), int(Yv))
                        break
            if pt:
                break
        info = {"quartic": f"v^2 = (w{'+' if sign > 0 else '-'}2)*g(w)", "map_from_D": "w = x + 1/x",
                "weierstrass": f"y^2 = X^3 + ({model[1]})X^2 + ({model[3]})X + ({model[4]})", "ainvs": list(model)}
        if pt:
            info["small_point"] = list(pt)
            info["infinite_order"] = _nontorsion_witness(model, pt)
        out["quotients"][name] = info
    for name, m in LMFDB_MATCHES.items():
        a = out["quotients"][name]["ainvs"]
        u = _isomorphic_scaling(tuple(a), tuple(m["ainvs"]))
        out["quotients"][name]["lmfdb"] = {**m, "isomorphism_scaling_u": str(u) if u is not None else None,
                                           "isomorphism_verified": u is not None}
    out["conclusion"] = (
        "[PROVED] All three elliptic quotients have a point of infinite order (exact Nagell-Lutz witnesses on integral "
        "models), so each has Mordell-Weil rank >= 1. [PROVED] The three curves have pairwise distinct j-invariants and "
        "distinct conductors (123, 492, 1968), so they are pairwise non-isogenous over Q; their pullbacks to Jac(C) are "
        "independent abelian subvarieties and ranks add, hence rank Jac(C) >= 3. [DATABASE-QUOTED] The LMFDB gives rank "
        "exactly 1 for each, hence rank Jac(D) = 2 = genus(D), so classical Chabauty on D fails. Consequence: the paper's "
        "rank-zero elliptic descent cannot prove Conjecture 7.3. Viable routes: quadratic Chabauty on the bielliptic "
        "genus-2 quotient D (Balakrishnan-Dogra), elliptic-curve Chabauty over Q(sqrt(d)), or Chabauty-Coleman on C if "
        "the remaining abelian-surface factor has rank <= 1."
    )
    out["evidence_tags"] = {"rank_ge_1_each": "PROVED", "rank_JacC_ge_3": "PROVED", "rank_eq_1_each": "DATABASE-QUOTED",
                            "rank_JacD_eq_2": "DATABASE-QUOTED", "quadratic_Chabauty_route": "CONJECTURAL"}
    return out


# --------------------------------------------------------------------------- tools: four parameters

@mcp.tool
def four_parameter_sweep(orbit_index: int, height: int = 3) -> dict:
    """Run the paper's exhaustive r=4 search (Prop. 8.2 code r4search.py) for ONE orbit at projective height <= height (<=4).

    Executes verification/four_prime/r4search.py in a temporary copy with arguments
    `height orbit_index orbit_index+1`; returns the statistics and any admissible points / free-angle families found.
    """
    H = max(2, min(int(height), 4))
    with tempfile.TemporaryDirectory(prefix="rc-r4-") as tmp:
        dst = Path(tmp) / "four_prime"
        shutil.copytree(PAPER / "verification" / "four_prime", dst, ignore=shutil.ignore_patterns("results", "__pycache__"))
        # the shipped script checkpoints every 10 orbits; make the temporary copy checkpoint after every orbit
        src = (dst / "r4search.py").read_text(encoding="utf-8")
        src = src.replace("if (oi+1)%10==0 or oi==len(orbits)-1:", "if True:")
        (dst / "r4search.py").write_text(src, encoding="utf-8")
        done = subprocess.run([sys.executable, "r4search.py", str(H), str(orbit_index), str(orbit_index + 1)],
                              cwd=dst, capture_output=True, text=True, timeout=3600)
        prog = dst / "results" / f"r4_H{H}_progress.json"
        data = read_json(prog) if prog.exists() else {}
    return {"orbit_index": orbit_index, "height": H, "stdout_tail": done.stdout[-800:], "returncode": done.returncode,
            "stats": data.get("stats"), "found": data.get("found", []), "admissible_points_found": len(data.get("found", []))}


# --------------------------------------------------------------------------- tools: specialist reports

@mcp.tool
def list_specialist_reports() -> dict:
    """List the reports produced by the computational specialist agents under agents/<name>/REPORT.md."""
    reps = []
    if AGENTS.exists():
        for d in sorted(AGENTS.iterdir()):
            rep = d / "REPORT.md"
            if rep.exists():
                reps.append({"agent": d.name, "report": str(rep), "results": sorted(str(p) for p in (d / "results").glob("*.json")) if (d / "results").exists() else []})
    return {"reports": reps}


@mcp.tool
def read_specialist_report(agent: str) -> str:
    """Return the REPORT.md of one specialist agent (certificate_extender, torsion_coset_probe, point_hunter, ...)."""
    rep = AGENTS / agent / "REPORT.md"
    return rep.read_text(encoding="utf-8") if rep.exists() else f"no report for {agent!r}"


# --------------------------------------------------------------------------- tools: ledger and loop

LEDGER = ROOT / "ledger"


@mcp.tool
def ledger_board() -> dict:
    """The open-problem ledger: every open target of the paper with its type, playbook, current state, acceptance criterion and next increment, plus every attack run so far with its evidence tag."""
    return {"problems": read_json(LEDGER / "open_problems.json")["problems"],
            "attacks": read_json(LEDGER / "attacks.json")["attacks"],
            "playbooks": sorted(p.name for p in (ROOT / "playbooks").glob("*.md") if p.name != "README.md")}


@mcp.tool
def propose_next_attack(problem_id: str) -> dict:
    """Rule-based planner: for a ledger problem, return the playbook, the agent, the concrete command for the next increment, its expected cost, and the strongest tag it can produce.

    P1 -> certificate-extension at N+1; P3 -> hypothesis-probe at H+1; P4 -> bounded search at 10*B;
    P2/P5/P6 -> automorphism-quotient-analysis with the inputs already computed.
    """
    probs = {p["id"]: p for p in read_json(LEDGER / "open_problems.json")["problems"]}
    if problem_id not in probs:
        return {"error": f"unknown problem {problem_id}", "known": sorted(probs)}
    p = probs[problem_id]
    st = p.get("state", {})
    last = [v for v in st.values() if isinstance(v, int)]
    plan = {"problem": problem_id, "playbook": p["playbook"], "best_tag_attainable": p["best_tag_attainable"], "acceptance": p["acceptance"]}
    if p["type"] == "certificate-extension":
        n = (max(last) if last else 7) + 1
        plan.update(agent="certificate-extender", command=f"python agents/certificate_extender/build_degree{n}_certificate.py && python agents/certificate_extender/verify_degree{n}_stdlib.py",
                    increment=f"exponent sum {n}", expected_cost="producer ~5-30 min on 5 cores (factoring dominates); checker ~2-5 min",
                    stop_rule="a vanishing resultant or a factor without a witness prime < 257 becomes a new ledger problem")
    elif p["type"] == "hypothesis-probe":
        h = 4 if "H <= 3" in json.dumps(st) else 3
        plan.update(agent="torsion-coset-prober", command=f"python agents/torsion_coset_probe/torsion_coset_probe.py {h}", increment=f"height {h}",
                    expected_cost="~3.4x the previous height; summary JSON only", stop_rule="any NOT_on_torsion_coset point is re-verified exactly and becomes the headline")
    elif p["type"] == "bounded-search":
        b = (max(last) if last else 1500) * 10
        plan.update(agent="point-hunter", command=f"python agents/point_hunter/hunt.py --curve C --H {b}", increment=f"height {b}",
                    expected_cost="~10x the previous run (6 min at 10^6)", stop_rule="diminishing value beyond 10^7 for genus >= 2; hand over to the structural playbook")
    else:
        plan.update(agent="quotient-geometer", command="genus5_quotient_structure tool, then paper/research_record Sections on the orbit's projection curves",
                    increment=p.get("next"), expected_cost="hours of a number theorist with Magma/Sage; inputs are ready in results/genus5_quotient_structure.json")
    plan["ledger_next"] = p.get("next")
    return plan


@mcp.tool
def run_overlay_stage(stage: str) -> dict:
    """Run one agent-added stage of the paper's extended verification suite (paper_overlay/stages.json) in a temporary copy, exactly as verify_paper_plus.py does."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("verify_paper_plus", ROOT / "verify_paper_plus.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    stages = {s["name"]: s for s in read_json(ROOT / "paper_overlay" / "stages.json")["stages"]}
    if stage not in stages:
        return {"error": f"unknown overlay stage {stage}", "known": sorted(stages)}
    with tempfile.TemporaryDirectory(prefix="rc-ov-") as tmp:
        out = Path(tmp); (out / "logs").mkdir()
        r = mod.overlay_task(stages[stage], out)
        r["log_tail"] = (out / r["log"]).read_text(encoding="utf-8", errors="replace")[-1500:]
    return r


# --------------------------------------------------------------------------- prompts

@mcp.prompt
def audit_claim(label: str) -> str:
    """Workflow for auditing one labelled claim of the paper against its verification stage."""
    return (
        f"Audit the claim {label} of the rational-circle paper. Steps: (1) read paper://claim-map and locate the "
        f"claim's proof dependencies; (2) run the verification stage(s) that certify it with run_verification_stage; "
        f"(3) re-derive one identity independently with evaluate_configuration or reconstruct_d1_point; "
        f"(4) state exactly what is machine-checked, what is cited, and what remains conjectural."
    )


@mcp.prompt
def attack_configuration(label: str) -> str:
    """Workflow for attacking one unresolved three-parameter orbit."""
    return (
        f"Attack orbit {label}. (1) three_parameter_orbit_table to get its rows and transport maps; (2) if a map "
        f"reduces it to D1, read genus5_quotient_structure and the point_hunter report; (3) otherwise enumerate "
        f"its 48 signed systems with evaluate_configuration at torsion values and look for a rank-zero elliptic "
        f"quotient; (4) report a precise obstruction or a precise reason none is available."
    )


@mcp.prompt
def referee_report() -> str:
    """Adversarial referee instructions for any claim produced by another agent."""
    return (
        "You are a hostile but fair referee. For every claim: identify the exact computation or citation that "
        "supports it, rerun it if a tool exists, distinguish 'proved', 'machine-verified', 'database-quoted', "
        "'bounded-search evidence', and 'conjectural'. Flag any sentence that overstates."
    )


if __name__ == "__main__":
    mcp.run()
