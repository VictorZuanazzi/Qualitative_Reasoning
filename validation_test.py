import unittest

from validation import isStateValid, getRelationQuantities
from quantity import Quantity
from magnitude import Magnitude, MValue
from derivative import Derivative, DValue

class TestValidation(unittest.TestCase):
    
    def test_getRelationQuantities(self):
        state = {
            "B" : {
                "Q" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.PLUS))
            },
            "C" : {
                "Q" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))
            },
        }
        relation = {
            "type" : "P+",
            "args" : None,
            "Q1" : ("B", "Q"),
            "Q2" : ("C", "Q"),
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
            "B" : {
                "Q" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))
            },
            "C" : {
                "Q" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))
            },
        }
        relations = [
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("B", "Q"),
                "Q2" : ("C", "Q"),
            },
        ]

        self.assertEqual(isStateValid(state, relations), True)

    def test_isStateValid_singleRelation_invalid(self):
        state = {
            "A" : { "Q" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.PLUS)) },
            "B" : { "Q" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO)) },
        }
        relations = [
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("A", "Q"),
                "Q2" : ("B", "Q"),
            },
        ]

        self.assertEqual(isStateValid(state, relations), False)

    def test_isStateValid_multiRelation_valid(self):
        state = {
            "B" : {
                "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS))
            },
            "C" : {
                "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS))
            },
        }
        relations = [
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("B", "Q"),
                "Q2" : ("C", "Q"),
            },
            {
                "type" : "I-",
                "args" : None,
                "Q1" : ("C", "Q"),
                "Q2" : ("B", "Q"),
            },
            {
                "type" : "EX",
                "args" : None,
                "Q1" : ("B", "Q"),
                "Q2" : ("B", "Q"),
            },
        ]

        self.assertEqual(isStateValid(state, relations), True)

    def test_isStateValid_multiRelation_sameTail_ambiguous(self):
        state1 = {
            "A" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS)) },
            "B" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS)) },
            "C" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.ZERO)) },
        }
        state2 = {
            "A" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS)) },
            "B" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.ZERO)) },
            "C" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.ZERO)) },
        }
        state3 = {
            "A" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS)) },
            "B" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.PLUS)) },
            "C" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.ZERO)) },
        }
        relations = [
            {
                "type" : "EX",
                "args" : None,
                "Q1" : ("A", "Q"),
                "Q2" : ("A", "Q"), 
            },
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("A", "Q"),
                "Q2" : ("B", "Q"),
            },
            {
                "type" : "I+",
                "args" : None,
                "Q1" : ("C", "Q"),
                "Q2" : ("B", "Q"),
            },
        ]

        self.assertEqual(isStateValid(state1, relations), True)
        self.assertEqual(isStateValid(state2, relations), True)
        self.assertEqual(isStateValid(state3, relations), True)

    def test_isStateValid_multiRelation_invalid(self):
        state = {
            "A" : {
                "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.ZERO))
            },
            "B" : {
                "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.ZERO))
            },
        }
        relations = [
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("A", "Q"),
                "Q2" : ("B", "Q"),
            },
            {
                "type" : "I-",
                "args" : None,
                "Q1" : ("B", "Q"),
                "Q2" : ("A", "Q"),
            },
        ]

        self.assertEqual(isStateValid(state, relations), False)

    def test_isStateValid_VC_not_affect_derivative(self):
        state = {
            "A" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.PLUS)) },
            "B" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS)) },
            "C" : { "Q" : Quantity(Magnitude(MValue.PLUS), Derivative(DValue.MINUS)) },
        }
        relations = [
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("A", "Q"),
                "Q2" : ("B", "Q"),
            },
            {
                "type" : "VC",
                "args" : MValue.MAX,
                "Q1" : ("C", "Q"),
                "Q2" : ("B", "Q"),
            },
        ]

        self.assertEqual(isStateValid(state, relations), False)

    def test_isStateValid_upper_boundary_derivatives(self):
        state_invalid = {
            "A" : { "Q" : Quantity(Magnitude(MValue.MAX), Derivative(DValue.PLUS)) },
        }
        state_valid = {
            "A" : { "Q" : Quantity(Magnitude(MValue.MAX), Derivative(DValue.MINUS)) },
        }
        relations = [
            {
                "type" : "EX",
                "args" : None,
                "Q1" : ("A", "Q"),
                "Q2" : ("A", "Q"),
            }
        ]

        self.assertEqual(isStateValid(state_invalid, relations), False)
        self.assertEqual(isStateValid(state_valid, relations), True)

    def test_isStateValid_lower_boundary_derivatives(self):
        state_invalid = {
            "A" : { "Q" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.MINUS)) },
        }
        state_valid = {
            "A" : { "Q" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.PLUS)) },
        }
        relations = [
            {
                "type" : "EX",
                "args" : None,
                "Q1" : ("A", "Q"),
                "Q2" : ("A", "Q"),
            }
        ]

        self.assertEqual(isStateValid(state_invalid, relations), False)
        self.assertEqual(isStateValid(state_valid, relations), True)

    def test_isStateValid_noEX(self):
        state = { "A" : { "Q" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.PLUS)) } }
        relations = []

        self.assertEqual(isStateValid(state, relations), False)

    def test_isStateValid_otherEX(self):
        state = { 
            "A" : { "Q" : 
                Quantity(Magnitude(MValue.ZERO), 
                Derivative(DValue.ZERO)) 
            },
            "B" : { "Q" : 
                Quantity(Magnitude(MValue.ZERO), 
                Derivative(DValue.PLUS)) 
            },
            "C" : { "Q" : 
                Quantity(Magnitude(MValue.ZERO), 
                Derivative(DValue.PLUS)) 
            },
        }
        relations = [
            {
                "type" : "I+",
                "args" : None,
                "Q1" : ("A", "Q"),
                "Q2" : ("B", "Q"),
            },
            {
                "type" : "I-",
                "args" : None,
                "Q1" : ("C", "Q"),
                "Q2" : ("B", "Q"),
            },
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("B", "Q"),
                "Q2" : ("C", "Q"),
            },
            {
                "type" : "VC",
                "args" : MValue.MAX,
                "Q1" : ("B", "Q"),
                "Q2" : ("C", "Q"),
            },
            {
                "type" : "VC",
                "args" : MValue.ZERO,
                "Q1" : ("B", "Q"),
                "Q2" : ("C", "Q"),
            },
            {
                "type" : "VC",
                "args" : MValue.MAX,
                "Q1" : ("C", "Q"),
                "Q2" : ("B", "Q"),
            },
            {
                "type" : "VC",
                "args" : MValue.ZERO,
                "Q1" : ("C", "Q"),
                "Q2" : ("B", "Q"),
            },
        ]

        self.assertEqual(isStateValid(state, relations), False)

    def test_isStateValid_relationOrder(self):
        state = { 
            "A" : { "Q" : 
                Quantity(Magnitude(MValue.ZERO), 
                Derivative(DValue.ZERO)) 
            },
            "B" : { "Q" : 
                Quantity(Magnitude(MValue.PLUS), 
                Derivative(DValue.MINUS)) 
            },
            "C" : { "Q" : 
                Quantity(Magnitude(MValue.PLUS), 
                Derivative(DValue.ZERO)) 
            },
        }
        relations = [
            {
                "type" : "I+",
                "args" : None,
                "Q1" : ("A", "Q"),
                "Q2" : ("B", "Q"),
            },
            {
                "type" : "I-",
                "args" : None,
                "Q1" : ("C", "Q"),
                "Q2" : ("B", "Q"),
            },
            {
                "type" : "P+",
                "args" : None,
                "Q1" : ("B", "Q"),
                "Q2" : ("C", "Q"),
            },
        ]
        self.assertEqual(isStateValid(state, relations), False)

if __name__ == '__main__':
    unittest.main()