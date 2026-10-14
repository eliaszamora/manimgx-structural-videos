"""Visual remake: real 3D reinforced concrete volume, no titles, no panels.
Narration clock remains exactly synchronized with interaction_pm.story.BEATS.
Reference: section mechanics in model.py. Positive P is compression.
The prism/bar geometry is schematic; only the 2D section quantities are to scale.
"""
import math
import os
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).parent))
from model import S, analyze, points
from story import BEATS, TOTAL_SECONDS
import manimgx as m

INK = "#061521"
TURQUOISE = "#58D6C9"
STEEL = "#E8BF72"
COMPRESS = "#FEA36E"
TENSION = "#79B3F5"
WHITE = "#E9F4F9"
MUTED = "#748E9F"
GRID = "#233849"
GOLD = "#F6DC81"
SOFT = "#23465A"
PINK = "#F183A4"

def txt(value, x=0, y=0, size=29, color=WHITE):
    return m.Text(value, font="Noto Sans", font_size=size, color=color).move_to([x,y,0])

def stroke(p, q, color, width=3):
    return m.Line(p, q, color=color, stroke_width=width)

def world(x,y,z):
    return np.array([x,y,z], dtype=float)

# Real 3D section: 400 x 400 mm mapped to 1.76 x 1.76 scene units.
X0, Y0 = -3.55, 0.0
SIDE = 2.12
HALF = SIDE/2
L = 4.30
def bar_xy():
    for sign in (1,-1):
        for xx in (-.65,-.22,.22,.65):
            yield xx, sign*(HALF - SIDE*S.dp/S.h)

def neutral_y(c):
    return HALF - SIDE*c/S.h

def block_depth(c):
    return max(.014, min(SIDE, SIDE*S.beta1*c/S.h))

def block3d(c):
    depth = block_depth(max(.02, c))
    return m.Prism(dimensions=[SIDE-.035,depth,L-.05],
              fill_color=COMPRESS,fill_opacity=.20,
              stroke_color=COMPRESS,stroke_width=.35
              ).move_to(world(X0,HALF-depth/2,0))

def axis_line(a,b,width=2,color=GRID):
    return stroke([a[0],a[1],0], [b[0],b[1],0],color,width)

# Fixed-frame right side, dimensions chosen for no text collisions at 1920x1080
SCX, SCY=2.05,-.32
SH=2.82
SX=2.77
def section_overlay(c):
    r=analyze(max(.02,c))
    grp=m.VGroup()
    grp.add(m.Rectangle(width=SX,height=SH,fill_color=SOFT,fill_opacity=.14,
                         stroke_color=TURQUOISE,stroke_width=2.2).move_to([SCX,SCY,0]))
    # Compression block occupies fraction a/h, measured from TOP.
    dep=min(SH,SH*r['a']/S.h)
    if dep>.02:
        grp.add(m.Rectangle(width=SX-.026,height=dep,fill_color=COMPRESS,
                         fill_opacity=.19,stroke_width=0).move_to([SCX,SCY+SH/2-dep/2,0]))
    yy=SCY+SH/2-SH*max(.0,min(1.,c/S.h))
    if 0<c<S.h:
        grp.add(stroke([SCX-SX/2-.26,yy,0],[SCX+SX/2+.26,yy,0],GOLD,2.5))
    for y in (S.dp,S.dt):
        color=COMPRESS if r["steel"][0 if y==S.dp else 1]["eps"]>=0 else TENSION
        for dx in (-.90,-.30,.30,.90):
            grp.add(m.Dot(point=[SCX+dx,SCY+SH/2-SH*y/S.h,0],radius=.079,color=color))
    return grp

# Actual strain distribution: compatible with c and eps_cu=0.003
ex0=4.60
def strain_overlay(c):
    c=max(.02,c)
    grp=m.VGroup()
    top=SCY+SH/2
    bottom=SCY-SH/2
    # ε linearly varies along depth; ε = 0 along vertical reference.
    grp.add(stroke([ex0,top+.11,0],[ex0,bottom-.1,0],MUTED,1.5))
    # Epsilon=0 axis, + ε towards right; scale kept legible while tension grows.
    eps_bottom=S.eps_cu*(c-S.h)/c
    scale=.69/max(.003,abs(eps_bottom))
    x_top=ex0+S.eps_cu*scale
    x_bot=ex0+eps_bottom*scale
    grp.add(stroke([x_top,top,0],[x_bot,bottom,0],GOLD,4))
    grp.add(stroke([ex0,top,0],[x_top,top,0],COMPRESS,2))
    if eps_bottom<0:
        grp.add(stroke([x_bot,bottom,0],[ex0,bottom,0],TENSION,2))
    grp.add(m.Dot(point=[x_top,top,0],radius=.075,color=COMPRESS))
    grp.add(m.Dot(point=[x_bot,bottom,0],radius=.075,color=TENSION if eps_bottom<0 else COMPRESS))
    return grp

