"""Cinematic proof-of-concept: cause -> mechanism -> interaction.
49 seconds synchronized with first Kokoro narration beat; no chapter cards.
ManimGX 3D + rigorous section geometry from model.py.
"""
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
from model import S, analyze, points
import manimgx as m

BG="#0B101C"; CONCRETE="#50D7D0"; STEEL="#F9C35D"
COMP="#FF9568"; TENSION="#77ABFF"; WHITE="#EDF2FA"
MUTED="#8DA2BC"; ZERO="#F7DC79"
SIDE=3.65; L=5.85; MID=np.array([-2.27,-.15,-.20])
R=.095

def tx(value, size=27, color=WHITE):
    return m.Text(value, font="Noto Sans", font_size=size, color=color)

def line(p,q,col,width=2):
    return m.Line([p[0],p[1],0],[q[0],q[1],0],color=col,stroke_width=width)

def point3(x,y,z):
    return MID+np.array([x,y,z])

def rectangle_section(c):
    """Constant scale mapping of c and Whitney a. One physical section."""
    r=analyze(c)
    cx,cy=3.24,.12
    sz=3.14
    half=sz/2
    g=m.VGroup()
    g.add(m.Rectangle(width=sz,height=sz,stroke_color=CONCRETE,stroke_width=3,
                      fill_color="#21424D",fill_opacity=.22).move_to([cx,cy,0]))
    # a <= h; block lies top, never centered around neutral axis.
    block_h=sz*r["a"]/S.h
    if block_h>.02:
        g.add(m.Rectangle(width=sz-.03,height=block_h,stroke_width=0,
                           fill_color=COMP,fill_opacity=.26
                          ).move_to([cx,cy+half-block_h/2,0]))
    nt_y=cy+half-sz*c/S.h
    if nt_y>cy-half and nt_y<cy+half:
        g.add(line([cx-half-.16,nt_y],[cx+half+.16,nt_y],ZERO,2))
    for i,y in enumerate((S.dp,S.dt)):
        ypos=cy+half-sz*y/S.h
        for x in np.linspace(cx-half+sz*S.dp/S.b,cx+half-sz*S.dp/S.b,4):
            col=COMP if r["steel"][i]["eps"]>0 else TENSION
            g.add(m.Dot(point=[x,ypos,0],radius=.083,color=col))
    return g

def strain_graph(c):
    """ε(y) = 0.003(1 - y/c), x-positive=compression, scales physically."""
    cx=5.13; y0=1.53; y1=-1.29
    # Fixed epsilon scaling independent of c (unlike previous version).
    per=.28/.003
    es_bottom=.003*(c-S.h)/c
    top_x=cx+.003*per
    bot_x=cx+max(-.006,min(.006,es_bottom))*per
    grp=m.VGroup()
    grp.add(line([cx,y0+.12],[cx,y1-.12],MUTED,1.4))
    grp.add(line([top_x,y0],[bot_x,y1],ZERO,3.6))
    grp.add(m.Dot(point=[top_x,y0,0],radius=.07,color=COMP))
    grp.add(m.Dot(point=[bot_x,y1,0],radius=.07,
                color=TENSION if es_bottom<0 else COMP))
    return grp

def dot_on_chart(c):
    rr=analyze(c)
    xp=-4.55+9.1*rr["Mn"]/350
    yp=-2.25+4.5*(rr["Pn"]+720)/(4600+720)
    return m.Dot(point=[xp,yp,0],radius=.11,color=ZERO)

def chart():
    g=m.VGroup()
    xmax=4.60; xmin=-4.55; ymin=-2.25; ymax=2.40
    g.add(line([xmin,ymin],[xmin,ymax],MUTED,2))
    g.add(line([xmin,-1.641],[xmax,-1.641],MUTED,2))
    # Curves are obtained from engineering model, not manually drawn Béziers.
    sample=[p for p in points(350) if p["Mn"]>0 and p["Mn"]<360]
    curve=m.VMobject(color=CONCRETE,stroke_width=5)
    coords=[]
    for rr in sample:
        xp=xmin+9.1*rr["Mn"]/350
        yp=-2.25+4.5*(rr["Pn"]+720)/(4600+720)
        coords.append([xp,yp,0])
    curve.set_points_smoothly(coords)
    g.add(curve)
    g.add(tx("P",23,MUTED).move_to([-4.78,2.63,0]))
    g.add(tx("M",23,MUTED).move_to([4.82,-1.77,0]))
    return g

