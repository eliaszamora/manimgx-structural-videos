"""Guards against the two known visual defects of the earlier V3."""
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class RenderContract(unittest.TestCase):
    def test_move_material_points_instead_of_tracing_final_shape(self):
        scene=(ROOT/"demo"/"scene.py").read_text()
        self.assertIn("m.Transform(axes,deformed())",scene)
        self.assertNotIn("m.Create(deform)",scene)
    def test_diagrams_use_undeformed_member_axis(self):
        scene=(ROOT/"demo"/"scene.py").read_text()
        self.assertIn("m.Transform(axes,original())",scene)
        self.assertIn("split_signed_plot(col_left,'M',lambda pt:world(pt)",scene)
        self.assertIn("split_signed_plot(col_left,'V',lambda pt:world(pt)",scene)
        self.assertNotIn("diagram_panel(",scene)
if __name__=="__main__":unittest.main()
