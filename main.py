from quantity import Quantity
from magnitude import Magnitude, MValue
from derivative import Derivative, DValue
from overgeneration import over_generate
from validation import isStateValid
from connect_states import connect_states

def main():
    relations = [
        {
            "type" : "I+",
            "args" : None,
            "Q1" : ("Hoose", "Inflow"),
            "Q2" : ("Container", "Volume"),
        },
        {
            "type" : "I-",
            "args" : None,
            "Q1" : ("Drain", "Outflow"),
            "Q2" : ("Container", "Volume"),
        },
        {
            "type" : "P+",
            "args" : None,
            "Q1" : ("Container", "Volume"),
            "Q2" : ("Drain", "Outflow"),
        },
        {
            "type" : "VC",
            "args" : MValue.MAX,
            "Q1" : ("Container", "Volume"),
            "Q2" : ("Drain", "Outflow"),
        },
        {
            "type" : "VC",
            "args" : MValue.ZERO,
            "Q1" : ("Container", "Volume"),
            "Q2" : ("Drain", "Outflow"),
        },
        {
            "type" : "VC",
            "args" : MValue.MAX,
            "Q1" : ("Drain", "Outflow"),
            "Q2" : ("Container", "Volume"),
        },
        {
            "type" : "VC",
            "args" : MValue.ZERO,
            "Q1" : ("Drain", "Outflow"),
            "Q2" : ("Container", "Volume"),
        },
    ]

    states = over_generate()
    pruned_states = [s for s in states if isStateValid(s, relations)]
    connected_states = connect_states(pruned_states)
    
    #print("\n".join([str(s) for s in states]))
    #print("States before:", len(states))
    
    print("\n".join([str(s) for s in connected_states]))
    print("States after pruning:",len(connected_states))
    
if __name__ == "__main__":
    main()