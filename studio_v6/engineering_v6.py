"""Independent presentation contract for the four FEM analysis elements."""
import sys, math, json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parent/"studio_v3"/"demo"))
from portal_solver import solve,member_matrices,EA,EI_COLUMN,EI_BEAM,ELEMENTS,NODES
import numpy as np
LABELS=("C1","Viga-1","Viga-2","C2")
def members(case="lateral"):
    r=solve(case)
    output=[]
    for label,e in zip(LABELS,r["elements"]):
        f=e["end_forces_local"]
        # Standard local tension sign: member end force at i is -N.
        n=-f[0]
        m0=e["samples"][0]["M"];m1=e["samples"][-1]["M"]
        vi=e["samples"][0]["V"];vlast=e["samples"][-1]["V"]
        assert abs(n-f[3])<1e-6
        assert abs(m1-m0-vi*e["length"])<1e-5
        assert abs(vi-vlast)<1e-6
        output.append(dict(name=label,nodes=e["nodes"],length=e["length"],
                      N=round(float(n),6),V=round(float(vi),6),
                      M0=round(float(m0),6),M1=round(float(m1),6),
                      zero_M=(-m0/vi if abs(vi)>1e-9 and 0<=-m0/vi<=e["length"] else None)))
    return output
def check():
    r=solve("lateral");data=members()
    assert len(data)==4 and all(x["length"]>0 for x in data)
    assert all(x["nodes"]==[a,b] for x,(a,b,_) in zip(data,ELEMENTS))
    R=np.array(r["reaction"]); F=np.array([24.,0.,0.])
    assert abs(R[:,0].sum()+F[0])<1e-7
    assert abs(R[:,1].sum())<1e-7
    moment_load=-24.*3.4
    mr=(R[:,2]+NODES[:,0]*R[:,1]-NODES[:,1]*R[:,0]).sum()
    assert abs(mr+moment_load)<1e-6
    # Adjacent beam halves are in fact continuous: bending at centre agrees.
    assert abs(data[1]["M1"]-data[2]["M0"])<1e-5
    # Under this lateral-only case, no point load at the beam centre -> V continuous.
    assert abs(data[1]["V"]-data[2]["V"])<1e-5
    print("Engineering V6 PASS: all 4 M,V,N profiles, local axes, both columns, two beam segments, global equilibrium")
    print(json.dumps(data,indent=2,ensure_ascii=False))
    return data
if __name__=="__main__":
    check()
