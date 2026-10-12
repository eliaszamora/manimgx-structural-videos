"""Checks every signed diagram before permitting animation rendering."""
import numpy as np
from mechanics import solve,H,VERTICAL_LOAD,HORIZONTAL_LOAD
def main():
    for case in ['gravity','lateral']:
        d=solve(case)
        assert d['global_residual_max'] < 1.e-6
        for e in d['elements']:
            ss=e['samples']; M=np.array([p['M'] for p in ss]);V=np.array([p['V'] for p in ss])
            step=e['length']/(len(ss)-1)
            assert np.max(np.abs(np.diff(M)/step-V[:-1]))<1.e-7
            assert np.ptp(V)<1.e-9
            xy=np.array([p['xy'] for p in ss]); u=np.array([p['uxy'] for p in ss])
            axis=(xy[-1]-xy[0])/e['length']; n=np.array([-axis[1],axis[0]])
            w=u@n
            curv=np.gradient(np.gradient(w,step),step)
            assert np.max(abs(e['EI']*curv[2:-2]-M[2:-2]))<.045
    g=solve('gravity'); h=solve('lateral')
    g1,g2=g['elements'][1:3]
    assert g1['samples'][0]['M']<0<g1['samples'][-1]['M']
    assert g2['samples'][0]['M']>0>g2['samples'][-1]['M']
    assert abs(g1['samples'][0]['V']-17.5)<.01
    assert abs(g2['samples'][0]['V']+17.5)<.01
    assert abs(g1['samples'][0]['V']-g2['samples'][0]['V']-VERTICAL_LOAD)<1.e-6
    for i in [0,3]:
        e=h['elements'][i];lo=e['samples'][0]['M'];hi=e['samples'][-1]['M']
        assert lo<0<hi
        z=H*abs(lo)/(abs(lo)+abs(hi))
        assert 1.75<z<2.15
    assert abs(sum(h['elements'][i]['samples'][0]['V'] for i in [0,3])-HORIZONTAL_LOAD)<1.e-6
    print('PASS: 8 member M and V diagrams, curvature, equilibrium, shear jump, inflection points')
if __name__=='__main__':main()
