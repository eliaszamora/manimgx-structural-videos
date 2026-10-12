"""Frame animation computed from the FEM reference; load cases A and B."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import manimgx as m
from mechanics import solve,L,H
from story import BEATS
import numpy as np
GRAVITY=solve('gravity');LATERAL=solve('lateral')
BG='#071523';WHITE='#F4F7FF';MUTED='#A3B8CA';STEEL='#466076'
TEAL='#42E2C2';CORAL='#FF9881';BLUE='#87ADFF';GOLD='#FFD58B'
X0=-3.42;BASE=-2.03;SCALE=1.16;GAIN=170

def pos(xy):return [X0+SCALE*xy[0],BASE+SCALE*xy[1],0]
def text(s,y=-3.42,x=0,size=23,color=WHITE):
    return m.Text(s,font_size=size,color=color).move_to([x,y,0])
def line(a,b,c=STEEL,w=5):
    return m.Line(a,b,color=c,stroke_width=w)
def frame(result,displaced=False,color=TEAL,width=8):
    curves=[]
    for e in result['elements']:
        pts=[pos(np.array(p['xy'])+(GAIN*np.array(p['uxy']) if displaced else 0)) for p in e['samples']]
        obj=m.VMobject(color=color,stroke_width=width)
        obj.set_points_smoothly(pts);curves.append(obj)
    return m.VGroup(*curves)
def supports():
    a=[]
    for x in (0,L):
        p=pos([x,0])
        a.append(m.Rectangle(width=.20,height=.68,fill_color=STEEL,fill_opacity=1,
                    stroke_color=MUTED,stroke_width=1).move_to([p[0],p[1]-.05,0]))
        for i in range(4):
            x0=p[0]-.20+i*.13
            a.append(line([x0,p[1]-.43,0],[x0+.20,p[1]-.69,0],STEEL,1.8))
    return m.VGroup(*a)
def dot(result,node,color=GOLD):
    xy=np.array(result['nodes'][node])+GAIN*np.array(result['u'][node][:2])
    return m.Dot(point=pos(xy),radius=.09,color=color)
def beam_moment(result):
    chunks=result['elements'][1:3];y=-2.44
    axis=line([X0,y,0],[X0+SCALE*L,y,0],MUTED,2)
    peak=max(abs(s['M']) for e in chunks for s in e['samples'])
    plots=[]
    for e in chunks:
        pts=[[pos(p['xy'])[0],y-.74*p['M']/peak,0] for p in e['samples']]
        curve=m.VMobject(color=CORAL,stroke_width=5)
        curve.set_points_smoothly(pts);plots.append(curve)
    return axis,m.VGroup(*plots)
def column_moment(result):
    curves=[];dots=[]
    for e in (result['elements'][0],result['elements'][3]):
        v=e['samples'];peak=max(abs(p['M']) for p in v)
        # Both columns point bottom -> top, so the +M plot side is global RIGHT.
        pts=[]
        for p in v:
            q=pos(p['xy']);q[0]+=.72*p['M']/peak;pts.append(q)
        c=m.VMobject(color=GOLD,stroke_width=5);c.set_points_smoothly(pts);curves.append(c)
        ma,mb=v[0]['M'],v[-1]['M']
        if ma*mb<0:
            t=-ma/(mb-ma)
            xyz=np.array(v[0]['xy'])+t*(np.array(v[-1]['xy'])-np.array(v[0]['xy']))
            dots.append(m.Dot(point=pos(xyz),radius=.11,color=CORAL))
    return m.VGroup(*curves),m.VGroup(*dots)

class PortalEngineeringLesson(m.Scene):
    def animate(self,*a,t=1):
        self.play(*a,run_time=t);self.elapsed+=t
    def pause(self,t):
        if t>0:self.wait(t);self.elapsed+=t
    def chapter(self,i):
        self.elapsed=0
        b=BEATS[i];self.limit=b['seconds']
        title=text(b['id']+'  /  '+b['heading'],y=3.24,size=35)
        foot=text(b['subtitle'],y=-3.35,size=28)
        if i==0:
            self.title=title;self.foot=foot
            self.animate(m.FadeIn(self.title),m.FadeIn(self.foot),t=1.2)
        else:self.animate(m.Transform(self.title,title),m.Transform(self.foot,foot),t=1.1)
    def finish(self):
        delta=self.limit-self.elapsed
        if delta<-.06:raise ValueError(f'Chapter exceeds narrated interval: {self.elapsed:.2f}>{self.limit}')
        self.pause(max(0,delta))
    def construct(self):
        self.camera.background_color=BG
        eyebrow=text('MECÁNICA ESTRUCTURAL / DEFORMADAS Y ESFUERZOS',y=3.72,size=18,color=MUTED)
        underline=line([-5.6,2.79,0],[5.6,2.79,0],STEEL,2)
        fixed=supports()
        ghost=frame(GRAVITY,False,color=STEEL,width=4)
        steel=frame(GRAVITY,False)
        self.add(eyebrow,underline)

        self.chapter(0)
        self.animate(m.FadeIn(fixed),m.Create(steel),t=2.2)
        n=text('Bases: ux = uy = giro = 0',y=-2.62,size=24,color=GOLD)
        self.animate(m.FadeIn(n),t=1.2)
        joint=m.VGroup(m.Dot(point=pos([0,H]),color=GOLD,radius=.10),m.Dot(point=pos([L,H]),color=GOLD,radius=.10))
        self.animate(m.FadeIn(joint),t=1.2)
        self.pause(2.1)
        self.animate(m.FadeOut(n),m.FadeOut(joint),t=.9)
        self.finish()

        self.chapter(1)
        p=pos([L/2,H])
        down=m.Arrow([p[0],2.67,0],[p[0],p[1]+.13,0],buff=0,color=CORAL,stroke_width=7)
        load_label=text('35 kN',x=p[0]+.68,y=2.43,size=25,color=CORAL)
        self.animate(m.GrowArrow(down),m.FadeIn(load_label),t=2.4)
        caption=text('Simetría: no hay desplazamiento lateral global',y=-2.62,size=22,color=GOLD)
        self.animate(m.FadeIn(caption),t=1.2)
        self.pause(2.2)
        self.animate(m.FadeOut(caption),t=.8)
        self.finish()

        self.chapter(2)
        self.add(ghost)
        self.animate(m.Transform(steel,frame(GRAVITY,True)),t=4.5)
        mid=dot(GRAVITY,2,color=CORAL)
        ends=m.VGroup(dot(GRAVITY,1),dot(GRAVITY,3))
        self.animate(m.FadeIn(mid),m.FadeIn(ends),t=1.25)
        msg=text('Los dos nudos giran en sentidos opuestos',y=-2.63,size=23,color=GOLD)
        self.animate(m.FadeIn(msg),t=1)
        tangents=m.VGroup()
        for i in (1,3):
            u=GRAVITY['u'][i];xy=np.array(GRAVITY['nodes'][i])+GAIN*np.array(u[:2])
            pt=pos(xy);r=GAIN*u[2]
            dx,dy=.55*np.cos(r),.55*np.sin(r)
            tangents.add(line([pt[0]-dx/2,pt[1]-dy/2,0],[pt[0]+dx/2,pt[1]+dy/2,0],GOLD,3))
        self.animate(m.Create(tangents),t=1.6)
        self.pause(1.5)
        self.animate(m.FadeOut(tangents),m.FadeOut(msg),t=.8)
        self.finish()

        self.chapter(3)
        axis,curves=beam_moment(GRAVITY)
        self.animate(m.Create(axis),m.Create(curves),t=4.3)
        signs=m.VGroup(text('M positivo: bajo',x=4.65,y=-2.10,size=22,color=GOLD),
                       text('M negativo: sobre',x=4.65,y=-2.56,size=22,color=CORAL))
        self.animate(m.FadeIn(signs),t=1.4)
        self.pause(2)
        self.animate(m.FadeOut(axis),m.FadeOut(curves),m.FadeOut(signs),t=1.6)
        self.finish()

        self.chapter(4)
        roof=pos([L,H])
        force=m.Arrow([roof[0]-.1,roof[1],0],[roof[0]+1.58,roof[1],0],buff=0,color=BLUE,stroke_width=7)
        label=text('24 kN',x=roof[0]+.82,y=roof[1]+.35,size=23,color=BLUE)
        self.animate(m.Transform(steel,frame(LATERAL,False)),
                     m.FadeOut(down),m.FadeOut(load_label),m.FadeOut(mid),m.FadeOut(ends),t=1.7)
        self.animate(m.GrowArrow(force),m.FadeIn(label),t=1.8)
        self.animate(m.Transform(steel,frame(LATERAL,True)),t=4.1)
        sway=text('Sway: ambos nudos se desplazan a la derecha →',y=-2.62,size=22,color=GOLD)
        self.animate(m.FadeIn(sway),t=1.2)
        self.pause(2)
        self.animate(m.FadeOut(sway),t=.6)
        self.finish()

        self.chapter(5)
        corners=m.VGroup(dot(LATERAL,1),dot(LATERAL,3))
        self.animate(m.FadeIn(corners),t=1.3)
        moving=m.Arrow(pos([L/2,H+.38]),
                       [pos([L/2,H+.38])[0]+1.05,pos([L/2,H+.38])[1],0],
                       buff=0,color=GOLD,stroke_width=5)
        self.animate(m.GrowArrow(moving),t=1.5)
        a=text('Bases fijas: los fustes deben curvarse',y=-2.59,size=23,color=GOLD)
        self.animate(m.FadeIn(a),t=1.3)
        self.pause(1.7)
        self.animate(m.Transform(a,text('La viga conecta los giros de ambos nudos',y=-2.59,size=22,color=TEAL)),t=1.4)
        self.pause(1.9)
        self.animate(m.FadeOut(a),m.FadeOut(corners),m.FadeOut(moving),t=1.3)
        self.finish()

        self.chapter(6)
        moments,zeros=column_moment(LATERAL)
        self.animate(m.Create(moments),t=3.5)
        self.animate(m.FadeIn(zeros),t=1.3)
        a=text('M = 0 en los puntos de inflexión',y=-2.52,size=23,color=GOLD)
        b=text('Inflexión NO significa rótula',y=-2.03,size=23,color=CORAL)
        self.animate(m.FadeIn(a),t=1.2)
        self.animate(m.FadeIn(b),t=1.0)
        self.pause(2.2)
        self.animate(m.FadeOut(a),m.FadeOut(b),t=.9)
        self.finish()

        self.chapter(7)
        arrows=[]
        for idx in (0,3):
            p=pos(LATERAL['elements'][idx]['samples'][0]['xy'])
            y=p[1]+1.25
            arrows.append(m.Arrow([p[0]+.5,y,0],[p[0]-.5,y,0],buff=0,color=BLUE,stroke_width=6))
        self.animate(m.GrowArrow(arrows[0]),m.GrowArrow(arrows[1]),t=2.0)
        sumshear=text('Cortantes en columnas: suma = 24 kN',y=-2.32,size=23,color=BLUE)
        self.animate(m.FadeIn(sumshear),t=1.3)
        compare=text('Vertical: sin sway    |    Horizontal: sway + inflexión',y=-2.84,size=21,color=GOLD)
        self.animate(m.FadeIn(compare),t=1.3)
        self.pause(1.7)
        self.animate(m.FadeOut(moments),m.FadeOut(zeros),m.FadeOut(compare),m.FadeOut(sumshear),t=1.5)
        end=text('Primero compatibilidad y equilibrio. Después el dibujo.',y=-2.55,size=23,color=TEAL)
        self.animate(m.FadeIn(end),t=1.2)
        self.finish()
