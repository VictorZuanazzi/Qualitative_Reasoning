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
    def __init__(self, value, upperBound = MValue.MAX):
        
        #if value is type int, it is converted to Enum.
        if value is int:
            value = MValue(value)
        
        self.value = value
        self.upperBound = upperBound

    def greaterZero(self):
        return self.value > MValue.ZERO

    def isAtUpperBound(self):
        return self.value == self.upperBound

    def isAtLowerBound(self):
        return self.value == MValue.ZERO

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return {
            0 : "0",
            1 : "+",
            2 : "max",
        }.get(self.value)
