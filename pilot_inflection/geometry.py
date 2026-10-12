"""Source-of-truth transforms for the 32 s inflection-point visual study.

All curves are interpolated from the FEM's Hermite displacement fields. No hand-
drawn deflection or arbitrary inflection-point position is used for the video.
"""
import sys
from pathlib import Path
from math import hypot
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE.parent/"studio_v3"/"demo"),str(HERE.parent/"studio_v3")]
from portal_solver import solve,H,L
from structural_viz.model import member_from_solver

CASE=solve("lateral")
LEFT=member_from_solver(CASE["elements"][0],"C1")
RIGHT=member_from_solver(CASE["elements"][3],"C2")
MEMBERS=tuple(member_from_solver(e,k) for e,k in zip(CASE["elements"],("C1","V1","V2","C2")))
INFLECTION_T=-LEFT.samples[0].M/(LEFT.samples[-1].M-LEFT.samples[0].M)  # exact affine root from ends; samples round t to 5 decimals
INFLECTION_H=INFLECTION_T*H
AMPLIFICATION=155.0
PORTAL_ORIGIN=(-3.57,-2.36)
PORTAL_SCALE=1.28
ZOOM_ORIGIN=(-1.25,-2.57)
ZOOM_SCALE=1.37

def point(p,alpha=0,zoom=False):
    x=p.x+alpha*AMPLIFICATION*p.displacement_x
    y=p.y+alpha*AMPLIFICATION*p.displacement_y
    if zoom:
        return (ZOOM_ORIGIN[0]+ZOOM_SCALE*x,ZOOM_ORIGIN[1]+ZOOM_SCALE*y)
    return (PORTAL_ORIGIN[0]+PORTAL_SCALE*x,PORTAL_ORIGIN[1]+PORTAL_SCALE*y)

def member_samples(member,alpha=0,zoom=False):
    return [point(s,alpha,zoom) for s in member.samples]

def roof_joint(alpha=0):
    a=CASE["nodes"][3];b=CASE["u"][3]
    return (PORTAL_ORIGIN[0]+PORTAL_SCALE*(a[0]+alpha*AMPLIFICATION*b[0]),
            PORTAL_ORIGIN[1]+PORTAL_SCALE*(a[1]+alpha*AMPLIFICATION*b[1]))

def inflection_point(alpha=1,zoom=True):
    samples=LEFT.samples;t=INFLECTION_T
    for a,b in zip(samples[:-1],samples[1:]):
        if a.t<=t<=b.t:
            w=(t-a.t)/(b.t-a.t)
            class Pt:pass
            p=Pt()
            p.x=a.x+(b.x-a.x)*w
            p.y=a.y+(b.y-a.y)*w
            p.displacement_x=a.displacement_x+(b.displacement_x-a.displacement_x)*w
            p.displacement_y=a.displacement_y+(b.displacement_y-a.displacement_y)*w
            return point(p,alpha,zoom)
    raise RuntimeError("Zero moment point could not be interpolated")

def tangent_at(t,alpha=1,zoom=True):
    # Use displaced geometry derivative dx/dy, NOT a guessed rotation.
    p=LEFT.samples
    i=min(range(1,len(p)-1),key=lambda j:abs(p[j].t-t))
    a=point(p[i-1],alpha,zoom);b=point(p[i+1],alpha,zoom)
    delta=(b[0]-a[0],b[1]-a[1])
    l=hypot(*delta)
    centre=point(p[i],alpha,zoom)
    unit=(delta[0]/l,delta[1]/l)
    half=.52
    return ((centre[0]-unit[0]*half,centre[1]-unit[1]*half),
            (centre[0]+unit[0]*half,centre[1]+unit[1]*half)),centre

def diagram_coords():
    # M(x) is affine under this load. Positive to right of original upright axis.
    base=(ZOOM_ORIGIN[0],ZOOM_ORIGIN[1])
    high=(ZOOM_ORIGIN[0],ZOOM_ORIGIN[1]+ZOOM_SCALE*H)
    mid=(ZOOM_ORIGIN[0],ZOOM_ORIGIN[1]+ZOOM_SCALE*INFLECTION_H)
    m0=LEFT.samples[0].M;m1=LEFT.samples[-1].M
    scale=1.0/max(abs(m0),abs(m1))
    return {"base":base,"high":high,"mid":mid,
            "negative_tip":(base[0]+m0*scale*1.36,base[1]),
            "positive_tip":(high[0]+m1*scale*1.36,high[1]),
            "m0":m0,"m1":m1}

def verify():
    from math import isclose
    assert abs(INFLECTION_H-1.981)<.07,(INFLECTION_H,INFLECTION_T)
    m0=LEFT.samples[0].M;m1=LEFT.samples[-1].M
    assert m0<0<m1
    assert abs(m0+LEFT.samples[0].V*INFLECTION_H)<1e-5
    assert point(LEFT.samples[0],0,True)==point(LEFT.samples[0],1,True)
    assert roof_joint(1)[0]>roof_joint(0)[0]
    assert all(-6.9<x<6.9 and -3.8<y<3.4 for member in MEMBERS for x,y in member_samples(member,1))
    print(f"PASS FEM: M0={m0:.4f}kNm, M1={m1:.4f}kNm; zero at {INFLECTION_H:.4f}m")
    return True
if __name__=="__main__":verify()
