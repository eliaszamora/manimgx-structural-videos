"""Visual pilot V7 — 32 seconds, silent on purpose.

Question: Why does a fixed-base portal column have a point of inflection?
Geometry comes from Euler–Bernoulli frame FEM; not from guessed curves.

Visual grammar: one physical object, camera-free contextual enlargement,
tangent sweep, true zero-curvature marker, signed moment derived from FEM.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import manimgx as m
from geometry import (CASE,MEMBERS,LEFT,AMPLIFICATION,point,member_samples,
                      roof_joint,tangent_at,inflection_point,diagram_coords,
                      verify,H)
verify()
# Blue-first visual system inspired by 3Blue1Brown / classic Manim palettes.
# Color carries meaning consistently: structure blue; load orange; ±M yellow/red.
BG="#0B192C"; INK="#F2F6FA"; MUTED="#BDCBD9"; AXIS="#526780"
FRAME="#58C4DD"; LOAD="#F4A261"; NEG="#FC6255"; POS="#F5D76E"; ZERO="#B9A0E5"
ZOOM_X=-1.25
def V(p):return [float(p[0]),float(p[1]),0]
def label(t,x=0,y=0,size=24,color=INK):
    return m.Text(t,font="DejaVu Sans",font_size=size,color=color).move_to([x,y,0])
def ln(a,b,color=AXIS,width=3):return m.Line(V(a),V(b),color=color,stroke_width=width)
def path(points,color=FRAME,width=8):
    c=m.VMobject(color=color,stroke_width=width)
    c.set_points_smoothly([V(v) for v in points])
    return c
def drawing(alpha=0,color=FRAME,width=8):
    return m.VGroup(*[path(member_samples(e,alpha),color,width) for e in MEMBERS])
def foot(x,y):
    baseline=ln((x-.45,y-.04),(x+.45,y-.04),INK,4.5)
    hatch=[ln((x-.43+i*.165,y-.06),(x-.57+i*.165,y-.31),AXIS,2)
           for i in range(6)]
    return m.VGroup(baseline,*hatch)
def load_arrow(alpha,length=1.15):
    x,y=roof_joint(alpha)
    return m.Arrow(V((x,y)),V((x+length,y)),buff=0,
                   color=LOAD,stroke_width=7)
def tip_label():return label("H",5.60,2.02,22,LOAD)
def closeup(alpha=1,color=FRAME,width=9):
    return path(member_samples(LEFT,alpha,zoom=True),color,width)
class InflectionVisualPilot(m.Scene):
    def act(self,*animations,sec=1.0):
        self.play(*animations,run_time=sec);self.sec+=sec
    def hold_until(self,target):
        if target>self.sec:self.wait(target-self.sec);self.sec=target
    def caption(self,message,color=MUTED):
        target=label(message,0,-3.45,27,color)
        if getattr(self,"caption_current",None) is not None:
            self.act(m.FadeOut(self.caption_current),sec=.16)
        self.act(m.FadeIn(target),sec=.27)
        self.caption_current=target
    def construct(self):
        self.sec=0
        self.camera.background_color=BG
        brand=label("MECÁNICA ESTRUCTURAL  /  ESTUDIO VISUAL",0,3.65,19,MUTED)
        title=label("¿DÓNDE CAMBIA LA CURVATURA?",0,3.14,31,INK)
        frame=drawing(0)
        ghost=drawing(0,AXIS,3)
        a=CASE["nodes"][0];b=CASE["nodes"][4]
        feet=m.VGroup(foot(*point(MEMBERS[0].samples[0])),
                      foot(*point(MEMBERS[3].samples[0])))
        self.add(brand)
        self.act(m.FadeIn(title),m.FadeIn(feet),sec=.65)
        self.act(m.FadeIn(frame),sec=1.10)
        self.caption("PÓRTICO RÍGIDO · BASES EMPOTRADAS")
        self.hold_until(3.0)
        force=load_arrow(0,.30)
        self.act(m.GrowArrow(force),sec=.75)
        self.caption("LA FUERZA DESPLAZA LOS NUDOS")
        self.add(ghost)
        self.hold_until(4.7)
        # Single material-point morph: load increases in the same animation.
        self.act(m.Transform(frame,drawing(1)),m.Transform(force,load_arrow(1,1.12)),sec=4.25)
        self.hold_until(9.5)
        # Isolate the genuine deformed left column, then enlarge while the
        # original frame fades. Other members are no longer visually competing.
        left=path(member_samples(LEFT,1),FRAME,9)
        self.act(m.FadeOut(frame),m.FadeOut(ghost),
                 m.FadeOut(feet),m.FadeOut(force),m.FadeIn(left),sec=.8)
        self.act(m.Transform(left,closeup()),sec=1.55)
        self.caption("LA COLUMNA PERMANECE CONTINUA")
        self.hold_until(13.2)
        # Tangent transported along the *deformed* FEM curve.
        tangent_1,pos=tangent_at(.13)
        tangent=ln(*tangent_1,POS,6)
        marker=m.Dot(point=V(pos),radius=.095,color=POS)
        self.act(m.Create(tangent),m.FadeIn(marker),sec=.75)
        self.hold_until(14.4)
        ta,p=tangent_at(.38)
        self.act(m.Transform(tangent,ln(*ta,POS,6)),
                 m.Transform(marker,m.Dot(point=V(p),radius=.095,color=POS)),sec=1.30)
        self.hold_until(16.1)
        tb,q=tangent_at(.83)
        self.act(m.Transform(tangent,ln(*tb,POS,6)),
                 m.Transform(marker,m.Dot(point=V(q),radius=.095,color=POS)),sec=1.35)
        self.hold_until(17.55)
        self.act(m.FadeOut(tangent),m.FadeOut(marker),sec=.30)
        zero_xy=inflection_point()
        dot=m.Dot(point=V(zero_xy),radius=.135,color=ZERO)
        ring=m.Circle(radius=.28,color=ZERO,stroke_width=3).move_to(V(zero_xy))
        self.act(m.FadeIn(dot),m.Create(ring),sec=.82)
        inflection_tag=label("INFLEXIÓN",1.23,.50,25,ZERO)
        arrowline=ln((.10,.33),(zero_xy[0]+.16,zero_xy[1]+.08),ZERO,2)
        self.act(m.FadeIn(inflection_tag),m.Create(arrowline),sec=.65)
        self.caption("CAMBIA LA CONCAVIDAD, NO HAY RÓTULA",ZERO)
        self.hold_until(20.9)
        self.act(m.FadeOut(dot),m.FadeOut(ring),m.FadeOut(inflection_tag),
                 m.FadeOut(arrowline),sec=.55)
        # Drop the exaggerated deflected curve but keep the original local axis.
        data=diagram_coords()
        axis=ln(data["base"],data["high"],INK,3.5)
        faint=closeup(1,AXIS,3)
        self.act(m.FadeIn(axis),m.Transform(left,faint),sec=1.1)
        self.caption("AHORA SOBRE EL EJE NO DEFORMADO")
        self.hold_until(23.15)
        # The actual signed affine M(x) is two lobes sharing M=0.
        neg=m.Polygon(V(data["base"]),V(data["negative_tip"]),V(data["mid"]),
                      color=NEG,fill_color=NEG,fill_opacity=.28,stroke_width=3)
        pos=m.Polygon(V(data["mid"]),V(data["positive_tip"]),V(data["high"]),
                      color=POS,fill_color=POS,fill_opacity=.28,stroke_width=3)
        self.act(m.FadeIn(neg),sec=1.16)
        self.act(m.FadeIn(pos),sec=1.16)
        sneg=ln((data["negative_tip"][0]-.60,-1.75),(data["negative_tip"][0]-.22,-1.75),NEG,6)
        spos=label("+",data["positive_tip"][0]+.36,1.45,43,POS)
        self.act(m.FadeIn(sneg),m.FadeIn(spos),sec=.55)
        marker=m.Dot(point=V(data["mid"]),radius=.105,color=ZERO)
        label_zero=label("M = 0",1.0,data["mid"][1]+.05,27,ZERO)
        self.act(m.FadeIn(marker),m.FadeIn(label_zero),sec=.7)
        self.caption("CURVATURA = 0  ⇔  MOMENTO = 0",INK)
        self.hold_until(32)
