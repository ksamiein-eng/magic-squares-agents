#!/usr/bin/env python3
"""Adversarial regression tests for the new rank-zero and transport checkers."""
from pathlib import Path
import copy,json
from verify_octic import certificate,verify,ProofError
from crosscheck_transport_stdlib import verify as verify_maps,Invalid
HERE=Path(__file__).resolve().parent

def main():
 out=[]
 def reject(name,data,fn,change,exc):
  d=copy.deepcopy(data);change(d)
  try:fn(d)
  except exc:out.append(name);return
  raise AssertionError('Accepted damaged evidence: '+name)
 c=certificate();verify(c)
 reject('different octic',c,verify,lambda d:d['H_coefficients_low_to_high'].__setitem__(4,35),ProofError)
 reject('omitted descent square class',c,verify,lambda d:d['images'][1]['excluded'].pop('3'),ProofError)
 reject('false small-modulus obstruction',c,verify,lambda d:d['images'][1]['excluded'].__setitem__('3',[2,1]),ProofError)
 reject('wrong real sign',c,verify,lambda d:d['images'][0]['excluded'].__setitem__('2','negative'),ProofError)
 reject('false finite-field point count',c,verify,lambda d:d['good_prime_counts'].__setitem__('5',8),ProofError)
 reject('missing good prime',c,verify,lambda d:d['good_prime_counts'].pop('7'),ProofError)
 reject('extra elliptic rational point',c,verify,lambda d:d['elliptic_rational_points'].append(['1','1']),ProofError)
 reject('false quartic point',c,verify,lambda d:d['quartic_affine_points'].__setitem__(0,['1','8']),ProofError)
 reject('wrong infinity count',c,verify,lambda d:d.__setitem__('octic_infinity_points',1),ProofError)
 r=json.loads((HERE/'progress_verification.json').read_text());verify_maps(r)
 reject('wrong integer frequency map',r,verify_maps,lambda d:d['torus_morphisms'][0]['matrix'][0].__setitem__(0,2),Invalid)
 reject('wrong sine sign',r,verify_maps,lambda d:d['torus_morphisms'][0]['signed_frequency_permutation'][0].__setitem__(1,-1),Invalid)
 reject('missing signed assignment',r,verify_maps,lambda d:d['torus_morphisms'][0]['signed_system_transport'].pop(),Invalid)
 reject('wrong target system',r,verify_maps,lambda d:d['torus_morphisms'][0]['signed_system_transport'][0].__setitem__('target_system',15),Invalid)
 reject('degree-two map called degree one',r,verify_maps,lambda d:d['torus_morphisms'][1].__setitem__('degree',1),Invalid)
 reject('false inverse',r,verify_maps,lambda d:d['torus_morphisms'][0]['inverse_matrix'][0].__setitem__(0,17),Invalid)
 reject('claiming a new whole-orbit closure',r,verify_maps,lambda d:d.__setitem__('new_closed_whole_orbits',1),Invalid)
 (HERE/'negative_tests.json').write_text(json.dumps({'status':'PASS','rejected_mutations':out,'count':len(out)},indent=2)+'\n')
 print('PASS:',len(out),'deliberately corrupted claims rejected.')
if __name__=='__main__':main()
