"""ManimGX adapters. Analytical / sign data are supplied by model.py only."""
import manimgx as m
from .style import STYLE

def label(txt,x,y,size=29,color=None):
    return m.Text(txt,font_size=size,color=color or STYLE.ink).move_to([x,y,0])

def segment(a,b,color=None,width=4):
    return m.Line([*a[:2],0],[*b[:2],0],color=color or STYLE.steel,stroke_width=width)

def curve(points,color=None,width=6):
    pts=[[x,y,0] for x,y in points]
    if len(pts)==2:return segment(pts[0],pts[1],color,width)
    p=m.VMobject(color=color or STYLE.deformed,stroke_width=width)
    p.set_points_smoothly(pts)
    return p

def supports(at,size=.43):
    px,py=at
    mark=m.Rectangle(width=.16,height=.65,fill_color=STYLE.steel,fill_opacity=1,stroke_color=STYLE.steel).move_to([px-.07,py-.04,0])
    hashes=[segment((px-.4+k*.19,py-.42),(px-.19+k*.19,py-.64),STYLE.muted,2) for k in range(4)]
    return m.VGroup(mark,*hashes)

def split_signed_plot(member,kind,convert,maxval=None,scale=.5):
    """Render sign-separated diagram in member-local coordinates.

    Explicit zero crossings prevent spurious color changes between samples.
    Positive = clockwise normal of member local x; negative = counterclockwise.
    """
    values=[getattr(s,kind) for s in member.samples]
    pts=member.offset_curve(kind,size=scale,reference=maxval)
    pieces=[]
    for i in range(len(pts)-1):
        p,q=pts[i],pts[i+1]
        v,w=values[i],values[i+1]
        if v*w<0:
            t=-v/(w-v)
            middle=(p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t)
            pieces += [segment(convert(p),convert(middle),STYLE.moment_positive if v>0 else STYLE.moment_negative,5),
                       segment(convert(middle),convert(q),STYLE.moment_positive if w>0 else STYLE.moment_negative,5)]
        else:
            pieces.append(segment(convert(p),convert(q),
                           STYLE.moment_positive if (v+w)>=0 else STYLE.moment_negative,5))
    return m.VGroup(*pieces)

def diagram_panel(member,kind,x=2.1,y=-1.58,length=2.6,amplitude=.92):
    """Separate panel, vertical axis base-to-top, positive local M to right."""
    base=segment((x,y),(x,y+length),STYLE.steel,3)
    values=[getattr(s,kind) for s in member.samples]
    maxv=max(max(abs(v) for v in values),1e-9)
    points=[(x+amplitude*v/maxv, y+length*s.t) for s,v in zip(member.samples,values)]
    out=[base]
    for i in range(len(points)-1):
        aa=values[i];bb=values[i+1]
        if aa*bb<0:
            t=-aa/(bb-aa)
            at=(points[i][0]+t*(points[i+1][0]-points[i][0]),points[i][1]+t*(points[i+1][1]-points[i][1]))
            out.append(segment(points[i],at,STYLE.moment_positive if aa>0 else STYLE.moment_negative,5))
            out.append(segment(at,points[i+1],STYLE.moment_positive if bb>0 else STYLE.moment_negative,5))
        else:
            out.append(segment(points[i],points[i+1],STYLE.shear if kind=='V' else STYLE.moment_positive if aa+bb>=0 else STYLE.moment_negative,5))
    zeros=member.zeros(kind)
    for z in zeros:
        if z>1e-7 and z<1-1e-7:
            out.append(m.Dot(point=[x,y+z*length,0],radius=.095,color=STYLE.inflection))
    out.append(label('+' if kind=='M' else 'V local',x+1.10,y+length+.22,size=23,color=STYLE.moment_positive if kind=='M' else STYLE.shear))
    if kind=='M':out.append(label('−',x-.58,y+length+.22,size=23,color=STYLE.moment_negative))
    return m.VGroup(*out)
