from magnitude import Magnitude, MValue
from derivative import Derivative, DValue

class Quantity:
    def __init__(self, magnitude, derivative):
        self.magnitude = magnitude
        self.derivative = derivative

    def copy(self):
        return Quantity(Magnitude(self.magnitude.value), Derivative(self.derivative.value))

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Quantity):
            return self.magnitude.value == other.magnitude.value and self.derivative.value == other.derivative.value
        return False
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"[{self.magnitude.value}/{self.magnitude.upperBound},{self.derivative.value}]"

    @staticmethod
    def applyDerivative(orignal):
        copy = orignal.copy()

        copy.magnitude.value = MValue.add(copy.magnitude.value, 1 * copy.derivative.value)
        if(MValue.isBound(copy.magnitude.value)):
            copy.derivative.value = DValue.ZERO

        if(MValue.isInterval(orignal.magnitude.value)):
            return [copy, orignal.copy()]
        else:
            return [copy]
