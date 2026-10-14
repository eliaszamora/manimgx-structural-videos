"""ACI 318-19 uniaxial P-M section equilibrium (demonstration, tied column).

Sign: compression positive; M>0 when top face is compressed.
Every bar is represented by its actual circular area, including the exact area and
first moment of concrete displaced if the Whitney block crosses the bar.
Inputs mm, MPa; outputs kN and kN.m. Does not check second order/biaxial/seismic detailing.
"""
from dataclasses import dataclass
import math
import numpy as np

@dataclass(frozen=True)
class Section:
    b:float=400.;h:float=400.;fc:float=28.;fy:float=420.;Es:float=200000.
    bar_d:float=16.;bars_face:int=4;dp:float=50.;eps_cu:float=.003
    @property
    def Ag(self):return self.b*self.h
    @property
    def As_layer(self):return self.bars_face*math.pi*self.bar_d**2/4
    @property
    def Ast(self):return 2*self.As_layer
    @property
    def dt(self):return self.h-self.dp
    @property
    def eps_y(self):return self.fy/self.Es
    @property
    def beta1(self):return max(.65,min(.85,.85-.05*max(0,self.fc-28)/7))
    @property
    def balanced_c(self):return self.dt*self.eps_cu/(self.eps_cu+self.eps_y)
    @property
    def Po(self):return .85*self.fc*(self.Ag-self.Ast)+self.fy*self.Ast
    @property
    def Pt(self):return -self.fy*self.Ast
    @property
    def cap(self):return .80*.65*self.Po

S=Section()

def segment_area_first_moment(diameter,upper_offset):
    """Circle portion above horizontal chord, y positive downward.

    Returns (area in mm², first moment ∫(y-yc) dA in mm³).
    upper_offset = Whitney block depth - bar center depth.
    This is exact for a fully enclosed, absent, or partially traversed circle.
    """
    R=diameter/2.0
    if upper_offset<=-R:return 0.,0.
    if upper_offset>= R:return math.pi*R*R,0.
    z=upper_offset/R
    area=R*R*(math.asin(z)+z*math.sqrt(max(0.,1-z*z))+math.pi/2)
    first=-(2./3.)*max(0.,R*R-upper_offset*upper_offset)**1.5
    return area,first

def analyze(c,s=S):
    """Neutral axis from top (mm). Nominal resultants in kN and kN.m."""
    if not (math.isfinite(c) and c>0):raise ValueError('c must be finite, positive')
    a=min(s.beta1*c,s.h)
    cc=.85*s.fc*s.b*a
    P=cc
    M=cc*(s.h/2-a/2)
    steel=[]
    for y in (s.dp,s.dt):
        eps=s.eps_cu*(c-y)/c
        stress=max(-s.fy,min(s.fy,s.Es*eps))
        shifted_area, shifted_first=segment_area_first_moment(s.bar_d,a-y)
        displaced_area=s.bars_face*shifted_area
        displaced_first=s.bars_face*(y*shifted_area+shifted_first)
        Fsteel=s.As_layer*stress
        Fdisplaced=-.85*s.fc*displaced_area
        # Steel is concentrated at bar center; displaced concrete may not be.
        Msteel=Fsteel*(s.h/2-y)
        Mdisplaced=-.85*s.fc*(displaced_area*s.h/2-displaced_first)
        F=Fsteel+Fdisplaced
        Mc=Msteel+Mdisplaced
        P+=F
        M+=Mc
        steel.append(dict(y=y,eps=eps,stress=stress,
                          force_kN=F/1000,moment_kNm=Mc/1e6,
                          steel_force_kN=Fsteel/1000,displaced_force_kN=Fdisplaced/1000,
                          displaced_area=displaced_area))
    et=max(0.,-steel[-1]['eps'])
    phi=.65 if et<=s.eps_y else (.90 if et>=s.eps_y+.003 else .65+.25*(et-s.eps_y)/.003)
    return dict(c=c,a=a,Cc_kN=cc/1000,steel=steel,Pn=P/1000,Mn=M/1e6,
                phi=phi,eps_t=et,phiPn=min(phi*P,s.cap)/1000,phiMn=phi*M/1e6)

def points(n=501,s=S):
    return [analyze(float(c),s) for c in np.logspace(-1,5,n)]

def find_pure_bending(s=S):
    """Bisection with guaranteed bracket: nominal Pn=0 at concrete crushing."""
    lo=1.e-6;hi=s.h
    if analyze(lo,s)['Pn']>=0 or analyze(hi,s)['Pn']<=0:raise ValueError('Cannot bracket Pn=0')
    for _ in range(100):
        md=(lo+hi)/2
        if analyze(md,s)['Pn']>0:hi=md
        else:lo=md
    return analyze((lo+hi)/2,s)
