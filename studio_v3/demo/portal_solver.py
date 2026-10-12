"""2D Euler Bernoulli frame finite element analysis, explicit sign convention.
Nodes: 0 L base, 1 L roof, 2 beam centre, 3 R roof, 4 R base.
Elements are oriented upwards for columns, from left to right for beam.
"""
import json
from pathlib import Path
import numpy as np

L=5.6; H=3.4
EA=1.4e7
EI_BEAM=28000.0
EI_COLUMN=20000.0
VERTICAL_LOAD=35.0 # kN downward at beam midpoint
HORIZONTAL_LOAD=24.0 # kN right at right roof joint
NODES=np.array([[0,0],[0,H],[L/2,H],[L,H],[L,0]],float)
ELEMENTS=[(0,1,EI_COLUMN),(1,2,EI_BEAM),(2,3,EI_BEAM),(4,3,EI_COLUMN)]
FREE=np.array([3,4,5,6,7,8,9,10,11])


def member_matrices(n1,n2,EI):
    p=NODES[n1]; q=NODES[n2]
    vec=q-p; le=float(np.linalg.norm(vec)); c,s=vec/le
    ea=EA/le; e2=EI/le; b=12*EI/le**3; d=6*EI/le**2
    kl=np.array([[ ea,0,0,-ea,0,0],
                 [0,b,d,0,-b,d],
                 [0,d,4*e2,0,-d,2*e2],
                 [-ea,0,0,ea,0,0],
                 [0,-b,-d,0,b,-d],
                 [0,d,2*e2,0,-d,4*e2]],float)
    T=np.zeros((6,6))
    for off in (0,3):
        T[off:off+2,off:off+2]=[[c,s],[-s,c]]
        T[off+2,off+2]=1
    ix=np.array([n1*3,n1*3+1,n1*3+2,n2*3,n2*3+1,n2*3+2])
    return le,kl,T,ix


def solve(case):
    assert case in ('gravity','lateral')
    ndof=3*len(NODES)
    K=np.zeros((ndof,ndof)); F=np.zeros(ndof)
    for n1,n2,EI in ELEMENTS:
        le,kl,T,ix=member_matrices(n1,n2,EI)
        K[np.ix_(ix,ix)] += T.T@kl@T
    if case=='gravity': F[2*3+1]=-VERTICAL_LOAD
    else: F[3*3]=HORIZONTAL_LOAD
    u=np.zeros(ndof);u[FREE]=np.linalg.solve(K[np.ix_(FREE,FREE)],F[FREE]);react=K@u-F
    element_data=[]
    for n1,n2,EI in ELEMENTS:
        le,kl,T,ix=member_matrices(n1,n2,EI)
        dl=T@u[ix]; fl=kl@dl
        # Local forces at element end: V_i and M_i. Internal M(x)=-M_i+V_i*x for q=0
        vals=[]
        for t in np.linspace(0,1,31):
            v=((1-3*t*t+2*t**3)*dl[1]+(t-2*t*t+t**3)*le*dl[2]
                 +(3*t*t-2*t**3)*dl[4]+(-t*t+t**3)*le*dl[5])
            ux=(1-t)*dl[0]+t*dl[3]
            vec=T[:2,:2].T@np.array([ux,v])
            p=NODES[n1]*(1-t)+NODES[n2]*t
            vals.append({'t':round(float(t),5),'xy':[round(float(k),8) for k in p],
                         'uxy':[round(float(k),10) for k in vec],
                         'M':round(float(-fl[2]+fl[1]*le*t),8),
                         'V':round(float(fl[1]),8)})
        element_data.append({'nodes':[n1,n2], 'EI':EI,'length':le,'end_forces_local':[float(x) for x in fl],
                             'rotations_end':[float(dl[2]),float(dl[5])],
                             'samples':vals})
    nodeU=u.reshape(-1,3)
    return {'case':case,'nodes':NODES.tolist(),'u':nodeU.tolist(),'reaction':react.reshape(-1,3).tolist(),
            'elements':element_data,'load':float(VERTICAL_LOAD if case=='gravity' else HORIZONTAL_LOAD),
            'global_residual_max':float(np.max(np.abs((K@u-F)[FREE])))}


def verify():
    v=solve('gravity');h=solve('lateral')
    assert v['global_residual_max'] < 1e-6 and h['global_residual_max']<1e-6
    for r in (v,h):
        u=np.array(r['u'])
        assert np.allclose(u[[0,4]],0)
        for e in r['elements']:
            # M'(x) = V on every prismatic member segment with no distributed transverse loading
            M=e['samples']; Lm=e['length']; delta=(M[-1]['M']-M[0]['M'])/Lm
            assert abs(delta-M[0]['V'])<1e-6
            assert np.isclose(M[0]['M'],-e['end_forces_local'][2],atol=1e-7)
    # Symmetric vertical load: left/right tip vertical displacements equal and lateral shifts antisymmetric.
    uv=np.array(v['u'])
    assert np.isclose(uv[1,1],uv[3,1],atol=1e-9)
    assert np.isclose(uv[1,0],-uv[3,0],atol=1e-9)
    assert uv[2,1]<uv[1,1]<0
    assert np.isclose(uv[1,2],-uv[3,2],atol=1e-9)
    uh=np.array(h['u'])
    assert uh[1,0]>0 and uh[3,0]>0
    assert (uh[1,0]+uh[3,0])/2 > 0
    assert np.isclose(np.sum(np.array(v['reaction'])[:,1]),VERTICAL_LOAD,rtol=0,atol=1e-7)
    assert np.isclose(np.sum(np.array(h['reaction'])[:,0]),-HORIZONTAL_LOAD,rtol=0,atol=1e-7)
    print('Cases:',v['case'],h['case'])
    print('Gravity displacements: ',np.array(v['u']).round(7))
    print('Lateral displacements: ',np.array(h['u']).round(7))
    for r in (v,h):
        print(r['case'],'local M_end and V_i:')
        for e in r['elements']:
            print(e['nodes'], 'M_0',round(e['samples'][0]['M'],3),'M_L',round(e['samples'][-1]['M'],3),'V',round(e['samples'][0]['V'],3), 'internal root',round(e['end_forces_local'][2],3))
    return v,h

if __name__=='__main__':
    v,h=verify();out=Path('frame_data.json');out.write_text(json.dumps({'gravity':v,'lateral':h, 'geometry':{'H':H,'L':L,'EA':EA,'EI_beam':EI_BEAM,'EI_columns':EI_COLUMN}},indent=2))
