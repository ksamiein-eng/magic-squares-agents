#!/usr/bin/env python3
"""Rigorous Gram-matrix enclosures and minimum-height lower bounds.
Full-generation input is the matched published Cremona basis, not an assumption
that a finite-prime saturation computation is globally complete.
"""
from pathlib import Path
from fractions import Fraction as Q
import json
from verify_published_bases import records
from height_exact import interval,require
ROOT=Path(__file__).resolve().parent

def main():
 cert=json.loads((ROOT/'height_certificate.json').read_text());maps={r['label']:r for r in cert['models']};out=[]
 for row in records():
  if row['rank']!=2:continue
  c=maps[row['label']];iv={}
  for p in c['points']:
   v=interval(row['model'],tuple(map(Q,p['point'])),c['bezout'],6);require(v==p['interval'],'height certificate mismatch');iv[p['tag']]=(Q(v['lower']),Q(v['upper']))
  a,A=iv['G1'];d,D=iv['G2'];s,S=iv['G1+G2'];b=(s-A-D)/2;B=(S-a-d)/2
  dl=a*d-max(abs(b),abs(B))**2;tr=A+D;require(a>0 and dl>0,'positive definiteness not certified')
  lam=dl/tr;require(lam>Q(1,50),'minimum-height lower bound 0.02 not reached')
  out.append({'label':row['label'],'basis':[[str(v) for v in P] for P in row['basis']],'gram_intervals':[[[str(a),str(A)],[str(b),str(B)]],[[str(b),str(B)],[str(d),str(D)]]],'determinant_lower':str(dl),'trace_upper':str(tr),'nonzero_lattice_height_lower':str(lam),'reason':'lambda_min >= det/trace; every nonzero integral coefficient vector has Euclidean norm at least one','basis_premise':'matched Cremona full basis'})
  print(row['label'],'height >=',float(lam))
 (ROOT/'rank_two_height_matrices.json').write_text(json.dumps({'status':'PASS','canonical_height_normalization':'lim 4^-n h(x(2^nP))','records':out,'not_claimed':'large rank-two Mordell-Weil sieve height bounds'},indent=2)+'\n')
if __name__=='__main__':main()
