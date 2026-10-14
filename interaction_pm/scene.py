"""Escena ManimGX nativa para las 21 etapas de flexocompresión uniaxial.
Mismo motor que el repositorio; geometría y posiciones del marcador salen de model.py.
No asumir render verificado hasta ejecutar el flujo y revisar fotogramas.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from model import S, analyze, points
from story import BEATS, TOTAL_SECONDS
import manimgx as m

C={"bg":"#081321","text":"#F4F7FD","muted":"#A9BBCF","grid":"#29455D",
   "teal":"#4FE5C6","orange":"#FFA16D","blue":"#79B5FF","gold":"#FFD58D"}

def label(s,x=0,y=0,sz=26,color="text"):
    return m.Text(str(s),font="Noto Sans",font_size=sz,color=C.get(color,color)).move_to([x,y,0])

def seg(x1,y1,x2,y2,color="grid",width=3):
    return m.Line([x1,y1,0],[x2,y2,0],color=C.get(color,color),stroke_width=width)

def axis_point(M,P):
    # M from 0 to 350 kNm, P from -800 to +4800 kN
    return [0.9+4.42*M/350,-1.74+3.44*(P+800)/5600,0]

DATA=points(480)

def chart_line(key_M,key_P,color):
    out=m.VMobject(color=C[color],stroke_width=5)
    out.set_points_smoothly([axis_point(z[key_M],z[key_P]) for z in DATA])
    return out

def cap_c(v):
    return max(.05,float(v))

def strain_profile(c):
    top_y=1.64;bot_y=-1.64;zero=-1.25
    # Positive compression to the right, tension to the left.
    top_x=-.52
    bottom_eps=S.eps_cu*(c-S.h)/c
    bottom_x=max(-1.95,min(.20,zero+.73*bottom_eps/S.eps_cu))
    return seg(top_x,top_y,bottom_x,bot_y,"gold",5)

def make_bar(i,c,xx,yy):
    r=analyze(c)
    stress=r["steel"][i]["eps"]
    return m.Dot([xx,yy,0],radius=.105,color=C["orange"] if stress>0 else C["blue"])

FORMULAS=[
 "La pregunta: resistencia simultánea P y M", "M = P · e",
 "(Mn, Pn): un estado de deformaciones", "b = h = 400 mm   |   8 barras Ø16",
 "Compatibilidad + material + equilibrio",
 "c: profundidad del eje neutro",
 "εs(y) = 0,003 (c − y) / c",
 "εy = fy / Es = 0,0021",
 "a = β1 c   |   Cc = 0,85 f'c b a",
 "Fs = As (fs − 0,85 f'c) dentro del bloque",
 "Pn = Cc + Σ Fs",
 "Mn = Cc (h/2 − a/2) + Σ Fs (h/2 − y)",
 "cb = dt · 0,003 / (0,003 + εy)",
 "Variar c → variar ε, fuerzas, P y M",
 "Po = 0,85 f'c (Ag−Ast) + fy Ast",
 "Pn = 0 → Mn aún puede ser positivo",
 "Pt = −Ast fy   |   Mn = 0",
 "φ: 0,65 en compresión → 0,90 en tracción",
 "(Pu, Mu) frente a (φPn, φMn)",
 "Esbeltez P–Δ, P–Mx–My y detallamiento",
 "c → ε → fs, Cc → Pn, Mn → φ → verificar"
]
FOCUS_C=[400,600,235,205,380,270,245,150,230,205,190,175,
         S.balanced_c,1000,3500,130,40,170,115,170,S.balanced_c]

class DiagramaInteraccionPM(m.Scene):
    def construct(self):
        self.camera.background_color=C["bg"]
        eyebrow=label("INGENIERÍA ESTRUCTURAL   ·   FLEXOCOMPRESIÓN",0,3.69,19,"muted")
        head=label("¿QUÉ ES EL DIAGRAMA P–M?",0,3.10,32)
        foot=label(BEATS[0]["caption"],0,-3.35,20,"muted")
        formula=label(FORMULAS[0],0,-2.70,28,"gold")
        rule=seg(-5.8,2.64,5.8,2.64,"grid",2)
        self.add(eyebrow,head,rule,foot,formula)
        # Central section 400x400 mm, x=-4.0, bar layers 50 and 350 mm
        square=m.Rectangle(width=2.25,height=3.28,stroke_color=C["teal"],
                           stroke_width=5,fill_color="#103147",fill_opacity=.40).move_to([-4.06,0,0])
        stirrup=m.Rectangle(width=2.02,height=3.03,stroke_color=C["muted"],stroke_width=2).move_to([-4.06,0,0])
        self.add(square,stirrup,label("b = 400 mm",-4.07,2.02,20,"muted"))
        ctracker=m.ValueTracker(float(FOCUS_C[0]))
        bar_groups=[]
        for j,y in enumerate([1.23,-1.23]):
            for x in [-4.91,-4.36,-3.81,-3.26]:
                obj=m.always_redraw(lambda x=x,y=y,j=j: make_bar(j,cap_c(ctracker.get_value()),x,y))
                bar_groups.append(obj)
        self.add(*bar_groups)
        neutral=m.always_redraw(lambda: seg(-5.27,1.64-3.28*cap_c(ctracker.get_value())/400,
                                            -2.85,1.64-3.28*cap_c(ctracker.get_value())/400,
                                            "gold",3))
        profile=m.always_redraw(lambda: strain_profile(cap_c(ctracker.get_value())))
        axis_zero=seg(-1.25,1.68,-1.25,-1.68,"muted",2)
        self.add(neutral,axis_zero,profile,label("ε = 0",-1.54,-2.04,20,"muted"))
        # The graph stays present while every strain state moves the same marker.
        for P in [0,1000,2000,3000,4000]:
            Y=axis_point(0,P)[1]
            self.add(seg(.86,Y,5.5,Y,"grid",1))
        for MM in [0,100,200,300]:
            X=axis_point(MM,0)[0]
            self.add(seg(X,-1.79,X,1.8,"grid",1))
        self.add(seg(.85,-1.84,.85,1.82,"muted",3),
                 seg(.82,axis_point(0,0)[1],5.55,axis_point(0,0)[1],"muted",3),
                 label("P (kN)",1.2,2.05,22,"muted"),
                 label("M (kN·m)",4.7,-2.04,20,"muted"))
        nominal=chart_line("Mn","Pn","teal")
        design=chart_line("phiMn","phiPn","orange")
        self.add(nominal,design,
                 label("— nominal",3.7,2.23,18,"teal"),
                 label("— diseño",5.04,2.23,18,"orange"))
        marker=m.always_redraw(lambda:m.Dot(axis_point(analyze(cap_c(ctracker.get_value()))["Mn"],
                                                      analyze(cap_c(ctracker.get_value()))["Pn"]),
                                            radius=.14,color=C["gold"]))
        self.add(marker)
        assert len(BEATS)==len(FOCUS_C)==len(FORMULAS)
        for i,beat in enumerate(BEATS):
            used=0.0
            if i:
                new_head=label(f'{i+1:02d}   {beat["heading"]}',0,3.10,
                               31 if len(beat["heading"])<33 else 27)
                new_foot=label(beat["caption"],0,-3.35,20 if len(beat["caption"])<75 else 18,"muted")
                new_formula=label(FORMULAS[i],0,-2.70,27 if len(FORMULAS[i])<50 else 23,"gold")
                self.play(m.Transform(head,new_head),m.Transform(foot,new_foot),
                          m.Transform(formula,new_formula),run_time=1.6)
                used+=1.6
            if i==13:
                self.play(ctracker.animate.set_value(350),run_time=4)
                self.play(ctracker.animate.set_value(S.balanced_c),run_time=5)
                self.play(ctracker.animate.set_value(75),run_time=8)
                used+=17
            else:
                target=FOCUS_C[i]
                self.play(ctracker.animate.set_value(float(target)),run_time=4.3)
                used+=4.3
            # Three deliberate pauses for narration; formula and plot remain on screen.
            gap=beat["duration"]-used
            if gap<0:raise ValueError(f'Timing overrun chapter {i+1}')
            self.wait(gap)
        # Scene time is the voice track time. All 21 captions have shared clock.
