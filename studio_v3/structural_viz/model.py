"""Deterministic structural-to-scene contract; no manimgx dependency.

Member local x runs from node i to j. Local y points left of this axis.
Positive local bending is drawn on the CLOCKWISE normal (right of local x),
negative on the left. For horizontal left-to-right beams, positive is below.
Treat the *shape* convention separately from face-of-cut force arrows.
"""
from dataclasses import dataclass
from math import hypot, isfinite

@dataclass(frozen=True)
class Sample:
    x: float
    y: float
    displacement_x: float
    displacement_y: float
    M: float
    V: float
    t: float

@dataclass(frozen=True)
class Member:
    name: str
    start: tuple[float,float]
    end: tuple[float,float]
    samples: tuple[Sample,...]
    def __post_init__(self):
        if len(self.samples)<2: raise ValueError('at least 2 samples')
        if hypot(self.end[0]-self.start[0], self.end[1]-self.start[1])<1e-8: raise ValueError('zero length')
        if any(not isfinite(s.M) or not isfinite(s.V) for s in self.samples): raise ValueError('invalid force')
        if any(self.samples[i].t>self.samples[i+1].t for i in range(len(self.samples)-1)):
            raise ValueError('unordered sample')
    @property
    def normal(self):
        dx,dy=self.end[0]-self.start[0],self.end[1]-self.start[1]
        length=hypot(dx,dy)
        return (dy/length,-dx/length) # clockwise relative to local x
    @property
    def length(self):
        return hypot(self.end[0]-self.start[0],self.end[1]-self.start[1])
    def zeros(self,kind='M'):
        vals=[getattr(s,kind) for s in self.samples]
        result=[]
        for a,b,sa,sb in zip(vals[:-1], vals[1:],self.samples[:-1],self.samples[1:]):
            if abs(a)<1e-8: result.append(sa.t)
            elif a*b<0: result.append(sa.t+(-a)/(b-a)*(sb.t-sa.t))
        if abs(vals[-1])<1e-8: result.append(self.samples[-1].t)
        return tuple(sorted(set(round(x,8) for x in result)))
    def offset_curve(self,kind='M',size=.6, reference=None):
        scale=reference or max(abs(getattr(s,kind)) for s in self.samples)
        if scale<1e-10:return [(s.x,s.y) for s in self.samples]
        nx,ny=self.normal
        return [(s.x+nx*size*getattr(s,kind)/scale,s.y+ny*size*getattr(s,kind)/scale) for s in self.samples]
    def deformed(self,gain=100):
        return [(s.x+gain*s.displacement_x,s.y+gain*s.displacement_y) for s in self.samples]

def member_from_solver(element,name):
    samples=tuple(Sample(float(d['xy'][0]),float(d['xy'][1]),float(d['uxy'][0]),float(d['uxy'][1]),float(d['M']),float(d['V']),float(d['t'])) for d in element['samples'])
    return Member(name,(samples[0].x,samples[0].y),(samples[-1].x,samples[-1].y),samples)

def time_plan(events,duration):
    starts=[e['at'] for e in events]
    if not starts or starts != sorted(starts) or min(starts)<0 or max(starts)>=duration:
        raise ValueError('invalid temporal cues')
    return [(e,events[i+1]['at']-e['at'] if i+1<len(events) else duration-e['at']) for i,e in enumerate(events)]
