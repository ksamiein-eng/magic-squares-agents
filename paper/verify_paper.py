#!/usr/bin/env python3
"""Run the focused paper's proof checks in independent temporary copies.

This is a nine-stage suite. It does not claim novelty or peer review and does
not turn the remaining genus-five conjecture into a theorem.
"""
from __future__ import annotations
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
ROOT=Path(__file__).resolve().parent
JOBS=[
 ('article_identities_and_tables',None,['check_paper.py']),
 ('mathematical_review_and_appendices',None,['review_math.py']),
 ('two_prime_sum7','two_prime',['verify_degree7_stdlib.py']),
 ('two_prime_symbolic','two_prime',['crosscheck_degree7_sympy.py']),
 ('two_prime_negative_tests','two_prime',['test_degree7_verifier.py']),
 ('D1_normalization_and_descent','d1_norm',['verify_d1_stdlib.py']),
 ('D1_symbolic_transport','d1_norm',['audit_d1_transfer.py']),
 ('D1_negative_tests','d1_norm',['test_d1.py']),
 ('torus_rowspace_crosscheck','orbit_progress',['crosscheck_transport_stdlib.py']),
]
FOUR_PRIME_JOBS=[
 ('four_prime_general_type_invariants','four_prime',['general_type_check.py']),
 ('four_prime_hadamard_type_I','four_prime',['verify_hadamard_types.py','I']),
 ('four_prime_hadamard_type_II','four_prime',['verify_hadamard_types.py','II']),
 ('four_prime_hadamard_type_III','four_prime',['verify_hadamard_types.py','III']),
 ('four_prime_hadamard_type_IV','four_prime',['verify_hadamard_types.py','IV']),
 ('four_prime_height3_sweep','four_prime',['r4search.py','3']),
 ('archive_audit_curves_and_identities','archive_audit',['archive_checks.py']),
]

def task(job,output_dir):
    name,tree,command=job
    start=time.perf_counter()
    log=output_dir/'logs'/(name+'.log')
    with tempfile.TemporaryDirectory(prefix='rational-circle-paper-') as tmp:
        root=Path(tmp)
        shutil.copytree(ROOT/'verification',root/'verification',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        if tree is None:
            shutil.copytree(ROOT/'manuscript',root/'manuscript')
            shutil.copytree(ROOT/'editorial',root/'editorial')
            shutil.copy2(ROOT/'check_paper.py',root/'check_paper.py')
            shutil.copy2(ROOT/'review_math.py',root/'review_math.py')
            cwd=root
        else:
            cwd=root/'verification'/tree
        with log.open('w') as f:
            done=subprocess.run([sys.executable]+command,cwd=cwd,stdout=f,stderr=subprocess.STDOUT)
    return {'stage':name,'passed':done.returncode==0,'returncode':done.returncode,
            'seconds':round(time.perf_counter()-start,3),'log':str(log.relative_to(output_dir))}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'verification_runs/focused/latest.json')
    parser.add_argument('--workers',type=int,default=3)
    parser.add_argument('--skip-four-prime',action='store_true',help='run only the original nine stages')
    args=parser.parse_args()
    if not __debug__:raise RuntimeError('Assertions must remain enabled; do not use -O.')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    (args.output.parent/'logs').mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1,min(args.workers,3))) as pool:
        futures=[pool.submit(task,j,args.output.parent) for j in (JOBS if args.skip_four_prime else JOBS+FOUR_PRIME_JOBS)]
        results=[]
        for future in futures:
            result=future.result();results.append(result);print(result,flush=True)
    report={'status':'PASS' if all(r['passed'] for r in results) else 'FAIL',
            'scope':'Two-parameter exclusion through exponent sum seven; specified integer-torus maps; D1 normalization and exact genus-five existence equivalence.',
            'stages':results,'stage_count':len(results),
            'paper_sha256':hashlib.sha256((ROOT/'manuscript/paper.tex').read_bytes()).hexdigest(),
            'not_certified':['Historical priority','Independent human review','Completeness of the eight-point genus-five list','All three-prime orbit exclusions'],
            'isolation':'Each stage runs in its own temporary copy. Shipped proof files are not modified.',
            'software':'Python and SymPy exact routines and the shipped checker implementations; not a formal proof assistant.'}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    if report['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
