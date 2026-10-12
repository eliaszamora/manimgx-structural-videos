import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from geometry import *
class TestMechanicalStoryboard(unittest.TestCase):
 def test_zero_is_computed(self):
  self.assertTrue(verify())
 def test_load_joint_anchored(self):
  for a in (0,.25,.5,.75,1):
   x,y=roof_joint(a)
   self.assertTrue(1<x<6.5)
 def test_deformation_continuity(self):
  a=member_samples(LEFT,0,True)
  b=member_samples(LEFT,1,True)
  mid=member_samples(LEFT,.5,True)
  for p,q,r in zip(a,b,mid):
   self.assertAlmostEqual(r[0],(p[0]+q[0])/2,places=8)
   self.assertAlmostEqual(r[1],(p[1]+q[1])/2,places=8)
 def test_opposite_curvatures(self):
  # Finite-difference x''(z) matches sign of M under x-left/right orientation
  p=member_samples(LEFT,1,True)
  def dd(k):return p[k+1][0]-2*p[k][0]+p[k-1][0]
  dlow=dd(5);dtop=dd(26)
  self.assertLess(dlow*dtop,0)
 def test_diagram_anchored(self):
  d=diagram_coords()
  self.assertAlmostEqual(d["base"][0],d["mid"][0])
  self.assertAlmostEqual(d["high"][0],d["mid"][0])
  self.assertLess(d["negative_tip"][0],d["base"][0])
  self.assertGreater(d["positive_tip"][0],d["high"][0])
if __name__=="__main__":unittest.main()
