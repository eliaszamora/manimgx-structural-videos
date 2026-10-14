"""Twenty-one beat cinematographic P-M lecture, ManimGX native.

Render in parallel 5 acts: PM_ACT_INDEX=0..4, then stitch with one Kokoro
master voice from story.py. Never fake a stress state: model.analyze(c) owns
strain, concrete Whitney block, steel stress and section resultants.

No slide titles. Axial P>0 compression; M>0 compression on upper face.
Volume coordinates: x horizontal, y through section depth, z member axis.
"""
import os,sys,math
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).parent))
from model import S, analyze, points, find_pure_bending
from story import BEATS
import manimgx as m

BG="#0A101D"; WHITE="#EDF2FB"; SOFT="#A9B9CC"; GRID="#243849"
CONCRETE="#4DD7D2"; STEEL="#F6C969"; COMP="#FF9B70"
TENS="#7CB4FF"; AXIS="#FCE08E"
SECTION_W=3.55
VOLUME_W=3.62
RANGE_P=(-900.,4700.); RANGE_M=(-20.,360.)
ACTS=((0,4),(4,10),(10,13),(13,19),(19,21))
ACT_INDEX=int(os.environ.get("PM_ACT_INDEX","0"))
assert 0 <= ACT_INDEX < len(ACTS)

def txt(s,x=0,y=0,size=27,color=WHITE):
    return m.Text(str(s),font="Noto Sans",font_size=size,color=color).move_to([x,y,0])

def ln(p,q,color=SOFT,w=2):
    return m.Line([p[0],p[1],0],[q[0],q[1],0],stroke_width=w,color=color)

def rect(w,h,x,y,fill=BG,opacity=.0,color=CONCRETE,stroke=2):
    return m.Rectangle(width=w,height=h,fill_color=fill,fill_opacity=opacity,
             stroke_color=color,stroke_width=stroke).move_to([x,y,0])

def animate_section(c,center=(-2.66,.12),w=SECTION_W,include_neutral=True,include_bar=True):
    """A true scaled section tied to model: no painted fictional concrete."""
    rr=analyze(c); cx,cy=center
    top=cy+w/2
    grp=m.VGroup(rect(w,w,cx,cy,fill="#234353",opacity=.18))
    h=w*rr["a"]/S.h
    if h>0.001:
        grp.add(rect(w-.025,h,cx,top-h/2,fill=COMP,opacity=.25,color=COMP,stroke=0))
    if include_neutral and c<=S.h:
        ny=top-w*c/S.h
        grp.add(ln([cx-w/2-.15,ny],[cx+w/2+.15,ny],AXIS,3))
    if include_bar:
        for j,y in enumerate((S.dp,S.dt)):
            sy=top-w*y/S.h
            col=COMP if rr["steel"][j]["eps"]>=0 else TENS
            for sx in np.linspace(cx-w*(.5-S.dp/S.b),cx+w*(.5-S.dp/S.b),4):
                grp.add(m.Dot(point=[sx,sy,0],radius=.078,color=col))
    return grp

def animate_strain(c,origin=(2.05,.12),height=SECTION_W,scale=110.):
    """True linear strain profile; extrema are NOT silently clamped."""
    cx,cy=origin
    top=cy+height/2
    low=cy-height/2
    eb=S.eps_cu*(c-S.h)/c
    if abs(eb)> .030:
        # Change of plotting scale is explicit; not a silent clamp.
        scale=min(scale,.85/max(abs(eb),.003))
    group=m.VGroup(ln([cx,top+.15],[cx,low-.15],SOFT,2))
    xt=cx+scale*S.eps_cu
    xb=cx+scale*eb
    group.add(ln([xt,top],[xb,low],AXIS,4))
    group.add(ln([cx,top],[xt,top],COMP,3))
    group.add(m.Dot(point=[xt,top,0],radius=.065,color=COMP))
    group.add(m.Dot(point=[xb,low,0],radius=.065,color=COMP if eb>=0 else TENS))
    group.add(txt("ε = 0",cx-.50,low-.38,21,SOFT))
    return group

def steel_indicator(c):
    # Same bottom bar strain as the section; follows linear branch then yield plateau.
    strain=analyze(c)["steel"][-1]["eps"]
    ey=S.eps_y
    pos=max(-1.30,min(1.30,.42*strain/ey))
    stress=max(-1.,min(1.,strain/ey))
    return m.Dot(point=[2.03+pos,-.1+1.04*stress,0],
                 radius=.105,color=COMP if stress>=0 else TENS)

