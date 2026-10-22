import sympy as sp, itertools, time
t,u,v = sp.symbols('t u v', real=True)
VARS=(t,u,v)
def Zp(var,k): return (1+sp.I*var)**(2*k) if k>=0 else (1-sp.I*var)**(2*(-k))
def E(m):
    val = sp.im(sp.expand(Zp(t,m[0])*Zp(u,m[1])*Zp(v,m[2])))
    for var,mm in zip(VARS,m):
        if mm==0: val=val*(1+var**2)
    return sp.expand(val)

# the 16 sub-configurations (elements as exponent vectors (m1,m2,m3) for angles (x,z,w))
F={'++':(1,1,1),'+-':(1,1,-1),'-+':(1,-1,1),'--':(1,-1,-1)}
XZ=(1,1,0); XW=(1,0,1); ZW=(0,1,1); ZmW=(0,1,-1); W=(0,0,1)
CONF={
 'A':[F['++'],F['+-'],F['-+'],F['--']],
 'B1':[F['+-'],F['-+'],F['--'],XZ],
 'B2':[F['++'],F['+-'],F['--'],XZ],
 'C':[F['++'],F['+-'],F['-+'],W],
 'D1':[F['++'],F['+-'],XZ,XW],
 'D2':[F['++'],F['--'],XZ,XW],
 'D3':[F['+-'],F['-+'],XZ,XW],
 'D4':[F['+-'],F['--'],XZ,XW],
 'E1':[F['++'],F['+-'],XZ,W],
 'E2':[F['-+'],F['--'],XZ,W],
 'E3':[F['++'],F['-+'],XZ,W],
 'E4':[F['++'],F['--'],XZ,W],
 'F+1':[F['++'],XZ,XW,ZW],
 'F+2':[F['+-'],XZ,XW,ZW],
 'F-1':[F['++'],XZ,XW,ZmW],
 'F-2':[F['--'],XZ,XW,ZmW],
 'F-3':[F['+-'],XZ,XW,ZmW],
}
def systems(Es):
    for i,j in itertools.combinations(range(4),2):
        rest=[k for k in range(4) if k not in (i,j)]
        for k in rest:
            l=[r for r in rest if r!=k][0]
            for e2,e3 in itertools.product([1,-1],repeat=2):
                yield (i,j,k,l,e2,e3), sp.expand(Es[i]-e2*Es[k]-e3*Es[l]), sp.expand(Es[j]-e2*Es[k]+e3*Es[l])
