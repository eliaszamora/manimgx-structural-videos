"""2D Euler-Bernoulli rigid-joint portal finite element model; member local signs explicit."""
import json
from pathlib import Path
import numpy as np
L,H=5.6,3.4
EA=1.4e7; EI_BEAM=28000.0; EI_COLUMN=20000.0
VERTICAL_LOAD=35.0;HORIZONTAL_LOAD=24.0
NODES=np.array([[0,0],[0,H],[L/2,H],[L,H],[L,0]],dtype=float)
ELEMENTS=[(0,1,EI_COLUMN),(1,2,EI_BEAM),(2,3,EI_BEAM),(4,3,EI_COLUMN)]
FREE=np.array([3,4,5,6,7,8,9,10,11])

def member_matrices(n1,n2,EI):
    p=NODES[n1];q=NODES[n2]
    v=q-p;ell=float(np.linalg.norm(v));c,s=v/ell
    ea=EA/ell;e=EI/ell;b=12*EI/ell**3;d=6*EI/ell**2
    k=np.array([[ea,0,0,-ea,0,0],[0,b,d,0,-b,d],[0,d,4*e,0,-d,2*e],
                [-ea,0,0,ea,0,0],[0,-b,-d,0,b,-d],[0,d,2*e,0,-d,4*e]])
    T=np.zeros((6,6))
    for i in (0,3):
        T[i:i+2,i:i+2]=[[c,s],[-s,c]];T[i+2,i+2]=1
    ix=np.array([n1*3,n1*3+1,n1*3+2,n2*3,n2*3+1,n2*3+2])
    return ell,k,T,ix

def solve(case):
    assert case in ('gravity','lateral')
    ndof=3*len(NODES);K=np.zeros((ndof,ndof));F=np.zeros(ndof)
    for a,b,EI in ELEMENTS:
        ell,k,T,ix=member_matrices(a,b,EI)
        K[np.ix_(ix,ix)]+=T.T@k@T
    if case=='gravity':F[2*3+1]=-VERTICAL_LOAD
    else:F[3*3]=HORIZONTAL_LOAD
    u=np.zeros(ndof);u[FREE]=np.linalg.solve(K[np.ix_(FREE,FREE)],F[FREE])
    reactions=K@u-F
    elements=[]
    for a,b,EI in ELEMENTS:
        ell,k,T,ix=member_matrices(a,b,EI)
        dl=T@u[ix];f=k@dl
        samples=[]
        for t in np.linspace(0,1,31):
            uy=((1-3*t*t+2*t**3)*dl[1]+(t-2*t*t+t**3)*ell*dl[2]+
                (3*t*t-2*t**3)*dl[4]+(-t*t+t**3)*ell*dl[5])
            ux=(1-t)*dl[0]+t*dl[3]
            move=T[:2,:2].T@np.array([ux,uy])
            xy=NODES[a]*(1-t)+NODES[b]*t
            samples.append({'t':float(t),'xy':xy.tolist(),'uxy':move.tolist(),
                            'M':float(-f[2]+f[1]*ell*t),'V':float(f[1])})
        elements.append({'nodes':[a,b],'EI':EI,'length':ell,
                         'end_forces_local':f.tolist(),'samples':samples})
    return {'case':case,'nodes':NODES.tolist(),'u':u.reshape(-1,3).tolist(),
            'reaction':reactions.reshape(-1,3).tolist(),'elements':elements,
            'global_residual_max':float(np.max(np.abs((K@u-F)[FREE])))}

def verify():
    g=solve('gravity');h=solve('lateral')
    for r in (g,h):
        assert r['global_residual_max']<1e-6
        for e in r['elements']:
            assert abs((e['samples'][-1]['M']-e['samples'][0]['M'])/e['length']-e['samples'][0]['V'])<1e-6
        u=np.array(r['u']);assert np.allclose(u[[0,4]],0)
    gU=np.array(g['u']);hU=np.array(h['u'])
    assert np.isclose(gU[1,1],gU[3,1],atol=1e-9)
    assert np.isclose(gU[1,0],-gU[3,0],atol=1e-9)
    assert gU[2,1]<gU[1,1]<0
    assert np.isclose(gU[1,2],-gU[3,2],atol=1e-9)
    assert hU[1,0]>0 and hU[3,0]>0
    assert np.isclose(np.sum(np.array(g['reaction'])[:,1]),VERTICAL_LOAD,atol=1e-7)
    assert np.isclose(np.sum(np.array(h['reaction'])[:,0]),-HORIZONTAL_LOAD,atol=1e-7)
    for i in (0,3):
        e=h['elements'][i]
        assert e['samples'][0]['M']*e['samples'][-1]['M']<0, 'No column inflection'
    print('PASS: equilibrium, compatibility, symmetric gravity, lateral sway and double curvature')
    for r in (g,h):
        print(r['case'],'upper displacements',np.array(r['u'])[1:4].tolist())
        for e in r['elements']:print(e['nodes'],'M_end',[round(e['samples'][0]['M'],3),round(e['samples'][-1]['M'],3)],'V',round(e['samples'][0]['V'],3))
    return g,h

if __name__=='__main__':
    g,h=verify()
    Path('frame_data.json').write_text(json.dumps({'gravity':g,'lateral':h,
                                'geometry':{'H':H,'L':L,'EA':EA}},indent=2))
