from derivative import DValue

def getFunc(key):
    return {
        "P+" : propotionalPositive,
        "I+" : influencePositive,
    }

def propotionalPositive(q1, q2):
    q2.derivative.value = q1.derivative.value

def influencePositive(q1, q2):
    if(q1.magnitude.greaterZero()):
        q2.derivative.value = DValue.increment(q2.derivative.value)

def influenceNegative(q1, q2):
    if(q1.magnitude.greaterZero()):
        q2.derivative.value = DValue.decrement(q2.derivative.value)