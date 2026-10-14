import math, unittest
try:
    from .model import S, analyze
except ImportError:
    from model import S, analyze

class SectionInteractionTest(unittest.TestCase):
    def test_area_and_materials(self):
        self.assertAlmostEqual(S.Ag,160000)
        self.assertAlmostEqual(S.Ast,8*math.pi*16**2/4)
        self.assertAlmostEqual(S.eps_y,.0021)
    def test_balanced(self):
        r=analyze(S.balanced_c)
        self.assertAlmostEqual(r['steel'][-1]['eps'],-S.eps_y,places=8)
        self.assertAlmostEqual(r['phi'],.65)
    def test_equilibrium(self):
        for c in [50,100,S.balanced_c,400,1000]:
            r=analyze(c)
            P=r['Cc_kN']+sum(b['force_kN'] for b in r['steel'])
            M=r['Cc_kN']*(S.h/2-r['a']/2)/1000+sum(b['force_kN']*(S.h/2-b['y'])/1000 for b in r['steel'])
            self.assertAlmostEqual(P,r['Pn'],places=6)
            self.assertAlmostEqual(M,r['Mn'],places=6)
    def test_endpoints_and_cap(self):
        self.assertAlmostEqual(analyze(1e10)['Pn'],S.Po/1000,places=1)
        self.assertAlmostEqual(analyze(1e-5)['Pn'],S.Pt/1000,places=1)
        self.assertLessEqual(max(analyze(c)['phiPn'] for c in [100,500,1000,5000]),S.cap/1000+1e-6)
if __name__=='__main__':unittest.main()
