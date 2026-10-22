#!/usr/bin/env python3
"""Check coverage of the proposed exponent-sum-seven stage. No elimination.

Only signatures already proved in the degree-six certificate are inherited.
The proposed new representatives remain unresolved until checked separately.
"""
from math import gcd
from pathlib import Path
import json
from verify_degree6_stdlib import canonical_set, normal, orbit, require

PLANS = [((6,1), [(1,0),(5,0)]),
         ((5,2), [(m,n) for m in (1,2,3,4) for n in (1,-1)]),
         ((4,3), [(m,n) for m in (1,3) for n in (1,-1,2,-2)])]

def main():
    cases=[]
    for (a,b),reps in PLANS:
        routes=[]
        remaining=set()
        for m in range(1-a,a):
            for n in range(1-b,b):
                reduced=[a//gcd(a,abs(m)), b//gcd(b,abs(n))]
                inherited=sum(reduced)<=6
                routes.append({'drops':[m,n], 'reduced_bounds':reduced,
                               'status':'EXCLUDED_BY_VERIFIED_LOWER_SIGNATURE' if inherited else 'NOT_ELIMINATED'})
                if not inherited: remaining.add(canonical_set(normal(a,b,m,n)))
        covered=set()
        for m,n in reps:
            block=orbit(normal(a,b,m,n),(a,b))
            require(not covered.intersection(block),'duplicate proposed orbit')
            covered.update(block)
        require(covered==remaining,'representatives fail to cover remaining normal forms')
        cases.append({'bounds':[a,b],'raw_configurations':len(routes),
                      'inherited_exclusions':sum(r['status'].startswith('EXCLUDED') for r in routes),
                      'remaining_raw_configurations':len(remaining),
                      'new_representatives':[list(x) for x in reps],
                      'status':'PLAN_ONLY: no new elimination or exclusion claimed','routes':routes})
    report={'status':'COVERAGE_VERIFIED_PLAN_ONLY','cases':cases,
            'new_representatives':sum(len(c['new_representatives']) for c in cases),
            'proposed_signed_systems':48*sum(len(c['new_representatives']) for c in cases)}
    out=Path(__file__).resolve().parent/'results'/'next_sum7_plan.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
