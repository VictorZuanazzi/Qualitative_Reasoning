from magnitude import MValue
from derivative import DValue
from graph_maker import make_state_graph
from qr_engine import qr_engine

def make_simple_graph():
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
    
    mags = list(map(int, MValue))    
    ders = list(map(int, DValue))
    
    blue_print = {
            "Hoose" : {
                "Inflow" : ([0,1], ders)
            },
            "Container" : {
                "Volume" : (mags, ders),
            },
            "Drain" : {
                "Outflow" : (mags, ders)
            },
        }

    states = qr_engine(blue_print, relations)
    
    make_state_graph(states, '../state_graph')

def make_extended_graph():
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
            "Q2" : ("Container", "Height"),
        },
        {
            "type" : "P+",
            "args" : None,
            "Q1" : ("Container", "Height"),
            "Q2" : ("Container", "Pressure"),
        },
        {
            "type" : "P+",
            "args" : None,
            "Q1" : ("Container", "Pressure"),
            "Q2" : ("Drain", "Outflow"),
        },
        {
            "type" : "VC",
            "args" : MValue.MAX,
            "Q1" : ("Container", "Volume"),
            "Q2" : ("Container", "Height"),
        },
        {
            "type" : "VC",
            "args" : MValue.ZERO,
            "Q1" : ("Container", "Volume"),
            "Q2" : ("Container", "Height"),
        },
        {
            "type" : "VC",
            "args" : MValue.MAX,
            "Q1" : ("Container", "Height"),
            "Q2" : ("Container", "Pressure"),
        },
        {
            "type" : "VC",
            "args" : MValue.ZERO,
            "Q1" : ("Container", "Height"),
            "Q2" : ("Container", "Pressure"),
        },
        {
            "type" : "VC",
            "args" : MValue.MAX,
            "Q1" : ("Container", "Pressure"),
            "Q2" : ("Drain", "Outflow"),
        },
        {
            "type" : "VC",
            "args" : MValue.ZERO,
            "Q1" : ("Container", "Pressure"),
            "Q2" : ("Drain", "Outflow"),
        },
    ]
    
    mags = list(map(int, MValue))    
    ders = list(map(int, DValue))
    
    blue_print = {
            "Hoose" : {
                "Inflow" : ([0,1], ders)
            },
            "Container" : {
                "Volume" : (mags, ders),
                "Height" : (mags, ders),
                "Pressure" : (mags, ders),
            },
            "Drain" : {
                "Outflow" : (mags, ders)
            },
        }

    states = qr_engine(blue_print, relations)
    
    make_state_graph(states, '../state_graph_expanded')

def main():
    make_simple_graph()
    make_extended_graph()
    
if __name__ == "__main__":
    main()