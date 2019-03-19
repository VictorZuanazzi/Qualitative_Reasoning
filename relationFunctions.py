from derivative import DValue
from functools import partial

def getFunc(key, *args):
    return {
        "P+" : propotionalPositive,
        "I+" : influencePositive,
        "I-" : influenceNegative,
        "VC" : partial(correspondence, args),
    }.get(key)

def propotionalPositive(q1, q2):
    q2.derivative.value = q1.derivative.value

def influencePositive(q1, q2):
    if(q1.magnitude.greaterZero()):
        q2.derivative.value = DValue.add(q2.derivative.value, 1)

def influenceNegative(q1, q2):
    if(q1.magnitude.greaterZero()):
        q2.derivative.value = DValue.add(q2.derivative.value, -1)

def correspondence(q1, q2, value):
    if q1.magnitude.value == value:
            q2.magnitude.value = value