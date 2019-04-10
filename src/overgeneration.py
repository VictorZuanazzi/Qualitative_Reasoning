# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:55:06 2019

@author: Victor Zuanazzi
"""

from quantity import Quantity
from magnitude import Magnitude, MValue
from derivative import Derivative, DValue
from itertools import product

def over_generate(blue_print=None, mag_Enum=MValue, der_Enum=DValue):
    """generates all combinations of states.
    Assumes that all quantities have the can take the same magnetude and 
    derivative values.
    Input:
        blue_print: dict(dict: (list, list))) defining the state and the values it 
        can take.
        mag_Enum: IntEnum with the possible values for magntudes.
        der_Enum: IntEnum with the possible values for derivatives.            
    Output:
        list(states) all possible states.
    """
    
    #defaut state blueprint in case none is given.
    if blue_print == None:
        
        mags = list(map(int, mag_Enum))
        ders = list(map(int, der_Enum))
        
        blue_print = {
            "Hoose" : {
                "Inflow" : ([0,1], ders)
            },
            "Container" : {
                "Volume" : (mags, ders)
            },
            "Drain" : {
                "Outflow" : (mags, ders)
            },
        }
    
    
    #Creates all states
    states = []
    t = []
    
    for e in blue_print:
        for q in blue_print[e]:
            t.append(blue_print[e][q][0])
            t.append(blue_print[e][q][1])
            
    t = tuple(t)
    combs = list(product(*t))
    
    for c in combs:
        idx = 0
        
        state = {}
        for e in blue_print:
            state[e] = {}
            for q in blue_print[e]:
                mag_bound = blue_print[e][q][0][-1]
                state[e][q] = Quantity(Magnitude(c[idx], upperBound=mag_bound), Derivative(c[idx+1]))
                idx += 2
                           
        states.append(state)
    
    return states

def main():
    print(over_generate())

if __name__ == "__main__":
    main()