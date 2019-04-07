from quantity import Quantity
from magnitude import Magnitude, MValue
from derivative import Derivative, DValue
from overgeneration import over_generate
from validation import isStateValid, pruneInvalidStates
from connect_states import connect_states
from graph_maker import make_state_graph

def main():
    relations = [
        {
            "type" : "EX",
            "args" : 1,
            "Q1" : ("Hoose", "Inflow"),
            "Q2" : ("Hoose", "Inflow"),
        },
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
    ders = list(map(int, DValue))
    pruned_states = pruneInvalidStates(states, relations) 
    connected_states = connect_states(pruned_states, relations)
    
    #print("\n".join([str(s) for s in states]))
    #print("States before:", len(states))
    
    print("\n".join([str(s) for s in connected_states]))
    print("States after pruning:",len(connected_states))
    
    make_state_graph(connected_states, 'state_graph')
    
if __name__ == "__main__":
    main()