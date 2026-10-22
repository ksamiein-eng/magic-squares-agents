#!/usr/bin/env python3
"""Negative tests and arithmetic regressions for the degree-eight verifier (adapted from test_degree7_verifier.py)."""
from __future__ import annotations
from copy import deepcopy
from itertools import permutations
from pathlib import Path
from fractions import Fraction
import json
import random
import verify_degree8_stdlib as v

ROOT=Path(__file__).resolve().parent


def main():
    original=json.loads((ROOT/'results'/'certificate_degree8.json').read_text())
    outcomes=[]
    def reject(name, mutate):
        data=deepcopy(original)
        mutate(data)
        try:
            v.verify(data)
        except RuntimeError as e:
            outcomes.append({'test':name,'status':'PASS: rejected','reason':str(e)})
        else:
            raise RuntimeError('Verifier accepted mutation: '+name)
    reject('missing exponent case', lambda d:d['cases'].pop())
    reject('missing signed system', lambda d:d['cases'][1]['systems'].pop())
    reject('altered frequency', lambda d:d['cases'][1]['frequencies'][2].__setitem__(0,2))
    reject('altered sine numerator', lambda d:d['cases'][0]['area_numerators'][0][0].__setitem__(1,123))
    reject('altered determinant coefficient', lambda d:d['cases'][0]['systems'][0]['resultant'][0].__setitem__(1,123))
    reject('invalid removed factor', lambda d:d['cases'][0]['systems'][0].__setitem__('removed_t_power',9))
    first_no_root=next(i for i,f in enumerate(original['factor_catalog']) if f['type']=='no_rational_root')
    reject('composite alleged prime', lambda d:d['factor_catalog'][first_no_root].__setitem__('prime',9))
    reject('false modular residues', lambda d:d['factor_catalog'][first_no_root]['residues'].__setitem__(0,0))
    reject('missing factor in product', lambda d:d['cases'][0]['systems'][0]['factors'].pop())
    def invisible_high_degree(d):
        r=d['cases'][0]['systems'][0]
        f,g=v.decode(r['F']),v.decode(r['G'])
        m,n=v.degree(f,1),v.degree(g,1)
        D=n*v.degree(f,0)+m*v.degree(g,0)
        # Vanishes at every point used for checking a degree-D identity.
        # It must nevertheless be rejected by the independent degree bound.
        p=v.ONE
        for k in range(D+1):p=v.mul(p,v.add(v.T,v.scale(v.ONE,-k)))
        forged=v.add(v.decode(r['resultant'],1),p)
        r['resultant']=[[[i],c] for (i,j),c in sorted(forged.items(),reverse=True)]
    reject('higher degree polynomial invisible on evaluation grid',invisible_high_degree)
    es=[v.numerator(f,(3,1)) for f in v.normal(3,1,1,0)]
    try:
        v.finite_fiber(es,Fraction(2))
    except RuntimeError as e:
        outcomes.append({'test':'an unproved finite fiber cannot be marked degenerate','status':'PASS: rejected','reason':str(e)})
    else:raise RuntimeError('Unexpected acceptance of unproved t=2 fiber')
    reject('missing new (3,3) representative',lambda d:d['cases'].pop(19))
    reject('altered new (4,2) resultant',lambda d:d['cases'][15]['systems'][0]['resultant'][0].__setitem__(1,321))
    reject('changed relative sign of new (3,3) frequency',lambda d:d['cases'][20]['frequencies'][3].__setitem__(1,1))
    reject('missing sum-seven representative',lambda d:d['cases'].pop(25))
    reject('altered sum-seven resultant',lambda d:d['cases'][25]['systems'][0]['resultant'][0].__setitem__(1,987))
    idx={c['id']:i for i,c in enumerate(original['cases'])}
    reject('missing sum-eight (4,4) representative',lambda d:d['cases'].pop(idx['44_m1_n1']))
    reject('missing sum-eight (7,1) representative',lambda d:d['cases'].pop(idx['71_m6_n0']))
    reject('altered sum-eight (5,3) resultant',lambda d:d['cases'][idx['53_m2_n2']]['systems'][5]['resultant'][0].__setitem__(1,4321))
    reject('altered sum-eight (6,2) numerator',lambda d:d['cases'][idx['62_m5_n1']]['area_numerators'][2][0].__setitem__(1,77))
    reject('changed relative sign of sum-eight (4,4) frequency',lambda d:d['cases'][idx['44_m3_nminus3']]['frequencies'][3].__setitem__(1,3))
    reject('sum-eight system marked unresolved',lambda d:d['cases'][idx['71_m1_n0']]['systems'][0].__setitem__('status','UNRESOLVED_zero_resultant'))
    reject('certificate carries unresolved list',lambda d:d.__setitem__('unresolved',['x']))
    def drop_witness(d):
        f=next(f for f in d['factor_catalog'] if f['type']=='no_rational_root' and f['id']>'P1189')
        f['type']='UNRESOLVED_no_small_prime_witness'
    reject('sum-eight factor without witness',drop_witness)
    def partial_missing_case(d):
        d['cases'].pop(idx['53_m4_nminus2'])
        used={r['factor_id'] for c in d['cases'] for s in c['systems'] for r in s['factors']}
        d['factor_catalog']=[f for f in d['factor_catalog'] if f['id'] in used]  # as --merge would produce
    data=deepcopy(original);partial_missing_case(data)
    rep=v.verify(data,allow_partial=True)
    v.require(rep['status']=='PARTIAL' and rep['missing_cases']==['53_m4_nminus2'] and [5,3] not in rep['fully_certified_signatures'] and [4,4] in rep['fully_certified_signatures'],'partial mode must downgrade the claim')
    outcomes.append({'test':'partial certificate is reported PARTIAL, (5,3) not certified','status':'PASS'})
    # Independent Leibniz regression for integer Bareiss determinants.
    rng=random.Random(7393)
    checked=0
    for n in range(1,7):
        for _ in range(30):
            matrix=[[rng.randrange(-3,4) for _ in range(n)] for _ in range(n)]
            exact=0
            for p in permutations(range(n)):
                x=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
                for i,j in enumerate(p):x*=matrix[i][j]
                exact+=x
            v.require(v.integer_det(matrix)==exact,'Bareiss/Leibniz discrepancy')
            checked+=1
    report={'status':'PASS','rejected_mutations_or_invalid_claims':outcomes,
            'determinant_regression':'Bareiss vs independent Leibniz formula',
            'determinant_test_matrices':checked,'regressions_are_not_the_proof':True}
    (ROOT/'results'/'degree8_mutation_tests.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
