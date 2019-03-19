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
        state: dict(dict: Quantity(mag_Enum, der_Enum)) defining the state.
        
    Output:
        list(state) all possible states.
    """
    
    #defaut state in case no state is given.
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
    
    #gets a list of possible values for magintude and derivatives
    
    
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
                
                state[e][q] = Quantity(Magnitude(c[idx]), Derivative(c[idx+1]))
                idx += 2
                           
        states.append(state)
    
    return states

def main():
    print(over_generate())

if __name__ == "__main__":
    main()