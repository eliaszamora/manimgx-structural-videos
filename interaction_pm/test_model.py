"""Independent validation of the teaching P-M model.

The reference uses fiber integration / numerical quadrature, NOT the circular
segment closed-form function used by model.analyze().
"""
import math
import unittest
import numpy as np
try:
    from .model import S,analyze,points,find_pure_bending,segment_area_first_moment
except ImportError:
    from model import S,analyze,points,find_pure_bending,segment_area_first_moment

def numerical_result(c, s=S, integration_points=3001):
    """Alternative concrete integration as horizontal fibers, bar cutouts via quadrature."""
    a=min(s.beta1*c,s.h)
    # Reference concrete rectangle integrated analytically from depth 0 to a,
    # and bar cutouts integrated numerically from circle chords.
    P=.85*s.fc*s.b*a
    M=P*(s.h/2-a/2)
    r=s.bar_d/2
    bararea=math.pi*r*r*s.bars_face
    for y in (s.dp,s.dt):
        eps=s.eps_cu*(c-y)/c
        fs=np.clip(s.Es*eps,-s.fy,s.fy)
        P+=fs*bararea
        M+=fs*bararea*(s.h/2-y)
        start=y-r
        stop=min(a,y+r)
        if stop<=start:continue
        yfib=np.linspace(start,stop,integration_points)
        chords=2*np.sqrt(np.maximum(0.,r*r-(yfib-y)**2))
        dispa=s.bars_face*np.trapezoid(chords,yfib)
        first=s.bars_face*np.trapezoid(chords*(s.h/2-yfib),yfib)
        P-=.85*s.fc*dispa
        M-=.85*s.fc*first
    return P/1000,M/1e6

class SectionQC(unittest.TestCase):
    def test_01_properties(self):
        self.assertAlmostEqual(S.Ag,160000)
        self.assertAlmostEqual(S.Ast,8*math.pi*16**2/4)
        self.assertAlmostEqual(S.eps_y,.0021)
        self.assertAlmostEqual(S.balanced_c,350*.003/(.003+.0021),6)
        self.assertAlmostEqual(S.beta1,.85)
    def test_02_exact_circle_moment(self):
        R=8.
        area,first=segment_area_first_moment(16,0)
        self.assertAlmostEqual(area,math.pi*R*R/2,places=10)
        self.assertAlmostEqual(first,-2*R**3/3,places=9)
        for lim in [-R,R]:
            a,f=segment_area_first_moment(16,lim)
            self.assertAlmostEqual(f,0)
    def test_03_extreme_limits(self):
        self.assertAlmostEqual(analyze(1e12)["Pn"],S.Po/1000,places=2)
        self.assertAlmostEqual(analyze(1e-8)["Pn"],S.Pt/1000,places=2)
        self.assertAlmostEqual(analyze(1e12)["Mn"],0,places=1)
        self.assertAlmostEqual(analyze(1e-8)["Mn"],0,places=1)
    def test_04_steel_sign_and_balance(self):
        b=analyze(S.balanced_c)
        self.assertAlmostEqual(b["steel"][1]["eps"],-S.eps_y,places=10)
        self.assertAlmostEqual(b["steel"][0]["eps"],S.eps_cu*(1-S.dp/S.balanced_c),places=10)
        self.assertEqual(b["phi"],.65)
    def test_05_equilibrium_both_resultants(self):
        # Exact net steel force and exact first moment of displaced concrete.
        for c in [30,50,52,60,100,169,180,350,402,419,1000]:
            r=analyze(c)
            P=r["Cc_kN"]+sum(v["force_kN"] for v in r["steel"])
            M=r["Cc_kN"]*(S.h/2-r["a"]/2)/1000 +sum(v["moment_kNm"] for v in r["steel"])
            self.assertAlmostEqual(P,r["Pn"],places=7)
            self.assertAlmostEqual(M,r["Mn"],places=7)
    def test_06_independent_fiber_integration(self):
        # Include c with Whitney-block edge CUTTING through each steel circle.
        for c in [35,48/0.85,50/0.85,54/0.85,100,150,200,343/0.85,350/0.85,356/0.85,800]:
            r=analyze(c)
            refP,refM=numerical_result(c)
            self.assertAlmostEqual(r["Pn"],refP,delta=.035, msg=f"Pn mismatch at c={c}")
            self.assertAlmostEqual(r["Mn"],refM,delta=.009, msg=f"Mn mismatch at c={c}")
    def test_07_pure_bending(self):
        r=find_pure_bending()
        self.assertAlmostEqual(r["Pn"],0,delta=1.e-8)
        self.assertGreater(r["Mn"],0)
    def test_08_phi_and_axial_cap(self):
        for c in np.geomspace(0.001,100000,120):
            r=analyze(float(c))
            self.assertGreaterEqual(r["phi"],.65)
            self.assertLessEqual(r["phi"],.90)
            self.assertLessEqual(r["phiPn"],S.cap/1000+1e-6)
            self.assertAlmostEqual(r["phiMn"],r["phi"]*r["Mn"],places=9)
        self.assertAlmostEqual(analyze(S.dt*S.eps_cu/(S.eps_cu+S.eps_y+.003))["phi"],.90,places=8)
    def test_09_continuity_crossing_bars(self):
        for y in (S.dp,S.dt):
            for edge in (y-S.bar_d/2,y,y+S.bar_d/2):
                c=edge/S.beta1
                before,after=analyze(c-1e-5),analyze(c+1e-5)
                self.assertLess(abs(before["Pn"]-after["Pn"]),.01)
                self.assertLess(abs(before["Mn"]-after["Mn"]),.005)
    def test_10_finite_curve(self):
        allpts=points(1001)
        for p in allpts:
            for key in ("Mn","Pn","phiMn","phiPn"):
                self.assertTrue(math.isfinite(p[key]))
        self.assertGreater(max(x["Mn"] for x in allpts),120)
        self.assertGreater(max(x["Pn"] for x in allpts),3500)
if __name__=="__main__": unittest.main()
