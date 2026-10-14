"""Interacción uniaxial P-M: resistencia nominal y diseño, compatible con numpy."""
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

def analyze(c,s=S):
    """c in mm, Pn/kN positive compression, Mn/kNm positive top compression."""
    if c<=0:raise ValueError('c must be positive')
    a=min(s.beta1*c,s.h)
    cc=.85*s.fc*a*s.b
    P=cc;M=cc*(s.h/2-a/2)
    steel=[]
    for y in (s.dp,s.dt):
        eps=s.eps_cu*(c-y)/c
        stress=max(-s.fy,min(s.fy,s.Es*eps))
        z=(a-y)/(s.bar_d/2)
        if z<=-1:fraction=0
        elif z>=1:fraction=1
        else:fraction=.5+(math.asin(z)+z*math.sqrt(1-z*z))/math.pi
        F=s.As_layer*(stress-.85*s.fc*fraction)
        P+=F;M+=F*(s.h/2-y)
        steel.append(dict(y=y,eps=eps,stress=stress,force_kN=F/1000))
    et=max(0,-steel[-1]['eps'])
    phi=.65 if et<=s.eps_y else (.90 if et>=s.eps_y+.003 else .65+.25*(et-s.eps_y)/.003)
    return dict(c=c,a=a,Cc_kN=cc/1000,steel=steel,Pn=P/1000,Mn=M/1e6,
                phi=phi,eps_t=et,phiPn=min(phi*P,s.cap)/1000,phiMn=phi*M/1e6)

def points(n=501,s=S):
    return [analyze(float(c),s) for c in np.logspace(-1,5,n)]
