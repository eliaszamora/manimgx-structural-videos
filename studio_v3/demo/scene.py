"""ManimGX real: physically driven portal and a separate sign-explained left-column plot."""
import sys,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
sys.path.insert(0,str(HERE.parent))
import manimgx as m
from portal_solver import solve,L,H
from structural_viz.model import member_from_solver
from structural_viz.manim_primitives import label,segment,curve,supports,diagram_panel
from structural_viz.style import STYLE as S
from story import BEATS,SECONDS_PER_BEAT,TOTAL_SECONDS

result=solve('lateral')
col_left=member_from_solver(result['elements'][0],'Columna izquierda')
col_right=member_from_solver(result['elements'][3],'Columna derecha')
all_members=[member_from_solver(e,f'e{i}') for i,e in enumerate(result['elements'])]
AMP=145.0

def world(pos):return (-5.0+pos[0]*.89,-1.43+pos[1]*.92)
def original():return m.VGroup(*[curve([world((s.x,s.y)) for s in e.samples],S.steel,4) for e in all_members])
def deformed():return m.VGroup(*[curve([world(p) for p in e.deformed(AMP)],S.deformed,7) for e in all_members])
def joint(idx,deformed_flag):
    x,y=result['nodes'][idx];ux,uy=result['u'][idx][:2]
    return world((x+(AMP*ux if deformed_flag else 0),y+(AMP*uy if deformed_flag else 0)))
def arr(a,b,color):return m.Arrow([*a,0],[*b,0],buff=0,color=color,stroke_width=6)

