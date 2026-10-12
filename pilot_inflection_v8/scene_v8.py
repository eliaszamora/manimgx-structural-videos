"""Structural Studio V8 — advanced ManimGX visual-only pilot (≈28 s).

- One ValueTracker for load fraction: EVERY member, joint and load update per frame.
- Actual 2D camera.frame zoom: no substitute enlarged drawing.
- Continuous FEM cubic tangent; curvature changes sign at FEM M=0.
- Signed local M fills emerge on the original, nondeformed left-column axis.

Silent deliberately: judge pedagogical motion before recording Alex natural.
"""
import sys
from pathlib import Path
import numpy as np
import manimgx as m
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parent/"pilot_inflection")]
from geometry_v8 import (MEMBERS,LEFT,CASE,H,INFLECTION_T,INFLECTION_H,
                         AMPLIFICATION,member_samples,roof_joint,
                         parametric,tangent,signed_moment,proof)
proof()
BG="#0B192C"; TEXT="#F2F6FA"; QUIET="#BDD0E2"; GHOST="#4E637B"
STRUCTURE="#58C4DD"; FORCE="#F4A261"; NEG="#FC6255"; POS="#F5D76E"; ZERO="#B9A0E5"
X0,Y0=-3.57,-2.36
S=1.28
def V(x):return np.array([float(x[0]),float(x[1]),0.])
def write(t,xy=(0,0),size=29,color=TEXT):
    return m.Text(t,font="DejaVu Sans",font_size=size,color=color).move_to(V(xy))
def line(p,q,col=QUIET,thick=3):
    return m.Line(V(p),V(q),color=col,stroke_width=thick)
def shape(coords,col=STRUCTURE,thick=8):
    a=m.VMobject(color=col,stroke_width=thick)
    a.set_points_smoothly([V(p) for p in coords])
    return a
def member_mob(element,lambda_value):
    if element is LEFT:
        points=[parametric(float(t),lambda_value) for t in np.linspace(0,1,49)]
    else:
        points=[V(p) for p in member_samples(element,lambda_value)]
    return shape(points)
def fixed(x,y):
    baseline=line((x-.48,y-.025),(x+.48,y-.025),TEXT,4)
    hatch=[line((x-.45+i*.17,y-.04),(x-.60+i*.17,y-.31),GHOST,2)
           for i in range(6)]
    return m.VGroup(baseline,*hatch)
def attached_force(lam):
    x,y=roof_joint(lam)
    # force TAIL EXACTLY ON ROOF JOINT; length increases with load
    return m.Arrow(V((x,y)),V((x+.30+.90*lam,y)),buff=0,
                   color=FORCE,stroke_width=8)
def tangent_mob(t):
    a,b=tangent(float(t),1.,half=.70)
    col=NEG if signed_moment(float(t))<0 else POS
    return line(a,b,col,6)
def tangent_dot(t):
    col=NEG if signed_moment(float(t))<0 else POS
    return m.Dot(point=parametric(float(t),1.),radius=.105,color=col)
def tangent_ref(t):
    p=parametric(float(t),1.)
    return m.DashedLine(p-.63*m.UP,p+.63*m.UP,
                        color=QUIET,stroke_width=2.3,dash_length=.095)
def split_col(lo,hi,col):
    pts=[parametric(float(t),1.) for t in np.linspace(lo,hi,27)]
    return shape(pts,col,11)
def plot_partial(a,b,progress,col):
    # Bending about the UNDEFORMED upward member centerline, same convention
    # negative to local left; positive to local right.
    progress=float(progress)
    upper=a+(b-a)*progress
    y0=Y0+S*H*a
    y1=Y0+S*H*upper
    # Normalize both signs by common absolute maximum.
    maxmoment=max(abs(signed_moment(0)),abs(signed_moment(1)))
    offset=lambda t:1.28*signed_moment(t)/maxmoment
    if a==0:
        points=[(X0,y0),(X0+offset(a),y0),
                (X0+offset(upper),y1),(X0,y1)]
    else:
        points=[(X0,y0),(X0+offset(upper),y1),(X0,y1)]
    return m.Polygon(*[V(v) for v in points],
              color=col,fill_color=col,fill_opacity=.30,stroke_width=3)
