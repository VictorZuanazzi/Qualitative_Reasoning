import unittest
from quantity import Quantity
from derivative import Derivative, DValue
import relationFunctions as r

class TestRelationFunctions(unittest.TestCase):

    def test_p_plus_no_change(self):
        q1 = Quantity(None, Derivative(DValue.ZERO))
        q2 = Quantity(None, Derivative(DValue.ZERO))

        r.propotionalPositive(q1, q2)

        self.assertEqual(q2.derivative.value, DValue.ZERO)

    def test_p_plus_change_positive(self):
        q1 = Quantity(None, Derivative(DValue.PLUS))
        q2 = Quantity(None, Derivative(DValue.ZERO))

        r.propotionalPositive(q1, q2)

        self.assertEqual(q2.derivative.value, DValue.PLUS)

    def test_p_plus_copy_value(self):
        q1 = Quantity(None, Derivative(DValue.PLUS))
        q2 = Quantity(None, Derivative(DValue.ZERO))

        # apply proportion relation
        r.propotionalPositive(q1, q2)
        self.assertEqual(q2.derivative.value, DValue.PLUS)
        # change q1 derivative without affecting q2 derivative
        q1.derivative.value = DValue.MINUS
        self.assertEqual(q2.derivative.value, DValue.PLUS)

if __name__ == '__main__':
    unittest.main()