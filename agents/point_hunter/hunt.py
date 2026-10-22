#!/usr/bin/env python
"""
hunt.py -- exact rational point search on the genus-5 curve

    C : Y^2 = P(h) = h^12 + 70 h^10 - 1009 h^8 + 7060 h^6 - 1009 h^4 + 70 h^2 + 1

and on its quotients

    D  : Y^2 = f(x) = x^6 + 70x^5 - 1009x^4 + 7060x^3 - 1009x^2 + 70x + 1   (x = h^2)
    E0 : v^2 = g(s) = s^3 + 70 s^2 - 1012 s + 6920                          (s = h^2 + h^-2, v = Y/h^3)

Method.  For h = p/q in lowest terms the condition Y in Q is equivalent to the
homogeneous form  P_hom(p,q) = sum_i c_i p^{2(6-i)} q^{2i}  being a perfect
square.  P is even and palindromic, so P_hom(p,q) = P_hom(-p,q) = P_hom(q,p)
and it suffices to search 0 <= p <= q.  For every q we build a boolean array
over p by tiling precomputed residue tables: for a modulus M the table
T_M[q mod M][p mod M] is True iff P_hom(p,q) mod M lies in the set of squares
mod M.  Three composite moduli (2^6*3^3, 5^2*7^2, 11*13*17) are ANDed over the
whole array; the survivors are then filtered through seven more composite
moduli covering every prime up to 73 (fancy indexing on the survivor list
only).  Only the final survivors are evaluated exactly with Python integers
and tested with math.isqrt.  The sieve is a necessary condition only, so it can
never discard a true point (see --selftest).

Usage:
    python hunt.py --selftest
    python hunt.py --curve C  --H 100000
    python hunt.py --curve D  --H 200000
    python hunt.py --curve E0 --H 2000
    python hunt.py --all --HC 100000 --HD 200000 --HE 2000   (writes results/search_results.json)
"""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(HERE, "results")

# ----------------------------------------------------------------------------
# The forms.  A form is a list of (a, b, c) meaning  c * p^a * q^b.
# ----------------------------------------------------------------------------
P_EVEN = [1, 70, -1009, 7060, -1009, 70, 1]       # P(h) = sum c_i h^{2(6-i)}
G_COEF = [1, 70, -1012, 6920]                     # g(s) = s^3+70s^2-1012s+6920

FORM_C = [(2 * (6 - i), 2 * i, c) for i, c in enumerate(P_EVEN)]   # P_hom(p,q), deg 12
FORM_D = [((6 - i), i, c) for i, c in enumerate(P_EVEN)]           # f_hom(p,q), deg 6
# For E0 with s=p/q:  v^2 = g(p/q)  <=>  q * g_hom(p,q)  is a square (times q^4).
FORM_E0 = [((3 - i), i + 1, c) for i, c in enumerate(G_COEF)]      # q*g_hom(p,q), deg 4
FORM_SQUARE = [(4, 0, 1), (2, 2, 2), (0, 4, 1)]                     # (p^2+q^2)^2, always a square

CURVES = {
    # name: (form, p-range, degree, description, known points as (p,q))
    # p-range: "half" = 0<=p<=q (even+palindromic form), "sym" = -q<=p<=q (palindromic),
    #          "full" = -H<=p<=H (no reciprocity symmetry; E0's g is not palindromic)
    "C":  (FORM_C,  "half", 12, "Y^2 = P(h), h = p/q, 0<=p<=q<=H", [(0, 1), (1, 1)]),
    "D":  (FORM_D,  "sym",  6,  "Y^2 = f(x), x = p/q, -q<=p<=q<=H", [(0, 1), (1, 1)]),
    "E0": (FORM_E0, "full", 4,  "v^2 = g(s), s = p/q, |p|<=H, 1<=q<=H", [(2, 1)]),
}

# Modulus selection.  The pass rate of a prime power depends strongly on the
# form (for C, every power of 2, 3, 5 and the primes 7 and 11 are useless: the
# identity P = D^2 - (48 h^2(1-h^2))^2 makes P_hom a square mod 2^8*3^2, and C has
# maximal point counts mod 5, 7, 11).  So the moduli are chosen per form by
# measuring the fraction of (p mod M, q mod M) that survive, discarding useless
# ones, and greedily packing the strongest prime powers into composite moduli
# of size at most TABLE_LIMIT.  The N_STAGE1 strongest composites are ANDed over
# the whole p-array (stage 1); the rest filter the survivor list (stage 2).
PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
          73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
PRIME_POWERS = {2: [4, 8, 16, 32, 64, 128, 256], 3: [3, 9, 27, 81], 5: [5, 25, 125],
                7: [7, 49], 11: [11, 121], 13: [13, 169]}