class ColumnaDoubleCurvature(m.Scene):
    def wait_until(self,x):
        if x>self.clock:self.wait(x-self.clock);self.clock=x
    def show(self,*events,secs=1):
        self.play(*events,run_time=secs);self.clock+=secs
    def begin(self,idx):
        self.clock=0.;b=BEATS[idx]
        header=label(b['head'],0,3.21,S.heading_text)
        sub=label(b['sub'],0,-3.25,S.label_text)
        if idx==0:
            self.header=header;self.subtitle=sub
            self.show(m.FadeIn(header),m.FadeIn(sub),secs=.60)
        else:self.show(m.Transform(self.header,header),m.Transform(self.subtitle,sub),secs=.60)
    def finish(self):
        if self.clock>SECONDS_PER_BEAT+.01:raise ValueError('chapter overrun')
        self.wait_until(SECONDS_PER_BEAT)
    def construct(self):
        self.camera.background_color=S.background
        rail=segment((.83,-2.75),(.83,2.63),S.steel,2)
        brand=label('LABORATORIO DE ESTRUCTURAS  /  MECÁNICA VISUAL',0,3.72,19,S.muted)
        self.add(brand,rail)
        axes=original()
        foundation=m.VGroup(supports(world((0,0))),supports(world((L,0))))
        deform=deformed()
        header2=label('MODELO Y RESTRICCIONES',3.52,2.21,26,S.muted)
        left_x=world((0,H))[0];right_x=world((L,H))[0]

        self.begin(0)
        self.show(m.FadeIn(foundation),m.Create(axes),secs=2.8)
        self.wait_until(5.0)
        horizontal_force=arr((right_x-.1,world((L,H))[1]),(right_x+1.12,world((L,H))[1]),S.load)
        # arrow is intentionally temporarily shown on the ORIGINAL geometry
        self.show(m.GrowArrow(horizontal_force),secs=1.2)
        note=label('H = 24 kN →',3.4,.65,30,S.load)
        self.show(m.FadeIn(note),secs=.6)
        self.wait_until(9.7)
        supportforces=label('R1x + R2x = −24 kN',3.39,-.25,26,S.shear)
        self.show(m.FadeIn(supportforces),secs=.8)
        self.finish()

        self.begin(1)
        self.show(m.FadeOut(horizontal_force),m.FadeOut(note),m.FadeOut(supportforces),secs=.75)
        self.wait_until(2.3)
        self.show(m.Create(deform),secs=2.5)
        dot=m.Dot(point=[*joint(1,True),0],radius=.105,color=S.inflection)
        self.show(m.FadeIn(dot),secs=.75)
        self.wait_until(8.9)
        ext=label('Deformada exagerada ×145',3.47,.48,28,S.deformed)
        u=label('u = +2,93 mm',3.47,-.29,27,S.ink)
        self.show(m.FadeIn(ext),m.FadeIn(u),secs=1.2)
        self.finish()

        self.begin(2)
        self.show(m.FadeOut(ext),m.FadeOut(u),secs=.65)
        self.wait_until(2.1)
        foot=world((0,0))
        tangent_bottom=segment((foot[0],foot[1]-.43),(foot[0],foot[1]+.43),S.moment_positive,5)
        self.show(m.Create(tangent_bottom),secs=1.)
        self.wait_until(6.55)
        top=joint(1,True);theta=AMP*result['u'][1][2]
        tangent_top=segment((top[0]+.43*math.sin(theta),top[1]-.43*math.cos(theta)),
                            (top[0]-.43*math.sin(theta),top[1]+.43*math.cos(theta)),S.inflection,5)
        self.show(m.Create(tangent_top),secs=1.25)
        explain=label('θbase = 0   /   θnudo ≠ 0',3.50,-.17,27,S.ink)
        self.show(m.FadeIn(explain),secs=.65)
        self.wait_until(10.15)
        note=label('Tangentes → curvatura',3.53,-1.05,25,S.muted)
        self.show(m.FadeIn(note),secs=.7)
        self.finish()

        self.begin(3)
        self.show(m.FadeOut(tangent_bottom),m.FadeOut(tangent_top),m.FadeOut(explain),m.FadeOut(note),secs=.65)
        panelheading=label('MOMENTO  /  COLUMNA IZQUIERDA',3.50,2.28,25,S.ink)
        self.show(m.Transform(header2,panelheading) if header2 in self.mobjects else m.FadeIn(panelheading),secs=.6)
        self.wait_until(2.0)
        plot=diagram_panel(col_left,'M',x=2.65,y=-1.52,length=3.10,amplitude=.85)
        self.show(m.FadeIn(plot),secs=2.1)
        low=label('Mbase = −23,73 kN·m',3.39,-2.1,25,S.moment_negative)
        self.show(m.FadeIn(low),secs=.65)
        self.wait_until(7.3)
        high=label('Mtop = +17,05 kN·m',3.39,-2.48,25,S.moment_positive)
        self.show(m.FadeIn(high),secs=.65)
        self.wait_until(10.4)
        zero=label('Inflexión: z ≈ 1,98 m',3.48,.07,25,S.inflection)
        self.show(m.FadeIn(zero),secs=.6)
        self.finish()

        self.begin(4)
        self.show(m.FadeOut(plot),m.FadeOut(low),m.FadeOut(high),m.FadeOut(zero),secs=.65)
        self.wait_until(2.15)
        shearplot=diagram_panel(col_left,'V',x=2.63,y=-1.50,length=3.08,amplitude=.64)
        self.show(m.FadeIn(shearplot),secs=1.8)
        value=label('Vlocal = +11,99 kN',3.52,-2.15,27,S.shear)
        self.show(m.FadeIn(value),secs=.8)
        self.wait_until(7.15)
        reaction=arr((foot[0]+.75,foot[1]+.30),(foot[0]-.25,foot[1]+.30),S.load)
        self.show(m.GrowArrow(reaction),secs=.95)
        msg=label('Reacción global: ← 11,99 kN',3.53,-2.5,24,S.load)
        self.show(m.FadeIn(msg),secs=.75)
        self.wait_until(10.5)
        sumv=label('11,99 + 12,01 = 24 kN',3.48,.10,26,S.ink)
        self.show(m.FadeIn(sumv),secs=.6)
        self.finish()

        self.begin(5)
        self.show(m.FadeOut(shearplot),m.FadeOut(value),m.FadeOut(reaction),m.FadeOut(msg),m.FadeOut(sumv),secs=.75)
        self.wait_until(2.8)
        recap=label('BLOQUEO → GIROS → M → V',3.45,.82,28,S.moment_positive)
        self.show(m.FadeIn(recap),secs=.8)
        self.wait_until(6.8)
        one=label('1. Compatibilidad geométrica',3.45,.06,25,S.deformed)
        two=label('2. Equilibrio de fuerzas',3.45,-.56,25,S.shear)
        self.show(m.FadeIn(one),m.FadeIn(two),secs=1.2)
        self.wait_until(10.7)
        end=label('La deformada se DEDUCE.',3.46,-1.45,26,S.ink)
        self.show(m.FadeIn(end),secs=.8)
        self.finish()
