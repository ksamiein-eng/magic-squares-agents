"""torsion_coset_probe.py -- exhaustive record of EVERY exact rational-circle solution of every signed system, for all
113 full-depth four-parameter orbit representatives, with three parameters tan(chi_j/2) of projective height <= H,
and an EXACT (complete, not exponent-bounded) test of the torsion-coset hypothesis (Conjecture `conj:torsion` of
rigidity.tex) at each solution.

Adapted from paper/verification/four_prime/r4search.py (same orbits, grid, linear forms and three branches), but every
exact solution is recorded -- not only admissible ones -- and deduplicated per configuration.

Torsion-coset test.  A point of T(Q) with tan(chi/2)=p/q (lowest terms) is z = (q+ip)/(q-ip) = w/conj(w), w=q+ip.
Since gcd(p,q)=1, no rational prime divides w; for each split prime l = a^2+b^2 (l = 1 mod 4) dividing N=p^2+q^2 exactly
one of pi=a+bi, conj(pi) divides w, with multiplicity v_l(N).  Hence in Q(i)^*/units,
        z = prod_l (pi_l/conj(pi_l))^{e_l(z)},  e_l(z) = +-v_l(N),
and (1+i)/(1-i)=i, inert primes contribute nothing.  T(Q) = {+-1,+-i} x (free abelian group on the pi_l/conj(pi_l)),
so   prod_j z_j^{n_j} in {+-1,+-i}   <=>   sum_j n_j e(z_j) = 0 in Z^{(split primes)}.
Thus a nontrivial relation exists iff the 4 exponent vectors e(z_j) are linearly dependent, i.e. rank < 4.  This is a
complete test: it is not bounded by the size of the exponents.

Usage:  python torsion_coset_probe.py H [START END]      (H<=3; per-orbit checkpoints in results/partial_H{H}/)
        python torsion_coset_probe.py H aggregate         (write results/torsion_coset_H{H}.json)
"""
import itertools, json, sys, time, math, os, random
import numpy as np
from fractions import Fraction as Fr

H = int(sys.argv[1]) if len(sys.argv) > 1 else 2
MODE = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].isdigit() else 'sweep'
START = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 0
END = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
assert 1 <= H <= 3, "int64 exactness of det^2 is only guaranteed for H<=3 (see overflow guard)"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results'); os.makedirs(OUT, exist_ok=True)
PART = os.path.join(OUT, f'partial_H{H}'); os.makedirs(PART, exist_ok=True)
LOG = open(os.path.join(OUT, f'probe_H{H}.log'), 'a')
def log(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); LOG.write(s + '\n'); LOG.flush()

# ---------------- configurations and orbits (identical to r4search.py) ----------------
vecs = [v for v in itertools.product((-1, 0, 1), repeat=4) if any(v) and v[next(i for i, x in enumerate(v) if x)] > 0]
def canon(v):
    i = next(k for k, x in enumerate(v) if x); return tuple(v) if v[i] > 0 else tuple(-x for x in v)
confs = [frozenset(S) for S in itertools.combinations(vecs, 4) if all(sum(1 for v in S if v[c] != 0) >= 3 for c in range(4))]
G = [(sg, pm) for sg in itertools.product((1, -1), repeat=4) for pm in itertools.permutations(range(4))]
act = lambda g, v: canon([g[0][i] * v[g[1][i]] for i in range(4)])
orbits = []; seen = set()
for S in confs:
    if S in seen: continue
    orb = {frozenset(act(g, v) for v in S) for g in G}; seen |= orb; orbits.append((sorted(S), len(orb)))
assert len(confs) == 11862 and len(orbits) == 113

