import sys,unittest,numpy as np
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from geometry_v8 import *
class VisualMath(unittest.TestCase):
 def test_material_fixed_base(self):
  self.assertTrue(all(np.allclose(parametric(0,a),parametric(0,0)) for a in [0,.25,.75,1]))
 def test_joints_follow_same_load_fraction(self):
  a=np.array(roof_joint(0));b=np.array(roof_joint(1));m=np.array(roof_joint(.5))
  self.assertTrue(np.allclose(m,(a+b)/2))
 def test_tangent_is_true_curve_derivative(self):
  for t in [.14,.45,.70,.86]:
   finite=parametric(t+1e-4)-parametric(t-1e-4)
   finite/=np.linalg.norm(finite)
   self.assertGreater(float(np.dot(finite,dparametric(t))),.9999)
 def test_inflection_moment_and_curvature(self):
  data=proof()
  self.assertAlmostEqual(signed_moment(INFLECTION_T),0,places=6)
 def test_chart_original_axis_signs(self):
  d=diagram_coords()
  self.assertLess(d["negative_tip"][0],d["base"][0])
  self.assertGreater(d["positive_tip"][0],d["high"][0])
  self.assertAlmostEqual(d["base"][0],d["mid"][0])
if __name__=="__main__":unittest.main()
