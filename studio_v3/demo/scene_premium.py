"""Studio V4: premium explainer. All displaced points and M/V derive from solver.
The animation depicts quasi-static load interpolation, NOT time-history dynamics.
Moment/shear diagrams are anchored to the UNDEFORMED left-column axis.
"""
import sys, math
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parent))
import manimgx as m
from portal_solver import solve,L,H
from structural_viz.model import member_from_solver
from story import BEATS,SECONDS_PER_BEAT
from structural_viz.style import STYLE as S

R=solve('lateral')
MEM=[member_from_solver(e,'barra_'+str(i)) for i,e in enumerate(R['elements'])]
COL=MEM[0]
AMP=175.0
ORIGIN=(-4.75,-2.18)
SC=0.99
ink="#F5FAFF"; muted="#B3C7D9"; grid="#344D61"; bg="#081521"
sea="#56E6C8"; orange="#FF9F7B"; gold="#FFD488"; red="#FF817E"; blue="#81B9FF"; violet="#D2B2FF"

def screen(p):return (ORIGIN[0]+SC*p[0],ORIGIN[1]+SC*p[1])
def vec(p):return [float(p[0]),float(p[1]),0]
def ln(a,b,color=grid,w=3):return m.Line(vec(a),vec(b),color=color,stroke_width=w)
def tx(text,x,y,size=28,color=ink):
    return m.Text(text,font="DejaVu Sans",font_size=size,color=color).move_to([x,y,0])
def path(pts,color,w):
    obj=m.VMobject(color=color,stroke_width=w)
    obj.set_points_smoothly([vec(p) for p in pts])
    return obj
def geometry(scale,stroke=sea,w=8):
    parts=[]
    for e in MEM:
        pts=[screen((s.x+scale*s.displacement_x,s.y+scale*s.displacement_y)) for s in e.samples]
        parts.append(path(pts,stroke,w))
    return m.VGroup(*parts)
def node(i,scale=0):
    x,y=R['nodes'][i]; ux,uy=R['u'][i][:2]
    return screen((x+scale*ux,y+scale*uy))
def arrow(a,b,col=orange):
    return m.Arrow(vec(a),vec(b),buff=0,color=col,stroke_width=7)
def support(at):
    x,y=at
    block=m.Rectangle(width=.22,height=.78,fill_color=grid,fill_opacity=1,stroke_color=muted)
    block.move_to([x-.06,y-.03,0])
    cuts=[ln((x-.36+i*.19,y-.43),(x-.14+i*.19,y-.70),muted,2) for i in range(4)]
    return m.VGroup(block,*cuts)
def fixed_sign_diagram(kind):
    """Use ORIGINAL left-column axis, with local +M to the right and -M to left."""
    x,y=screen((0,0))
    yt=screen((0,H))[1]
    bot=COL.samples[0];top=COL.samples[-1]
    vmax=max(abs(getattr(s,kind)) for s in COL.samples)
    width=.84 if kind=='M' else .61
    def of(v):return width*v/vmax
    if kind=='M':
        z=COL.zeros('M')[0]
        yz=y+(yt-y)*z
        xb=x+of(bot.M);xt=x+of(top.M)
        neg=m.Polygon(vec((x,y)),vec((xb,y)),vec((x,yz)),
                color=red,fill_color=red,fill_opacity=.24,stroke_width=3)
        pos=m.Polygon(vec((x,yz)),vec((xt,yt)),vec((x,yt)),
                color=gold,fill_color=gold,fill_opacity=.24,stroke_width=3)
        end=m.VGroup(neg,pos,
            ln((xb,y),(x,yz),red,5),ln((x,yz),(xt,yt),gold,5),
            m.Dot(point=vec((x,yz)),radius=.105,color=violet))
        return end
    ox=x+of(bot.V)
    rect=m.Polygon(vec((x,y)),vec((ox,y)),vec((ox,yt)),vec((x,yt)),
             color=blue,fill_color=blue,fill_opacity=.22,stroke_width=3)
    return m.VGroup(rect,ln((ox,y),(ox,yt),blue,5))
def upper_tangent():
    x,y=node(1,AMP)
    a=AMP*float(R['u'][1][2])
    ux,uy=math.sin(a),math.cos(a)
    return ln((x-.51*ux,y-.51*uy),(x+.51*ux,y+.51*uy),gold,5)
def dotted_displacement():
    a=node(1,0);b=node(1,AMP)
    return m.VGroup(ln(a,b,violet,4),m.Dot(point=vec(b),radius=.115,color=violet))

