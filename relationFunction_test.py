import unittest
from quantity import Quantity
from derivative import Derivative, DValue
from magnitude import Magnitude, MValue

import relationFunctions as r

class TestRelationFunctions(unittest.TestCase):

    # P+
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

    # I+
    def test_i_plus_inactive(self):
        q1 = Quantity(Magnitude(MValue.ZERO), None)
        q2 = Quantity(None, Derivative(DValue.ZERO))

        r.influencePositive(q1, q2)
        self.assertEqual(q2.derivative.value, DValue.ZERO)

    def test_i_plus_active(self):
        q1 = Quantity(Magnitude(MValue.PLUS), None)
        q2 = Quantity(None, Derivative(DValue.ZERO))

        r.influencePositive(q1, q2)
        self.assertEqual(q2.derivative.value, DValue.PLUS)

    def test_i_plus_active_boundary(self):
        q1 = Quantity(Magnitude(MValue.PLUS), None)
        q2 = Quantity(None, Derivative(DValue.PLUS))

        r.influencePositive(q1, q2)
        self.assertEqual(q2.derivative.value, DValue.PLUS)
    
    # I-
    def test_i_minus_inactive(self):
        q1 = Quantity(Magnitude(MValue.ZERO), None)
        q2 = Quantity(None, Derivative(DValue.ZERO))

        r.influenceNegative(q1, q2)
        self.assertEqual(q2.derivative.value, DValue.ZERO)

    def test_i_minus_active(self):
        q1 = Quantity(Magnitude(MValue.PLUS), None)
        q2 = Quantity(None, Derivative(DValue.ZERO))

        r.influenceNegative(q1, q2)
        self.assertEqual(q2.derivative.value, DValue.MINUS)

    def test_i_minus_active_boundary(self):
        q1 = Quantity(Magnitude(MValue.PLUS), None)
        q2 = Quantity(None, Derivative(DValue.MINUS))

        r.influenceNegative(q1, q2)
        self.assertEqual(q2.derivative.value, DValue.MINUS)

    def test_c_inactive(self):
        q1 = Quantity(Magnitude(MValue.PLUS), None)
        q2 = Quantity(Magnitude(MValue.PLUS), None)

        r.getFunc("VC", MValue.MAX)(q1,q2)
        self.assertEqual(q2.magnitude.value, MValue.PLUS)

    def test_c_active(self):
        q1 = Quantity(Magnitude(MValue.MAX), None)
        q2 = Quantity(Magnitude(MValue.PLUS), None)

        r.getFunc("VC", MValue.MAX)(q1,q2)
        self.assertEqual(q2.magnitude.value, MValue.MAX)
    
    #EX
    def test_ex_increase_minus(self):
        q1 = Quantity(None, DValue.MINUS)
        q2 = Quantity(None, DValue.MINUS)
        
        r.getFunc("EX", 1)(q1, q2)
        self.assertEqual(q2.derivative.value, DValue.ZERO)
    
    def test_ex_increase_zero(self):
        q1 = Quantity(None, DValue.ZERO)
        q2 = Quantity(None, DValue.ZERO)
        
        r.getFunc("EX", 1)(q1, q2)
        self.assertEqual(q2.derivative.value, DValue.PLUS)
    
    def test_ex_increase_plus(self):
        q1 = Quantity(None, DValue.PLUS)
        q2 = Quantity(None, DValue.PLUS)
        
        r.getFunc("EX", 1)(q1, q2)
        self.assertEqual(q2.derivative.value, DValue.PLUS)
        
    

if __name__ == '__main__':
    unittest.main()