class VisualInflectionV8(m.Scene):
    def construct(self):
        self.camera.background_color=BG
        lam=m.ValueTracker(0.)
        s=m.ValueTracker(.12)
        full=m.VGroup(*[m.always_redraw(lambda element=e:member_mob(element,lam.get_value()))
                        for e in MEMBERS])
        u0=MEMBERS[0].samples[0];ur=MEMBERS[-1].samples[0]
        feet=m.VGroup(fixed(X0,Y0),
                      fixed(-3.57+S*5.6,Y0))
        undeformed=m.VGroup(*[shape(member_samples(e,0),GHOST,2.5)
                             for e in MEMBERS])
        h=write("¿POR QUÉ CAMBIA LA CURVATURA?",(0,3.44),30)
        sub=write("PÓRTICO RÍGIDO   ·   ESTUDIO VISUAL",(0,2.91),20,QUIET)
        self.add(undeformed,full,feet)
        self.play(m.FadeIn(h),m.FadeIn(sub),run_time=.75)
        self.wait(.4)
        force=m.always_redraw(lambda:attached_force(lam.get_value()))
        readout=m.DecimalNumber(0,num_decimal_places=0,font_size=28,color=FORCE)
        readout.add_updater(lambda x:x.set_value(100*lam.get_value()))
        label=write("Carga aplicada: ",(0,-3.44),22,QUIET)
        readout.move_to([1.57,-3.44,0])
        readout.add_updater(lambda mob:mob.move_to([1.57,-3.44,0]))
        pct=write("%",(2.0,-3.44),22,QUIET)
        self.play(m.FadeIn(force),m.FadeIn(label),m.FadeIn(readout),
                  m.FadeIn(pct),run_time=.50)
        # Frame-by-frame coordinated physics. No Transform to a pre-made curve.
        self.play(lam.animate.set_value(1.),run_time=4.1)
        self.wait(.35)
        # Focus the SAME continuously deforming column with a real camera zoom.
        self.play(m.FadeOut(h),m.FadeOut(sub),m.FadeOut(label),
                  m.FadeOut(readout),m.FadeOut(pct),
                  m.FadeOut(force),m.FadeOut(feet),
                  *[m.FadeOut(obj) for obj in list(full)[1:]],
                  self.camera.frame.animate.scale(.70).move_to(np.array([-2.6,-.09,0.])),
                  run_time=2.55)
        # The original axis persists as a faint reference. No graphical jump.
        focus=write("LA PENDIENTE CAMBIA",( -1.46,2.34),28)
        self.play(m.FadeIn(focus),run_time=.40)
        tan=m.always_redraw(lambda:tangent_mob(s.get_value()))
        ref=m.always_redraw(lambda:tangent_ref(s.get_value()))
        dot=m.always_redraw(lambda:tangent_dot(s.get_value()))
        theta=m.always_redraw(lambda:write("θ",
                (parametric(s.get_value())[0]+.91,parametric(s.get_value())[1]+.12),
                32,POS if signed_moment(s.get_value())>=0 else NEG))
        self.play(m.FadeIn(tan),m.FadeIn(ref),m.FadeIn(dot),m.FadeIn(theta),
                  run_time=.55)
        # True continuous tangent motion — no nearest-sample jumps.
        self.play(s.animate.set_value(.89),run_time=5.4)
        self.play(m.FadeOut(tan),m.FadeOut(ref),m.FadeOut(dot),
                  m.FadeOut(theta),m.FadeOut(focus),run_time=.38)
        # Opposite-curvature regions identified on SAME FEM column.
        below=split_col(0,INFLECTION_T,NEG)
        above=split_col(INFLECTION_T,1,POS)
        pivot=m.Dot(point=parametric(INFLECTION_T),radius=.15,color=ZERO)
        ring=m.Circle(radius=.27,color=ZERO,stroke_width=3).move_to(parametric(INFLECTION_T))
        curv=write("CAMBIA LA CONCAVIDAD",(-1.47,2.34),26,QUIET)
        note=write("NO ES UNA RÓTULA",(-.76,-2.47),27,ZERO)
        self.play(m.FadeIn(below),m.FadeIn(above),m.FadeIn(pivot),
                  m.Create(ring),m.FadeIn(curv),run_time=.95)
        self.play(m.FadeIn(note),run_time=.32)
        self.wait(.65)
        self.play(m.FadeOut(below),m.FadeOut(above),m.FadeOut(pivot),
                  m.FadeOut(ring),m.FadeOut(curv),m.FadeOut(note),
                  m.FadeOut(full[0]),
                  run_time=.65)
        # Exactly ORIGINAL straight member: no distorted baseline behind diagram.
        axis=line((X0,Y0),(X0,Y0+S*H),TEXT,4)
        self.play(m.FadeIn(axis),run_time=.55)
        m0=write("MOMENTO SOBRE EL EJE ORIGINAL",(-1.42,2.34),25,QUIET)
        self.play(m.FadeIn(m0),run_time=.35)
        pneg=m.ValueTracker(0.)
        ppos=m.ValueTracker(0.)
        neg=m.always_redraw(lambda:plot_partial(0,INFLECTION_T,pneg.get_value(),NEG))
        pos=m.always_redraw(lambda:plot_partial(INFLECTION_T,1,ppos.get_value(),POS))
        self.add(neg,pos)
        self.play(pneg.animate.set_value(1),run_time=1.85)
        self.play(ppos.animate.set_value(1),run_time=1.85)
        d=m.Dot(point=V((X0,Y0+S*INFLECTION_H)),radius=.12,color=ZERO)
        z=write("M = 0",(X0+1.22,Y0+S*INFLECTION_H+.05),28,ZERO)
        self.play(m.FadeIn(d),m.FadeIn(z),run_time=.55)
        end=write("INFLEXIÓN ↔ MOMENTO NULO",(-1.25,-2.50),25,QUIET)
        self.play(m.FadeIn(end),run_time=.55)
        self.wait(.95)
