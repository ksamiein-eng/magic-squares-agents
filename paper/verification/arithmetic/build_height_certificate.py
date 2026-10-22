#!/usr/bin/env python3
from pathlib import Path
import json
import sympy as s
from math import lcm
from fractions import Fraction as Q
from verify_published_bases import records
from height_exact import forms,interval,conv
from elliptic_exact import add
ROOT=Path(__file__).resolve().parent

def witness(model):
 F,G=forms(model);cols=[]
 for H in (F,G):
  for j in range(4):cols.append([0]*j+H+[0]*(3-j))
 M=s.Matrix.hstack(*(s.Matrix(c) for c in cols));sols=[]
 for k in (7,0):
  v=s.zeros(8,1);v[k]=1;sols.append(list(M.inv()*v))
 D=lcm(*(int(q.q) for v in sols for q in v));r={'D':D}
 for name,v in zip(('X7','Z7'),sols):
  vv=[int(D*q) for q in v];r[name]={'U':vv[:4],'V':vv[4:]}
 return r
rows=[]
for r in records():
 w=witness(r['model']);ps=[]
 pts=[('G'+str(i+1),p) for i,p in enumerate(r['basis'])]
 if r['rank']==2:pts.append(('G1+G2',add(r['model'],*r['basis'])))
 for tag,p in pts:
  iv=interval(r['model'],p,w,steps=6)
  ps.append({'tag':tag,'point':[str(z) for z in p],'interval':iv})
  print(r['label'],tag,float(Q(iv['lower'])),float(Q(iv['upper'])),flush=True)
 rows.append({'label':r['label'],'model':r['model'],'bezout':w,'points':ps})
(ROOT/'height_certificate.json').write_text(json.dumps({'schema':'canonical-height/duplication-bezout/v1','models':rows},indent=2)+'\n')
