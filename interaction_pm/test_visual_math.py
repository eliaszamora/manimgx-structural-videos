"""Frame-by-frame visual physics checks for 3D pilot without importing ManimGX."""
import math
import unittest
try:
    from .model import S,analyze
    from .visual_math import G,display_state
except ImportError:
    from model import S,analyze
    from visual_math import G,display_state

class VisualPhysicsQC(unittest.TestCase):
    def test_01_3d_and_2d_neutral_match(self):
        for c in [100+i for i in range(251)]:
            s=display_state(c)
            top3=G.volume_side/2
            top2=G.section_cy+G.section_size/2
            self.assertAlmostEqual((top3-s['yneutral_3d'])/G.volume_side,
                                   (top2-s['yneutral_2d'])/G.section_size,places=12)
            self.assertAlmostEqual((top2-s['yneutral_2d'])/G.section_size,c/S.h,places=12)
    def test_02_block_and_axis_are_not_confused(self):
        for c in range(100,351):
            r=display_state(c)
            self.assertAlmostEqual(r['a'],S.beta1*c,places=12)
            self.assertAlmostEqual(r['blockdepth_3d']/G.volume_side,r['a']/S.h,places=12)
            self.assertAlmostEqual(r['blockdepth_2d']/G.section_size,r['a']/S.h,places=12)
            self.assertGreater(r['yneutral_2d'],G.section_cy-G.section_size/2)
    def test_03_strain_profile(self):
        for c in [100,150,175,206,265,290,350]:
            r=display_state(c)
            self.assertAlmostEqual(r['epsilon_top'],.003,places=12)
            self.assertAlmostEqual(r['epsilon_bottom'],S.eps_cu*(c-S.h)/c,places=12)
            xzero=r['strain_x_top'] -r['epsilon_top']*G.strain_scale
            self.assertAlmostEqual(xzero,G.strain_x0,places=12)
            self.assertAlmostEqual(r['strain_x_bottom']-G.strain_x0,
                                   G.strain_scale*r['epsilon_bottom'],places=12)
    def test_04_section_and_strain_do_not_overlap_pilot(self):
        section_edge=G.section_cx+G.section_size/2
        # Pilot tracker range is 175..290 mm.
        for c in range(175,291):
            r=display_state(c)
            self.assertGreater(r['strain_x_bottom']-section_edge,.40)
    def test_05_curve_and_marker_same_calculation(self):
        for c in range(100,351):
            r=display_state(c)
            analysis=analyze(c)
            self.assertAlmostEqual(
                G.moment_scale*(r['chart_x']-G.chart_xmin)/G.chart_xlen,
                analysis['Mn'],places=11)
            self.assertAlmostEqual(
                G.pmin+(r['chart_y']-G.chart_ymin)*(G.pmax-G.pmin)/G.chart_ylen,
                analysis['Pn'],places=11)
    def test_06_mobile_safe_frame_for_actual_pilot(self):
        for c in range(175,291):
            r=display_state(c)
            self.assertGreater(r['chart_x'],-5)
            self.assertLess(r['chart_x'],5)
            self.assertGreater(r['chart_y'],-2.9)
            self.assertLess(r['chart_y'],2.7)
            self.assertLess(r['strain_x_top'],6.3)
            self.assertGreater(r['strain_x_bottom'],5.1)
    def test_07_illegal_tracker_state_fails(self):
        for invalid in (-1,0,50,99,351,1000,float('nan')):
            with self.assertRaises(ValueError):display_state(invalid)
if __name__=='__main__':unittest.main()
