"""Complete-at-bounded-height search for admissible rational-circle points of four-parameter full-depth configurations.
For each orbit representative and each choice of 'solved' coordinate j, sweep (t_i)_{i!=j} over rationals of height<=H;
the two signed relations are linear in (cos chi_j, sin chi_j); solve (det!=0 by Cramer; det==0 by line-circle intersection)
and test the unit-circle condition exactly. Any solution with three parameters of height<=H is found."""
import itertools, json, sys, time, math, os
import numpy as np
from fractions import Fraction as Fr
H=int(sys.argv[1]) if len(sys.argv)>1 else 5
START=int(sys.argv[2]) if len(sys.argv)>2 else 0
END=int(sys.argv[3]) if len(sys.argv)>3 else 10**9
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'results'); os.makedirs(OUT,exist_ok=True)
# ---- configurations and orbits ----
vecs=[v for v in itertools.product((-1,0,1),repeat=4) if any(v) and v[next(i for i,x in enumerate(v) if x)]>0]
def canon(v):
    i=next(k for k,x in enumerate(v) if x); return tuple(v) if v[i]>0 else tuple(-x for x in v)
confs=[frozenset(S) for S in itertools.combinations(vecs,4) if all(sum(1 for v in S if v[c]!=0)>=3 for c in range(4))]
G=[(sg,pm) for sg in itertools.product((1,-1),repeat=4) for pm in itertools.permutations(range(4))]
act=lambda g,v: canon([g[0][i]*v[g[1][i]] for i in range(4)])
orbits=[]; seen=set()
for S in confs:
    if S in seen: continue
    orb={frozenset(act(g,v) for v in S) for g in G}; seen|=orb; orbits.append((sorted(S),len(orb)))
# ---- grid of rationals of height<=H ----
# projective parameters [p:q] of height max(|p|,q)<=H, including 0=[0:1] and infinity=[1:0] (chi = 0 and chi = pi)
vals=sorted({Fr(p,q) for p in range(-H,H+1) for q in range(1,H+1)}, key=lambda f:(abs(f.numerator)+f.denominator,f))   # includes 0
PQ=[(f.numerator,f.denominator) for f in vals]+[(1,0)]          # append infinity
vals=vals+['inf']
P=np.array([pq[0] for pq in PQ],dtype=np.int64); Q=np.array([pq[1] for pq in PQ],dtype=np.int64)
Cc=Q*Q-P*P; Ss=2*P*Q; Dd=Q*Q+P*P          # cos=Cc/Dd, sin=Ss/Dd
n=len(vals)
systems=[(i,j,k,l,e2,e3) for i,j in itertools.combinations(range(4),2) for k in [x for x in range(4) if x not in (i,j)] for l in [x for x in range(4) if x not in (i,j) and x!=k] for e2 in (1,-1) for e3 in (1,-1)]
def admissible(mags):
    mags=sorted(mags)
    if 0 in mags or len(set(mags))<4: return None
    for a_i,b_i in itertools.combinations(range(4),2):
        A,B=max(mags[a_i],mags[b_i]),min(mags[a_i],mags[b_i]); rest=sorted(mags[k] for k in range(4) if k not in (a_i,b_i))
        if rest==sorted([A+B,A-B]) and A!=2*B: return (A,B)
    return None
def isq(N): 
    if N<0: return None
    r=math.isqrt(N); return r if r*r==N else None