def steel_law():
    g=m.VGroup()
    cx,cy=2.03,-.1; wx=3.3;hy=3.2
    g.add(ln([cx-wx/2,cy],[cx+wx/2,cy],SOFT,2))
    g.add(ln([cx,cy-hy/2],[cx,cy+hy/2],SOFT,2))
    g.add(ln([cx-1.30,cy-1.04],[cx-.42,cy-1.04],TENS,4))
    g.add(ln([cx-.42,cy-1.04],[cx+.42,cy+1.04],STEEL,4))
    g.add(ln([cx+.42,cy+1.04],[cx+1.30,cy+1.04],COMP,4))
    g.add(txt("σs",cx-.18,cy+1.74,24,SOFT))
    g.add(txt("εs",cx+1.66,cy-.24,24,SOFT))
    g.add(txt("fy",cx+1.15,cy+1.30,22,COMP))
    return g

def moment_arms(c):
    """Visual lever arms measured about the geometric centroid of the section."""
    rr=analyze(c)
    cx,cy=-2.70,.13
    w=5.15;top=cy+w/2
    ys=[top-w*S.dp/S.h, top-w*rr['a']/(2*S.h),top-w*S.dt/S.h]
    x=.18
    result=m.VGroup(ln([x,cy-2.65],[x,cy+2.65],SOFT,2))
    result.add(m.Dot(point=[x,cy,0],radius=.07,color=AXIS))
    for j,y in enumerate(ys):
        if j==1:col=COMP;mark="zCc"
        else:col=STEEL;mark="z"+str(j)
        result.add(ln([x,cy],[x,y],col,3))
        result.add(ln([x-.15,y],[x+.15,y],col,2))
        # Place dimension text away from closely spaced upper forces.
        if j in (0,2):
            result.add(txt(mark,x-.48,(y+cy)/2,19,col))
    return result

def force_vectors(c):
    """Arrows tied to physical positions and net internal forces (kN)."""
    rr=analyze(c)
    top=.13+5.15/2
    cx=.86
    grp=m.VGroup()
    for j,v in enumerate(rr["steel"]):
        y=top-5.15*v["y"]/S.h
        F=v["force_kN"];length=min(2.30,.30+abs(F)/190)
        endpoint=cx+length*(1 if F>=0 else -1)
        col=COMP if F>=0 else TENS
        grp.add(m.Arrow([cx,y,0],[endpoint,y,0],buff=0,color=col,stroke_width=7))
        labelx=endpoint+.33 if F>=0 else endpoint-.40
        labely=y+.23 if j==0 else y-.24
        grp.add(txt("Fs"+str(j+1),labelx,labely,21,col))
    Cc=rr["Cc_kN"]; y=top-5.15*rr["a"]/(2*S.h)
    length=min(2.55,.50+Cc/1050)
    endpoint=cx+length
    grp.add(m.Arrow([cx,y,0],[endpoint,y,0],buff=0,color=COMP,stroke_width=8))
    grp.add(txt("Cc",endpoint+.35,y-.28,23,COMP))
    return grp

def chart_coord(M,P):
    x=-4.80 + 9.4*(M-RANGE_M[0])/(RANGE_M[1]-RANGE_M[0])
    y=-2.12 + 4.40*(P-RANGE_P[0])/(RANGE_P[1]-RANGE_P[0])
    return [x,y,0]

def curve_object(which="nominal"):
    dat=list(reversed(points(510)))
    coords=[chart_coord(r["Mn"],r["Pn"]) if which=="nominal" else
            chart_coord(r["phiMn"],r["phiPn"]) for r in dat]
    line=m.VMobject(color=CONCRETE if which=="nominal" else COMP,stroke_width=5)
    line.set_points_smoothly(coords)
    return line

def chart_axes():
    g=m.VGroup()
    xa=chart_coord(0,0)[0];ya=chart_coord(0,0)[1]
    g.add(ln([xa,-2.28],[xa,2.39],SOFT,3))
    g.add(ln([-4.90,ya],[4.80,ya],SOFT,3))
    for p in (0,1000,2000,3000,4000):
        y=chart_coord(0,p)[1]
        g.add(ln([-4.80,y],[4.70,y],GRID,1))
    for mm in (100,200,300):
        x=chart_coord(mm,0)[0]
        g.add(ln([x,-2.21],[x,2.36],GRID,1))
    g.add(txt("P (kN)",-4.00,2.65,22,SOFT))
    g.add(txt("M (kN·m)",3.38,-2.55,21,SOFT))
    return g

def plot_dot(c,phi=False):
    z=analyze(c)
    P=z["phiPn"] if phi else z["Pn"]
    M=z["phiMn"] if phi else z["Mn"]
    return m.Dot(point=chart_coord(M,P),radius=.118,color=AXIS)

