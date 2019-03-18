def getFunc(key):
    return {
        "P+" : propotionalPositive
    }


def propotionalPositive(q1, q2):
    q2.derivative.value = q1.derivative.value