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

Iteration 2 (torsion_coset_probe_H4.py): same sweep, extended to H=4 (24 grid values, 13824 triples).
  * int64 overflow guard rewritten: at H=4, Dfull <= 25^3 = 15625, row coefficients <= Dfull, so A,B,C <= 3*15625 = 46875 and
    det, Nc, Ns <= 2*46875^2 = 4.39e9 (exact in int64), but det^2 ~ 1.9e19 exceeds 2^63.  The circle test Nc^2+Ns^2 == det^2 is
    therefore done as a float64 prefilter (|Nc^2+Ns^2-det^2| < 1e6, which can never reject a true solution since the rounding error
    of each square is < 2^-52 * 2e19 < 5e3) followed by an EXACT Python-int re-test of every surviving candidate.  The exact
    int64 range of det, Nc, Ns is asserted from the actual maxima (not assumed).
  * per-orbit checkpoints are SLIM (counts, distributions, counterexamples, <= 20 examples, in-orbit brute-force sample), so no
    multi-hundred-MB JSON is produced; orbits run in a multiprocessing pool.
Usage:  python torsion_coset_probe_H4.py 4 [workers]        (per-orbit checkpoints in results/partial_H4/)
        python torsion_coset_probe_H4.py 4 aggregate        (write results/torsion_coset_H4_summary.json + _examples.json)