TABLE_LIMIT = 6000      # largest composite modulus (table is M*M bytes)
N_STAGE1 = 3
USELESS = 0.95          # drop a prime power whose pass rate exceeds this


def choose_moduli(form, verbose=False):
    """Return (stage1, stage2, info) lists of composite moduli for this form."""
    cands = []           # (rate, prime, power)
    for ell in [2] + PRIMES:
        best = None
        for M in PRIME_POWERS.get(ell, [ell]):
            rate = float(build_table(form, M).mean())
            if best is None or rate < best[0] - 1e-9:
                best = (rate, ell, M)
        if best[0] <= USELESS:
            cands.append(best)
    cands.sort()
    composites = []      # list of [product, rate, [members]]
    for rate, ell, M in cands:
        for comp in composites:
            if comp[0] * M <= TABLE_LIMIT:
                comp[0] *= M
                comp[1] *= rate
                comp[2].append(M)
                break
        else:
            composites.append([M, rate, [M]])
    composites.sort(key=lambda c: c[1])
    stage1 = [c[0] for c in composites[:N_STAGE1]]
    stage2 = [c[0] for c in composites[N_STAGE1:]]
    total = 1.0
    for c in composites:
        total *= c[1]
    info = {"prime_powers": [(M, round(r, 4)) for r, _, M in cands],
            "composites": [(c[0], c[2], round(c[1], 5)) for c in composites],
            "stage1_rate": round(float(np.prod([c[1] for c in composites[:N_STAGE1]])), 6),
            "overall_rate": total}
    if verbose:
        print("  prime powers used (modulus, pass rate):", info["prime_powers"])
        print("  stage1 composites:", [(c[0], c[2]) for c in composites[:N_STAGE1]],
              " stage1 rate ~", info["stage1_rate"])
        print("  stage2 composites:", [(c[0], c[2]) for c in composites[N_STAGE1:]],
              " overall rate ~ %.3g" % total)
    return stage1, stage2, info


def form_eval(form, p, q):
    """Exact integer evaluation with Python big integers."""
    return sum(c * p ** a * q ** b for a, b, c in form)


def square_set(M):
    sq = np.zeros(M, dtype=bool)
    r = np.arange(M, dtype=np.int64)
    sq[(r * r) % M] = True
    return sq


def build_table(form, M):
    """T[q mod M, p mod M] is True iff form(p,q) mod M is a square residue mod M."""
    r = np.arange(M, dtype=np.int64)
    maxdeg = max(max(a, b) for a, b, _ in form)
    pw = [np.ones(M, dtype=np.int64)]
    for _ in range(maxdeg):
        pw.append((pw[-1] * r) % M)
    val = np.zeros((M, M), dtype=np.int64)          # indexed [q, p]
    for a, b, c in form:
        term = (pw[b][:, None] * pw[a][None, :]) % M
        term = (term * (c % M)) % M
        val += term
    val %= M
    return square_set(M)[val]                        # bool (M, M)


def build_tables(form, moduli):
    return {M: build_table(form, M) for M in moduli}


def tiled_row(row, M, p_lo, n):
    """row tiled so that result[i] = row[(p_lo + i) mod M] for i in range(n)."""
    off = p_lo % M
    reps = (off + n + M - 1) // M
    return np.tile(row, reps)[off:off + n]


def search_form(form, H, prange, tables1, tables2, q_start=1, progress=None, exact=True):
    """
    Search all p/q with 1 <= q <= H and p in the window given by prange
    ("half": 0..q, "sym": -q..q, "full": -H..H).
    Returns dict with found points [(p, q, root)], counters and timing.
    A found point means form(p,q) == root^2 with gcd(p,q) == 1.
    """
    t0 = time.time()
    found = []
    n_pairs = 0
    n_stage1 = 0
    n_stage2 = 0
    n_exact = 0
    mods1 = list(tables1.keys())
    mods2 = list(tables2.keys())
    next_report = time.time() + 30
    for q in range(q_start, H + 1):
        if prange == "half":
            p_lo, p_hi = 0, q
        elif prange == "sym":
            p_lo, p_hi = -q, q
        else:
            p_lo, p_hi = -H, H
        n = p_hi - p_lo + 1
        n_pairs += n
        acc = None
        for M in mods1:
            t = tiled_row(tables1[M][q % M], M, p_lo, n)
            if acc is None:
                acc = t
            else:
                np.logical_and(acc, t, out=acc)
        idx = np.flatnonzero(acc)
        n_stage1 += idx.size
        if idx.size == 0:
            continue
        ps = idx + p_lo
        for M in mods2:
            keep = tables2[M][q % M][ps % M]
            ps = ps[keep]
            if ps.size == 0:
                break
        n_stage2 += ps.size
        if not exact:
            continue
        for p in ps.tolist():
            if math.gcd(p, q) != 1:
                continue
            n_exact += 1
            v = form_eval(form, p, q)
            if v < 0:
                continue
            r = math.isqrt(v)
            if r * r == v:
                found.append((p, q, r))
        if progress and time.time() > next_report:
            progress(q, H, time.time() - t0, len(found))
            next_report = time.time() + 30
    return {
        "H": H,
        "pairs_scanned": n_pairs,
        "stage1_survivors": n_stage1,
        "stage2_survivors": n_stage2,
        "exact_tests": n_exact,
        "found": found,
        "seconds": time.time() - t0,
    }


