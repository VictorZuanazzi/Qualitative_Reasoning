# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:05:34 2019

@author: Victor Zuanazzi
"""

#not used yet to keep the data structure consistent.
class State:
    
    def __init__(self, s_id, s_desc):
        self.id =  s_id    
        self.description = s_desc
        self.previous = []
        self.next = []
    
    def add_next_state(self, next_id):
        self.previous.append(next_id)
    
    def add_previous_state(self, prev_id):
        self.next.append(prev_id)
        
        
        
def add_directional_connection(prev_s, next_s):
    """makes the directional connections between states.
    Inputs:
        prev_s: (dict state format) the previous state.
        next_s: (dict state format) the next state.
    Result:
        prev_s["next"] = next_s["id"] adds the id of the next state to the 
            previous state
        next_s["prev"] = prev_s["id"] adds the id of the previous state to the 
            next state.
    """
    
    #add the id of the next state to the previous state.
    if prev_s.get("next"):
        prev_s["next"].add(next_s["id"])
    else:
        prev_s["next"] = {next_s["id"]}
        
    #add the id of the previous state to the next state.
    if next_s.get("prev"):
        next_s["prev"].add(prev_s["id"])
    else:
        next_s["prev"] = {prev_s["id"]}
        
    

def connect_states(unconnected_states):
    """create phisically possible connection between states.
    NOT FULLU WORKING YET"""
    
    #add an id to each state.
    for i, s in enumerate(unconnected_states.copy()):
        s["id"] = i
        
    #For each state, check if it is possible to transition to the other state.
    for s_1 in unconnected_states:
        
        #hardcoded, to be changed later
        
        for thing in s_1.copy():
            
            if (thing == "id") | (thing == "prev") | (thing == "next"):
                continue
            
            for q in s_1[thing]:
                
                for s_2 in unconnected_states.copy():
                    
                    #those are the obligatory changes:
                    #derivative changes the magnitude.
                    #check cross quatities must happen.
                    if s_1[thing][q].derivative.value > 0:
                        if s_2[thing][q].magnitude.value > s_1[thing][q].magnitude.value:
                            add_directional_connection(s_1, s_2)
                    
                    elif s_1[thing][q].derivative.value < 0:
                        if s_2[thing][q].magnitude.value < s_1[thing][q].magnitude.value:
                            add_directional_connection(s_1, s_2)
                            
                            
                    #quantities that can change at will:
                    if q  == "Inflow":
                        
                        if s_1[thing][q].magnitude.value == 0:
                            if s_2[thing][q].magnitude.value == 1:
                                add_directional_connection(s_1, s_2)
                            
                        if s_1[thing][q].magnitude.value == 1:
                            if s_2[thing][q].magnitude.value == 0:
                                add_directional_connection(s_1, s_2)
                            
                            
                    
        
        
        
        
        
        
    return unconnected_states
        
        
        
        
        
        
        
        
        
        
        
        
        