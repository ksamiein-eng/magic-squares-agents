"""Independent exact checks of uploaded three-prime inputs and projection support.
Usage: python audit_inputs.py PATH_TO_EXTRACTED_ARCHIVE OUTPUT_JSON
Only rational polynomial arithmetic; never imports the supplied pipeline.
"""
from pathlib import Path
import ast, json, itertools, collections, sys, time
import sympy as sp
from concurrent.futures import ProcessPoolExecutor
T,U,V,TAU=sp.symbols('t u v tau', real=True)
VS=(T,U,V); names=dict(t=T,u=U,v=V,tau=TAU)

def expr(text):
    def parse(x):
        if isinstance(x,ast.Constant) and type(x.value) is int: return sp.Integer(x.value)
        if isinstance(x,ast.Name) and x.id in names: return names[x.id]
        if isinstance(x,ast.UnaryOp) and isinstance(x.op,(ast.UAdd,ast.USub)):
            a=parse(x.operand); return a if isinstance(x.op,ast.UAdd) else -a
        if isinstance(x,ast.BinOp):
            a,b=parse(x.left),parse(x.right)
            if isinstance(x.op,ast.Add): return a+b
            if isinstance(x.op,ast.Sub): return a-b
            if isinstance(x.op,ast.Mult): return a*b
            if isinstance(x.op,ast.Div): return a/b
            if isinstance(x.op,ast.Pow) and b.is_Integer and abs(b)<=100: return a**b
        raise ValueError('Unsupported polynomial input')
    return parse(ast.parse(str(text),mode='eval').body)

def canon(m):
    m=tuple(m)
    return m if next(x for x in m if x)!=-1 else tuple(-x for x in m)

def numerator(m):
    re,im=sp.Integer(1),sp.Integer(0)
    for z,h in zip(VS,m):
        c=1-z*z if h else 1+z*z
        s=2*z*h
        re,im=sp.expand(re*c-im*s),sp.expand(re*s+im*c)
    return im

def rowkey(tag):
    i,j,k,l,e,f=tag
    a=[0]*4;b=[0]*4
    a[i]=1;a[k]=-e;a[l]=-f
    b[j]=1;b[k]=-e;b[l]=f
    return tuple(sp.Matrix([a,b]).rref()[0])

def check_one(payload):
    name,es,ss,idx=payload
    orig1=expr(ss['G1']); orig2=expr(ss['G2']); i,j,k,l,e,f=ss['tag']
    assert sp.expand(orig1-es[i]+e*es[k]+f*es[l])==0
    assert sp.expand(orig2-es[j]+e*es[k]-f*es[l])==0
    cf=expr(ss['common_factor']) if ss.get('common_factor') else sp.Integer(1)
    # Global constants are irrelevant to zero loci, but variable factors are checked.
    p=sp.Poly(orig1,*VS,domain=sp.QQ);q=sp.Poly(orig2,*VS,domain=sp.QQ)
    h=sp.Poly(cf,*VS,domain=sp.QQ)
    f1,rem=p.div(h); assert rem.is_zero
    f2,rem=q.div(h); assert rem.is_zero
    removed=[]
    if cf.free_symbols:
        for fac,mult in sp.factor_list(cf)[1]:
            fp=sp.Poly(fac,*VS,domain=sp.QQ)
            witnesses=[]
            for a in range(4):
                if sp.Poly(es[a],*VS).rem(fp).is_zero: witnesses.append(['zero',a])
                for b in range(a):
                    for sg in [-1,1]:
                        if sp.Poly(es[a]-sg*es[b],*VS).rem(fp).is_zero: witnesses.append(['equal',a,b,sg])
            assert witnesses,(name,idx,'removed factor not degenerate',str(fac))
            removed.append({'factor':str(fac),'witness':witnesses[0]})
    if not isinstance(ss['projection'],dict): raise ValueError((name,idx,ss['projection']))
    lookup={'x':T,'z':U,'w':V}
    elim=lookup[ss['projection']['eliminated']]
    ab=tuple(lookup[x] for x in ss['projection']['plane'])
    F=sp.Poly(f1.as_expr(),elim); G=sp.Poly(f2.as_expr(),elim)
    m,n=F.degree(),G.degree()
    aa=F.all_coeffs();bb=G.all_coeffs()
    # An explicitly constructed Sylvester matrix, not the producer's resultant routine.
    mat=sp.Matrix([[0]*r+aa+[0]*(n-1-r) for r in range(n)]+[[0]*r+bb+[0]*(m-1-r) for r in range(m)])
    R=sp.Poly(mat.det(method='domain-ge'),*ab,domain=sp.QQ)
    assert not R.is_zero,(name,idx,'zero resultant')
    rest=R; factors=[]
    for fr in ss['factors']:
        pp=sp.Poly(expr(fr['poly']),*ab,domain=sp.QQ)
        assert [pp.degree(x) for x in ab]==fr['bidegree']
        num=0
        while not rest.is_ground:
            q,r=rest.div(pp)
            if not r.is_zero: break
            rest=q; num+=1
        assert num>0,(name,idx,'not a factor',str(pp.as_expr()))
        factors.append({'poly':str(pp.as_expr()),'multiplicity':num,'type':fr['type']})
    assert rest.is_ground,(name,idx,'missing factors',str(rest.as_expr()))
    return {'orbit':name,'index':idx,'tag':ss['tag'],'degrees':[m,n], 'resultant_total_degree':R.total_degree(),'factorization_constant':str(rest.as_expr()),'factors':factors,'removed_components':removed}