def describe_point(curve, p, q, r):
    """Return a human-readable description of a found point in lowest terms."""
    if curve == "C":
        # Y^2 = P_hom(p,q)/q^12,  Y = r/q^6
        return {"h": f"{p}/{q}", "Y": f"{r}/{q**6}", "p": p, "q": q, "root": r}
    if curve == "D":
        return {"x": f"{p}/{q}", "Y": f"{r}/{q**3}", "p": p, "q": q, "root": r}
    if curve == "E0":
        # v^2 = g_hom(p,q)/q^3 = q*g_hom/q^4, v = r/q^2
        return {"s": f"{p}/{q}", "v": f"{r}/{q**2}", "p": p, "q": q, "root": r}
    return {"p": p, "q": q, "root": r}


def is_known(curve, p, q):
    _, _, _, _, known = CURVES[curve]
    return (p, q) in known or (q, p) in known


def run_curve(curve, H, q_start=1, verbose=True):
    form, prange, deg, desc, known = CURVES[curve]
    t0 = time.time()
    stage1, stage2, minfo = choose_moduli(form, verbose=verbose)
    tables1 = build_tables(form, stage1)
    tables2 = build_tables(form, stage2)
    t_tables = time.time() - t0

    def progress(q, H, dt, nf):
        if verbose:
            print(f"  [{curve}] q={q}/{H}  {100.0*q/H:5.1f}%  {dt:7.1f}s  points so far={nf}", flush=True)

    if verbose:
        print(f"== Curve {curve}: {desc}; H={H}; tables built in {t_tables:.2f}s", flush=True)
    res = search_form(form, H, prange, tables1, tables2, q_start=q_start, progress=progress)
    res["curve"] = curve
    res["description"] = desc
    res["q_start"] = q_start
    res["table_seconds"] = t_tables
    res["moduli_stage1"] = stage1
    res["moduli_stage2"] = stage2
    res["moduli_info"] = minfo
    pts = []
    new = []
    for (p, q, r) in res["found"]:
        # final independent verification
        assert form_eval(form, p, q) == r * r and math.gcd(p, q) == 1
        d = describe_point(curve, p, q, r)
        d["known"] = is_known(curve, p, q)
        pts.append(d)
        if not d["known"]:
            new.append(d)
    res["points"] = pts
    res["new_points"] = new
    del res["found"]
    if verbose:
        print(f"  pairs={res['pairs_scanned']}  stage1={res['stage1_survivors']}  "
              f"stage2={res['stage2_survivors']}  exact={res['exact_tests']}  "
              f"time={res['seconds']:.1f}s")
        print(f"  points found ({len(pts)}):")
        for d in pts:
            print("    ", d)
        if new:
            print("\n" + "!" * 78)
            print(f"!!!  NEW POINT(S) ON {curve} (not in the known list):")
            for d in new:
                print("!!!   ", d)
            print("!" * 78 + "\n", flush=True)
        else:
            print(f"  No new points on {curve} up to height {H}.", flush=True)
    return res


