from enum import IntEnum

class MValue(IntEnum):
    ZERO = 0
    PLUS = 1
    MAX = 2

class Magnitude:
    def __init__(self, value):
        self.value = value

    def greaterZero(self):
        return self.value > MValue.ZERO