# ---------------- grid of rationals of height <= H (identical to r4search.py) ----------------
vals = sorted({Fr(p, q) for p in range(-H, H + 1) for q in range(1, H + 1)}, key=lambda f: (abs(f.numerator) + f.denominator, f))
PQ = [(f.numerator, f.denominator) for f in vals] + [(1, 0)]          # infinity = [1:0], chi = pi
vals = vals + ['inf']
P = np.array([pq[0] for pq in PQ], dtype=np.int64); Q = np.array([pq[1] for pq in PQ], dtype=np.int64)
Cc = Q * Q - P * P; Ss = 2 * P * Q; Dd = Q * Q + P * P          # cos=Cc/Dd, sin=Ss/Dd
n = len(vals)
systems = [(i, j, k, l, e2, e3) for i, j in itertools.combinations(range(4), 2)
           for k in [x for x in range(4) if x not in (i, j)] for l in [x for x in range(4) if x not in (i, j) and x != k]
           for e2 in (1, -1) for e3 in (1, -1)]
assert len(systems) == 48

# ---------------- exact Gaussian-rational arithmetic ----------------
ONE = (Fr(1), Fr(0))
TORSION = {(Fr(1), Fr(0)), (Fr(-1), Fr(0)), (Fr(0), Fr(1)), (Fr(0), Fr(-1))}
def gmul(a, b): return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])
def gpow(z, m):
    if m < 0: z = (z[0], -z[1]); m = -m          # |z|=1, so z^{-1} = conj(z)
    r = ONE
    for _ in range(m): r = gmul(r, z)
    return r
def z_of_pq(pq):
    p, q = pq; N = p * p + q * q; return (Fr(q * q - p * p, N), Fr(2 * p * q, N))
def pq_of_cs(c, s):
    assert c * c + s * s == 1
    if c == -1: return (1, 0)
    t = s / (1 + c); pq = (t.numerator, t.denominator); assert z_of_pq(pq) == (c, s); return pq
def tstr(pq): return 'inf' if pq[1] == 0 else str(Fr(pq[0], pq[1]))
def sines_of(rows, zs):
    out = []
    for m in rows:
        w = ONE
        for j in range(4):
            if m[j]: w = gmul(w, gpow(zs[j], m[j]))
        out.append(w[1])
    return out

# ---------------- Gaussian-prime support and exact kernel test ----------------
def factor(N):
    f = {}; d = 2
    while d * d <= N:
        while N % d == 0: f[d] = f.get(d, 0) + 1; N //= d
        d += 1
    if N > 1: f[N] = f.get(N, 0) + 1
    return f
_rep = {}
def split_rep(l):
    """canonical a+bi with a>b>0, a^2+b^2=l, for a prime l = 1 mod 4"""
    if l not in _rep:
        for b in range(1, math.isqrt(l) + 1):
            a2 = l - b * b; a = math.isqrt(a2)
            if a * a == a2 and a > b: _rep[l] = (a, b); break
    return _rep[l]
def support(pq):
    """exponent vector e(z) : {split prime l -> +-v_l(p^2+q^2)} for z = (q+ip)/(q-ip)"""
    p, q = pq; N = p * p + q * q; v = {}
    for l, e in factor(N).items():
        if l == 2: continue
        assert l % 4 == 1, (pq, l)
        a, b = split_rep(l)
        if (q * a + p * b) % l == 0 and (p * a - q * b) % l == 0: v[l] = e          # pi | w
        else:
            assert (q * a - p * b) % l == 0 and (p * a + q * b) % l == 0, (pq, l); v[l] = -e   # conj(pi) | w
    return v