def volume_geometry():
    base=np.array([-.45,0.,-.25])
    def v(x,y,z):return base+np.array([x,y,z])
    solid=m.Prism(dimensions=[VOLUME_W,VOLUME_W,5.65],
                  fill_color=CONCRETE,fill_opacity=.15,
                  stroke_color=CONCRETE,stroke_width=1.4).move_to(base)
    bars=m.Group()
    r=VOLUME_W*(.5-S.dp/S.h)
    for y in (-r,r):
        for x in np.linspace(-r,r,4):
            b=m.Cylinder(radius=.075,height=5.55,direction=m.Z_AXIS,
                        resolution=(12,6),checkerboard_colors=False,
                        fill_color=STEEL,fill_opacity=1,stroke_width=0)
            b.move_to(v(x,y,0))
            bars.add(b)
    ties=m.Group()
    half=VOLUME_W/2-.16
    for z in np.linspace(-2.55,2.55,9):
        tie=m.Polygon(*[v(x,y,z) for x,y in
                      [(-half,-half),(half,-half),(half,half),(-half,half)]],
                        stroke_width=2,fill_opacity=0,color=CONCRETE)
        ties.add(tie)
    load=m.Arrow3D(v(0,0,3.88),v(0,0,2.85),color=COMP,thickness=.07)
    m.Group(solid,bars,ties,load).scale(1.10,about_point=base)
    return solid,bars,ties,load,base