class PorQuePM3D(m.ThreeDScene):
    def construct(self):
        self.camera.background_color=BG
        self.set_camera_orientation(phi=65*m.DEGREES,theta=-48*m.DEGREES)
        self.add(m.SunLight(2*m.UP+3*m.OUT),m.AmbientLight(intensity=.70))
        volume=m.Prism(dimensions=[SIDE,SIDE,L],fill_color=CONCRETE,
                  fill_opacity=.16,stroke_color=CONCRETE,stroke_width=1.7
                 ).move_to(MID)
        bars=m.Group()
        a=SIDE*(.5-S.dp/S.h)
        for yy in (-a,a):
            for xx in np.linspace(-a,a,4):
                rod=m.Cylinder(radius=R,height=L-.12,direction=m.Z_AXIS,
                            resolution=(12,6),fill_color=STEEL,fill_opacity=1,
                            stroke_width=0,checkerboard_colors=False)
                rod.move_to(point3(xx,yy,0))
                bars.add(rod)
        ties=m.Group()
        for zz in np.linspace(-L/2+.25,L/2-.25,9):
            h=SIDE*.5-.16
            pts=[point3(x,y,zz) for x,y in
                 [(-h,-h),(h,-h),(h,h),(-h,h)]]
            ties.add(m.Polygon(*pts,color=CONCRETE,stroke_width=2.3,fill_opacity=0))
        # The same c drives the equivalent compression block and the section.
        c=m.ValueTracker(290.)
        block=m.always_redraw(lambda:
             m.Prism(dimensions=[SIDE-.08,max(.025,SIDE*analyze(c.get_value())["a"]/S.h),L-.08],
                  fill_color=COMP,fill_opacity=.22,stroke_color=COMP,stroke_width=.3
             ).move_to(point3(0,SIDE/2-max(.025,SIDE*analyze(c.get_value())["a"]/S.h)/2,0)))
        neutral=m.always_redraw(lambda:
             m.Prism(dimensions=[SIDE+.13,.015,L+.13],
                      fill_color=ZERO,fill_opacity=.23,stroke_color=ZERO,
                      stroke_width=.8
                     ).move_to(point3(0,SIDE/2-SIDE*c.get_value()/S.h,0)))
        # Load and geometric eccentricity act in the SAME bending plane (y).
        load=m.Arrow3D(point3(0,0,L/2+1.28),point3(0,0,L/2+.1),
                       color=COMP,thickness=.075)
        center=m.Line(point3(0,0,L/2+1.28),
                      point3(0,0,L/2+.05),stroke_width=1,color=MUTED)
        section=m.always_redraw(lambda:rectangle_section(c.get_value()))
        eps=m.always_redraw(lambda:strain_graph(c.get_value()))
        trace=chart()
        dot=m.always_redraw(lambda:dot_on_chart(c.get_value()))
        self.play(m.FadeIn(volume),run_time=2.2)
        self.play(m.FadeIn(bars),run_time=3.6)
        self.play(m.FadeIn(ties),run_time=2.2)          # t=8
        self.move_camera(phi=60*m.DEGREES,theta=-37*m.DEGREES,run_time=3)
        self.play(m.FadeIn(load),run_time=3)          # t=14
        self.play(load.animate.shift(.64*m.UP),run_time=4.5) # eccentric along global Y
        self.move_camera(phi=64*m.DEGREES,theta=-54*m.DEGREES,run_time=3.5) # t=22
        self.play(m.FadeIn(block),m.FadeIn(neutral),run_time=3.0)
        self.add_fixed_in_frame_mobjects(section,eps)
        self.play(m.FadeIn(section),m.FadeIn(eps),run_time=4.0) # t=29
        self.play(c.animate.set_value(175.),run_time=6.5) # t=35.5
        self.play(m.FadeOut(section),m.FadeOut(eps),
                  m.FadeOut(volume),m.FadeOut(bars),m.FadeOut(ties),
                  m.FadeOut(load),run_time=1.8)
        self.remove(block,neutral)
        self.add_fixed_in_frame_mobjects(trace,dot)
        self.play(m.Create(trace),m.FadeIn(dot),run_time=4.2) # t=41.5
        self.play(c.animate.set_value(265.),run_time=7.5) # t=49
