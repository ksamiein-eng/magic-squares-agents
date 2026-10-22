# Version 1 to version 2

The v1 core and the original full manuscript are preserved as separate input
artifacts. This release replaces only the working core and its status summary.

## Completed in v2

1. Proved the complete configuration reductions for (3,1) and (2,2).
2. Regenerated four new representative calculations, 48 signed systems each.
3. Reverified the (2,1) representative in the new unified certificate.
4. Added a standard-library verifier with exact degree-bounded determinant
   identity checks and an independent Chebyshev/direct-symbolic checker.
5. Checked all permitted finite fibers, removed t=0 components, and parameters
   at infinity. For (3,1), t=+/-1 is excluded by equal offsets, not by a zero
   offset; the distinction is explicit in both proof and checker.
6. Raised the certified two-prime central-root exponent bound from 4 to 5.
7. Added one-way harmonic inheritance and uniform deficiency-ratio exclusions.

## Not reinstated

The earlier full manuscript's exponent-sum-seven exclusion, other three-prime
closures, genus classifications, global saturation claims, and large height
bounds are still unverified. The existing E_B/E_C complementary-quotient proof
is retained, but complete rational points on their genus-two cover remain a
separate problem. There is no claim of historical novelty in this release.

## Next highest priority

At exponent sum five, (4,1) needs only the new drop representatives (1,0) and
(3,0). The (3,2) pair needs (1,1), (1,-1), (2,1), (2,-1). All other raw
configurations follow from proved pruning rules. These six representatives
would require 288 new signed systems. They are planned, not certified here.
