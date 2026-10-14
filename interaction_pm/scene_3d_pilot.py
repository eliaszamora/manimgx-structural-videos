"""Exploración visual 3D: una sección real, no diapositivas.
Piloto 24 s sin voz para verificar renderer antes de reelaborar clase entera.
"""
import manimgx as m
import numpy as np
from math import pi
BG="#0B0E17"; CYAN="#4DDAC7"; GOLD="#F2C967"; ORANGE="#F49A66"; BLUE="#6D9DFB"

class Columna3DPiloto(m.ThreeDScene):
    def construct(self):
        self.camera.background_color=BG
        self.set_camera_orientation(phi=70*m.DEGREES,theta=-53*m.DEGREES)
        # z: altura de columna; x/y: plano de la sección.
        concrete=m.Cube(side_length=2,fill_color=CYAN,fill_opacity=.12,
                        stroke_color=CYAN,stroke_width=1.4)
        concrete.stretch(1.8,2)
        concrete.shift([-1.6,0,0])
        rods=m.VGroup()
        for x,y in [(-.78,-.78),(-.26,-.78),(.26,-.78),(.78,-.78),
                    (-.78,.78),(-.26,.78),(.26,.78),(.78,.78)]:
            bar=m.Cylinder(radius=.055,height=3.55,resolution=(7,12),
                           fill_color=GOLD,fill_opacity=1,stroke_width=0)
            bar.shift([x-1.6,y,0])
            rods.add(bar)
        plane=m.Surface(lambda u,v: np.array([-1.6+u,v,0]),
                        u_range=[-1.0,1.0],v_range=[-1.0,1.0],
                        resolution=(6,6),fill_color=BLUE,fill_opacity=.24,stroke_width=0)
        # Minimal typography: no chapter title, no labels covering the object.
        caption=m.Text("Una columna resiste fuerza y flexión a la vez",
                       font_size=28,color="#E5EEF8").move_to([0,-3.3,0])
        self.add_fixed_in_frame_mobjects(caption)
        self.play(m.FadeIn(concrete),run_time=2)
        self.play(*[m.FadeIn(b) for b in rods],run_time=3)
        self.move_camera(phi=58*m.DEGREES,theta=-18*m.DEGREES,run_time=4)
        self.play(m.FadeIn(plane),run_time=2)
        self.move_camera(phi=68*m.DEGREES,theta=-65*m.DEGREES,run_time=4)
        self.wait(2)
        self.play(m.FadeOut(plane),run_time=2)
        self.wait(5)
