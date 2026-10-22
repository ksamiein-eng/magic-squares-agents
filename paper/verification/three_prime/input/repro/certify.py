"""certify.py <CONFIG>... : per-system machine-readable certificate (Appendix A format). Reconstructed; uses the
original (2m) parametrization, which is birationally equivalent to the corrected one by the pullback identity (App. B)."""
import sys, json, time
src=open('/tmp/tp/pipe3.py').read(); exec(src[:src.index('if __name__')])
S=str
def certify(name,H=5000):
    Es=[E(m) for m in CONF[name]]
    rec={'config':name,'elements':CONF[name],'parametrization':'original 2m (see Appendix B pullback identity)','E_polys':[S(e) for e in Es],'systems':[],'summary':{},'fibers':None}
    cnt={'degenerate_component':0,'univariate_torsion':0,'genus1_complete':0,'genus1_incomplete':0,'genus>=2':0,'genus0':0,'nonlinear':0,'isolated_line_points_checked':0}
    for tag,G1,G2 in systems(Es):
        s={'tag':list(tag),'G1':S(G1),'G2':S(G2),'common_factor':None,'projection':None,'factors':[],'nondegenerate_solutions':[]}
        g=sp.gcd(G1,G2)
        if sp.Poly(g,t,u,v).total_degree()>0: s['common_factor']=S(sp.factor(g)); G1=sp.cancel(G1/g); G2=sp.cancel(G2/g)
        cands=[]
        for elim,(a,b) in ((v,(t,u)),(u,(t,v)),(t,(u,v))):
            R=sp.resultant(G1,G2,elim)
            if R==0: continue
            fl=sp.factor_list(R)[1]
            nbad=sum(1 for f,_ in fl if sp.Poly(f,a,b).degree(a)>1 and sp.Poly(f,a,b).degree(b)>1 and find_linear_basis(support(f,a,b)) is None)
            cands.append(((nbad,max(sp.Poly(f,a,b).degree(a)+sp.Poly(f,a,b).degree(b) for f,_ in fl)),elim,a,b,fl))
        if not cands: s['projection']='all resultants zero'; rec['systems'].append(s); continue
        cands.sort(key=lambda c:c[0]); _,elim,a,b,fl=cands[0]; s['projection']={'eliminated':ANG[elim],'plane':[ANG[a],ANG[b]]}
        for F,mult in fl:
            P=sp.Poly(F,a,b); fr={'poly':S(F),'bidegree':[P.degree(a),P.degree(b)]}
            if P.degree(b)==0 or P.degree(a)==0:
                var=a if P.degree(b)==0 else b; roots=rational_roots(F,var) or []
                fr['type']='univariate'; fr['rational_roots']=[S(r) for r in roots]; cnt['univariate_torsion']+=1; s['factors'].append(fr); continue
            if P.degree(a)==1 or P.degree(b)==1:
                cd=component_degenerate(F,G1,G2,Es,a,b,elim)
                if cd is True: fr['type']='degenerate_component'; cnt['degenerate_component']+=1
                elif cd=='no common v-branch (finite)': fr['type']='isolated_line_points'; cnt['isolated_line_points_checked']+=1
                else: fr['type']='rational_component_UNRESOLVED'; fr['note']=S(cd)
                s['factors'].append(fr); continue
            Ssup=support(F,a,b); fb=find_linear_basis(Ssup)
            if fb is None: fr['type']='nonlinear'; cnt['nonlinear']+=1; s['factors'].append(fr); continue
            M,A,coords=fb; fr['type']='linear_in_circle_point'; fr['basis_M']=[[int(M[0,0]),int(M[0,1])],[int(M[1,0]),int(M[1,1])]]; fr['A']=A; fr['quotients']=[]; chosen=None; sols=[]
            for B in valid_Bs(coords):
                dd=discriminant(Ssup,M,A,coords,B)
                if dd is None: continue
                D,p,q,r,_=dd; kind,taus,data=quartic_points(D,H)
                q_={'B':B,'line':{'p':S(p),'q':S(q),'r':S(r)},'D(tau)':S(D.as_expr()),'curve_kind':kind}
                if kind=='genus1':
                    Em=pari.ellminimalmodel(pari.ellinit(pari.ellfromeqn(pari('y^2')-to_pari(sp.sympify(data['D'])))))
                    q_['curve']={'D_squarefree':data['D'],'minimal_model':[int(x) for x in Em[0:5]],'conductor':int(pari.ellglobalred(Em)[0]),'rank_bounds':list(data['rank']),'torsion':data['torsion'],'complete':data['complete'],'tau_values':[S(x) for x in taus]}
                elif kind=='genus>=2': q_['curve']={'D_squarefree':data['D'],'genus':data['genus'],'points_found':[S(x) for x in taus]}
                elif kind in ('genus0','genus0-const-square'): q_['curve']={'note':'genus 0 quotient (too coarse or linear-relation component; see Lemma 5.4)'}
                fr['quotients'].append(q_)
                finite=(kind=='genus1' and data['complete']) or kind=='genus>=2' or kind in ('none','zero')
                if finite and chosen is None:
                    chosen=B; q_['used']=True
                    if kind in ('genus1','genus>=2'): sols=lift(F,G1,G2,Es,taus,M,a,b,elim,B)
                    cnt['genus1_complete' if kind=='genus1' else 'genus>=2' if kind=='genus>=2' else 'genus1_complete']+=1
            if chosen is None:
                fr['status']='NO FINITE QUOTIENT (honest curve recorded; linear-relation or open)'
                last=[q for q in fr['quotients'] if q.get('B')==1]
                cnt['genus0' if (last and last[0]['curve_kind'] in ('genus0','genus0-const-square')) else 'genus1_incomplete']+=1
            else: fr['status']=f'finite quotient at B={chosen}'
            fr['lifted_points']=[{'point':{ANG[k]:S(vv) for k,vv in pt.items()} if isinstance(pt,dict) and 'note' not in pt else S(pt),'areas':[S(x) for x in vals] if vals else None} for pt,vals in sols]
            for pt,vals in sols:
                if vals: s['nondegenerate_solutions'].append({'point':{ANG[k]:S(vv) for k,vv in pt.items()},'areas':[S(x) for x in vals]})
            s['factors'].append(fr)
        rec['systems'].append(s)
    fs,fc=fibers(name); rec['fibers']={'nondegenerate_solutions':[S(x) for x in fs],'components':[S(x) for x in fc]}
    rec['summary']=cnt; rec['any_nondegenerate_solution']=any(s['nondegenerate_solutions'] for s in rec['systems']) or bool(fs)
    return rec
if __name__=="__main__":
    import os; os.makedirs('/tmp/tp/certs',exist_ok=True)
    for name in sys.argv[1:]:
        t0=time.time(); rec=certify(name); rec['runtime_s']=round(time.time()-t0)
        json.dump(rec,open(f'/tmp/tp/certs/{name}.json','w'),indent=1,default=str)
        print(name,rec['summary'],'nondegenerate:',rec['any_nondegenerate_solution'],f'[{rec["runtime_s"]}s]',flush=True)