"""
import itertools, json, sys, time, math, os, random
import numpy as np
from fractions import Fraction as Fr

H = int(sys.argv[1]) if len(sys.argv) > 1 else 2
MODE = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].isdigit() else 'sweep'
WORKERS = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 6
assert 1 <= H <= 4, 'overflow analysis in the header covers H<=4 only'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results'); os.makedirs(OUT, exist_ok=True)
PART = os.path.join(OUT, f'partial_H{H}'); os.makedirs(PART, exist_ok=True)
LOG = open(os.path.join(OUT, f'probe_H{H}.log'), 'a') if __name__ == '__main__' else open(os.devnull, 'w')
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
        # A,B,C are sums of three row coefficients -> |A|,|B|,|C| <= 3*mx; det,Nc,Ns are 2-term products -> <= 2*(3*mx)^2.
        # These must be exact in int64; the squares in the circle test are NOT (H=4) and are handled by prefilter + exact re-test.
        assert 2 * (3 * mx) ** 2 < 2 ** 62, ("int64 overflow guard for det/Nc/Ns", mx)
        cnt['max_abs_row_coeff'] = max(cnt.get('max_abs_row_coeff', 0), mx)
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
            cnt['max_abs_det'] = max(cnt.get('max_abs_det', 0), int(np.abs(det).max()), int(np.abs(Nc).max()), int(np.abs(Ns).max()))
            Ncf = Nc.astype(np.float64); Nsf = Ns.astype(np.float64); detf = det.astype(np.float64)
            cand = nz & (np.abs(Ncf * Ncf + Nsf * Nsf - detf * detf) < 1e6)   # float64 prefilter, cannot lose a true hit (see header)
            hit = np.zeros_like(cand)
            for idx in map(tuple, np.argwhere(cand)):
                a, b, c = int(Nc[idx]), int(Ns[idx]), int(det[idx])
                cnt['prefilter_candidates'] = cnt.get('prefilter_candidates', 0) + 1
                if a * a + b * b == c * c: hit[idx] = True                  # exact Python-int test
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

def orbit_job(oi):
    rows, osize = orbits[oi]
    fn = os.path.join(PART, f'orbit_{oi:03d}.json')
    if os.path.exists(fn): return oi, None
    t1 = time.time()
    pts, fams, cnt = sweep_orbit(oi, rows)
    P_ = [serialize_point(r) for r in pts.values()]; F_ = [serialize_family(r) for r in fams.values()]
    bycls = {}; by_ntors = {}; by_rank = {}; deg = {'zero_sine': 0, 'equal_magnitudes': 0, 'both': 0, 'neither': 0}; br = {}
    primes_all = set()
    for r in P_:
        bycls[r['class']] = bycls.get(r['class'], 0) + 1
        by_ntors[r['n_torsion_coords']] = by_ntors.get(r['n_torsion_coords'], 0) + 1
        by_rank[r['rank']] = by_rank.get(r['rank'], 0) + 1
        z = bool(r['zero_rows']); e = bool(r['equal_pairs'])
        deg['both' if z and e else 'zero_sine' if z else 'equal_magnitudes' if e else 'neither'] += 1
        for b in r['branches']: br[b] = br.get(b, 0) + 1
        for v in r['support']: primes_all |= set(int(l) for l in v)
    counter = [r for r in P_ if r['class'] == 'NOT_on_torsion_coset' or r['admissible']]
    fam_counter = [f for f in F_ if f['rank_fixed'] == 3 or f['degeneracy'] == 'NONE']
    fam_by_deg = {}; fam_by_rank = {}
    for f in F_:
        fam_by_deg[f['degeneracy']] = fam_by_deg.get(f['degeneracy'], 0) + 1
        fam_by_rank[f['rank_fixed']] = fam_by_rank.get(f['rank_fixed'], 0) + 1
    ex = sorted((r for r in P_ if r['n_torsion_coords'] == 0), key=lambda r: (-r['rank'], -max(abs(x) for k in r['kernel_basis'] for x in k), r['t']))[:20]
    # in-orbit independent cross-check: exponent-bounded brute force + sympy rank on a small random sample
    import sympy
    random.seed(1000 + oi); sample = random.sample(P_, min(4, len(P_))) + counter
    bstats = {'checked': 0, 'agree': 0, 'disagree': []}
    for r in sample:
        zs = [z_of_pq(tuple(pq)) for pq in r['pq']]; bf = brute_relation(zs, 4)
        sups = [support(tuple(pq)) for pq in r['pq']]; primes = sorted(set().union(*sups))
        M = sympy.Matrix([[v.get(l, 0) for l in primes] for v in sups]) if primes else sympy.zeros(4, 1)
        ok = (M.rank() == r['rank']) and all(check_relation(zs, k) for k in r['kernel_basis'])
        if bf is not None: ok = ok and r['class'] != 'NOT_on_torsion_coset'
        if [k for k in r['kernel_basis'] if max(abs(x) for x in k) <= 4]: ok = ok and bf is not None
        if r['class'] == 'NOT_on_torsion_coset': ok = ok and bf is None
        bstats['checked'] += 1
        if ok: bstats['agree'] += 1
        else: bstats['disagree'].append({'t': r['t'], 'brute': bf, 'record': r})
    for c in counter:
        zs = [z_of_pq(tuple(pq)) for pq in c['pq']]; sn = sines_of(rows, zs); i, j, k, l, e2, e3 = c['example_system']
        c['recheck_system_holds'] = (sn[i] - e2 * sn[k] - e3 * sn[l] == 0) and (sn[j] - e2 * sn[k] + e3 * sn[l] == 0)
        c['brute_N8'] = brute_relation(zs, 8)
    out = {'orbit': oi, 'rows': rows, 'orbit_size': osize, 'H': H, 'counts': cnt, 'n_points': len(P_), 'points_by_class': bycls,
           'points_by_number_of_torsion_coordinates': by_ntors, 'points_by_rank': by_rank, 'points_by_degeneracy': deg, 'points_by_branch': br,
           'max_rank': max(by_rank) if by_rank else 0, 'split_primes_in_supports': sorted(primes_all),
           'n_families': len(F_), 'families_by_degeneracy': fam_by_deg, 'families_by_rank_of_fixed_triple': fam_by_rank,
           'families_with_independent_fixed_triple': sum(1 for f in F_ if f['rank_fixed'] == 3),
           'families_nondegenerate': sum(1 for f in F_ if f['degeneracy'] == 'NONE'),
           'admissible_points': sum(1 for r in P_ if r['admissible']),
           'counterexample_candidates_points': counter, 'counterexample_candidates_families': fam_counter,
           'examples_no_torsion_coord_highest_rank': ex, 'brute_force_crosscheck': bstats, 'elapsed_s': round(time.time() - t1, 1)}
    json.dump(out, open(fn + '.tmp', 'w')); os.replace(fn + '.tmp', fn)
    return oi, out

def run_sweep():
    import multiprocessing as mp
    t0 = time.time()
    log(f'=== sweep H={H}: {n} grid values, {n**3} triples, {len(orbits)} orbits, {WORKERS} workers ===')
    todo = [oi for oi in range(len(orbits)) if not os.path.exists(os.path.join(PART, f'orbit_{oi:03d}.json'))]
    log(f'{len(orbits)-len(todo)} checkpoints present, {len(todo)} orbits to do')
    done = len(orbits) - len(todo)
    with mp.Pool(WORKERS) as pool:
        for oi, out in pool.imap_unordered(orbit_job, todo):
            if out is None: continue
            done += 1
            log(f'orbit {oi:3d} ({done}/{len(orbits)}) rows={out["rows"]}: {out["n_points"]} points {out["points_by_class"]} ranks {out["points_by_rank"]}, '
                f'{out["n_families"]} families (indep-fixed {out["families_with_independent_fixed_triple"]}, nondeg {out["families_nondegenerate"]}), '
                f'admissible {out["admissible_points"]}, counterex {len(out["counterexample_candidates_points"])}, maxdet {out["counts"].get("max_abs_det")}, '
                f'brute {out["brute_force_crosscheck"]["agree"]}/{out["brute_force_crosscheck"]["checked"]}, {out["elapsed_s"]}s, wall {time.time()-t0:.0f}s')
    log(f'sweep done in {time.time()-t0:.0f}s wall')

def aggregate():
    files = sorted(f for f in os.listdir(PART) if f.endswith('.json'))
    partial = len(files) < len(orbits)
    def acc(dst, src_):
        for k, v in src_.items(): dst[str(k)] = dst.get(str(k), 0) + v
    tot = {'points': 0, 'families': 0, 'elapsed_s': 0}; sysc = {}; bycls = {}; by_ntors = {}; by_rank = {}
    deg = {'zero_sine': 0, 'equal_magnitudes': 0, 'both': 0, 'neither': 0}; br = {}; fam_by_deg = {}; fam_by_rank = {}
    per_orbit = []; counter = []; fam_counter = []; examples = []; bstats = {'checked': 0, 'agree': 0, 'disagree': []}
    primes_sup = set(); max_rank = 0; max_det = 0; max_coeff = 0; adm = 0
    for f in files:
        d = json.load(open(os.path.join(PART, f)))
        tot['points'] += d['n_points']; tot['families'] += d['n_families']; tot['elapsed_s'] += d['elapsed_s']
        for k, v in d['counts'].items():
            if k.startswith('max_'): continue
            sysc[k] = sysc.get(k, 0) + v
        max_det = max(max_det, d['counts'].get('max_abs_det', 0)); max_coeff = max(max_coeff, d['counts'].get('max_abs_row_coeff', 0))
        acc(bycls, d['points_by_class']); acc(by_ntors, d['points_by_number_of_torsion_coordinates']); acc(by_rank, d['points_by_rank'])
        acc(deg, d['points_by_degeneracy']); acc(br, d['points_by_branch']); acc(fam_by_deg, d['families_by_degeneracy']); acc(fam_by_rank, d['families_by_rank_of_fixed_triple'])
        primes_sup |= set(d['split_primes_in_supports']); max_rank = max(max_rank, d['max_rank']); adm += d['admissible_points']
        counter += [dict(orbit=d['orbit'], rows=d['rows'], **c) for c in d['counterexample_candidates_points']]
        fam_counter += [dict(orbit=d['orbit'], rows=d['rows'], **c) for c in d['counterexample_candidates_families']]
        examples += [dict(orbit=d['orbit'], rows=d['rows'], **c) for c in d['examples_no_torsion_coord_highest_rank']]
        bstats['checked'] += d['brute_force_crosscheck']['checked']; bstats['agree'] += d['brute_force_crosscheck']['agree']
        bstats['disagree'] += [dict(orbit=d['orbit'], **x) for x in d['brute_force_crosscheck']['disagree']]
        per_orbit.append({k: d[k] for k in ['orbit', 'rows', 'orbit_size', 'n_points', 'points_by_class', 'points_by_rank', 'n_families',
                                            'families_with_independent_fixed_triple', 'families_nondegenerate', 'admissible_points', 'elapsed_s']})
    grid_N = sorted({p * p + q * q for p, q in PQ}); grid_primes = sorted({l for N in grid_N for l in factor(N) if l % 4 == 1})
    examples = sorted(examples, key=lambda r: (-r['rank'], -max(abs(x) for k in r['kernel_basis'] for x in k)))[:20]
    res = {'H': H, 'partial': partial, 'orbits_completed': len(files), 'grid_values': n, 'grid': [tstr(pq) for pq in PQ], 'triples': n**3, 'orbits': len(orbits), 'raw_confs': len(confs),
           'grid_norms_p2_plus_q2': grid_N, 'split_primes_in_grid': grid_primes, 'split_primes_in_all_supports_incl_solved_coord': sorted(primes_sup),
           'max_exponent_rank_observed': max_rank, 'overflow_guard': {'max_abs_row_coeff': max_coeff, 'max_abs_det_Nc_Ns': max_det, 'int64_limit': 2**63 - 1,
                                                                        'circle_test': 'float64 prefilter |Nc^2+Ns^2-det^2|<1e6 then exact Python-int re-test'},
           'system_evaluations': sysc, 'totals': tot, 'points_by_class': bycls, 'points_by_exponent_rank': by_rank,
           'points_by_number_of_torsion_coordinates': by_ntors, 'points_by_degeneracy': deg, 'points_by_branch': br, 'admissible_points': adm,
           'families_by_degeneracy': fam_by_deg, 'families_by_rank_of_fixed_triple': fam_by_rank,
           'counterexample_candidates_points': counter, 'counterexample_candidates_families': fam_counter,
           'brute_force_crosscheck': {'checked': bstats['checked'], 'agree': bstats['agree'], 'n_disagree': len(bstats['disagree']), 'disagree': bstats['disagree'][:20]},
           'per_orbit': per_orbit}
    fn = os.path.join(OUT, f'torsion_coset_H{H}_summary.json'); json.dump(res, open(fn, 'w'), indent=1)
    json.dump({'H': H, 'partial': partial, 'orbits_completed': len(files), 'description': 'up to 20 points with no torsion coordinate and the highest exponent rank seen, with relation basis',
               'examples': examples}, open(os.path.join(OUT, f'torsion_coset_H{H}_examples.json'), 'w'), indent=1)
    log(f'aggregate written to {fn} (partial={partial}, {len(files)}/{len(orbits)} orbits)')
    log(json.dumps({k: res[k] for k in ['totals', 'points_by_class', 'points_by_exponent_rank', 'points_by_number_of_torsion_coordinates', 'points_by_degeneracy',
                                        'points_by_branch', 'families_by_degeneracy', 'families_by_rank_of_fixed_triple', 'system_evaluations', 'overflow_guard',
                                        'split_primes_in_grid', 'split_primes_in_all_supports_incl_solved_coord', 'admissible_points']}, indent=1))
    log('counterexample candidate points:', len(counter), ' families:', len(fam_counter), ' brute:', bstats['checked'], 'checked', bstats['agree'], 'agree')

if __name__ == '__main__':
    if MODE == 'aggregate': aggregate()
    else: run_sweep()
