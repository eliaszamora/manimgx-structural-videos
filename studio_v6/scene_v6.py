"""Structural Studio V6 — ALL members, all signs, mechanical story."""
import sys,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE.parent/"studio_v3"/"demo"),str(HERE.parent/"studio_v3")]
import manimgx as m
from portal_solver import solve,L,H
from structural_viz.model import member_from_solver
from story_v6 import SECONDS_PER_BEAT
from engineering_v6 import members,check
R=solve("lateral")
ELEMENTS=[member_from_solver(e,name) for e,name in zip(R["elements"],("C1","V1","V2","C2"))]
VALUES=members()
check()
S=1.47; OX=-4.30; OY=-2.34; AMP=155.0
P=dict(bg="#091522",ink="#EDF5FD",muted="#B6C8D8",axis="#637589",
       frame="#49DAC1",force="#FFA77D",plus="#F9C77B",
       minus="#F57F80",shear_plus="#80B6F8",shear_minus="#C5A2FA",
       tension="#4FD7C6",compression="#FA9F9A",zero="#D5B3FF")
def ww(x,y):return(OX+S*x,OY+S*y)
def vv(p):return [float(p[0]),float(p[1]),0]
def line(a,b,col,width=3):return m.Line(vv(a),vv(b),color=col,stroke_width=width)
def text(s,x,y,size=23,col=None):
    return m.Text(str(s),font="DejaVu Sans",font_size=size,color=col or P["ink"]).move_to([x,y,0])
def path(points,col,width):
    out=m.VMobject(color=col,stroke_width=width)
    out.set_points_smoothly([vv(q) for q in points]);return out
def beam(a=0,col=None,width=7):
    return m.VGroup(*[path([ww(p.x+AMP*a*p.displacement_x,p.y+AMP*a*p.displacement_y) for p in e.samples],
            col or P["frame"],width) for e in ELEMENTS])
def node(i,a=0):
    xy=R["nodes"][i];u=R["u"][i]
    return ww(xy[0]+AMP*a*u[0],xy[1]+AMP*a*u[1])
def fix(p):
    x,y=p
    # Mechanical engineering classical fixed support (groundline/hatch).
    return m.VGroup(line((x-.46,y-.015),(x+.46,y-.015),P["ink"],5),
        *[line((x-.45+i*.16,y-.04),(x-.59+i*.16,y-.30),P["axis"],2) for i in range(6)])
def load(a):
    p=node(3,a)
    return m.Arrow(vv(p),vv((p[0]+.97,p[1])),buff=0,
                   color=P["force"],stroke_width=7)
def normal(e):
    dx=e.end[0]-e.start[0];dy=e.end[1]-e.start[1]
    l=math.hypot(dx,dy)
    return (dy/l,-dx/l)
def plot_all(kind):
    """Signed filled polygons on undeformed axes; identical normalization on 4 parts."""
    data=[[ (s.M if kind=="M" else s.V if kind=="V" else val["N"])
             for s in e.samples] for e,val in zip(ELEMENTS,VALUES)]
    reference=max(abs(v) for row in data for v in row)
    assert reference>1e-8
    shift={"M":.66,"V":.53,"N":.50}[kind]
    group=m.VGroup()
    for ei,(e,row) in enumerate(zip(ELEMENTS,data)):
        q0,q1=row[0],row[-1]
        nx,ny=normal(e)
        # Always use original/undeformed member coordinates. Split at true sign changes.
        cuts=[(0.,q0)]
        if q0*q1<0:
            t=-q0/(q1-q0)
            cuts.append((t,0.))
        cuts.append((1.,q1))
        for (ta,va),(tb,vb) in zip(cuts[:-1],cuts[1:]):
            def p(t):
                x=e.start[0]*(1-t)+e.end[0]*t
                y=e.start[1]*(1-t)+e.end[1]*t
                return ww(x,y)
            a=p(ta);b=p(tb)
            fac=lambda z:shift*z/reference
            aa=(a[0]+nx*fac(va),a[1]+ny*fac(va))
            bb=(b[0]+nx*fac(vb),b[1]+ny*fac(vb))
            avg=(va+vb)/2
            positive=avg>=0
            color=(P["plus"] if kind=="M" else P["shear_plus"] if kind=="V" else P["tension"]) if positive else (P["minus"] if kind=="M" else P["shear_minus"] if kind=="V" else P["compression"])
            group.add(m.Polygon(vv(a),vv(aa),vv(bb),vv(b),
                    color=color,fill_color=color,fill_opacity=.23,stroke_width=2))
            group.add(line(aa,bb,color,4))
            if abs(va)+abs(vb)>reference*.10 and tb-ta>.13:
                t=(ta+tb)/2
                base=p(t)
                centroid=(base[0]+nx*.52*(fac((va+vb)/2)),
                          base[1]+ny*.52*(fac((va+vb)/2)))
                sym=text("+" if positive else "−",centroid[0],centroid[1],24,color)
                group.add(sym)
        if kind=="M":
            for t in e.zeros("M"):
                if 0<t<1:
                    x=e.start[0]*(1-t)+e.end[0]*t
                    y=e.start[1]*(1-t)+e.end[1]*t
                    group.add(m.Dot(point=vv(ww(x,y)),radius=.09,color=P["zero"]))
    return group
