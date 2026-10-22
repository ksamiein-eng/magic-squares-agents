"""Targeted corruption tests for the audit's exact acceptance checks."""
import copy
import json
from pathlib import Path
import sys
from audit_inputs import check_one, numerator
from audit_quotients import reconstruct
from audit_inputs import expr, T, U
from audit_chabauty import residual
from verify_rank_zero import verify

HERE = Path(__file__).resolve().parent
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE / 'input'

def must_reject(name, fn):
    try:
        fn()
    except (AssertionError, ValueError, IndexError, KeyError, ZeroDivisionError):
        print(name, 'REJECTED')
        return
    raise AssertionError('Corruption was not rejected: ' + name)

if not __debug__:
    raise RuntimeError('Assertions must be enabled.')
r = json.loads((ROOT/'repro/certs/F-2.json').read_text())
es = [numerator(m) for m in r['elements']]
base = r['systems'][0]
check_one(('F-2', es, base, 0))
for label, mutate in [
    ('wrong input equation', lambda x: x.update(G1='('+x['G1']+')+1')),
    ('wrong role sign', lambda x: x['tag'].__setitem__(4, -x['tag'][4])),
    ('missing projection factor', lambda x: x['factors'].pop()),
    ('invalid common divisor', lambda x: x.update(common_factor='t+17')),
    ('wrong factor polynomial', lambda x: x['factors'][0].update(poly='t+17')),
]:
    x=copy.deepcopy(base); mutate(x)
    must_reject(label, lambda x=x:check_one(('F-2',es,x,0)))
cert = json.loads((HERE/'rank_zero_certificate.json').read_text())
verify(cert)
for label, mutate in [
    ('missing rank model',lambda x:x['curves'].pop()),
    ('wrong rational root shift',lambda x:x['curves'][-1].update(root_shift=67)),
    ('false finite-field cardinality',lambda x:x['curves'][-1]['good_prime_cardinalities'].update({'7':13})),
    ('missing descent square class',lambda x:x['curves'][-1]['image_bounds'][0]['not_excluded'].pop()),
    ('invalid modular obstruction',lambda x:x['curves'][-1]['image_bounds'][0]['excluded'].update({'-5':[2,1]})),
    ('false torsion upper bound',lambda x:x['curves'][-1].update(rational_torsion_order_divides=6)),
]:
    x=copy.deepcopy(cert);mutate(x)
    must_reject(label,lambda x=x:verify(x))
assert residual([0,1,0,11,35],[-2,3])==0
assert residual([0,1,0,11,35],[0,3])==-26
print('All 11 corrupted certificates rejected; original/corrected point distinction verified.')
(HERE/'negative_tests.json').write_text(json.dumps({'corrupted_certificates_rejected':11,'point_model_regression_passed':True},indent=2))