# ----------------------------------------------------------------------------
# self test
# ----------------------------------------------------------------------------
def selftest():
    import sympy as sp
    h, s, x = sp.symbols("h s x")
    P = h**12 + 70*h**10 - 1009*h**8 + 7060*h**6 - 1009*h**4 + 70*h**2 + 1
    F = h**6 - 13*h**4 + 83*h**2 + 1
    G = h**6 + 83*h**4 - 13*h**2 + 1
    g = s**3 + 70*s**2 - 1012*s + 6920
    f = x**6 + 70*x**5 - 1009*x**4 + 7060*x**3 - 1009*x**2 + 70*x + 1
    ok = True

    def check(name, cond):
        nonlocal ok
        print(f"  [{'OK' if cond else 'FAIL'}] {name}")
        ok = ok and bool(cond)

    print("Identity checks (sympy):")
    check("P = F*G", sp.expand(P - F*G) == 0)
    check("P(h)/h^6 = g(h^2 + h^-2)", sp.simplify(sp.expand(P / h**6 - g.subs(s, h**2 + h**-2))) == 0)
    check("(1+h^2)^2 (h^4+34h^2+1)^2 - (48h^2(1-h^2))^2 = P(h)",
          sp.expand((1 + h**2)**2 * (h**4 + 34*h**2 + 1)**2 - (48*h**2*(1 - h**2))**2 - P) == 0)
    check("P(h) = f(h^2)", sp.expand(P - f.subs(x, h**2)) == 0)
    check("P squarefree (gcd(P,P')=1)", sp.gcd(P, sp.diff(P, h)) == 1)
    check("P(1) = 72^2", P.subs(h, 1) == 72**2)
    check("g(2) = 72^2", g.subs(s, 2) == 72**2)

    print("Form / table consistency checks:")
    pp, qq = sp.symbols("pp qq")
    for name, form, poly, var in (("C", FORM_C, P, h), ("D", FORM_D, f, x)):
        hom = sum(c * pp**a * qq**b for a, b, c in form)
        deg = max(a + b for a, b, _ in form)
        check(f"FORM_{name} is the homogenization of its polynomial",
              sp.expand(hom - qq**deg * poly.subs(var, pp / qq)) == 0)
    hom = sum(c * pp**a * qq**b for a, b, c in FORM_E0)
    check("FORM_E0 = q^4 * g(p/q)", sp.expand(hom - qq**4 * g.subs(s, pp / qq)) == 0)

    rng = np.random.default_rng(12345)
    for curve, (form, prange, deg, desc, known) in CURVES.items():
        s1, s2, _ = choose_moduli(form)
        tables = build_tables(form, s1 + s2)
        bad = 0
        for M, T in tables.items():
            sqs = set(int(v) for v in np.flatnonzero(square_set(M)))
            for _ in range(300):
                p = int(rng.integers(-10**6, 10**6))
                q = int(rng.integers(1, 10**6))
                direct = (form_eval(form, p, q) % M) in sqs
                if bool(T[q % M, p % M]) != direct:
                    bad += 1
        check(f"{curve}: residue tables agree with direct big-int computation (3000 samples)", bad == 0)
        # planted known points pass every modulus
        allpass = all(bool(T[q % M, p % M]) for M, T in tables.items() for (p, q) in known)
        check(f"{curve}: known points {known} pass every sieve modulus", allpass)

    print("Sieve-never-discards test on an always-square form (p^2+q^2)^2:")
    s1, s2, _ = choose_moduli(FORM_C)      # use C's moduli on the always-square form
    t1 = build_tables(FORM_SQUARE, s1)
    t2 = build_tables(FORM_SQUARE, s2)
    res = search_form(FORM_SQUARE, 120, "sym", t1, t2)
    expected = sum(1 for q in range(1, 121) for p in range(-q, q + 1) if math.gcd(p, q) == 1)
    check(f"all {expected} coprime pairs survive the sieve and verify as squares",
          res["stage2_survivors"] == res["pairs_scanned"] and len(res["found"]) == expected)

    print("End-to-end: small searches recover the known points:")
    for curve in ("C", "D", "E0"):
        r = run_curve(curve, 50, verbose=False)
        got = {(d["p"], d["q"]) for d in r["points"]}
        known = set(CURVES[curve][4])
        check(f"{curve}: H=50 finds known {sorted(known)}; all found = {sorted(got)}", known <= got)

    print("SELFTEST", "PASSED" if ok else "FAILED")
    return ok


# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--curve", choices=list(CURVES.keys()))
    ap.add_argument("--H", type=int, default=1000)
    ap.add_argument("--q-start", type=int, default=1)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--HC", type=int, default=100000)
    ap.add_argument("--HD", type=int, default=200000)
    ap.add_argument("--HE", type=int, default=2000)
    ap.add_argument("--out", default=os.path.join(RESULTS_DIR, "search_results.json"))
    ap.add_argument("--merge", nargs="*", help="merge per-curve JSON files into --out")
    args = ap.parse_args()

    if args.merge:
        merged = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                  "python": sys.version.split()[0], "numpy": np.__version__, "curves": {}}
        for fn in args.merge:
            with open(fn) as fh:
                merged["curves"].update(json.load(fh)["curves"])
        with open(args.out, "w") as fh:
            json.dump(merged, fh, indent=2)
        print(f"merged {len(merged['curves'])} curve(s) into {args.out}")
        return

    if args.selftest:
        sys.exit(0 if selftest() else 1)

    results = {"timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
               "python": sys.version.split()[0], "numpy": np.__version__,
               "curves": {}}
    jobs = []
    if args.all:
        jobs = [("C", args.HC), ("D", args.HD), ("E0", args.HE)]
    elif args.curve:
        jobs = [(args.curve, args.H)]
    else:
        ap.print_help()
        return
    for curve, H in jobs:
        res = run_curve(curve, H, q_start=args.q_start)
        results["curves"][curve] = res
        os.makedirs(os.path.dirname(args.out), exist_ok=True)
        with open(args.out, "w") as fh:
            json.dump(results, fh, indent=2)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
