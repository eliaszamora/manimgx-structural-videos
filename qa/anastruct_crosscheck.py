"""Validación independiente del voladizo con anaStruct (FEM, no motor gráfico).

Este test NO comparte la fórmula de deformada con el renderizador;
compara una solución independiente con la solución analítica definida en QA.
"""
from __future__ import annotations
from math import isclose
from anastruct import SystemElements
from qa.mechanics import Cantilever

def solve_cantilever(m:Cantilever, direction:float)->dict:
    sys=SystemElements(EA=1.0e8, EI=m.EI)
    sys.add_element(location=[[0.0,0.0],[m.length,0.0]])
    sys.add_support_fixed(node_id=1)
    sys.point_load(node_id=2,Fy=direction*m.force)
    sys.solve()
    result=sys.get_node_displacements(node_id=2)
    return {"uy":float(result["uy"]), "phi_z":float(result["phi_z"])}

def main()->None:
    m=Cantilever()
    down=solve_cantilever(m,-1.0)
    up=solve_cantilever(m,1.0)
    expected=m.deflection(m.length)
    expected_rotation=m.slope(m.length)
    assert expected < 0
    # Punto libre negativo para una carga vertical negativa en anaStruct.
    assert down["uy"] < 0, f"Signo inesperado en uy FEM: {down}"
    assert isclose(down["uy"],expected,rel_tol=2e-3,abs_tol=1e-6), f"FEM {down} vs analítica {expected}"
    # Rotación analítica y FEM: comprobar magnitud y simetría del caso inverso.
    assert isclose(abs(down["phi_z"]),abs(expected_rotation),rel_tol=2e-3,abs_tol=1e-6), f"Rotación FEM {down} vs {expected_rotation}"
    assert isclose(up["uy"],-down["uy"],rel_tol=1e-6,abs_tol=1e-7)
    assert isclose(up["phi_z"],-down["phi_z"],rel_tol=1e-6,abs_tol=1e-7)
    print("ANAESTRUCT PASS: desplazamiento, rotación y superposición lineal")
    print(f"Viga L={m.length:g}, P={m.force:g}, EI={m.EI:g}")
    print(f"Tip uy:FEM={down['uy']:.8f}; analytic={expected:.8f}")
    print(f"Tip rot FEM={down['phi_z']:.8f}; analytic |theta|={abs(expected_rotation):.8f}")
    print("ATENCIÓN: no interpretar signos de momentos internos FEM sin mapear la cara y los ejes.")

if __name__=="__main__": main()
