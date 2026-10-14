"""Pure geometric bridge: analytic PM calculation -> exact displayed locations.

No Manim imports: validation can compare 3D volume, cut section, strain diagram and
P-M marker before spending GPU/CPU render time. Input lengths are millimeters.
"""
from dataclasses import dataclass
from math import isfinite
try:
    from .model import S, analyze
except ImportError:
    from model import S, analyze

@dataclass(frozen=True)
class Geometry:
    section_size:float=3.14
    section_cx:float=3.24
    section_cy:float=.12
    volume_side:float=3.65
    strain_x0:float=5.13
    strain_y0:float=1.53
    strain_y1:float=-1.29
    strain_scale:float=.28/.003
    chart_xmin:float=-4.55
    chart_xlen:float=9.1
    chart_ymin:float=-2.25
    chart_ylen:float=4.5
    moment_scale:float=350.
    pmin:float=-720.
    pmax:float=4600.

G=Geometry()

def display_state(c,geom=G,s=S):
    """All geometry from ONE c; no silent epsilon clamping.

    The pilot's physical range is restricted to 100<=c<=350mm. A full-film
    viewport must rescale its strain axis (and visibly announce scale change)
    before approaching pure tension where epsilon diverges as c->0.
    """
    if not isfinite(c) or c<100 or c>350:
        raise ValueError('pilot visual state requires 100 <= c <= 350 mm')
    r=analyze(c,s)
    a=r['a']
    yneutral_3d=geom.volume_side/2-geom.volume_side*c/s.h
    yblock_3d=geom.volume_side/2-geom.volume_side*a/(2*s.h)
    blockdepth_3d=geom.volume_side*a/s.h
    top2d=geom.section_cy+geom.section_size/2
    yneutral_2d=top2d-geom.section_size*c/s.h
    blockdepth_2d=geom.section_size*a/s.h
    blockcenter_2d=top2d-blockdepth_2d/2
    eps_top=s.eps_cu
    eps_bot=s.eps_cu*(c-s.h)/c
    ex_top=geom.strain_x0+eps_top*geom.strain_scale
    ex_bot=geom.strain_x0+eps_bot*geom.strain_scale
    plotx=geom.chart_xmin+geom.chart_xlen*r['Mn']/geom.moment_scale
    ploty=geom.chart_ymin+geom.chart_ylen*(r['Pn']-geom.pmin)/(geom.pmax-geom.pmin)
    return dict(c=c,a=a,
                yneutral_3d=yneutral_3d, yblock_3d=yblock_3d,
                blockdepth_3d=blockdepth_3d,
                yneutral_2d=yneutral_2d,blockcenter_2d=blockcenter_2d,
                blockdepth_2d=blockdepth_2d,
                epsilon_top=eps_top,epsilon_bottom=eps_bot,
                strain_x_top=ex_top,strain_x_bottom=ex_bot,
                chart_x=plotx,chart_y=ploty,analysis=r)
