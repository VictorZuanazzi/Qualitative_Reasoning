from quantity import Quantity
from magnitude import Magnitude, MValue
from derivative import Derivative, DValue
from overgeneration import over_generate
from validation import isStateValid

def main():
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
        }
    ]

    states = over_generate()
    pruned_states = [s for s in states if isStateValid(s, relations)]
    
    print("States before:", len(states))
    print("\n".join([str(s) for s in states]))
    print("States after pruning:",len(pruned_states))
    print("\n".join([str(s) for s in pruned_states]))

if __name__ == "__main__":
    main()