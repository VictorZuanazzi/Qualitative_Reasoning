# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 16:55:06 2019

@author: Victor Zuanazzi
"""

from quantity import Quantity
from magnitude import Magnitude, MValue
from derivative import Derivative, DValue


def Q_exceptions(q, mags):
    """Free space to hardcode shit.
    Output: 
        True if one of the exception cases is reached, False otherwise."""
    
    #exception 1: Inflow does not have a max quantity.
    if q == "Inflow" and mags == 2:
        return True
    
    return False

def over_generate(state=None, mag_Enum=MValue, der_Enum=DValue, exception=Q_exceptions):
    """generates all combinations of states.
    Assumes that all quantities have the can take the same magnetude and 
    derivative values.
    Input:
        state: dict(dict: Quantity(mag_Enum, der_Enum)) defining the state.
        
    Output:
        list(state) all possible states.
    """
    
    #defaut state in case no state is given.
    if state == None:
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
        }
    
    #gets a list of possible values for magintude and derivatives
    mags = list(map(int, mag_Enum))
    ders = list(map(int, der_Enum))
    
    #Creates all states
    states = []
    
    for element in state:
        for q in state[element]:
            for m in mags:
                for d in ders:
                    
                    #checks for exceptions
                    if exception(q, mags):
                        continue
                    
                    #generate a possibly impossible state.
                    state[element][q] = Quantity(Magnitude(m), Derivative(d))
                    
                    #glue all states together in a beautiful list.
                    states.append(state)
    
    return states