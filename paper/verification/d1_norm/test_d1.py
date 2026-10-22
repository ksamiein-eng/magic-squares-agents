#!/usr/bin/env python3
"""Mutation tests for the new D1 proof checker."""
from pathlib import Path
from copy import deepcopy
import json
from verify_d1_stdlib import verify,ProofError
H=Path(__file__).resolve().parent
base=json.loads((H/'d1_certificate.json').read_text())
def put(path,value):
 def mut(d):
  x=d
  for k in path[:-1]:x=x[k]
  x[path[-1]]=value
 return mut
cases=[
 ('wrong_frequency',put(['frequency_matrix',0,0],2)),
 ('wrong_angle_map',put(['angle_matrix',0,0],2)),
 ('missing_system',lambda d:d['systems'].pop()),
 ('duplicate_tag',put(['systems',1,'tag'],base['systems'][0]['tag'])),
 ('false_kernel',put(['systems',10,'kernel',0,0],1)),
 ('false_common_factor',put(['systems',8,'divisor',1],3)),
 ('false_norm',put(['systems',10,'norm_factor',0],5)),
 ('false_second_square',put(['systems',8,'second_norm',0],8)),
 ('false_elliptic_point',put(['models',0,'affine_rational_points',1,1],3)),
 ('false_isogeny',put(['models',1,'images',1,'A'],7)),
 ('missing_square_class',lambda d:d['models'][0]['images'][0]['not_excluded'].pop()),
 ('false_local_obstruction',put(['models',1,'images',1,'excluded','7'],[3,1])),
 ('false_good_prime_count',put(['models',0,'good_prime_counts','3'],8)),
 ('false_boundary',put(['boundaries',1],'r=infinity ignored')),
 ('false_residual_polynomial',put(['residual_polynomial',6],7059)),
 ('false_residual_point',put(['residual_known_finite_points',2,1],71)),
 ('false_completeness',put(['residual_points_complete'],True)),
 ('promoted_residual_system',put(['systems',8,'status'],'closed'))]
verify(base);results=[]
for name,mut in cases:
 bad=deepcopy(base);mut(bad)
 try:verify(bad)
 except (ProofError,ValueError,KeyError,IndexError) as e:results.append({'case':name,'rejected':True,'reason':str(e)})
 else:raise RuntimeError('Corruption accepted: '+name)
(H/'d1_negative_tests.json').write_text(json.dumps({'status':'PASS','tests':results},indent=2)+'\n')
print('PASS:',len(results),'deliberately invalid certificates rejected.')
