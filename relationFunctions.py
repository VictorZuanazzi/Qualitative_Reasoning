from derivative import DValue
from functools import partial

def getFunc(key, *args):
    return {
        "P+" : propotionalPositive,
        "I+" : influencePositive,
        "I-" : influenceNegative,
        "VC" : partial(correspondence, value=args[0]),
        "EX" : partial(exogenous, value=args[0])
        
    }.get(key)

def propotionalPositive(q1, q2):
    q2.derivative.value = q1.derivative.value

def influencePositive(q1, q2):
    if(q1.magnitude.greaterZero()):
        q2.derivative.value = DValue.PLUS

def influenceNegative(q1, q2):
    if(q1.magnitude.greaterZero()):
        q2.derivative.value = DValue.MINUS

def correspondence(q1, q2, value):
    if q1.magnitude.value == value:
        q2.magnitude.value = value
        
def exogenous(q1, q2, value):
    if type(value) == int:
        q2.derivative.value = DValue.add(q1.derivative.value, value)