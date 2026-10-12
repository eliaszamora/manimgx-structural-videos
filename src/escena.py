"""Prueba ManimGX: voladizo, deformada, M y V. M negativo SOBRE eje."""
import manimgx as m
BG='#061320'; W='#F1F6FC'; M='#A4B9CE'; T='#38D6C4'; O='#FF967B'; B='#76A9FF'; Y='#FFD48B'; D='#3E5B70'
def label(s,y=-2.95,c=W,z=25):
    return m.Text(s,font_size=z,color=c).move_to([0,y,0])
def pt(u,k=0):
    return [-4.9+8*u,0.45-0.9*k*u*u*(3-u)/2,0]
class VigaVoladizo(m.Scene):
    def construct(self):
        self.camera.background_color=BG
        title=label('DEFORMADA  /  MOMENTO  /  CORTANTE',3.25,W,37)
        subtitle=label('Viga empotrada; fuerza P en el extremo libre',2.75,M,22)
        support=m.Rectangle(width=.19,height=1.55,fill_color=D,fill_opacity=1,stroke_color=D).move_to([-5.05,.45,0])
        beam=m.Line(pt(0),pt(1),color=T,stroke_width=9)
        force=m.Arrow([3.1,1.95,0],[3.1,.54,0],color=O,buff=0,stroke_width=7)
        p=m.Text('P',font_size=32,color=O).move_to([3.55,1.4,0])
        self.play(m.Write(title),m.FadeIn(subtitle),run_time=2)
        self.play(m.FadeIn(support),m.Create(beam),run_time=2)
        self.play(m.GrowArrow(force),m.FadeIn(p),run_time=1.6)
        explanation=label('El empotramiento impide desplazamiento y giro')
        self.play(m.FadeIn(explanation),run_time=.8)
        self.wait(1.4)
        self.play(m.Transform(explanation,label("v(0) = 0     y     v'(0) = 0",c=Y)),run_time=1.1)
        curve=m.VMobject(color=T,stroke_width=9)
        curve.set_points_smoothly([pt(i/80,1) for i in range(81)])
        self.play(m.Transform(beam,curve),run_time=3)
        self.wait(.6)
        self.play(m.Transform(explanation,label('La pendiente parte de cero y se vuelve negativa')),run_time=.9)
        self.wait(1.5)
        self.play(m.Transform(explanation,label('La curvatura es negativa: M(x) = -P(L-x)',c=O)),run_time=1.1)
        self.wait(1.5)
        axis=m.Line([-4.9,-1.55,0],[3.1,-1.55,0],color=M)
        triangle=m.Polygon([-4.9,-1.55,0],[-4.9,-.82,0],[3.1,-1.55,0],color=O,fill_color=O,fill_opacity=.2,stroke_width=4)
        self.play(m.Create(axis),m.Create(triangle),run_time=2.3)
        self.play(m.Transform(explanation,label('M negativo: triangular y SOBRE el eje',c=O)),run_time=1)
        self.wait(1.6)
        vaxis=m.Line([-4.9,-2.04,0],[3.1,-2.04,0],color=M)
        rect=m.Polygon([-4.9,-2.04,0],[-4.9,-1.82,0],[3.1,-1.82,0],[3.1,-2.04,0],color=B,fill_color=B,fill_opacity=.23,stroke_width=3)
        self.play(m.FadeOut(triangle),m.Create(vaxis),m.Create(rect),run_time=1.8)
        self.play(m.Transform(explanation,label('V positivo: constante, igual a P',c=B)),run_time=1)
        self.wait(1.8)
        self.play(m.Transform(explanation,label('Primero equilibrio y compatibilidad; después el dibujo',c=Y)),run_time=1)
        self.wait(3)
