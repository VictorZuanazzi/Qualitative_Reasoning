import unittest
from derivative import Derivative, DValue
from magnitude import Magnitude, MValue

from quantity import Quantity

class TestQuantity(unittest.TestCase):

    def test_apply_derivative_zero(self):
        q = Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))

        qs = Quantity.applyDerivative(q)
        self.assertEqual(qs[0].magnitude.value, MValue.ZERO)

    def test_apply_derivative_plus(self):
        q = Quantity(Magnitude(MValue.ZERO), Derivative(DValue.PLUS))

        qs = Quantity.applyDerivative(q)
        self.assertEqual(qs[0].magnitude.value, MValue.PLUS)

    def test_apply_derivative_minus(self):
        q = Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS))

        qs = Quantity.applyDerivative(q)
        self.assertEqual(qs[0].magnitude.value, MValue.ZERO)

    def test_apply_derivative_upper_bound(self):
        q = Quantity(Magnitude(MValue.MAX), Derivative(DValue.PLUS))

        qs = Quantity.applyDerivative(q)
        self.assertEqual(qs[0].magnitude.value, MValue.MAX)
        self.assertEqual(qs[0].derivative.value, DValue.ZERO)

    def test_apply_derivative_lower_bound(self):
        q = Quantity(Magnitude(MValue.ZERO), Derivative(DValue.MINUS))

        qs = Quantity.applyDerivative(q)
        self.assertEqual(qs[0].magnitude.value, MValue.ZERO)
        self.assertEqual(qs[0].derivative.value, DValue.ZERO)

    def test_apply_derivative_multiverse(self):
        q = Quantity(Magnitude(MValue.PLUS), Derivative(DValue.PLUS))

        qs = Quantity.applyDerivative(q)
        self.assertEqual(len(qs), 2)
        self.assertIn(Quantity(Magnitude(MValue.PLUS), Derivative(DValue.PLUS)), qs)
        self.assertIn(Quantity(Magnitude(MValue.MAX), Derivative(DValue.ZERO)), qs)

if __name__ == '__main__':
    unittest.main()