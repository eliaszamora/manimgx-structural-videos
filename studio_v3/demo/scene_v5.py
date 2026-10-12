"""Structural Studio V5. Clean geometric presentation, familiar fixed supports.

- Centered portal with no explanatory sidebar or dividing rail.
- Load arrow starts at right top joint and follows joint throughout quasi-static loading.
- Displacement is a continuous interpolation of FEM material point positions.
- M and V attach to the UNDEFORMED left-column centerline, with local-axis signs.
- Positive local M plots to the right of the upward-oriented column; negative to left.
"""
import sys, math
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parent))
import manimgx as m
from portal_solver import solve,L,H
from structural_viz.model import member_from_solver
from story import SECONDS_PER_BEAT

R=solve("lateral")
MEM=[member_from_solver(e,f"e{i}") for i,e in enumerate(R["elements"])]
COL=MEM[0]
AMP=155.0
OX,OY=-4.90,-3.35
SC=1.75
C=dict(bg="#0A131F",ink="#EDF3FA",muted="#9AABB9",neutral="#8999A7",
       original="#546576",deform="#35D4BF",force="#FFAE7B",
       moment_neg="#FF8679",moment_pos="#FFCC83",cut="#83B8FF",pin="#D5B2FF")

def w(p):return (OX+SC*float(p[0]),OY+SC*float(p[1]))
def v(p):return [float(p[0]),float(p[1]),0]
def line(a,b,color=None,width=3):
    return m.Line(v(a),v(b),color=color or C["neutral"],stroke_width=width)
def txt(t,x,y,size=26,color=None):
    return m.Text(t,font="DejaVu Sans",font_size=size,color=color or C["ink"]).move_to([x,y,0])
def curve(points,color,width):
    shape=m.VMobject(color=color,stroke_width=width)
    shape.set_points_smoothly([v(p) for p in points])
    return shape
def geom(alpha=0.0,color=None,width=8):
    """Continuously interpolate every sample, not trace a pre-deformed contour."""
    pieces=[]
    for member in MEM:
        pts=[w((s.x+alpha*AMP*s.displacement_x,
                s.y+alpha*AMP*s.displacement_y)) for s in member.samples]
        pieces.append(curve(pts,color or C["deform"],width))
    return m.VGroup(*pieces)
def joint(idx,alpha=0):
    x,y=R["nodes"][idx]
    dx,dy=R["u"][idx][:2]
    return w((x+AMP*alpha*dx,y+AMP*alpha*dy))
def fixed_foot(p):
    """Conventional fixed base: footing line and diagonal foundation hatch BELOW column."""
    x,y=p
    baseline=line((x-.62,y-.025),(x+.62,y-.025),C["ink"],5)
    hatch=[line((x-.61+i*.22,y-.04),(x-.80+i*.22,y-.36),C["neutral"],2)
           for i in range(6)]
    return m.VGroup(baseline,*hatch)
def force_at_joint(alpha):
    """Force arrow TAIL is exactly at top right node (not offset above it)."""
    x,y=joint(3,alpha)
    return m.Arrow(v((x,y)),v((x+1.03,y)),buff=0,
                   color=C["force"],stroke_width=7)
def tangent_at_top():
    x,y=joint(1,1)
    theta=AMP*float(R["u"][1][2])
    dx,dy=math.sin(theta),math.cos(theta)
    return line((x-.43*dx,y-.43*dy),(x+.43*dx,y+.43*dy),C["moment_pos"],5)
def diagram(kind):
    """Filled diagram against ORIGINAL left-column axis; no displaced reference."""
    x,y=w((0,0));Y=w((0,H))[1]
    values=[getattr(s,kind) for s in COL.samples]
    norm=max(abs(q) for q in values)
    scale=1.15 if kind=="M" else .85
    offset=lambda q:scale*q/norm
    if kind=="M":
        z=COL.zeros("M")[0];zy=y+(Y-y)*z
        xb=x+offset(values[0]); xt=x+offset(values[-1])
        negative=m.Polygon(v((x,y)),v((xb,y)),v((x,zy)),
                    color=C["moment_neg"],fill_color=C["moment_neg"],
                    fill_opacity=.20,stroke_width=3)
        positive=m.Polygon(v((x,zy)),v((xt,Y)),v((x,Y)),
                    color=C["moment_pos"],fill_color=C["moment_pos"],
                    fill_opacity=.20,stroke_width=3)
        return m.VGroup(negative,positive,
             line((xb,y),(x,zy),C["moment_neg"],5),
             line((x,zy),(xt,Y),C["moment_pos"],5),
             m.Dot(point=v((x,zy)),radius=.10,color=C["pin"]))
    xx=x+offset(values[0])
    return m.VGroup(m.Polygon(v((x,y)),v((xx,y)),v((xx,Y)),v((x,Y)),
             color=C["cut"],fill_color=C["cut"],fill_opacity=.19,stroke_width=3),
             line((xx,y),(xx,Y),C["cut"],5))