class PremiumDoubleCurvature(m.Scene):
    def run(self,*animations,dt=1):
        self.play(*animations,run_time=dt)
        self.elapsed+=dt
    def wait_to(self,t):
        if t>self.elapsed:
            self.wait(t-self.elapsed);self.elapsed=t
    def chapter(self,index):
        self.elapsed=0.
        beat=BEATS[index]
        # Solid zones: no transforming text glyphs, only cross-fading complete blocks.
        header=tx(beat['head'],0,3.17,35)
        subtitle=tx(beat['sub'],0,-3.38,27,muted)
        count=tx(f"{index+1:02d}  /  06",5.91,3.60,22,sea)
        if index==0:
            self.head,self.sub,self.counter=header,subtitle,count
            self.run(m.FadeIn(header),m.FadeIn(subtitle),m.FadeIn(count),dt=.65)
        else:
            self.run(m.FadeOut(self.head),m.FadeOut(self.sub),m.FadeOut(self.counter),dt=.25)
            self.head,self.sub,self.counter=header,subtitle,count
            self.run(m.FadeIn(header),m.FadeIn(subtitle),m.FadeIn(count),dt=.40)
        self.details=[]
    def info(self,at,heading,lines,accent=sea):
        self.wait_to(at)
        heading_obj=tx(heading,4.08,1.52,29,accent)
        objs=[heading_obj]
        for i,s in enumerate(lines):
            objs.append(tx(s,4.08,.75-.58*i,26,ink if i==0 else muted))
        new=m.VGroup(*objs)
        if self.details:
            self.run(m.FadeOut(self.details[-1]),m.FadeIn(new),dt=.60)
        else:
            self.run(m.FadeIn(new),dt=.60)
        self.details=[new]
    def finish(self):
        if self.elapsed>SECONDS_PER_BEAT+.01:raise RuntimeError('Exceeded chapter duration')
        self.wait_to(SECONDS_PER_BEAT)
    def clear_details(self):
        if self.details:
            self.run(m.FadeOut(self.details[-1]),dt=.30)
            self.details=[]

    def construct(self):
        self.camera.background_color=bg
        self.add(ln((-6.52,2.66),(6.52,2.66),grid,2),
                 ln((1.62,-2.81),(1.62,2.45),grid,2),
                 tx('ESTRUCTURAS   /   EXPLICACIONES VISUALES',-2.7,3.65,20,muted))
        left,right=node(0),node(4)
        supports=m.VGroup(support(left),support(right))
        frame=geometry(0,sea,8)
        base_reference=geometry(0,grid,3)
        blueprints=m.VGroup(*[m.Dot(point=vec(node(i)),radius=.075,color=gold) for i in (1,3)])
        self.chapter(0)
        self.run(m.FadeIn(supports),m.Create(frame),dt=2.35)
        self.info(3.25,'MODELO','Un piso  ·  una crujía' .split('no delimiter'),gold) if False else None
        self.info(3.25,'SISTEMA',['Bases empotradas','Nudos rígidos'])
        a=node(3)
        F=arrow((a[0]-.08,a[1]),(a[0]+1.06,a[1]))
        self.wait_to(6.0);self.run(m.GrowArrow(F),dt=1.30)
        self.info(10.0,'CARGA HORIZONTAL',['H = 24 kN  →','Equilibrio en bases'],orange)
        self.finish()

        self.chapter(1)
        self.run(m.FadeOut(F),dt=.42)
        self.add(base_reference)
        self.info(2.35,'DEFORMACIÓN',['Carga aplicada 0 → 100 %','Desplazamiento continuo'],sea)
        # With Transform the ORIGINAL MATERIAL POINTS move to their FEM-computed positions.
        self.wait_to(5.65)
        self.run(m.Transform(frame,geometry(AMP,sea,8)),dt=3.65)
        tip=dotted_displacement()
        self.run(m.Create(tip),dt=.72)
        self.info(10.10,'ESCALA VISUAL',[f'Deformada ampliada ×{int(AMP)}','u superior ≈ 2,93 mm'],violet)
        self.finish()

        self.chapter(2)
        self.run(m.FadeOut(tip),dt=.32)
        self.info(2.1,'EMPOTRAMIENTO',['Desplazamiento = 0','Giro de la base = 0'],gold)
        bottom=ln((left[0],left[1]-.44),(left[0],left[1]+.44),gold,5)
        self.run(m.Create(bottom),dt=1.65)
        tangent=upper_tangent()
        self.info(5.45,'CONTINUIDAD',['El nudo superior gira','Viga y columna compatibles'],violet)
        self.run(m.Create(tangent),dt=1.70)
        self.info(10.1,'CONSECUENCIA',['Las pendientes cambian','y aparece la curvatura'],sea)
        self.finish()

        self.chapter(3)
        self.run(m.FadeOut(bottom),m.FadeOut(tangent),dt=.55)
        self.run(m.Transform(frame,geometry(0,sea,8)),m.FadeOut(base_reference),dt=1.48)
        self.info(2.15,'MOMENTO FLECTOR',['Eje: columna ORIGINAL','Negativo ←  |  + →'],red)
        plot=fixed_sign_diagram('M')
        self.run(m.Create(plot),dt=2.42)
        self.info(5.4,'CAMBIO DE SIGNO',['Base: −23,7 kN·m','Coronación: +17,0 kN·m'],gold)
        self.info(10.0,'INFLEXIÓN',['M = 0 a z ≈ 1,98 m','No representa una rótula'],violet)
        self.finish()

        self.chapter(4)
        self.run(m.FadeOut(plot),dt=.63)
        self.info(2.0,'CORTANTE',['Eje: columna ORIGINAL','Diagrama constante'],blue)
        vp=fixed_sign_diagram('V')
        self.run(m.Create(vp),dt=2.30)
        self.info(5.4,'CORTE LOCAL',['V = +11,99 kN','Se obtiene por equilibrio'],blue)
        self.info(10.0,'REACCIONES',['Dos bases empotradas','R1x + R2x = −24 kN'],orange)
        self.finish()

        self.chapter(5)
        self.run(m.FadeOut(vp),dt=.63)
        self.info(2.0,'PRIMERO LA FÍSICA',['Restricciones y compatibilidad','antes de dibujar curvas'],sea)
        self.run(m.Transform(frame,geometry(AMP,sea,8)),dt=2.75)
        self.info(6.35,'DESPUÉS LOS ESFUERZOS',['Curvatura ↔ momento','Equilibrio ↔ cortante'],gold)
        self.info(10.0,'IDEA CLAVE',['Comprender el mecanismo','es mejor que memorizar'],violet)
        self.finish()
