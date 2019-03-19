from quantity import Quantity
from magnitude import Magnitude, MValue
from derivative import Derivative, DValue
from overgeneration import over_generate

def main():
    state = {
        "Hoose" : {
            "Inflow" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))
        },
        "Container" : {
            "Volume" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))
        },
        "Drain" : {
            "Outflow" : Quantity(Magnitude(MValue.ZERO), Derivative(DValue.ZERO))
        },
        "pre_state": {},
        "next_state": {},
    }

    relations = [
        {
            "type" : "I+",
            "Q1" : ("Hoose", "Inflow"),
            "Q2" : ("Container", "Volume"),
        },
        {
            "type" : "I-",
            "Q1" : ("Drain", "Outflow"),
            "Q2" : ("Container", "Volume"),
        },
        {
            "type" : "P+",
            "Q1" : ("Container", "Volume"),
            "Q2" : ("Drain", "Outflow"),
        },
    ]

if __name__ == "__main__":
    main()