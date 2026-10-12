"""Independent anaStruct cross-check of both portal cases, displacement signs and values."""
from math import isclose
from anastruct import SystemElements
from mechanics import solve,NODES,ELEMENTS,EA,VERTICAL_LOAD,HORIZONTAL_LOAD

def independent_solve(case):
    model=SystemElements(EA=EA,EI=20000)
    for a,b,EI in ELEMENTS:
        model.add_element(location=[NODES[a].tolist(),NODES[b].tolist()],EA=EA,EI=EI)
    model.add_support_fixed(node_id=[1,5])
    if case=='gravity':model.point_load(node_id=3,Fy=-VERTICAL_LOAD)
    else:model.point_load(node_id=4,Fx=HORIZONTAL_LOAD)
    model.solve()
    return [model.get_node_displacements(i) for i in range(1,6)]

def main():
    for case in ('gravity','lateral'):
        expected=solve(case)['u'];actual=independent_solve(case)
        for node,(u,v) in enumerate(zip(expected,actual)):
            for key,j in (('ux',0),('uy',1)):
                assert isclose(float(v[key]),float(u[j]),rel_tol=.03,abs_tol=1.5e-5),(
                    case,node,key,'ours',u[j],'anaStruct',v[key])
        print('PASS independent anaStruct',case)
if __name__=='__main__':main()
