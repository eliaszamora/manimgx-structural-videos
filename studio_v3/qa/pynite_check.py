"""Independent 3D PyNite model restrained to the in-plane XY DOF.

Checks nodal displacement and global reactions. Internal member diagrams require
explicit local-axis mapping and remain a separate/manual sign check.
"""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from demo.portal_solver import solve,EI_COLUMN,EI_BEAM,EA,H,L,NODES

def main():
    from Pynite import FEModel3D
    model=FEModel3D()
    for i,(x,y) in enumerate(NODES):model.add_node('N'+str(i),float(x),float(y),0.0)
    E=10000.0
    model.add_material('MAT',E=E,G=E/2.6,nu=.3,rho=0)
    model.add_section('COL',A=EA/E,Iy=EI_COLUMN/E,Iz=EI_COLUMN/E,J=1)
    model.add_section('BEAM',A=EA/E,Iy=EI_BEAM/E,Iz=EI_BEAM/E,J=1)
    for a,b,sec in [(0,1,'COL'),(1,2,'BEAM'),(2,3,'BEAM'),(4,3,'COL')]:
        model.add_member(f'M{a}_{b}',f'N{a}',f'N{b}','MAT',sec)
    for idx in range(5):
        if idx in (0,4):
            model.def_support('N'+str(idx),True,True,True,True,True,True)
        else:
            model.def_support('N'+str(idx),support_DZ=True,support_RX=True,support_RY=True)
    model.add_node_load('N3','FX',24,case='LAT')
    model.add_node_load('N2','FY',-35,case='VERT')
    model.add_load_combo('LATERAL',{'LAT':1.0})
    model.add_load_combo('VERTICAL',{'VERT':1.0})
    model.analyze_linear(log=False,check_stability=True,check_statics=True)
    checks=[]
    for case,combo in [('lateral','LATERAL'),('gravity','VERTICAL')]:
        ours=solve(case)
        for node in [1,2,3]:
            obj=model.nodes['N'+str(node)]
            FEM=[obj.DX[combo],obj.DY[combo],obj.RZ[combo]]
            expected=ours['u'][node]
            for index,axis in enumerate('xyθ'):
                tol=1e-5 + abs(expected[index])*.015
                delta=abs(FEM[index]-expected[index])
                if delta>tol:raise AssertionError(f'{case} node {node} {axis}: FEM {FEM[index]} vs structural {expected[index]} delta {delta}')
                checks.append((case,node,axis,delta))
        base_rx=sum(model.nodes[f'N{i}'].RxnFX[combo] for i in [0,4])
        expected_rx=sum(ours['reaction'][i][0] for i in [0,4])
        assert abs(base_rx-expected_rx)<0.04,(case,base_rx,expected_rx)
    print('PyNite PASS:',len(checks),'nodal comparisons and 2 horizontal support reaction checks')
if __name__=='__main__':main()