class PeliculaInteraccionPM(m.ThreeDScene):
    def show(self,*obj):
        # Deferred registration: never flash explanatory objects before their beat.
        if not hasattr(self,"_fixed_pending"):
            self._fixed_pending={}
            self._fixed_registered=set()
        for item in obj:self._fixed_pending[id(item)]=item
        return obj
    def play_for(self,i,ops):
        """Use narration slot exactly; no unintended static holds."""
        total=sum(seconds for seconds,_ in ops)
        dur=BEATS[i]["duration"]
        if total>dur:raise ValueError(f"Beat {i+1}: animation overrun")
        factor=(dur-.5)/total
        elapsed=0.
        for seconds,anims in ops:
            seconds*=factor
            if anims is None:
                self.wait(seconds)
            else:
                for animation in anims:
                    ob=getattr(animation,"mobject",None)
                    if ob is not None and id(ob) in getattr(self,"_fixed_pending",{}) and id(ob) not in self._fixed_registered:
                        self.add_fixed_in_frame_mobjects(ob)
                        self._fixed_registered.add(id(ob))
                self.play(*anims,run_time=seconds)
            elapsed+=seconds
        remaining=dur-elapsed
        if remaining < -.01:raise ValueError(f"Beat {i+1}: clock mismatch")
        if remaining>0:self.wait(remaining)
    def construct(self):
        self.camera.background_color=BG
        self.set_camera_orientation(phi=64*m.DEGREES,theta=-51*m.DEGREES)
        self.add(m.SunLight(3*m.UP+2*m.OUT),m.AmbientLight(intensity=.65))
        start,end=ACTS[ACT_INDEX]
        if ACT_INDEX==0:self.act_volume(start,end)
        elif ACT_INDEX==1:self.act_compatibility(start,end)
        elif ACT_INDEX==2:self.act_equilibrium(start,end)
        elif ACT_INDEX==3:self.act_interaction(start,end)
        elif ACT_INDEX==4:self.act_limitations(start,end)

    def act_volume(self,start,end):
        solid,bars,ties,load,base=volume_geometry()
        detail=txt("400 × 400 mm   ·   8 Ø16",2.3,-2.62,26,SOFT)
        centroid=txt("P",1.8,1.90,29,COMP)
        moment=txt("M = P · e",2.36,-2.32,34,AXIS)
        sec=animate_section(220,center=(1.45,0),w=3.1)
        self.show(detail,centroid)
        self.play_for(0,[
            (5,[m.FadeIn(solid)]),(7,[m.FadeIn(bars)]),
            (5,[m.FadeIn(ties)]),(5,[m.FadeIn(load)]),
            (5,[m.FadeIn(centroid)]),
            (14,[m.FadeIn(detail)]),(5,None)])
        self.show(moment)
        if os.environ.get("PM_SMOKE")=="1":return
        self.play_for(1,[
            (6,[load.animate.shift(.5*m.UP)]),
            (8,[m.FadeIn(moment)]),
            (9,[m.FadeOut(detail)]),
            (10,[m.FadeOut(centroid)]),(10,[m.FadeIn(detail)])])
        self.show(sec);
        self.play_for(2,[
            (8,[solid.animate.shift(1.50*m.LEFT),bars.animate.shift(1.50*m.LEFT),
                 ties.animate.shift(1.50*m.LEFT),load.animate.shift(1.50*m.LEFT)]),
            (8,[m.FadeIn(sec)]),(12,[m.FadeOut(moment)]),
            (12,[m.FadeOut(sec)]),(10,[m.FadeIn(sec)])])
        # Changing from 3D to orthographic section is deliberately tied to narration.
        self.play_for(3,[
            (7,[m.FadeOut(solid),m.FadeOut(ties)]),
            (9,[m.FadeIn(solid)]),
            (9,[m.FadeOut(detail)]),
            (10,[m.FadeOut(sec)]),
            (8,[m.FadeIn(sec)])])

    def act_compatibility(self,start,end):
        c=m.ValueTracker(290.)
        sec=m.always_redraw(lambda:animate_section(c.get_value(),center=(-3.12,.08),w=5.05))
        strain=m.always_redraw(lambda:animate_strain(c.get_value(),origin=(2.65,.08),height=5.05))
        law=steel_law().scale(1.38).shift([.15,0,0])
        steelpoint=m.always_redraw(lambda:steel_indicator(c.get_value()))
        blocknote=txt("a = β1 c",2.0,-2.45,33,AXIS)
        epsnote=txt("εs(y) = 0,003 (c − y) / c",.55,-2.54,30,AXIS)
        force_note=txt("Cc = 0,85 f'c · b · a",.45,-2.55,31,COMP)
        bar_note=txt("− hormigón desplazado por el acero",.55,-2.57,27,SOFT)
        self.show(sec,strain,law,steelpoint,blocknote,epsnote,force_note,bar_note)
        
        
        self.play_for(4,[
            (8,[m.FadeIn(sec)]),(14,[m.FadeIn(strain)]),
            (17,[c.animate.set_value(240)]),(7,[c.animate.set_value(290)])])
        self.play_for(5,[
            (14,[c.animate.set_value(195)]),
            (13,[c.animate.set_value(265)]),
            (14,[c.animate.set_value(206)])])
        self.play_for(6,[
            (10,[m.FadeIn(epsnote)]),
            (16,[c.animate.set_value(135)]),
            (16,[c.animate.set_value(245)]),
            (6,[c.animate.set_value(185)])])
        self.play_for(7,[
            (8,[m.FadeOut(strain),m.FadeOut(epsnote)]),
            (12,[m.FadeIn(law),m.FadeIn(steelpoint)]),
            (16,[c.animate.set_value(155)]),
            (13,[c.animate.set_value(245)])])
        self.play_for(8,[
            (10,[m.FadeOut(law),m.FadeOut(steelpoint)]),(8,[m.FadeIn(strain)]),
            (10,[m.FadeIn(blocknote)]),
            (13,[c.animate.set_value(185)]),
            (12,[c.animate.set_value(290)])])
        self.play_for(9,[
            (11,[m.FadeOut(blocknote)]),(10,[m.FadeIn(force_note)]),
            (13,[c.animate.set_value(58.8235294)]),
            (11,[c.animate.set_value(290)]),
            (7,[m.FadeOut(force_note),m.FadeIn(bar_note)])])

    def act_equilibrium(self,start,end):
        c=m.ValueTracker(250.)
        sec=m.always_redraw(lambda:animate_section(c.get_value(),center=(-2.70,.13),w=5.15))
        forces=m.always_redraw(lambda:force_vectors(c.get_value()))
        arms=m.always_redraw(lambda:moment_arms(c.get_value()))
        Pnote=txt("Pn = Cc + Σ Fs",.8,-2.55,35,AXIS)
        Mnote=txt("Mn = Σ Fi · zi",.85,-2.55,35,AXIS)
        bal=txt("εt = − εy",1.43,-2.50,33,TENS)
        self.show(sec,forces,arms,Pnote,Mnote,bal)
        
        self.play_for(10,[
            (7,[m.FadeIn(sec)]),(9,[m.FadeIn(forces)]),
            (10,[m.FadeIn(Pnote)]),
            (11,[c.animate.set_value(150)]),
            (8,[c.animate.set_value(250)])])
        self.play_for(11,[
            (8,[m.FadeOut(Pnote)]),(9,[m.FadeIn(Mnote),m.FadeIn(arms)]),
            (13,[c.animate.set_value(175)]),
            (12,[c.animate.set_value(315)])])
        self.play_for(12,[
            (10,[m.FadeOut(Mnote),m.FadeOut(arms)]),
            (9,[m.FadeIn(bal)]),
            (18,[c.animate.set_value(S.balanced_c)]),
            (11,[c.animate.set_value(165)])])

    def act_interaction(self,start,end):
        axes=chart_axes()
        curve=curve_object()
        phi_curve=curve_object("design");
        c=m.ValueTracker(1800.)
        dot=m.always_redraw(lambda:plot_dot(c.get_value()))
        design_dot=m.always_redraw(lambda:plot_dot(c.get_value(),phi=True))
        nominal=txt("resistencia nominal",2.90,2.40,23,CONCRETE)
        design=txt("φPn, φMn",3.15,1.84,25,COMP)
        pure=txt("Pn = 0",2.0,-2.54,28,AXIS)
        cap=txt("0,80 φPo",-1.95,2.53,25,COMP)
        tension=txt("Pt = − Ast fy",-1.55,-2.56,26,TENS)
        demandA=m.Dot(point=chart_coord(130,850),radius=.115,color=STEEL)
        demandB=m.Dot(point=chart_coord(320,2100),radius=.115,color=TENS)
        for ob in (axes,dot,design_dot,curve,phi_curve,nominal,design,pure,cap,tension,demandA,demandB):
            self.show(ob)

        self.play_for(13,[
            (7,[m.FadeIn(axes)]),(14,[m.Create(curve)]),
            (9,[m.FadeIn(dot)]),
            (17,[c.animate.set_value(145)])])
        self.play_for(14,[
            (9,[m.FadeIn(nominal)]),
            (11,[c.animate.set_value(4000)]),
            (9,[m.FadeIn(cap)]),
            (16,[c.animate.set_value(600)])])
        # Bisection defines the actual zero axial section state.
        cb=find_pure_bending()["c"]
        self.play_for(15,[
            (8,[m.FadeOut(cap)]),(8,[m.FadeIn(pure)]),
            (23,[c.animate.set_value(cb)]),
            (10,[c.animate.set_value(cb*1.1)])])
        self.play_for(16,[
            (7,[m.FadeOut(pure)]),
            (12,[c.animate.set_value(22)]),
            (10,[m.FadeIn(tension)]),
            (10,[c.animate.set_value(1.0)])])
        # Design curve is not a uniform homothety; phi depends on extreme steel strain.
        self.play_for(17,[
            (9,[m.FadeOut(tension)]),
            (15,[m.FadeIn(phi_curve)]),
            (12,[m.FadeIn(design),m.FadeOut(dot),m.FadeIn(design_dot)]),
            (14,[c.animate.set_value(195)])])
        self.play_for(18,[
            (8,[m.FadeOut(nominal)]),
            (9,[m.FadeIn(demandA)]),
            (10,[m.FadeIn(demandB)]),
            (14,[c.animate.set_value(265)])])

    def act_limitations(self,start,end):
        solid,bars,ties,load,base=volume_geometry()
        # Blue deformed centroidal line is schematic, NOT a calculated buckling mode.
        bending=m.VMobject(color=TENS,stroke_width=7)
        B=[]
        for u in np.linspace(0,1,80):
            z=(-2.78+5.56*u)*1.25
            dy=(.95*(3*u*u-2*u*u*u))*1.25
            B.append(base+np.array([0,dy,z]))
        bending.set_points_smoothly(B)
        schematic=txt("deformada esquemática, amplificada",2.52,1.16,21,SOFT)
        delta=txt("P–Δ",2.75,1.75,41,AXIS)
        mx=txt("Mx",2.60,-.30,37,COMP)
        my=txt("My",4.00,-.30,37,TENS)
        caution=txt("La interacción uniaxial no verifica la estabilidad",.15,-2.54,26,SOFT)
        self.show(delta,mx,my,caution,schematic)

        self.play_for(19,[
            (10,[m.FadeIn(solid),m.FadeIn(bars)]),
            (9,[m.FadeIn(load)]),
            (13,[m.FadeIn(delta),m.Create(bending),m.FadeIn(schematic)]),
            (9,[m.FadeIn(mx),m.FadeIn(my)])])
        c=m.ValueTracker(220.)
        sec=m.always_redraw(lambda:animate_section(c.get_value(),center=(2.65,0),w=2.8))
        self.show(sec);
        self.play_for(20,[
            (8,[m.FadeOut(mx),m.FadeOut(my),m.FadeOut(delta),m.FadeOut(bending),m.FadeOut(schematic)]),
            (11,[m.FadeIn(sec)]),
            (16,[c.animate.set_value(150)]),
            (12,[c.animate.set_value(280)]),
            (8,[m.FadeIn(caution)])])