import json as _j
_prev=f'{OUT}/r4_H{H}_progress.json'
_pd=_j.load(open(_prev)) if (os.path.exists(_prev) and START>0) else None
found=_pd['found'] if _pd else []
stats={'orbits':len(orbits),'raw_confs':len(confs),'H':H,'grid_values':n,'triples':n**3,'systems_checked':0,'candidates_exact_checked':0}
t0=time.time()
for oi,(rows,osize) in enumerate(orbits):
    if oi<START or oi>=END: continue
    for solved in range(4):
        others=[c for c in range(4) if c!=solved]
        # broadcast grids for the three free coordinates
        shp=[1,1,1]; Cs=[];Sn=[];Dn=[]
        for ax,c in enumerate(others):
            s=[1,1,1]; s[ax]=n
            Cs.append(Cc.reshape(s)); Sn.append(Ss.reshape(s)); Dn.append(Dd.reshape(s))
        Dfull=Dn[0]*Dn[1]*Dn[2]
        # per row: (A,B,Cst) with  Dfull*sin(row) = A*c_s + B*s_s + Cst
        R=[]
        for m in rows:
            C=np.ones((1,1,1),dtype=np.int64); S=np.zeros((1,1,1),dtype=np.int64); D=np.ones((1,1,1),dtype=np.int64)
            for ax,c in enumerate(others):
                if m[c]==0: continue
                sj=Sn[ax]*m[c]
                C,S=C*Cs[ax]-S*sj, S*Cs[ax]+C*sj; D=D*Dn[ax]
            scale=Dfull//D
            if m[solved]==0: R.append((np.zeros_like(Dfull),np.zeros_like(Dfull),S*scale))
            else: R.append((S*scale,(C*m[solved])*scale,np.zeros_like(Dfull)))
        for (i,j,k,l,e2,e3) in systems:
            A1=R[i][0]-e2*R[k][0]-e3*R[l][0]; B1=R[i][1]-e2*R[k][1]-e3*R[l][1]; C1=R[i][2]-e2*R[k][2]-e3*R[l][2]
            A2=R[j][0]-e2*R[k][0]+e3*R[l][0]; B2=R[j][1]-e2*R[k][1]+e3*R[l][1]; C2=R[j][2]-e2*R[k][2]+e3*R[l][2]
            det=A1*B2-A2*B1; Nc=C2*B1-C1*B2; Ns=A2*C1-A1*C2
            stats['systems_checked']+=1
            # Cramer branch: Nc^2+Ns^2==det^2 (float filter, exact confirm)
            nz=det!=0
            f=(Nc.astype(float)**2+Ns.astype(float)**2-det.astype(float)**2)
            cand=np.argwhere(nz & (np.abs(f)<=1e-6*np.maximum(1.0,det.astype(float)**2)))
            # identically-zero branch (exact, vectorized): both relations vanish for EVERY value of the solved angle.
            # The four sines are then A_r c + B_r s + C_r along a one-parameter family; the family contains admissible
            # points (indeed all but finitely many) iff no row triple is zero and no two row triples are ±equal.
            allzero=(A1==0)&(B1==0)&(C1==0)&(A2==0)&(B2==0)&(C2==0)
            if allzero.any():
                stats['identically_zero_systems']=stats.get('identically_zero_systems',0)+int(allzero.sum())
                rowzero=np.zeros_like(allzero)
                for r in range(4): rowzero|=(R[r][0]==0)&(R[r][1]==0)&(R[r][2]==0)
                pm=np.zeros_like(allzero)
                for r in range(4):
                    for r2 in range(r+1,4):
                        pm|=((R[r][0]==R[r2][0])&(R[r][1]==R[r2][1])&(R[r][2]==R[r2][2]))|((R[r][0]==-R[r2][0])&(R[r][1]==-R[r2][1])&(R[r][2]==-R[r2][2]))
                fam=allzero&~rowzero&~pm
                stats['identically_zero_families_degenerate']=stats.get('identically_zero_families_degenerate',0)+int((allzero&(rowzero|pm)).sum())
                for idx in map(tuple,np.argwhere(fam)):
                    ts={c:str(vals[idx[ax]]) for ax,c in enumerate(others)}; ts[solved]='FREE (one-parameter family)'
                    found.append({'orbit':oi,'rows':rows,'solved_coord':solved,'system':(i,j,k,l,e2,e3),'t':ts,'family':True})
            # singular branch: det==0, not identically zero -> consistent line ∩ circle
            sing=np.argwhere((~nz)&(~allzero))
            for idx in list(map(tuple,cand))+list(map(tuple,sing)):
                a1,b1,c1,a2,b2,c2=int(A1[idx]),int(B1[idx]),int(C1[idx]),int(A2[idx]),int(B2[idx]),int(C2[idx])
                pts=[]
                dt=a1*b2-a2*b1
                if dt!=0:
                    nc=c2*b1-c1*b2; ns=a2*c1-a1*c2
                    if nc*nc+ns*ns==dt*dt: pts.append((Fr(nc,dt),Fr(ns,dt)))
                else:
                    lines=[(a1,b1,c1),(a2,b2,c2)]
                    if (a1,b1)==(0,0) and c1!=0: continue
                    if (a2,b2)==(0,0) and c2!=0: continue
                    if (a1,b1)!=(0,0) and (a2,b2)!=(0,0) and (a1*c2!=a2*c1 or b1*c2!=b2*c1): continue
                    if (a1,b1,c1)==(0,0,0) and (a2,b2,c2)==(0,0,0): continue   # handled exactly above
                    else:
                        a,b,c=[L for L in lines if (L[0],L[1])!=(0,0)][0]
                        disc=a*a+b*b-c*c; rt=isq(disc)
                        if rt is None: continue
                        for sgn in (1,-1):
                            pts.append((Fr(-a*c+sgn*b*rt,a*a+b*b),Fr(-b*c-sgn*a*rt,a*a+b*b)))
                stats['candidates_exact_checked']+=1
                for (c4,s4) in pts:
                    if c4*c4+s4*s4!=1: continue
                    sines=[(Fr(int(R[r][0][idx]))*c4+Fr(int(R[r][1][idx]))*s4+Fr(int(R[r][2][idx])))/Fr(int(Dfull[idx])) for r in range(4)]
                    ab=admissible([abs(x) for x in sines])
                    if ab:
                        ts={c:str(vals[idx[ax]]) for ax,c in enumerate(others)}  # 'inf' = chi=pi; ts[solved]=str(s4/(1+c4)) if c4!=-1 else 'inf'
                        found.append({'orbit':oi,'rows':rows,'solved_coord':solved,'system':(i,j,k,l,e2,e3),'t':ts,'sines':[str(x) for x in sines],'ab':[str(x) for x in ab]})
    if (oi+1)%10==0 or oi==len(orbits)-1:
        json.dump({'stats':stats,'orbits_done':oi+1,'elapsed_s':round(time.time()-t0),'found':found},open(f'{OUT}/r4_H{H}_progress.json','w'),indent=1)
        print(f"orbit {oi+1}/{len(orbits)} done, {time.time()-t0:.0f}s, found so far: {len(found)}",flush=True)
if END>=len(orbits):
    json.dump({'stats':stats,'orbits_done':len(orbits),'elapsed_s':round(time.time()-t0),'found':found,'complete':True},open(f'{OUT}/r4_H{H}_final.json','w'),indent=1)
    print('DONE. found:',len(found))
else: print('chunk done',START,END,'found so far:',len(found))