def fbd():
    """Global force equilibrium: only horizontal support reactions shown."""
    parts=m.VGroup()
    for nid in (0,4):
        x,y=node(nid)
        rx=R["reaction"][nid][0]
        if abs(rx)>.005:
            dx=(-.85 if rx<0 else .85)
            parts.add(m.Arrow(vv((x,y+.22)),vv((x+dx,y+.22)),buff=0,
                              color=P["shear_plus"],stroke_width=6))
    return parts
class FullFrameV6(m.Scene):
    def animate(self,*a,duration=1):
        self.play(*a,run_time=duration);self.elapsed+=duration
    def pause_to(self,t):
        if t>self.elapsed:self.wait(t-self.elapsed);self.elapsed=t
    def intro(self,chapter,title):
        self.elapsed=0
        name=text(title,0,3.70,26)
        counter=text(f"{chapter+1:02d}/08",6.17,3.69,17,P["muted"])
        if chapter==0:
            self.head=name;self.counter=counter
            self.animate(m.FadeIn(name),m.FadeIn(counter),duration=.48)
        else:
            self.animate(m.FadeOut(self.head),m.FadeOut(self.counter),duration=.20)
            self.head=name;self.counter=counter
            self.animate(m.FadeIn(name),m.FadeIn(counter),duration=.28)
    def note(self,s,color=None):
        new=text(s,0,-3.63,23,color or P["muted"])
        if getattr(self,"label",None) is not None:
            self.animate(m.FadeOut(self.label),duration=.18)
            self.animate(m.FadeIn(new),duration=.22)
        else:self.animate(m.FadeIn(new),duration=.40)
        self.label=new
    def finish(self):
        if self.elapsed>SECONDS_PER_BEAT+.03:
            raise ValueError(f"Overrun {self.elapsed:.3f} at chapter {self.head}")
        self.pause_to(SECONDS_PER_BEAT)
    def construct(self):
        self.camera.background_color=P["bg"]
        feet=m.VGroup(fix(node(0)),fix(node(4)))
        original=beam(0,P["axis"],3)
        frame=beam(0,P["frame"],7)
        headings=m.VGroup(text("C1",-5.03,.48,19,P["muted"]),
          text("C2",4.68,.48,19,P["muted"]),
          text("V1",-2.30,2.96,18,P["muted"]),
          text("V2",1.90,2.96,18,P["muted"]))
        self.intro(0,"PÓRTICO RÍGIDO · ELEMENTOS")
        self.animate(m.FadeIn(feet),m.FadeIn(frame),m.FadeIn(headings),duration=1.7)
        self.note("2 columnas · 1 viga (2 tramos de cálculo)")
        self.pause_to(5.0)
        force=load(0)
        self.animate(m.GrowArrow(force),duration=1.05)
        self.note("H = 24 kN → sobre el nudo superior derecho")
        self.finish()

        self.intro(1,"CARGA Y DEFORMADA")
        self.note("Aplicación cuasiestática progresiva")
        self.add(original)
        self.pause_to(4.65)
        for part in (.25,.50,.75,1.):
            self.animate(m.Transform(frame,beam(part,P["frame"],7)),
                         m.Transform(force,load(part)),duration=1.13)
        self.pause_to(9.35)
        self.note("λ = 100 % · deformada amplificada ×155")
        self.finish()

        self.intro(2,"GIROS Y CURVATURA")
        self.note("Bases: desplazamiento y giro nulos")
        x,y=node(0)
        t0=line((x,y-.42),(x,y+.42),P["plus"],4)
        self.pause_to(3.50);self.animate(m.Create(t0),duration=.9)
        self.pause_to(5.05)
        x,y=node(1,1)
        angle=AMP*float(R["u"][1][2])
        tangent=line((x-.40*math.sin(angle),y-.40*math.cos(angle)),
                     (x+.40*math.sin(angle),y+.40*math.cos(angle)),
                     P["plus"],4)
        self.animate(m.Create(tangent),duration=1.)
        self.note("El giro superior es compatible con la viga")
        self.pause_to(9.2)
        nodes=m.VGroup(*[m.Dot(point=vv(node(i,1)),radius=.10,color=P["zero"]) for i in (1,3)])
        self.animate(m.FadeIn(nodes),duration=.6)
        self.note("La curvatura cambia de signo en las columnas")
        self.finish()

        self.intro(3,"EQUILIBRIO GLOBAL")
        self.animate(m.FadeOut(t0),m.FadeOut(tangent),m.FadeOut(nodes),
                     m.Transform(frame,beam(0,P["frame"],7)),
                     m.Transform(force,load(0)),duration=1.25)
        self.animate(m.FadeOut(original),duration=.35)
        reactions=fbd()
        self.animate(m.FadeIn(reactions),duration=.75)
        self.note("Reacciones Rₐx y Rᵦx opuestas a H")
        self.pause_to(8.95)
        self.note("ΣFₓ = 0 : Rₐx + Rᵦx + 24 = 0")
        self.finish()

        self.intro(4,"M: TODOS LOS ELEMENTOS")
        self.animate(m.FadeOut(reactions),m.FadeOut(force),duration=.55)
        M=plot_all("M")
        self.animate(m.FadeIn(M),duration=1.65)
        self.note("M: + dorado (normal horaria) · − coral")
        self.pause_to(9.3)
        self.note("C1, V1, V2 y C2 · puntos violeta: M = 0")
        self.finish()

        self.intro(5,"V: TODOS LOS ELEMENTOS")
        self.animate(m.FadeOut(M),duration=.48)
        V=plot_all("V")
        self.animate(m.FadeIn(V),duration=1.65)
        self.note("Cortante + azul · − violeta · ejes locales")
        self.pause_to(9.3)
        self.note("Sin cargas distribuidas: V constante por tramo")
        self.finish()

        self.intro(6,"N: TRACCIÓN Y COMPRESIÓN")
        self.animate(m.FadeOut(V),duration=.48)
        N=plot_all("N")
        self.animate(m.FadeIn(N),duration=1.65)
        self.note("N positivo = tracción · negativo = compresión")
        self.pause_to(9.3)
        self.note("También en axial: cuatro tramos y cuatro signos")
        self.finish()

        self.intro(7,"TRES DIAGRAMAS · UN SOLO PÓRTICO")
        self.animate(m.FadeOut(N),duration=.45)
        self.note("M, V y N pertenecen a los mismos cuatro tramos")
        self.pause_to(4.6)
        M=plot_all("M")
        self.animate(m.FadeIn(M),duration=.8)
        self.pause_to(6.2)
        self.animate(m.FadeOut(M),m.FadeIn(plot_all("V")),duration=.7)
        self.pause_to(8.85)
        self.animate(m.FadeOut(*[]),duration=.05) if False else None
        self.note("Equilibrio + compatibilidad + signos locales")
        self.finish()
