"""Physics and geometry regression tests independent of ManimGX."""
import sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from structural_viz.model import member_from_solver,time_plan
from demo.portal_solver import solve,H
class DiagramTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.case=solve('lateral')
        cls.left=member_from_solver(cls.case['elements'][0],'left')
        cls.right=member_from_solver(cls.case['elements'][3],'right')
    def test_sway_and_fixed_bases(self):
        self.assertGreater(self.case['u'][1][0],0)
        self.assertEqual(self.case['u'][0],[0,0,0]);self.assertEqual(self.case['u'][4],[0,0,0])
    def test_local_positive_normal_in_columns(self):
        self.assertAlmostEqual(self.left.normal[0],1)
        self.assertAlmostEqual(self.right.normal[0],1)
        self.assertAlmostEqual(self.left.normal[1],0)
    def test_signs_and_zero_of_curvature(self):
        for col in [self.left,self.right]:
            self.assertLess(col.samples[0].M,0)
            self.assertGreater(col.samples[-1].M,0)
            roots=col.zeros('M');self.assertEqual(len(roots),1)
            self.assertTrue(1.6 < roots[0]*H < 2.2)
    def test_shear_equals_derivative(self):
        for col in [self.left,self.right]:
            grad=(col.samples[-1].M-col.samples[0].M)/col.length
            self.assertAlmostEqual(grad,col.samples[0].V,places=5)
    def test_diagram_side_consistency(self):
        col=self.left
        points=col.offset_curve('M',.6)
        self.assertLess(points[0][0],col.samples[0].x)
        self.assertGreater(points[-1][0],col.samples[-1].x)
    def test_reaction_equilibrium(self):
        self.assertAlmostEqual(self.case['reaction'][0][0]+self.case['reaction'][4][0],-24,places=5)
    def test_event_schedule(self):
        from demo.story import BEATS,SECONDS_PER_BEAT,TOTAL_SECONDS
        self.assertEqual(len(BEATS)*SECONDS_PER_BEAT,TOTAL_SECONDS)
        for b in BEATS:
            self.assertEqual(len(time_plan([{'at':a} for a,_ in b['events']],SECONDS_PER_BEAT)),3)
if __name__=='__main__':unittest.main()