def main(root,out):
    start=time.time(); paths=sorted((root/'repro/certs').glob('*.json'))
    records=[json.load(open(p)) for p in paths if p.name!='saturation_table.json']
    allv={}; tasks=[]; summary=[]
    required={tuple((i,j,k,l,e,f)) for i,j in itertools.combinations(range(4),2) for k,l in itertools.permutations([a for a in range(4) if a not in (i,j)]) for e,f in itertools.product([-1,1],repeat=2)}
    assert len(required)==48 and len({rowkey(x) for x in required})==48
    for r in records:
        assert len(r['systems'])==48 and {tuple(s['tag']) for s in r['systems']}==required
        es=[numerator(m) for m in r['elements']]
        assert all(sp.expand(a-expr(b))==0 for a,b in zip(es,r['E_polys']))
        for m,e in zip(r['elements'],es): allv[canon(m)]=e
        tasks.extend((r['config'],es,s,i) for i,s in enumerate(r['systems']))
        summary.append({'orbit':r['config'],'elements':r['elements'],'systems':48,'input_checks':4,'types':dict(collections.Counter(fr['type'] for s in r['systems'] for fr in s['factors']))})
    projective=sorted({canon(m) for m in itertools.product((-1,0,1),repeat=3) if any(m)})
    adm={frozenset(S) for S in itertools.combinations(projective,4) if all(sum(abs(m[i])==1 for m in S)>=3 for i in range(3))}
    def orbit(S):
        return {frozenset(canon(tuple(sg[i]*m[perm[i]] for i in range(3))) for m in S) for sg in itertools.product([-1,1],repeat=3) for perm in itertools.permutations(range(3))}
    seen=set(); distinct=set()
    for r in records:
        o=orbit(r['elements']); assert o<=adm
        seen|=o; distinct.add(min(tuple(sorted(S)) for S in o))
    assert seen==adm
    outdata={'scope':'INPUTS AND PROJECTION ZERO-SET SUPPORT ONLY; not downstream arithmetic completeness', 'counts':{'records':len(records),'stored_E_polynomials':4*len(records),'projective_vectors':len(projective),'admissible_four_sets':len(adm),'distinct_orbits':len(distinct),'signed_systems':len(tasks)},'orbit_summary':summary,'systems':[]}
    with ProcessPoolExecutor(max_workers=4) as ex:
        for k,row in enumerate(ex.map(check_one,tasks,chunksize=4),1):
            outdata['systems'].append(row)
            if k%48==0: print('Checked',k,'/',len(tasks),'elapsed',round(time.time()-start,1),flush=True)
    outdata['elapsed_s']=round(time.time()-start,2);outdata['passed']=True
    out.write_text(json.dumps(outdata,indent=2));print(json.dumps(outdata['counts']))
if __name__=='__main__': main(Path(sys.argv[1]),Path(sys.argv[2]))
