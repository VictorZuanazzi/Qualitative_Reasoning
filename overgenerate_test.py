# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:13:55 2019

@author: Victor Zuanazzi
"""

import unittest
from derivative import Derivative, DValue
from magnitude import Magnitude, MValue

from quantity import Quantity

class TestOvergeneration(unittest.TestCase):
    def test_p_plus_no_change(self):
        q1 = Quantity(None, Derivative(DValue.ZERO))
        q2 = Quantity(None, Derivative(DValue.ZERO))

        r.propotionalPositive(q1, q2)

        self.assertEqual(q2.derivative.value, DValue.ZERO)