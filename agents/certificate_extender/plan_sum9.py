#!/usr/bin/env python3
"""Check coverage of the exponent-sum-nine stage. No elimination.

Only signatures already proved in the degree-eight certificate are inherited
(reduced bounds k/gcd(k,|m|) + l/gcd(l,|n|) <= 8). Representatives of the
remaining raw normal forms are chosen greedily (smallest |m|, |n| first) and
their orbits under the frequency symmetries are checked to cover the remaining
forms exactly, with no overlap. The new representatives remain unresolved
until the certificate is built and independently checked.
"""
from math import gcd
from pathlib import Path
import json
from verify_degree7_stdlib import canonical_set, normal, orbit, require

SIGNATURES = [(5,4),(6,3),(7,2),(8,1)]
INHERIT_SUM = 8

def choose_representatives(a, b, remaining):
    reps=[]
    covered=set()
    order=sorted(((m,n) for m in range(1-a,a) for n in range(1-b,b)),
                 key=lambda mn:(abs(mn[0])+abs(mn[1]),abs(mn[0]),abs(mn[1]),-mn[0],-mn[1]))
    for m,n in order:
        key=canonical_set(normal(a,b,m,n))
        if key in remaining and key not in covered:
            block=orbit(normal(a,b,m,n),(a,b))
            require(not covered.intersection(block),'duplicate proposed orbit')
            require(block<=remaining,'orbit leaves the remaining set')
            covered.update(block)
            reps.append((m,n))
    require(covered==remaining,'representatives fail to cover remaining normal forms')
    return reps

def main():
    cases=[]
    for a,b in SIGNATURES:
        routes=[]
        remaining=set()
        for m in range(1-a,a):
            for n in range(1-b,b):
                reduced=[a//gcd(a,abs(m)), b//gcd(b,abs(n))]
                inherited=sum(reduced)<=INHERIT_SUM
                routes.append({'drops':[m,n],'reduced_bounds':reduced,
                               'status':'EXCLUDED_BY_VERIFIED_LOWER_SIGNATURE' if inherited else 'NOT_ELIMINATED'})
                if not inherited: remaining.add(canonical_set(normal(a,b,m,n)))
        reps=choose_representatives(a,b,remaining)
        cases.append({'bounds':[a,b],'raw_configurations':len(routes),
                      'inherited_exclusions':sum(r['status'].startswith('EXCLUDED') for r in routes),
                      'remaining_raw_configurations':len(remaining),
                      'new_representatives':[list(x) for x in reps],
                      'status':'PLAN_ONLY: no new elimination or exclusion claimed','routes':routes})
    total=sum(len(c['new_representatives']) for c in cases)
    report={'status':'COVERAGE_VERIFIED_PLAN_ONLY','inherit_reduced_sum_at_most':INHERIT_SUM,
            'cases':cases,'new_representatives':total,'proposed_signed_systems':48*total}
    out=Path(__file__).resolve().parent/'results'/'next_sum9_plan.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    for c in cases:
        print(tuple(c['bounds']),'raw',c['raw_configurations'],'inherited',c['inherited_exclusions'],
              'remaining',c['remaining_raw_configurations'],'reps',c['new_representatives'])
    print('new representatives',total,'proposed signed systems',48*total)
    # Case identifiers in the producer/verifier naming convention.
    ids=[]
    for c in cases:
        a,b=c['bounds']
        for m,n in c['new_representatives']:
            ids.append((f"{a}{b}_m{'minus' if m<0 else ''}{abs(m)}_n{'minus' if n<0 else ''}{abs(n)}",a,b,m,n))
    print(ids)
if __name__=='__main__':main()
