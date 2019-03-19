from enum import IntEnum

class DValue(IntEnum):
    MINUS = -1
    ZERO = 0
    PLUS = 1

    @staticmethod
    def add(dvalue, delta):
        return max(min(dvalue + delta, DValue.PLUS), DValue.MINUS)

class Derivative:
    def __init__(self, value):
        
        #if value is type int, it is converted to Enum.
        if value is int:
            value = DValue(value)
        
        self.value = value

    def equals(self, other):
        return self.value == other.value

    def greater(self, other):
        return self.value > other.value

    def greaterEqual(self, other):
        return self.greater(other) or self.equals(other)

    def greaterZero(self):
        return self.greater(Derivative(DValue.ZERO))

