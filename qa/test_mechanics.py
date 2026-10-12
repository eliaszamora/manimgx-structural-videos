"""Tests que deben aprobar ANTES de renderizar diagramas estructurales."""
import unittest
from math import isclose
from qa.mechanics import Cantilever

class TestCantilever(unittest.TestCase):
    def setUp(self):
        self.m=Cantilever()
        self.h=1e-4

    def test_conditions_support(self):
        self.assertAlmostEqual(self.m.deflection(0),0)
        self.assertAlmostEqual(self.m.slope(0),0)

    def test_tip_is_lower_and_has_nonzero_rotation(self):
        m=self.m
        self.assertLess(m.deflection(m.length),0)
        self.assertLess(m.slope(m.length),0)
        self.assertAlmostEqual(m.deflection(m.length),-m.force*m.length**3/(3*m.EI))

    def test_moment_sign_and_boundaries(self):
        m=self.m
        self.assertAlmostEqual(m.moment(0),-m.force*m.length)
        self.assertAlmostEqual(m.moment(m.length),0)
        for x in [0,m.length*.25,m.length*.50,m.length*.75]:
            self.assertLess(m.moment(x),0)

    def test_shear_is_positive_and_constant(self):
        m=self.m
        for x in [0,.5*m.length,m.length]:
            self.assertAlmostEqual(m.shear(x),m.force)

    def test_EI_curvature_equals_moment(self):
        m=self.m
        for x in [.1*m.length,.35*m.length,.8*m.length]:
            h=self.h
            numerical=(m.deflection(x+h)-2*m.deflection(x)+m.deflection(x-h))/(h*h)
            self.assertTrue(isclose(m.EI*numerical,m.moment(x),rel_tol=2e-5,abs_tol=1e-3))

    def test_first_derivative_moment_equals_shear(self):
        m=self.m
        for x in [0,.2*m.length,.75*m.length]:
            h=self.h
            grad=(m.moment(x+h)-m.moment(x-h))/(2*h)
            self.assertTrue(isclose(grad,m.shear(x),rel_tol=1e-8,abs_tol=1e-8))

    def test_normalized_curve_matches_scene_profile(self):
        m=self.m
        for u in [0,.1,.3,.6,.85,1]:
            self.assertAlmostEqual(m.normalized_deflection(u),-u*u*(3-u)/2)
        self.assertAlmostEqual(m.normalized_deflection(1),-1)

    def test_internal_action_balance_right_free_body(self):
        m=self.m
        for x in [.12*m.length,.5*m.length,.91*m.length]:
            # Momento antihorario (-M) equilibra momento horario externo P*(L-x).
            self.assertAlmostEqual(-m.moment(x),m.force*(m.length-x))
            # V ascendente en cara izquierda equilibra P descendente.
            self.assertAlmostEqual(m.shear(x)-m.force,0)

if __name__ == "__main__":unittest.main()
