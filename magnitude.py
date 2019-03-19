from enum import IntEnum

class MValue(IntEnum):
    ZERO = 0
    PLUS = 1
    MAX = 2

    @staticmethod
    def add(mvalue, delta):
        return max(min(mvalue + delta, MValue.MAX), MValue.ZERO)
    
    @staticmethod
    def isBound(mvalue):
        return mvalue == MValue.ZERO or mvalue == MValue.MAX

    @staticmethod
    def isInterval(mvalue):
        return mvalue == MValue.PLUS

class Magnitude:
    def __init__(self, value):
        
        #if value is type int, it is converted to Enum.
        if value is int:
            value = MValue(value)
        
        self.value = value

    def greaterZero(self):
        return self.value > MValue.ZERO