def integer_kernel(sups):
    """rank of the exponent vectors and a primitive integer basis of {n : sum_j n_j e(z_j) = 0}"""
    primes = sorted(set().union(*sups)); k = len(sups)
    rows = [[Fr(v.get(l, 0)) for v in sups] for l in primes]        # M^T : primes x k
    piv = []; r = 0
    for c in range(k):
        pr = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if pr is None: continue
        rows[r], rows[pr] = rows[pr], rows[r]
        pv = rows[r][c]; rows[r] = [x / pv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]; rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        piv.append(c); r += 1
    basis = []
    for fc in [c for c in range(k) if c not in piv]:
        nv = [Fr(0)] * k; nv[fc] = Fr(1)
        for i, pc in enumerate(piv): nv[pc] = -rows[i][fc]
        L = 1
        for x in nv: L = L * x.denominator // math.gcd(L, x.denominator)
        ni = [int(x * L) for x in nv]; g = 0
        for x in ni: g = math.gcd(g, abs(x))
        basis.append([x // g for x in ni])
    return len(piv), basis
def classify(pqs):
    sups = [support(pq) for pq in pqs]
    rank, basis = integer_kernel(sups)
    if rank == 0: cls = 'all_torsion'
    elif rank < len(pqs): cls = 'on_torsion_coset'
    else: cls = 'NOT_on_torsion_coset'
    return cls, rank, basis, sups
def brute_relation(zs, N):
    """exponent-bounded search, independent of the prime-support machinery: first n with |n_j|<=N, n!=0,
    prod z_j^{n_j} in {+-1,+-i}; ordered by max-norm so the first hit is a smallest relation"""
    pw = [[gpow(z, m) for m in range(-N, N + 1)] for z in zs]
    for M in range(1, N + 1):
        for nv in itertools.product(range(-M, M + 1), repeat=len(zs)):
            if max(abs(x) for x in nv) != M: continue
            w = pw[0][nv[0] + N]
            for j in range(1, len(zs)): w = gmul(w, pw[j][nv[j] + N])
            if w in TORSION: return list(nv)
    return None
def check_relation(zs, nv):
    w = ONE
    for z, m in zip(zs, nv): w = gmul(w, gpow(z, m))
    return w in TORSION

def admissible(mags):
    mags = sorted(mags)
    if 0 in mags or len(set(mags)) < 4: return None
    for a_i, b_i in itertools.combinations(range(4), 2):
        A, B = max(mags[a_i], mags[b_i]), min(mags[a_i], mags[b_i]); rest = sorted(mags[k] for k in range(4) if k not in (a_i, b_i))
        if rest == sorted([A + B, A - B]) and A != 2 * B: return (A, B)
    return None
def isq(N):
    if N < 0: return None
    r = math.isqrt(N); return r if r * r == N else None

# ---------------- the sweep ----------------
def sweep_orbit(oi, rows):
    pts = {}; fams = {}
    cnt = {'systems': 0, 'cramer_hits': 0, 'singular_cases': 0, 'singular_hits': 0, 'allzero_systems': 0}
    for solved in range(4):
        others = [c for c in range(4) if c != solved]
        Cs = []; Sn = []; Dn = []
        for ax, c in enumerate(others):
            s = [1, 1, 1]; s[ax] = n
            Cs.append(Cc.reshape(s)); Sn.append(Ss.reshape(s)); Dn.append(Dd.reshape(s))
        Dfull = Dn[0] * Dn[1] * Dn[2]
        R = []                      # per row: Dfull*sin(row) = A*cos(chi_solved) + B*sin(chi_solved) + C
        for m in rows:
            C = np.ones((1, 1, 1), dtype=np.int64); S = np.zeros((1, 1, 1), dtype=np.int64); D = np.ones((1, 1, 1), dtype=np.int64)
            for ax, c in enumerate(others):
                if m[c] == 0: continue
                sj = Sn[ax] * m[c]
                C, S = C * Cs[ax] - S * sj, S * Cs[ax] + C * sj; D = D * Dn[ax]
            scale = Dfull // D
            if m[solved] == 0: R.append((np.zeros_like(Dfull), np.zeros_like(Dfull), S * scale))
            else: R.append((S * scale, (C * m[solved]) * scale, np.zeros_like(Dfull)))
        mx = max(int(np.abs(x).max()) for r in R for x in r)
        assert 3 * mx < 39000, "int64 overflow guard for det^2 / Nc^2+Ns^2"
        rowzero = np.zeros(Dfull.shape, dtype=bool)
        for r in range(4): rowzero |= (R[r][0] == 0) & (R[r][1] == 0) & (R[r][2] == 0)
        pm = np.zeros(Dfull.shape, dtype=bool)
        for r in range(4):
            for r2 in range(r + 1, 4):
                pm |= ((R[r][0] == R[r2][0]) & (R[r][1] == R[r2][1]) & (R[r][2] == R[r2][2])) | ((R[r][0] == -R[r2][0]) & (R[r][1] == -R[r2][1]) & (R[r][2] == -R[r2][2]))

        def add_point(idx, c4, s4, system, branch):
            pqs = [None] * 4
            for ax, c in enumerate(others): pqs[c] = PQ[idx[ax]]
            pqs[solved] = pq_of_cs(c4, s4)
            key = tuple(pqs)
            if key in pts:
                rec = pts[key]; rec['hits'] += 1; rec['systems'].add(system); rec['branches'].add(branch); rec['solved_coords'].add(solved); return
            zs = [z_of_pq(pq) for pq in pqs]
            sn = sines_of(rows, zs)
            i, j, k, l, e2, e3 = system
            assert sn[i] - e2 * sn[k] - e3 * sn[l] == 0 and sn[j] - e2 * sn[k] + e3 * sn[l] == 0, (oi, key, system)
            # cross-check against the linear forms
            assert all(sn[r] == (Fr(int(R[r][0][idx])) * c4 + Fr(int(R[r][1][idx])) * s4 + Fr(int(R[r][2][idx]))) / Fr(int(Dfull[idx])) for r in range(4))
            cls, rank, basis, sups = classify(pqs)
            mags = [abs(x) for x in sn]
            pts[key] = {'pq': pqs, 'z': zs, 'sines': sn, 'class': cls, 'rank': rank, 'kernel': basis, 'support': sups,
                        'n_torsion_coords': sum(1 for v in sups if not v),
                        'zero_rows': [r for r in range(4) if sn[r] == 0],
                        'equal_pairs': [(r, r2) for r in range(4) for r2 in range(r + 1, 4) if mags[r] == mags[r2]],
                        'admissible': admissible(mags) is not None,
                        'hits': 1, 'systems': {system}, 'branches': {branch}, 'solved_coords': {solved}}

        for system in systems:
            (i, j, k, l, e2, e3) = system
            A1 = R[i][0] - e2 * R[k][0] - e3 * R[l][0]; B1 = R[i][1] - e2 * R[k][1] - e3 * R[l][1]; C1 = R[i][2] - e2 * R[k][2] - e3 * R[l][2]
            A2 = R[j][0] - e2 * R[k][0] + e3 * R[l][0]; B2 = R[j][1] - e2 * R[k][1] + e3 * R[l][1]; C2 = R[j][2] - e2 * R[k][2] + e3 * R[l][2]
            det = A1 * B2 - A2 * B1; Nc = C2 * B1 - C1 * B2; Ns = A2 * C1 - A1 * C2
            cnt['systems'] += 1
            nz = det != 0
            hit = nz & (Nc * Nc + Ns * Ns == det * det)                       # exact in int64 (guarded above)
            allzero = (A1 == 0) & (B1 == 0) & (C1 == 0) & (A2 == 0) & (B2 == 0) & (C2 == 0)
            sing = (~nz) & (~allzero)
            # --- Cramer branch ---
            for idx in map(tuple, np.argwhere(hit)):
                cnt['cramer_hits'] += 1
                add_point(idx, Fr(int(Nc[idx]), int(det[idx])), Fr(int(Ns[idx]), int(det[idx])), system, 'cramer')
            # --- singular (line-circle) branch ---
            for idx in map(tuple, np.argwhere(sing)):
                cnt['singular_cases'] += 1
                a1, b1, c1, a2, b2, c2 = int(A1[idx]), int(B1[idx]), int(C1[idx]), int(A2[idx]), int(B2[idx]), int(C2[idx])
                lines = [(a1, b1, c1), (a2, b2, c2)]
                if (a1, b1) == (0, 0) and c1 != 0: continue
                if (a2, b2) == (0, 0) and c2 != 0: continue
                if (a1, b1) != (0, 0) and (a2, b2) != (0, 0) and (a1 * c2 != a2 * c1 or b1 * c2 != b2 * c1): continue
                a, b, c = [L for L in lines if (L[0], L[1]) != (0, 0)][0]
                rt = isq(a * a + b * b - c * c)
                if rt is None: continue
                for sgn in (1, -1):
                    c4 = Fr(-a * c + sgn * b * rt, a * a + b * b); s4 = Fr(-b * c - sgn * a * rt, a * a + b * b)
                    assert c4 * c4 + s4 * s4 == 1
                    cnt['singular_hits'] += 1
                    add_point(idx, c4, s4, system, 'singular')
            # --- identically-zero branch: free-angle family ---
            for idx in map(tuple, np.argwhere(allzero)):
                cnt['allzero_systems'] += 1
                fixed = tuple(PQ[idx[ax]] for ax in range(3))
                key = (solved, fixed)
                if key in fams: fams[key]['systems'].add(system); continue
                sups = [support(pq) for pq in fixed]
                rank, basis = integer_kernel(sups)
                fams[key] = {'solved': solved, 'fixed': dict(zip(others, fixed)), 'support': sups, 'rank_fixed': rank, 'kernel_fixed': basis,
                             'n_torsion_coords': sum(1 for v in sups if not v),
                             'degeneracy': 'row_identically_zero' if rowzero[idx] else ('two_rows_identically_pm_equal' if pm[idx] else 'NONE'),
                             'coeffs': [[int(R[r][0][idx]), int(R[r][1][idx]), int(R[r][2][idx])] for r in range(4)], 'Dfull': int(Dfull[idx]),
                             'systems': {system}}
    return pts, fams, cnt

def serialize_point(rec):
    return {'t': [tstr(pq) for pq in rec['pq']], 'pq': [list(pq) for pq in rec['pq']],
            'z': [[str(c), str(s)] for c, s in rec['z']], 'sines': [str(x) for x in rec['sines']],
            'class': rec['class'], 'rank': rec['rank'], 'kernel_basis': rec['kernel'],
            'support': [{str(l): e for l, e in v.items()} for v in rec['support']], 'n_torsion_coords': rec['n_torsion_coords'],
            'zero_rows': rec['zero_rows'], 'equal_pairs': rec['equal_pairs'], 'admissible': rec['admissible'],
            'hits': rec['hits'], 'n_systems': len(rec['systems']), 'example_system': sorted(rec['systems'])[0],
            'branches': sorted(rec['branches']), 'solved_coords': sorted(rec['solved_coords'])}
def serialize_family(rec):
    return {'solved_coord': rec['solved'], 'fixed_t': {str(c): tstr(pq) for c, pq in rec['fixed'].items()},
            'support': [{str(l): e for l, e in v.items()} for v in rec['support']], 'rank_fixed': rec['rank_fixed'], 'kernel_fixed': rec['kernel_fixed'],
            'n_torsion_coords': rec['n_torsion_coords'], 'degeneracy': rec['degeneracy'],
            'sine_coeffs_ABC_over_Dfull': rec['coeffs'], 'Dfull': rec['Dfull'], 'n_systems': len(rec['systems']), 'example_system': sorted(rec['systems'])[0]}

def run_sweep():
    t0 = time.time()
    log(f'=== sweep H={H}: {n} grid values, {n**3} triples, orbits {START}..{min(END, len(orbits))-1} ===')
    for oi, (rows, osize) in enumerate(orbits):
        if oi < START or oi >= END: continue
        fn = os.path.join(PART, f'orbit_{oi:03d}.json')
        if os.path.exists(fn):
            log(f'orbit {oi}: checkpoint exists, skipping'); continue
        t1 = time.time()
        pts, fams, cnt = sweep_orbit(oi, rows)
        P_ = [serialize_point(r) for r in pts.values()]; F_ = [serialize_family(r) for r in fams.values()]
        bycls = {}
        for r in P_: bycls[r['class']] = bycls.get(r['class'], 0) + 1
        out = {'orbit': oi, 'rows': rows, 'orbit_size': osize, 'H': H, 'counts': cnt, 'n_points': len(P_), 'points_by_class': bycls,
               'n_families': len(F_), 'families_with_independent_fixed_triple': sum(1 for f in F_ if f['rank_fixed'] == 3),
               'families_nondegenerate': sum(1 for f in F_ if f['degeneracy'] == 'NONE'),
               'admissible_points': sum(1 for r in P_ if r['admissible']), 'elapsed_s': round(time.time() - t1, 1),
               'points': P_, 'families': F_}
        json.dump(out, open(fn + '.tmp', 'w')); os.replace(fn + '.tmp', fn)
        log(f'orbit {oi:3d}/{len(orbits)} rows={rows}: {len(P_)} points {bycls}, {len(F_)} families '
            f'(indep-fixed {out["families_with_independent_fixed_triple"]}, nondeg {out["families_nondegenerate"]}), '
            f'admissible {out["admissible_points"]}, {out["elapsed_s"]}s, total {time.time()-t0:.0f}s')
    log(f'sweep chunk done in {time.time()-t0:.0f}s')

def aggregate():
    files = sorted(os.listdir(PART)); files = [f for f in files if f.endswith('.json')]
    assert len(files) == len(orbits), f'only {len(files)} of {len(orbits)} orbit checkpoints present'
    per_orbit = []; nontrivial = []; counter = []; fam_counter = []; tot = {'points': 0, 'families': 0, 'elapsed_s': 0}
    bycls = {}; by_ntors = {}; deg = {'zero_sine': 0, 'equal_magnitudes': 0, 'both': 0, 'neither': 0}; branch_cnt = {}
    fam_by_deg = {}; fam_by_rank = {}; sysc = {}
    sample_for_brute = []
    for f in files:
        d = json.load(open(os.path.join(PART, f)))
        tot['points'] += d['n_points']; tot['families'] += d['n_families']; tot['elapsed_s'] += d['elapsed_s']
        for k, v in d['counts'].items(): sysc[k] = sysc.get(k, 0) + v
        per_orbit.append({k: d[k] for k in ['orbit', 'rows', 'orbit_size', 'n_points', 'points_by_class', 'n_families',
                                            'families_with_independent_fixed_triple', 'families_nondegenerate', 'admissible_points', 'elapsed_s']})
        for r in d['points']:
            bycls[r['class']] = bycls.get(r['class'], 0) + 1
            by_ntors[r['n_torsion_coords']] = by_ntors.get(r['n_torsion_coords'], 0) + 1
            z = bool(r['zero_rows']); e = bool(r['equal_pairs'])
            deg['both' if z and e else 'zero_sine' if z else 'equal_magnitudes' if e else 'neither'] += 1
            for b in r['branches']: branch_cnt[b] = branch_cnt.get(b, 0) + 1
            if r['class'] != 'all_torsion':
                nontrivial.append(dict(orbit=d['orbit'], **r))
            if r['class'] == 'NOT_on_torsion_coset' or r['admissible']: counter.append(dict(orbit=d['orbit'], rows=d['rows'], **r))
            sample_for_brute.append((d['orbit'], r))
        for fm in d['families']:
            fam_by_deg[fm['degeneracy']] = fam_by_deg.get(fm['degeneracy'], 0) + 1
            fam_by_rank[fm['rank_fixed']] = fam_by_rank.get(fm['rank_fixed'], 0) + 1
            if fm['rank_fixed'] == 3 or fm['degeneracy'] == 'NONE': fam_counter.append(dict(orbit=d['orbit'], rows=d['rows'], **fm))
    # ---- independent cross-check: exponent-bounded brute force on a sample, and sympy rank ----
    import sympy
    random.seed(12345)
    sample = random.sample(sample_for_brute, min(400, len(sample_for_brute)))
    sample += [(c['orbit'], c) for c in counter]
    brute_stats = {'checked': 0, 'agree': 0, 'disagree': []}
    N_BRUTE = 4
    for oi, r in sample:
        zs = [z_of_pq(tuple(pq)) for pq in r['pq']]
        bf = brute_relation(zs, N_BRUTE)
        sups = [support(tuple(pq)) for pq in r['pq']]
        primes = sorted(set().union(*sups))
        M = sympy.Matrix([[v.get(l, 0) for l in primes] for v in sups]) if primes else sympy.zeros(4, 1)
        srank = M.rank()
        kern_small = [k for k in r['kernel_basis'] if max(abs(x) for x in k) <= N_BRUTE]
        ok = (srank == r['rank']) and all(check_relation(zs, k) for k in r['kernel_basis'])
        if bf is not None: ok = ok and r['class'] != 'NOT_on_torsion_coset'
        if kern_small: ok = ok and bf is not None
        if r['class'] == 'NOT_on_torsion_coset': ok = ok and bf is None
        brute_stats['checked'] += 1
        if ok: brute_stats['agree'] += 1
        else: brute_stats['disagree'].append({'orbit': oi, 't': r['t'], 'brute': bf, 'sympy_rank': srank, 'record': r})
    # ---- counterexample candidates: independent re-verification ----
    verified_counter = []
    for c in counter:
        zs = [z_of_pq(tuple(pq)) for pq in c['pq']]; sn = sines_of(c['rows'], zs)
        i, j, k, l, e2, e3 = c['example_system']
        sysok = (sn[i] - e2 * sn[k] - e3 * sn[l] == 0) and (sn[j] - e2 * sn[k] + e3 * sn[l] == 0)
        verified_counter.append(dict(c, recheck_sines=[str(x) for x in sn], recheck_system_holds=sysok, brute_N8=brute_relation(zs, 8)))
    verified_fam_counter = []
    for fm in fam_counter:
        verified_fam_counter.append(fm)
    res = {'H': H, 'grid_values': n, 'grid': [tstr(pq) for pq in PQ], 'triples': n**3, 'orbits': len(orbits), 'raw_confs': len(confs),
           'system_evaluations': sysc, 'totals': tot, 'points_by_class': bycls, 'points_by_number_of_torsion_coordinates': by_ntors,
           'points_by_degeneracy': deg, 'points_by_branch': branch_cnt,
           'families_by_degeneracy': fam_by_deg, 'families_by_rank_of_fixed_triple': fam_by_rank,
           'counterexample_candidates_points': verified_counter, 'counterexample_candidates_families': verified_fam_counter,
           'brute_force_crosscheck': brute_stats, 'per_orbit': per_orbit, 'nontrivial_points': nontrivial}
    fn = os.path.join(OUT, f'torsion_coset_H{H}.json')
    json.dump(res, open(fn, 'w'), indent=1)
    log(f'aggregate written to {fn}')
    log(json.dumps({k: res[k] for k in ['totals', 'points_by_class', 'points_by_number_of_torsion_coordinates', 'points_by_degeneracy', 'points_by_branch',
                                        'families_by_degeneracy', 'families_by_rank_of_fixed_triple', 'system_evaluations']}, indent=1))
    log('counterexample candidate points:', len(verified_counter), ' families:', len(verified_fam_counter))
    log('brute-force cross-check:', brute_stats['checked'], 'checked,', brute_stats['agree'], 'agree,', len(brute_stats['disagree']), 'disagree')

if __name__ == '__main__':
    if MODE == 'aggregate': aggregate()
    else: run_sweep()
