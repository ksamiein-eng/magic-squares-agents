#!/usr/bin/env python3
"""Enumerate the next stage using proved gcd-normalized signature pruning.

This file proves coverage of a proposed calculation, not an exclusion of the
remaining signatures. It computes no resultant for the exponent-sum-six cases.
"""
from math import gcd
from pathlib import Path
import json
from verify_degree5_stdlib import canonical_set, normal, orbit, require

PLANS = [((5,1), [(1,0),(2,0),(3,0),(4,0)]),
         ((4,2), [(1,1),(1,-1),(3,1),(3,-1)]),
         ((3,3), [(1,1),(1,-1),(1,2),(1,-2),(2,2),(2,-2)])]

def main():
    cases=[]
    for (a,b),reps in PLANS:
        routes=[]
        remaining=set()
        for m in range(1-a,a):
            for n in range(1-b,b):
                reduced=[a//gcd(a,abs(m)), b//gcd(b,abs(n))]
                inherited=sum(reduced)<=5
                routes.append({'drops':[m,n], 'reduced_bounds':reduced,
                               'status':'EXCLUDED_BY_VERIFIED_LOWER_SIGNATURE' if inherited else 'NOT_ELIMINATED'})
                if not inherited: remaining.add(canonical_set(normal(a,b,m,n)))
        covered=set()
        for m,n in reps:
            block=orbit(normal(a,b,m,n),(a,b))
            require(not covered.intersection(block), 'duplicate proposed orbit')
            covered.update(block)
        require(covered==remaining,'proposed representatives do not cover all remaining normal forms')
        cases.append({'bounds':[a,b], 'raw_configurations':len(routes),
                      'inherited_exclusions':sum(r['status'].startswith('EXCLUDED') for r in routes),
                      'remaining_raw_configurations':len(remaining),
                      'new_representatives':[list(v) for v in reps],
                      'status':'PLAN_ONLY: no new elimination or exclusion claimed', 'routes':routes})
    report={'status':'COVERAGE_VERIFIED_PLAN_ONLY','cases':cases,
            'new_representatives':sum(len(c['new_representatives']) for c in cases),
            'proposed_signed_systems':48*sum(len(c['new_representatives']) for c in cases)}
    path=Path(__file__).resolve().parent/'results'/'next_sum6_plan.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
