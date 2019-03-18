from enum import Enum

class DValue(Enum):
    MINUS = -1
    ZERO = 0
    PLUS = 1

class Derivative:
    def __init__(self, value):
        self.value = value

    def equals(self, other):
        return self.value == other.value

    def greater(self, other):
        return int(self.value) > int(other.value)

    def greaterEqual(self, other):
        return self.greater(other) or self.equals(other)

    def greaterZero(self):
        return self.greater(Derivative(DValue.ZERO))