CX0,CY0=.70,-2.03
GW,GH=5.70,4.15
P_MIN,P_MAX=-850,4800
M_MAX=390
def graph_xy(M,P):
    return [CX0+GW*max(-.04,min(1.12,M/M_MAX)),
            CY0+GH*(P-P_MIN)/(P_MAX-P_MIN), 0]
SAMPLES=points(450)
def curve(xkey,ykey,color):
    geom=m.VMobject(color=color,stroke_width=4.4)
    coords=[graph_xy(p[xkey],p[ykey]) for p in SAMPLES]
    geom.set_points_smoothly(coords)
    return geom

EQ=[
    "P    +    M",
    "M = P · e",
    "(Mₙ, Pₙ)",
    "400 × 400 mm    ·    8 Ø16",
    "ε(y) : distribución lineal",
    "ε = 0  →  eje neutro",
    "εₛ(y) = 0,003 (c − y) / c",
    "εᵧ = fᵧ / Eₛ = 0,0021",
    "a = β₁ c    ·    Cc = 0,85 f'c b a",
    "Fₛ = Aₛ (fₛ − 0,85 f'c)  si la barra ocupa el bloque",
    "Pₙ = Cc + ∑ Fₛ",
    "Mₙ = ∑ Fᵢ (h/2 − yᵢ)",
    "cᵦ ≈ 206 mm    ·    εₜ = εᵧ",
    "c  →  (Mₙ, Pₙ)",
    "P₀ = 0,85 f'c (Aɢ − Aₛₜ) + fᵧ Aₛₜ",
    "Pₙ = 0   ;   Mₙ ≠ 0",
    "Pₜ = −Aₛₜ fᵧ",
    "φ : 0,65 → 0,90",
    "(Mᵤ, Pᵤ)  frente a  (φMₙ, φPₙ)",
    "P–Δ    ·    Mₓ    ·    Mᵧ",
    "c  →  ε  →  σ  →  fuerzas  →  (Pₙ,Mₙ)"
]
C_TARGET=[330,220,175,330,205,210,160,130,260,260,180,170,
          S.balanced_c,82,1800,102,8,132,185,220,S.balanced_c]
# The small changes are deliberate: camera visualizes a REAL cross-sectional mechanism,
# rather than jumping from one title-slide to another.
PHI=[65,62,70,46,34,28,30,42,63,52,57,60,32,48,67,64,59,57,46,68,63]
THETA=[-43,-37,-60,-74,-78,-89,-83,-61,-49,-55,-67,-52,-86,-47,-41,-65,-81,-58,-70,-29,-49]

