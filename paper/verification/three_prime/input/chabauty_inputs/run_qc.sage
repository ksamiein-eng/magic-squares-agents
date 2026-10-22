#!/usr/bin/env sage
# Bielliptic quadratic Chabauty for the magic-square genus-2 curves.
# Requires: Sage with the quadratic Chabauty package (or Bianchi's bielliptic QC code).
# For each curve C: Y^2 = f(w^2), rank J = 2, both elliptic quotients rank 1.
# Goal: prove C(Q) = {rational points listed}, i.e. no nondegenerate magic-square solution in that orbit.
import json
data = json.load(open("chabauty_inputs.json"))
R.<w> = QQ[]
results = {}
for name, rec in data["curves"].items():
    co = rec["sextic_coeffs_w6_to_w0"]        # a,0,b,0,c,0,d
    f = sum(QQ(co[i]) * w^(6-i) for i in range(7))
    try:
        C = HyperellipticCurve(f)
        J = C.jacobian()
        print(name, "genus", C.genus(), "  f =", f)
        # rational points up to a search bound (should be only Weierstrass / points at infinity / w=0)
        pts = C.rational_points(bound=2000)
        print("   rational points (bound 2000):", pts)
        # The bielliptic quadratic Chabauty step:
        #   from quadratic_chabauty import quadratic_chabauty_bielliptic   # Bianchi
        #   sol = quadratic_chabauty_bielliptic(C, primes=rec["good_primes_for_QC"])
        # We record the data the QC routine consumes; the call is environment-specific.
        results[name] = {"genus": int(C.genus()),
                         "rational_points_found": [str(P) for P in pts],
                         "good_primes": rec["good_primes_for_QC"],
                         "quotient_conductors": [rec["quotient1_E"]["label_conductor"],
                                                 rec["quotient2_Ep"]["label_conductor"]]}
    except Exception as e:
        print(name, "ERROR", e); results[name] = {"error": str(e)}
json.dump(results, open("qc_sage_results.json","w"), indent=1)
print("\nNext: run bielliptic QC (Bianchi's code or Sage's p-adic heights) at the recorded primes,")
print("then combine with the Mordell-Weil sieve residues in sieves_cubic.json to exclude non-trivial classes.")