class V5CleanPortal(m.Scene):
    def play_t(self,*actions,seconds=1):
        self.play(*actions,run_time=seconds)
        self._chapter_elapsed_v5+=seconds
    def hold(self,seconds):
        if seconds>0:
            self.wait(seconds)
            self._chapter_elapsed_v5+=seconds
    def until(self,t):
        self.hold(max(0,t-self._chapter_elapsed_v5))
    def mark(self,text,color=None):
        """Replace a concise micro-annotation outside the structural geometry."""
        new=txt(text,0,-2.74,26,color or C["muted"])
        if getattr(self,"annotation",None) is not None:
            # Never crossfade two full technical sentences; they become unreadable.
            self.play_t(m.FadeOut(self.annotation),seconds=.18)
            self.play_t(m.FadeIn(new),seconds=.22)
        else:self.play_t(m.FadeIn(new),seconds=.4)
        self.annotation=new
    def chapter(self,n,title):
        self._chapter_elapsed_v5=0
        heading=txt(title,-3.23,3.39,29,C["ink"])
        number=txt(f"{n+1:02d} / 06",5.85,3.38,20,C["muted"])
        if n==0:
            self.heading=heading;self.number=number
            self.play_t(m.FadeIn(heading),m.FadeIn(number),seconds=.55)
        else:
            self.play_t(m.FadeOut(self.heading),m.FadeOut(self.number),seconds=.23)
            self.heading=heading;self.number=number
            self.play_t(m.FadeIn(heading),m.FadeIn(number),seconds=.38)
    def end_chapter(self):
        if self._chapter_elapsed_v5>SECONDS_PER_BEAT+.03:
            raise RuntimeError(f"chapter exceeded 14s by {self._chapter_elapsed_v5-14:.2f}s")
        self.until(SECONDS_PER_BEAT)

    def construct(self):
        self.camera.background_color=C["bg"]
        ref=geom(0,C["original"],3)
        frame=geom(0,C["deform"],8)
        feet=m.VGroup(fixed_foot(joint(0)),fixed_foot(joint(4)))
        # Fixed supports remain attached to the ground; no artificial blocks.
        self.chapter(0,"PÓRTICO RÍGIDO")
        self.play_t(m.FadeIn(feet),m.FadeIn(frame),seconds=1.65)
        self.mark("Un piso · una crujía · bases empotradas")
        self.until(5.65)
        load=force_at_joint(0)
        f_label=txt("H = 24 kN",5.40,2.93,23,C["force"])
        self.play_t(m.GrowArrow(load),m.FadeIn(f_label),seconds=1.05)
        self.until(9.9)
        self.mark("La fuerza actúa sobre el nudo superior derecho",C["force"])
        self.end_chapter()

        self.chapter(1,"DESPLAZAMIENTO LATERAL")
        self.mark("Carga cuasiestática: 0 → 100 %")
        self.add(ref)
        self.until(5.45)
        final_arrow=force_at_joint(1)
        self.play_t(m.Transform(frame,geom(1,C["deform"],8)),
                    m.Transform(load,final_arrow),seconds=4.15)
        self.until(9.95)
        self.mark(f"Desplazamiento superior ≈ 2,93 mm · escala ×{int(AMP)}",C["deform"])
        self.end_chapter()

        self.chapter(2,"GIROS Y COMPATIBILIDAD")
        self.mark("La base NO se traslada ni gira",C["moment_pos"])
        ground_tangent=line((joint(0)[0],joint(0)[1]-.44),
                            (joint(0)[0],joint(0)[1]+.44),C["moment_pos"],5)
        self.until(3.15)
        self.play_t(m.Create(ground_tangent),seconds=1.0)
        self.until(5.45)
        self.mark("El nudo superior gira junto con la viga",C["pin"])
        upper_tangent=tangent_at_top()
        self.play_t(m.Create(upper_tangent),seconds=1.4)
        self.until(10.05)
        self.mark("Diferentes pendientes → curvatura",C["deform"])
        self.end_chapter()

        self.chapter(3,"MOMENTO FLECTOR")
        self.play_t(m.FadeOut(ground_tangent),m.FadeOut(upper_tangent),
                    m.FadeOut(load),m.FadeOut(f_label),seconds=.65)
        self.play_t(m.Transform(frame,geom(0,C["deform"],7)),
                    m.FadeOut(ref),seconds=1.55)
        self.mark("M sobre la columna ORIGINAL · negativo a la izquierda",C["moment_neg"])
        self.until(5.2)
        M=diagram("M")
        self.play_t(m.Create(M),seconds=2.05)
        self.until(9.8)
        self.mark("Base −23,7 · coronación +17,0 kN·m",C["moment_pos"])
        self.end_chapter()

        self.chapter(4,"CORTANTE EN LA COLUMNA")
        self.play_t(m.FadeOut(M),seconds=.55)
        self.mark("El cortante local mantiene signo y magnitud",C["cut"])
        self.until(5.15)
        V=diagram("V")
        self.play_t(m.Create(V),seconds=1.85)
        self.until(9.85)
        self.mark("V local = +11,99 kN",C["cut"])
        self.end_chapter()

        self.chapter(5,"DEFORMADA Y ESFUERZOS")
        self.play_t(m.FadeOut(V),seconds=.6)
        self.mark("Primero restricciones, luego compatibilidad")
        self.until(5.45)
        self.add(geom(0,C["original"],3))
        self.play_t(m.Transform(frame,geom(1,C["deform"],8)),seconds=3.0)
        self.until(9.9)
        self.mark("Y finalmente: curvatura → momento → cortante",C["deform"])
        self.end_chapter()