class FlexocompresionTresDimensiones(m.ThreeDScene):
    def construct(self):
        self.camera.background_color = INK
        self.set_camera_orientation(phi=65*m.DEGREES,theta=-43*m.DEGREES)
        self.add(m.SunLight(4*m.UP+3*m.OUT),
                 m.AmbientLight(intensity=.55))
        c=m.ValueTracker(330.)
        concrete=m.Prism(dimensions=[SIDE,SIDE,L],
                      fill_color="#4DA7B6",fill_opacity=.12,
                      stroke_color=TURQUOISE,stroke_width=1.5
                      ).move_to(world(X0,Y0,0))
        self.play(m.FadeIn(concrete),run_time=1.0)
        steel=m.Group()
        for dx,dy in bar_xy():
            rod=m.Cylinder(radius=.057,height=L-.05,
                           direction=m.Z_AXIS,
                           resolution=(12,6),fill_color=STEEL,
                           fill_opacity=1,stroke_width=0,checkerboard_colors=False)
            rod.set_color(STEEL)
            rod.move_to(world(X0+dx,dy,0))
            steel.add(rod)
        self.play(m.FadeIn(steel),run_time=1.1)
        ties=m.Group()
        for z in np.linspace(-L/2+.22,L/2-.22,10):
            rr=HALF-.12
            corners=[world(X0+x,y,z) for x,y in
                [(-rr,-rr),(rr,-rr),(rr,rr),(-rr,rr)]]
            tie=m.Polygon(*corners,color=TURQUOISE,stroke_width=1.6,
                          fill_opacity=0)
            ties.add(tie)
        self.play(m.FadeIn(ties),run_time=.9)
        concrete_group=m.VGroup(concrete,steel,ties)
        compress_zone=m.always_redraw(lambda:block3d(c.get_value()))
        self.add(compress_zone)
        # A 3D slicing surface extends through the column longitudinally.
        neutral=m.always_redraw(lambda:
            m.Prism(dimensions=[SIDE+.19,.019,L+.17],fill_color=GOLD,
                    fill_opacity=.18,stroke_color=GOLD,stroke_width=.5
                    ).move_to(world(X0, neutral_y(c.get_value()),0))
        )
        self.add(neutral)
        # Actual external axial load along column axis (Z).
        load=m.Arrow3D(world(X0,0,L/2+1.05),world(X0,0,L/2+.07),
                       color=COMPRESS,thickness=.055)
        self.add(load)

        sec=m.always_redraw(lambda: section_overlay(c.get_value()))
        strain=m.always_redraw(lambda: strain_overlay(c.get_value()))
        micro=m.VGroup(
           txt("c",.50,1.6,27,GOLD),
           txt("ε",5.65,1.55,27,GOLD),
        )
        formula=txt(EQ[0],2.8,-2.73,35,WHITE)
        self.add_fixed_in_frame_mobjects(sec,strain,micro,formula)
        self.add_fixed_in_frame_mobjects(
           txt("0,003",5.35,2.0,20,COMPRESS))
        # The graph will be swapped in AFTER the strain/mechanics has been understood.
        gx=m.VGroup()
        for P in (0,1000,2000,3000,4000):
            yy=graph_xy(0,P)[1]
            gx.add(stroke([CX0,yy,0],[CX0+GW,yy,0],GRID,1))
        for mm in (0,100,200,300):
            xx=graph_xy(mm,0)[0]
            gx.add(stroke([xx,CY0,0],[xx,CY0+GH,0],GRID,1))
        gx.add(stroke([CX0,CY0-.12,0],[CX0,CY0+GH+.10,0],MUTED,2))
        gx.add(stroke([CX0,graph_xy(0,0)[1],0],[CX0+GW+.17,graph_xy(0,0)[1],0],MUTED,2))
        gx.add(curve("Mn","Pn",TURQUOISE))
        gx.add(curve("phiMn","phiPn",COMPRESS))
        gx.add(txt("P",CX0-.32,CY0+GH+.25,29,MUTED))
        gx.add(txt("M",CX0+GW+.26,CY0-.23,29,MUTED))
        graph_dot_visibility=m.ValueTracker(0.0)
        point=m.always_redraw(lambda:m.Dot(point=graph_xy(analyze(max(.02,c.get_value()))["Mn"],
                              analyze(max(.02,c.get_value()))["Pn"]),radius=.115,color=GOLD).set_opacity(graph_dot_visibility.get_value()))
        gx.add(point)
        # initial graph invisible, but registered as screen-fixed.
        self.add_fixed_in_frame_mobjects(gx)
        gx.set_opacity(0)
        preview=os.environ.get("PM_3D_PREVIEW")=="1"
        lessons=BEATS[:1] if preview else BEATS
        for i,beat in enumerate(lessons):
            # Voice is aligned by chapter onset. No section titles or HUD.
            # Equations appear only where their physical referent is visible.
            spent=3.0 if i==0 else 0.0
            if i:
                eq=txt(EQ[i],2.8,-2.73,
                       28 if len(EQ[i])>41 else 33,WHITE)
                self.play(m.Transform(formula,eq),run_time=1.4)
                spent+=1.4
            if i==13:
                graph_dot_visibility.set_value(1.0)
                self.play(m.FadeOut(sec),m.FadeOut(strain),
                    m.FadeOut(micro),m.FadeIn(gx),run_time=2.3)
                spent+=2.3
            if i==20:
                # Return to physical space for summary, not a closing title-card.
                self.play(m.FadeOut(gx),m.FadeIn(sec),m.FadeIn(strain),
                          m.FadeIn(micro),run_time=2)
                spent+=2
            self.move_camera(phi=PHI[i]*m.DEGREES,
                            theta=THETA[i]*m.DEGREES,run_time=4.8)
            spent+=4.8
            target=float(C_TARGET[i])
            # From the load to the strain, the same tracker drives all representations.
            self.play(c.animate.set_value(target),run_time=11.0)
            spent+=11
            self.move_camera(phi=max(22,PHI[i]-10)*m.DEGREES,
                             theta=(THETA[i]+15)*m.DEGREES,
                             run_time=4.5)
            spent+=4.5
            detour=max(7,min(500,target*(.65 if i%2 else 1.33)))
            self.play(c.animate.set_value(detour),run_time=9)
            spent+=9
            # Animate continuously through the remaining voice slot, with the
            # primary physical state ending at the intended c of the chapter.
            remain=beat["duration"]-spent
            if remain<2:
                raise ValueError("Negative narration time: chapter "+str(i+1))
            self.play(c.animate.set_value(target),
                      run_time=remain)
        if not preview:
            assert len(lessons)==21 and len(EQ)==21
