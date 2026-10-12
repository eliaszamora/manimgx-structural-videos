"""V8 structural oracle. Cubic interpolation for a continuously moving tangent.
No guessed deformed curves or guessed inflection location.
"""
from __future__ import annotations
import sys
from functools import lru_cache
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"pilot_inflection"))
from geometry import (MEMBERS,LEFT,CASE,H,INFLECTION_T,INFLECTION_H,
                      AMPLIFICATION,member_samples,roof_joint,diagram_coords)
SCALE=1.28
ORIGIN=(-3.57,-2.36)

@lru_cache(maxsize=1)
def polynomials():
    # Hermite beam deflection is cubic; fit to sampled displacements.
    t=np.array([s.t for s in LEFT.samples],dtype=float)
    px=np.poly1d(np.polyfit(t,[s.displacement_x for s in LEFT.samples],3))
    py=np.poly1d(np.polyfit(t,[s.displacement_y for s in LEFT.samples],3))
    err=max(abs(px(s.t)-s.displacement_x) for s in LEFT.samples)
    assert err<2e-5, f"FEM displacement fit residual {err:g}"
    return px,py

def parametric(t,load=1.0):
    t=float(t);load=float(load)
    assert 0<=t<=1 and 0<=load<=1
    px,py=polynomials()
    x=ORIGIN[0]+SCALE*(AMPLIFICATION*load*px(t))
    y=ORIGIN[1]+SCALE*(H*t+AMPLIFICATION*load*py(t))
    return np.array([x,y,0.],dtype=float)

def dparametric(t,load=1.0):
    px,py=polynomials()
    dx=SCALE*(AMPLIFICATION*load*px.deriv()(t))
    dy=SCALE*(H+AMPLIFICATION*load*py.deriv()(t))
    d=np.array([dx,dy,0.],dtype=float)
    return d/np.linalg.norm(d)

def tangent(t,load=1.,half=.62):
    pos=parametric(t,load)
    d=dparametric(t,load)
    return pos-half*d,pos+half*d

def curvature(t):
    px,py=polynomials()
    dx=SCALE*AMPLIFICATION*px.deriv()(t)
    dy=SCALE*(H+AMPLIFICATION*py.deriv()(t))
    ddx=SCALE*AMPLIFICATION*px.deriv(2)(t)
    ddy=SCALE*AMPLIFICATION*py.deriv(2)(t)
    return (dx*ddy-dy*ddx)/(dx*dx+dy*dy)**1.5

def signed_moment(t):
    lo=LEFT.samples[0].M
    hi=LEFT.samples[-1].M
    return lo*(1-t)+hi*t

def proof():
    assert all(np.linalg.norm(parametric(0,lam)-parametric(0,0))<1e-9
               for lam in np.linspace(0,1,7))
    assert abs(signed_moment(INFLECTION_T))<1e-6
    assert abs(INFLECTION_H-1.979)<.07
    for a in np.linspace(.1,.9,9):
        d=dparametric(float(a));assert .999<np.linalg.norm(d)<1.001
    assert curvature(.15)*curvature(.84)<0
    assert abs(curvature(INFLECTION_T))<max(abs(curvature(.15)),abs(curvature(.84)))*.06
    return {"moment_zero_m":INFLECTION_H,
            "moment_base_kNm":LEFT.samples[0].M,
            "moment_top_kNm":LEFT.samples[-1].M,
            "initial_curvature":curvature(.15),
            "final_curvature":curvature(.84)}
if __name__=="__main__":
    print(proof())
