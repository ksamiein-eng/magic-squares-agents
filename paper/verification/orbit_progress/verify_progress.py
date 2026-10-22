#!/usr/bin/env python3
"""Verify new reciprocal-octic closures and integer-torus transport.

This extends, rather than silently substitutes for, the previously verified
three-prime input/component/fiber theorems. The new octic arithmetic has its own
standard-library checker. The D3 -> B1 transport cites the earlier complete
rank-zero genus-five family, whose checker is shipped under geometry/.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
import json,sys
import sympy as s
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'three_prime';GEO=HERE.parent/'geometry'
sys.path.insert(0,str(BASE))
from audit_inputs import expr,T,U,V,TAU,numerator,check_one
from audit_quotients import reconstruct
from audit_lifts import normal
from verify_octic import verify,need
ROOT=BASE/'input/repro/certs'
VARS={'x':T,'z':U,'w':V};COORD={'x':0,'z':1,'w':2}

MORPHISMS=[
 ('B2','C',[[1,0,1],[-1,0,0],[1,1,0]]),
 ('D1','B2',[[1,-1,-2],[0,2,2],[0,0,1]]),
 ('D1','C',[[0,-2,1],[0,2,0],[1,1,0]]),
 ('D1','E2',[[0,2,0],[0,-2,1],[1,-1,0]]),
 ('D3','B1',[[1,-1,0],[-2,0,1],[-2,0,0]])]

def load_records():
    out={}
    for p in sorted(ROOT.glob('*.json')):
        d=json.loads(p.read_text())
        if 'systems' in d:out[d['config']]=d
    need(len(out)==17,'expected 17 historical labels')
    return out

def rows(tag):
    i,j,k,l,e,f=tag
    C=s.zeros(2,4);C[0,i]=C[1,j]=1;C[0,k]=C[1,k]=-e;C[0,l]=-f;C[1,l]=f
    return C

def signed_permutation(source,target,M):
    A=s.Matrix(source);B=s.Matrix(target);C=A*M
    P=s.zeros(4,4);mapping=[]
    for i in range(4):
        matches=[(j,sg) for j in range(4) for sg in [1,-1] if C[i,:]==sg*B[j,:]]
        need(len(matches)==1,'integer map does not match one unique signed frequency')
        j,sg=matches[0];P[i,j]=sg;mapping.append([j,sg])
    need(abs(P.det())==1,'frequency matching is not a permutation')
    need(A*M==P*B,'frequency matrix identity failed')
    return P,mapping

def previous_closed(records):
    old=json.loads((BASE/'lift_audit.json').read_text())
    closed={(r['orbit'],r['system'],r['factor']) for r in old['factor_statuses'] if not r['status'].startswith('unresolved')}
    for row in json.loads((GEO/'reciprocal_octic_closures.json').read_text())['lifts']:
        closed.add((row['orbit'],row['system'],row['factor']))
    d3=json.loads((GEO/'d3_rank_zero_family.json').read_text())
    source_ids=[r['system'] for r in d3['closed_factors']]
    need(sorted(source_ids)==list(range(8)),'unexpected D3 source theorem scope')
    for sid in source_ids:
        for fi,f in enumerate(records['D3']['systems'][sid]['factors']):
            if f['type']=='nonlinear':closed.add(('D3',sid,fi))
    return closed,source_ids

def verify_octic_records(records):
    arithmetic=verify(json.loads((HERE/'octic_certificate.json').read_text()))
    H=TAU**8-13*TAU**6+36*TAU**4-13*TAU**2+1
    out=[]
    for name,rec in records.items():
        Es=[numerator(m) for m in rec['elements']]
        for sid,sy in enumerate(rec['systems']):
            for fi,f in enumerate(sy['factors']):
                for qi,q in enumerate(f.get('quotients',[])):
                    if q.get('curve_kind')!='genus>=2' or not q.get('used'):continue
                    D=expr(q['D(tau)'])
                    if normal(D).as_expr()!=H:continue
                    c=s.cancel(D/H)
                    need(c.is_Rational and c>0 and s.sqrt(c).is_Rational,'removed multiplier is not a nonzero rational square')
                    a,b=[VARS[x] for x in sy['projection']['plane']]
                    p0,q0,r0,D0=reconstruct(expr(f['poly']),a,b,f['basis_M'],f['A'],q['B'])
                    need(s.expand(D-D0)==0,'discriminant reconstruction failed')
                    need(all(s.expand(v-expr(q['line'][k]))==0 for k,v in zip(['p','q','r'],[p0,q0,r0])),'line coefficients mismatch')
                    # Also recheck that this plane factor belongs to the actual system.
                    check_one((name,Es,sy,sid))
                    lam=[0,0,0]
                    for name2,val in zip(sy['projection']['plane'],f['basis_M'][1]):lam[COORD[name2]]=q['B']*val
                    need(any(lam),'quotient angle is constant')
                    witnesses=[]
                    for i,j in combinations(range(4),2):
                        diff=[rec['elements'][i][k]-rec['elements'][j][k] for k in range(3)]
                        for sg in [1,-1]:
                            if diff==[sg*x for x in lam]:witnesses.append({'i':i,'j':j,'multiple':sg})
                    need(witnesses,'allowed quotient parameters do not force repeated sine magnitudes')
                    out.append({'orbit':name,'system':sid,'factor':fi,'quotient':qi,
                      'D_multiplier':str(c),'sqrt_multiplier':str(s.sqrt(c)),
                      'quotient_angle_vector':lam,'quotient_parameters':['0','infinity'],
                      'degeneracy_witness':witnesses[0],
                      'proof':'tau=0 or infinity implies exp(i*lambda.theta)=+1 or -1. The two frequencies differ by +/-lambda; hence their sine magnitudes coincide. This handles the full fibers, without a bounded lift search.'})
    need(len(out)==16 and Counter(r['orbit'] for r in out)=={'B1':8,'D3':8},'unexpected new octic record coverage')
    need({r['system'] for r in out if r['orbit']=='B1'}==set(range(16,24)),'wrong B1 octic systems')
    need({r['system'] for r in out if r['orbit']=='D3'}==set(range(40,48)),'wrong D3 octic systems')
    return arithmetic,out

def verify_transport(records):
    out=[]
    for source,target,m in MORPHISMS:
        M=s.Matrix(m);need(all(v.is_Integer for v in M) and M.det()!=0,'not a finite integer torus map')
        P,mp=signed_permutation(records[source]['elements'],records[target]['elements'],M)
        rowkeys={tuple(rows(sy['tag']).rref()[0]):i for i,sy in enumerate(records[target]['systems'])}
        smap=[]
        for sid,sy in enumerate(records[source]['systems']):
            C=rows(sy['tag'])*P;key=tuple(C.rref()[0]);need(key in rowkeys,'missing target signed system')
            tid=rowkeys[key];D=rows(records[target]['systems'][tid]['tag'])
            # Independent containment check: two rank-two row spaces have rank-two union.
            need(C.rank()==D.rank()==C.col_join(D).rank()==2,'row-space transport does not hold')
            smap.append({'source_system':sid,'target_system':tid})
        row={'source':source,'target':target,'matrix':m,'determinant':int(M.det()),'degree':abs(int(M.det())),
             'signed_frequency_permutation':mp,'signed_system_transport':smap,
             'direction':'Every rational-circle solution for target maps to source; nonexistence transfers from source to target.'}
        if abs(M.det())==1:
            inv=M.inv();need(all(v.is_Integer for v in inv),'claimed isomorphism has nonintegral inverse')
            row['inverse_matrix']=[[int(v) for v in inv[i,:]] for i in range(3)]
        out.append(row)
    return out

def universal_addition_obstruction(records):
    A=s.Matrix(records['F-1']['elements'])
    M=s.Matrix([[2,1,-1],[-1,0,1],[-1,-1,1]])
    # Source ordering is free phase gamma, alpha+beta, alpha, beta.
    B=s.Matrix([[0,0,1],[1,1,0],[1,0,0],[0,1,0]])
    need(A*M==B and abs(M.det())==1,'universal sine-addition map fails')
    return {'source':'F-1','target_frequencies':[list(B[i,:]) for i in range(4)],
       'matrix':[list(M[i,:]) for i in range(3)],'determinant':int(M.det()),
       'conclusion':'For arbitrary rational unit-circle points, the magnitudes of sin(alpha), sin(beta), sin(alpha+beta), and sin(gamma) cannot form the nondegenerate four-offset magic pattern.',
       'dependency':'The independently verified complete F-1 closure from the baseline.'}

def main():
    records=load_records();old,ids=previous_closed(records)
    arithmetic,new_octic=verify_octic_records(records)
    maps=verify_transport(records);univ=universal_addition_obstruction(records)
    added={(r['orbit'],r['system'],r['factor']) for r in new_octic}
    need(not added&old,'octic closures were already in the last release')
    chosen=next(r for r in maps if r['source']=='D3' and r['target']=='B1')
    proofmap={r['source_system']:r['target_system'] for r in chosen['signed_system_transport']}
    transfers=[]
    for sid in ids:
        need(all(('D3',sid,j) in old for j in range(len(records['D3']['systems'][sid]['factors']))),'source system is not fully closed by the prior theorem')
        tid=proofmap[sid];fresh=[]
        for j,f in enumerate(records['B1']['systems'][tid]['factors']):
            key=('B1',tid,j)
            if key not in old|added:added.add(key);fresh.append(j)
        transfers.append({'source':'D3','source_system':sid,'target':'B1','target_system':tid,'new_factor_indices':fresh})
    need(len(added)==24 and sum(len(t['new_factor_indices']) for t in transfers)==8,'new closure count differs')
    now=old|added;ledger=[]
    for label in ['A','B1','B2','C','D1','D2','D3','D4','E1','E2','E3','F-1','F-2','F+1','F+2']:
        pairs=[(label,i,j) for i,sy in enumerate(records[label]['systems']) for j,f in enumerate(sy['factors'])]
        prev=sum(k not in old for k in pairs);cur=sum(k not in now for k in pairs)
        systems_before=sum(all((label,i,j) in old for j in range(len(sy['factors']))) for i,sy in enumerate(records[label]['systems']))
        systems_after=sum(all((label,i,j) in now for j in range(len(sy['factors']))) for i,sy in enumerate(records[label]['systems']))
        ledger.append({'orbit':label,'previous_unresolved_factors':prev,'unresolved_factors':cur,
          'new_factor_closures':prev-cur,'previous_closed_systems':systems_before,'closed_systems':systems_after,
          'whole_orbit_closed':cur==0})
    need([r['orbit'] for r in ledger if r['whole_orbit_closed']]==['A','E1','E3','F-1','F-2'],'unexpected whole-orbit assertion')
    report={'status':'PASS','scope':'24 new factor-entry closures; no additional whole orbit asserted closed.',
      'arithmetic':arithmetic,'new_octic_factor_closures':new_octic,
      'torus_morphisms':maps,'new_transferred_closures':transfers,'new_factor_closures':24,
      'new_closed_whole_orbits':0,'orbit_ledger':ledger,
      'six_sufficient_primary_targets':['D1','D2','D3','D4','F+1','F+2'],
      'dependent_targets':{'B1':'D3','B2':'D1','C':'D1','E2':'D1'},
      'rationally_isomorphic_orbits':['B2','C'],
      'universal_addition_obstruction':univ,
      'baseline_dependencies':['three-prime input/projection/component/fiber checks','D3 rank-zero genus-five family','F-1 complete closure'],
      'not_claimed':['complete C_B or C_C rational-point lists','closure of the ten outstanding whole orbits','quadratic Chabauty execution','historical priority']}
    (HERE/'progress_verification.json').write_text(json.dumps(report,indent=2,default=int)+'\n')
    print('PASS: 16 new octic factor closures; 8 further factor closures by D3 -> B1.')
    print('PASS: B2 and C are rational-torus isomorphic; six targets suffice for the ten open orbit exclusions.')
    print('Whole-orbit closed count remains five.')

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Do not disable baseline assertions with -O.')
    main()
