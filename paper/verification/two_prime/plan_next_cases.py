#!/usr/bin/env python3
"""Derive sum-five coverage using proved pruning rules. Does NOT solve new systems."""
from fractions import Fraction
from pathlib import Path
import json
from verify_degree4_stdlib import canonical_set, normal, orbit, require


def inherited(a,b,m,n):
    ratios={Fraction(0),Fraction(1,2),Fraction(1,3),Fraction(2,3)}
    if n==0 and Fraction(abs(m),a) in ratios:return True
    if m==0 and Fraction(abs(n),b) in ratios:return True
    return Fraction(abs(m),a)==Fraction(1,2) and Fraction(abs(n),b)==Fraction(1,2)


def main():
    results=[]
    for (a,b), reps in [((4,1),[(1,0),(3,0)]),((3,2),[(1,1),(1,-1),(2,1),(2,-1)])]:
        raw=[(m,n) for m in range(1-a,a) for n in range(1-b,b)]
        remaining={canonical_set(normal(a,b,m,n)) for m,n in raw if not inherited(a,b,m,n)}
        covered=set()
        for m,n in reps:
            block=orbit(normal(a,b,m,n),(a,b))
            require(not (covered&block),'overlapping proposed representatives')
            covered |= block
        require(covered==remaining,'next-stage coverage discrepancy')
        results.append({'bounds':[a,b],'raw_configurations':len(raw),
                        'inherited_exclusions':len(raw)-len(remaining),
                        'remaining_raw_configurations':len(remaining),
                        'new_representatives':[list(r) for r in reps],
                        'status':'UNCOMPUTED: representative coverage only'})
    report={'status':'PLAN_ONLY_NOT_AN_EXCLUSION_CERTIFICATE','cases':results,
            'new_representatives':sum(len(c['new_representatives']) for c in results),
            'proposed_signed_systems':288}
    path=Path(__file__).resolve().parent/'results'/'next_sum5_plan.json'
    path.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
