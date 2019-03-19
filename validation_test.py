import unittest

from validation import isStateValid, getRelationQuantities
from quantity import Quantity
from magnitude import Magnitude, MValue
from derivative import Derivative, DValue

class TestValidation(unittest.TestCase):
    
    def test_getRelationQuantities(self):
        state = {
            "Container" : {
                "Volume" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.PLUS))
            },
            "Drain" : {
                "Outflow" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))
            },
        }
        relation = {
            "type" : "P+",
            "args" : None,
            "Q1" : ("Container", "Volume"),
            "Q2" : ("Drain", "Outflow"),
        }

        head, tail = getRelationQuantities(state, relation)
        self.assertEqual(head, Quantity(Magnitude(MValue.ZERO), Derivative(DValue.PLUS)))
        self.assertEqual(tail,  Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO)))

    def test_isStateValid_no_relations(self):
        state = {}
        relations = []

        self.assertEqual(isStateValid(state, relations), True)

    def test_isStateValid_singleRelation_valid(self):
        state = {
            "Container" : {
                "Volume" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))
            },
            "Drain" : {
                "Outflow" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))
            },
        }
        relations = [
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("Container", "Volume"),
                "Q2" : ("Drain", "Outflow"),
            },
        ]

        self.assertEqual(isStateValid(state, relations), True)

    def test_isStateValid_singleRelation_invalid(self):
        state = {
            "Container" : {
                "Volume" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.PLUS))
            },
            "Drain" : {
                "Outflow" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))
            },
        }
        relations = [
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("Container", "Volume"),
                "Q2" : ("Drain", "Outflow"),
            },
        ]

        self.assertEqual(isStateValid(state, relations), False)

    def test_isStateValid_multiRelation_valid(self):
        state = {
            "Container" : {
                "Volume" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS))
            },
            "Drain" : {
                "Outflow" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS))
            },
        }
        relations = [
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("Container", "Volume"),
                "Q2" : ("Drain", "Outflow"),
            },
            {
                "type" : "I-",
                "args" : None,
                "Q1" : ("Drain", "Outflow"),
                "Q2" : ("Container", "Volume"),
            },
        ]

        self.assertEqual(isStateValid(state, relations), True)

    def test_isStateValid_multiRelation_invalid(self):
        state = {
            "Container" : {
                "Volume" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.ZERO))
            },
            "Drain" : {
                "Outflow" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.ZERO))
            },
        }
        relations = [
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("Container", "Volume"),
                "Q2" : ("Drain", "Outflow"),
            },
            {
                "type" : "I-",
                "args" : None,
                "Q1" : ("Drain", "Outflow"),
                "Q2" : ("Container", "Volume"),
            },
        ]

        self.assertEqual(isStateValid(state, relations), False)

if __name__ == '__main__':
    unittest.main()