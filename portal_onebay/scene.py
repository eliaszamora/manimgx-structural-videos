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
X0=-4.80;BASE=-1.93;SCALE=1.02;GAIN=170

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


def member_diagrams(r,quantity='M'):
    """Verified member-by-member plot. Member local x is bottom->top for both columns
    and left->right for the beam. Graphic positive moment is clockwise of local axis:
    BELOW beams, RIGHT of rising columns; negative on opposite side.
    For shear, sign uses the same GRAPHIC convention, not a force-arrow convention.
    """
    vkey='M' if quantity=='M' else 'V'
    high=max(abs(q[vkey]) for e in r['elements'] for q in e['samples'])
    graphics=[]
    for e in r['elements']:
        a=np.array(e['samples'][0]['xy']);b=np.array(e['samples'][-1]['xy'])
        axis=(b-a)/np.linalg.norm(b-a)
        clockwise=np.array([axis[1],-axis[0]])
        coords=[]
        for q in e['samples']:
            p=np.array(q['xy']) + clockwise * (.57/high/SCALE) * q[vkey]
            coords.append(pos(p))
        for i in range(len(coords)-1):
            value=.5*(e['samples'][i][vkey]+e['samples'][i+1][vkey])
            col=(GOLD if value>=0 else CORAL) if quantity=='M' else BLUE
            graphics.append(line(coords[i],coords[i+1],col,4.2))
        if quantity=='V':
            graphics.append(line(pos(a),coords[0],BLUE,2))
            graphics.append(line(pos(b),coords[-1],BLUE,2))
    return m.VGroup(*graphics)

def fact_panel(lines_):
    """Short numerical captions in the empty right-hand pane, not on the structure."""
    return m.VGroup(*[
        text(value,x=3.83,y=1.62-i*.54,size=25,color=col)
        for i,(value,col) in enumerate(lines_)
    ])

class PortalEngineeringLesson(m.Scene):
    def animate(self,*a,t=1):
        self.play(*a,run_time=t);self.elapsed+=t
    def pause(self,t):
        if t>0:self.wait(t);self.elapsed+=t
    def chapter(self,i):
        self.elapsed=0
        b=BEATS[i];self.limit=b['seconds']
        title=text(b['id']+'  /  '+b['heading'],y=3.24,size=41)
        foot=text(b['subtitle'],y=-3.35,size=31)
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
        exaggeration=text('Deformada ampliada x170',x=3.83,y=1.92,size=24,color=MUTED)
        self.animate(m.FadeIn(exaggeration),t=.6)
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
        self.animate(m.FadeOut(tangents),m.FadeOut(msg),m.FadeOut(exaggeration),t=.8)
        self.finish()

        self.chapter(3)
        # All FOUR elements use the SAME declared member-axis sign convention.
        physical_M_A=member_diagrams(GRAVITY,'M')
        panel_A=fact_panel([
            ('M VIGA / kN.m',WHITE),('Extremos: -17.19',CORAL),
            ('Centro: +31.81',GOLD),('Col. sup.: +/-17.19',MUTED),
            ('+ abajo de viga',GOLD),('- arriba de viga',CORAL)])
        self.animate(m.FadeIn(physical_M_A),t=2.7)
        self.animate(m.FadeIn(panel_A),t=1.7)
        self.pause(1.8)
        physical_V_A=member_diagrams(GRAVITY,'V')
        panel_V_A=fact_panel([
            ('CORTE / kN',WHITE),('Viga izq.: +17.50',BLUE),
            ('Viga der.: -17.50',BLUE),('Salto: -35.00',GOLD),
            ('Col. izq.: -7.58',BLUE),('Col. der.: +7.58',BLUE)])
        self.animate(m.Transform(physical_M_A,physical_V_A),m.Transform(panel_A,panel_V_A),t=2.2)
        self.pause(2.4)
        self.animate(m.FadeOut(physical_M_A),m.FadeOut(panel_A),t=1.3)
        self.finish()

        self.chapter(4)
        roof=pos([L,H])
        force=m.Arrow([roof[0]-.1,roof[1],0],[roof[0]+1.58,roof[1],0],buff=0,color=BLUE,stroke_width=7)
        label=text('24 kN',x=roof[0]+.82,y=roof[1]+.35,size=23,color=BLUE)
        self.animate(m.Transform(steel,frame(LATERAL,False)),
                     m.FadeOut(down),m.FadeOut(load_label),m.FadeOut(mid),m.FadeOut(ends),t=1.7)
        self.animate(m.GrowArrow(force),m.FadeIn(label),t=1.8)
        newroof=pos(np.array([L,H])+GAIN*np.array(LATERAL['u'][3][:2]))
        newforce=m.Arrow([newroof[0]-.1,newroof[1],0],[newroof[0]+1.30,newroof[1],0],buff=0,color=BLUE,stroke_width=7)
        newlabel=text('24 kN',x=newroof[0]+.66,y=newroof[1]+.36,size=24,color=BLUE)
        self.animate(m.Transform(steel,frame(LATERAL,True)),m.Transform(force,newforce),m.Transform(label,newlabel),t=4.1)
        sway=text('Sway a derecha, ampliado x170 (2.93 mm)',y=-2.62,size=24,color=GOLD)
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
        self.animate(m.Transform(steel,frame(LATERAL,False)),m.FadeOut(force),m.FadeOut(label),t=1.1)
        diagram_B=member_diagrams(LATERAL,'M')
        info_B=fact_panel([
            ('M COLUMNAS / kN.m',WHITE),
            ('Bases: -23.7',CORAL),('Arriba: +17.0',GOLD),
            ('M=0 a 1.98 m',TEAL),
            ('Viga: +17 a -17',MUTED),
            ('+ derecha / - izq.',GOLD)])
        self.animate(m.FadeIn(diagram_B),t=2.8)
        self.animate(m.FadeIn(info_B),t=1.7)
        self.pause(3.1)
        self.animate(m.FadeOut(info_B),t=.9)
        self.finish()

        self.chapter(7)
        diagram_V_B=member_diagrams(LATERAL,'V')
        shear_info=fact_panel([
            ('CORTANTES LOCALES',WHITE),
            ('Col. 1: +11.99 kN',BLUE),
            ('Col. 2: +12.01 kN',BLUE),
            ('Viga: -6.09 kN',BLUE),
            ('Sum H=24.00 kN',GOLD),
            ('Reacciones: a izq.',CORAL)])
        self.animate(m.Transform(diagram_B,diagram_V_B),t=2.4)
        self.animate(m.FadeIn(shear_info),t=1.9)
        self.pause(2.2)
        summary=text('Reacción EXTERNA distinta del corte INTERNO',y=-2.64,size=25,color=GOLD)
        self.animate(m.FadeIn(summary),t=1.3)
        self.pause(1.4)
        self.animate(m.FadeOut(summary),m.FadeOut(diagram_B),m.FadeOut(shear_info),t=1.3)
        end=text('Equilibrio + compatibilidad ANTES del dibujo',y=-2.59,size=25,color=TEAL)
        self.animate(m.FadeIn(end),t=1.1)
        self.finish()
