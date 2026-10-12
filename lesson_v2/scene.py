"""Lección reproducible ManimGX: intuición y equilibrio con reloj compartido."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from story import BEATS, TOTAL_SECONDS
import manimgx as m

C = {"bg":"#081321","white":"#F3F7FE","muted":"#A9BBCF",
     "grid":"#31465E","teal":"#4FE5C6","coral":"#FF9C84",
     "blue":"#79B5FF","gold":"#FFD58D","panel":"#102237"}
LEFT, RIGHT, Y, SPAN = -5.05, 3.25, 0.63, 8.30

def txt(value, x=0, y=0, size=24, color=None):
    return m.Text(value,font_size=size,color=color or C["white"]).move_to([x,y,0])

def coord(u, scale=0):
    return [LEFT + SPAN*u, Y-1.18*scale*u*u*(3-u)/2, 0]

def deformed(scale=1):
    obj = m.VMobject(color=C["teal"],stroke_width=8)
    obj.set_points_smoothly([coord(i/110,scale) for i in range(111)])
    return obj

def line(a,b,color=None,width=3):
    return m.Line(a,b,color=color or C["muted"],stroke_width=width)

class LeccionVoladizoV2(m.Scene):
    def run(self, *animations, seconds=1):
        self.play(*animations,run_time=seconds)
        self._elapsed += seconds

    def hold(self,seconds):
        if seconds > 0:
            self.wait(seconds)
            self._elapsed += seconds

    def chapter(self,i):
        self._elapsed=0
        self._duration = BEATS[i]["duration"]
        heading=txt(f"{i+1:02d}  /  {BEATS[i]['heading']}",0,3.20,33,C["white"])
        caption=txt(BEATS[i]["caption"],0,-3.20,22,C["white"])
        if i==0:
            self.head=heading
            self.foot=caption
            self.run(m.FadeIn(self.head),m.FadeIn(self.foot),seconds=1.6)
        else:
            self.run(m.Transform(self.head,heading),m.Transform(self.foot,caption),seconds=1.4)

    def finish(self):
        rem = self._duration-self._elapsed
        if rem < -0.02:
            raise ValueError(f"Duración de capítulo excedida: {self._duration}, usado {self._elapsed}")
        self.hold(max(0,rem))

    def construct(self):
        self.camera.background_color = C["bg"]
        eyebrow=txt("INGENIERÍA ESTRUCTURAL  •  ENTENDER ANTES DE CALCULAR",0,3.72,18,C["muted"])
        rule=line([-5.75,2.59,0],[5.72,2.59,0],C["grid"],2)
        self.add(eyebrow,rule)
        # Gráficos principales permanecen dentro del escenario (superior a y=-2.9)
        base=line([LEFT,Y,0],[RIGHT,Y,0],C["grid"],3)
        support=m.Rectangle(width=.22,height=1.8,fill_color=C["grid"],fill_opacity=1,
                            stroke_color=C["muted"],stroke_width=2).move_to([LEFT-.14,Y,0])
        beam=line(coord(0),coord(1),C["teal"],8)
        load=m.Arrow([RIGHT,2.1,0],[RIGHT,.70,0],buff=0,color=C["coral"],stroke_width=7)
        loadtxt=txt("P",RIGHT+.43,1.65,28,C["coral"])
        start=txt("EMPOTRAMIENTO",LEFT+1.15,-.02,18,C["muted"])
        tip=txt("EXTREMO LIBRE",RIGHT-.35,-.02,18,C["muted"])

        self.chapter(0)
        self.run(m.FadeIn(support),m.Create(beam),seconds=2.6)
        self.run(m.GrowArrow(load),m.FadeIn(loadtxt),seconds=2.1)
        self.run(m.FadeIn(start),m.FadeIn(tip),seconds=1.5)
        desc=txt("¿Qué permite moverse cada extremo?",0,-1.65,29,C["gold"])
        self.run(m.FadeIn(desc),seconds=1.3)
        self.finish()

        self.chapter(1)
        fixed=m.Dot(point=[LEFT,Y,0],radius=.11,color=C["gold"])
        constraints=txt("v(0) = 0           giro(0) = 0",-.15,-1.55,31,C["gold"])
        self.run(m.FadeOut(desc),m.FadeIn(fixed),m.FadeIn(constraints),seconds=2.2)
        cross1=line([LEFT-.29,Y-.28,0],[LEFT+.29,Y+.28,0],C["gold"],3)
        cross2=line([LEFT-.29,Y+.28,0],[LEFT+.29,Y-.28,0],C["gold"],3)
        self.run(m.Create(cross1),m.Create(cross2),seconds=1.7)
        arrow2=m.Arrow([RIGHT+0.65,1.26,0],[RIGHT+0.65,.22,0],
                        color=C["blue"],buff=0,stroke_width=5)
        move=txt("La punta SÍ puede desplazarse",1.8,-1.05,22,C["blue"])
        self.run(m.GrowArrow(arrow2),m.FadeIn(move),seconds=2.2)
        self.finish()

        self.chapter(2)
        reference=line(coord(0),coord(1),C["grid"],3)
        self.run(m.FadeOut(constraints),m.FadeOut(cross1),m.FadeOut(cross2),
                 m.FadeOut(arrow2),m.FadeOut(move),m.FadeOut(start),m.FadeOut(tip),
                 m.Create(reference),seconds=2.0)
        self.run(m.Transform(beam,deformed(1)),seconds=5.0)
        lower_load=m.Arrow([RIGHT,.92,0],[RIGHT,-.45,0],color=C["coral"],buff=0,stroke_width=7)
        self.run(m.Transform(load,lower_load),m.Transform(loadtxt,txt("P",RIGHT+.43,.36,28,C["coral"])),seconds=1.8)
        slope1=line([LEFT+.25,.60,0],[LEFT+1.9,.39,0],C["gold"],3)
        slope2=line([1.00,.03,0],[2.80,-.67,0],C["gold"],3)
        hint=txt("Tangentes: cada vez más inclinadas",0,-1.40,23,C["gold"])
        self.run(m.Create(slope1),m.Create(slope2),m.FadeIn(hint),seconds=3.0)
        self.finish()

        self.chapter(3)
        self.run(m.FadeOut(slope1),m.FadeOut(slope2),m.FadeOut(hint),seconds=1.5)
        legend1=txt("curvatura < 0",0,-1.18,32,C["coral"])
        legend2=txt("M = E I · v''",0,-1.77,32,C["gold"])
        self.run(m.FadeIn(legend1),m.FadeIn(legend2),seconds=2.6)
        leftdot=m.Dot(point=coord(.16,1),radius=.10,color=C["coral"])
        rightdot=m.Dot(point=coord(.87,1),radius=.10,color=C["blue"])
        leftlab=txt("Mayor curvatura",LEFT+1.40,1.85,20,C["coral"])
        rightlab=txt("Menor curvatura",RIGHT-1.25,.82,20,C["blue"])
        self.run(m.FadeIn(leftdot),m.FadeIn(rightdot),m.FadeIn(leftlab),m.FadeIn(rightlab),seconds=3.0)
        self.finish()

        self.chapter(4)
        self.run(m.FadeOut(legend1),m.FadeOut(legend2),m.FadeOut(leftdot),m.FadeOut(rightdot),
                 m.FadeOut(leftlab),m.FadeOut(rightlab),m.Transform(beam,line(coord(0),coord(1),C["grid"],4)),
                 m.Transform(load,m.Arrow([RIGHT,2.1,0],[RIGHT,.70,0],buff=0,color=C["coral"],stroke_width=7)),
                 m.Transform(loadtxt,txt("P",RIGHT+.43,1.65,28,C["coral"])),seconds=2.8)
        cutx=-1.55
        active=line([cutx,Y,0],[RIGHT,Y,0],C["teal"],9)
        cut=line([cutx,Y+1.07,0],[cutx,Y-1.18,0],C["gold"],3)
        v=m.Arrow([cutx,.78,0],[cutx,1.69,0],color=C["blue"],buff=0,stroke_width=7)
        labv=txt("+ V",cutx-.55,1.79,25,C["blue"])
        span=line([cutx,-.34,0],[RIGHT,-.34,0],C["muted"],3)
        ldim=txt("L − x",.9,-.72,26,C["gold"])
        self.run(m.Create(active),m.Create(cut),m.Create(span),m.FadeIn(ldim),seconds=3.0)
        self.run(m.GrowArrow(v),m.FadeIn(labv),seconds=2.0)
        eq=txt("M(x) = −P(L − x)",0,-1.70,34,C["coral"])
        sign=txt("El momento equilibrante es ANTIHORARIO",0,-2.30,24,C["gold"])
        self.run(m.FadeIn(eq),m.FadeIn(sign),seconds=2.5)
        self.finish()

        self.chapter(5)
        self.run(m.FadeOut(active),m.FadeOut(cut),m.FadeOut(v),m.FadeOut(labv),m.FadeOut(span),
                 m.FadeOut(ldim),m.FadeOut(eq),m.FadeOut(sign),seconds=2.3)
        mbase=-1.83
        maxh=.92
        maxm=txt("− P L",LEFT+.52,-.68,23,C["coral"])
        free=txt("0",RIGHT+.26,-1.83,24,C["muted"])
        mname=txt("M(x) NEGATIVO",-.9,-.76,23,C["coral"])
        axis=line([LEFT,mbase,0],[RIGHT,mbase,0],C["muted"],3)
        area=m.Polygon([LEFT,mbase,0],[LEFT,mbase+maxh,0],[RIGHT,mbase,0],
                       color=C["coral"],fill_color=C["coral"],fill_opacity=.21,stroke_width=4)
        self.run(m.Create(axis),seconds=1.2)
        self.run(m.Create(area),seconds=4.0)
        self.run(m.FadeIn(maxm),m.FadeIn(free),m.FadeIn(mname),seconds=1.6)
        note=txt("Convención: positivo BAJO el eje",0,-2.63,23,C["gold"])
        self.run(m.FadeIn(note),seconds=1.4)
        self.finish()

        self.chapter(6)
        self.run(m.FadeOut(note),seconds=1.5)
        vbase=-2.73
        vs=line([LEFT,vbase,0],[RIGHT,vbase,0],C["muted"],3)
        va=m.Polygon([LEFT,vbase,0],[LEFT,vbase+.47,0],[RIGHT,vbase+.47,0],[RIGHT,vbase,0],
                     color=C["blue"],fill_color=C["blue"],fill_opacity=.22,stroke_width=3)
        vname=txt("V(x) = +P",.05,-2.46,25,C["blue"])
        self.run(m.Create(vs),m.Create(va),seconds=3.3)
        self.run(m.FadeIn(vname),seconds=1.3)
        relation=txt("dM / dx = V = + P",0,.02,26,C["gold"])
        self.run(m.FadeIn(relation),seconds=1.6)
        self.finish()

        self.chapter(7)
        recap=txt("RESTRICCIONES    →    CURVATURA    →    M    →    V",0,1.85,24,C["gold"])
        self.run(m.FadeOut(relation),m.FadeIn(recap),seconds=2.0)
        final=txt("Comprender el equilibrio evita memorizar dibujos.",0,-.29,25,C["teal"])
        self.run(m.FadeIn(final),seconds=2.0)
        self.finish()
