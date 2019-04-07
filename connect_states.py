# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 14:05:34 2019

@author: Victor Zuanazzi
"""
from quantity import Quantity
from itertools import product
from copy import deepcopy
from validation import applyCausalMode

def state_copy(state):
    """copy quantities of the state.
    Not entities that have no quantity are ignored.
    """
    c_s = {}
    
    for entity in state:
        
        if (entity == "id") | (entity == "prev") | (entity == "next"):
            #c_s[entity] = state[entity].copy()
            continue
        
        c_s[entity] = {}
        
        for q in state[entity]:
            c_s[entity][q] = state[entity][q].copy()

    return c_s
        
def add_directional_connection(prev_s, next_s, explanation = ""):
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
        prev_s["next"][next_s["id"]] = explanation
    else:
        prev_s["next"] = {next_s["id"]: explanation}
        
    #add the id of the previous state to the next state.
    if next_s.get("prev"):
        next_s["prev"].add(prev_s["id"])
    else:
        next_s["prev"] = {prev_s["id"]}

def eq(s1, s2):
    result = True
    for eKey, e in s1.items():
        for qKey, q in e.items():
            result &= s2[eKey][qKey] == q
    return result

def compare_states_except(state_1, state_2, exc_quantity = "Inflow"):
    """compare if the quantities of the states are the same except for the
    given quantity. Non-quantities are ignored.
    Input:
        state_1, state_2: (dict state format) states to be compared.
        exc_quantity: quantity to be ignored during the comparison.
        
    Ouput (bool) True if the states are the same (except for the excluded 
          quantity) or False if at least one quantity differs. 
    """
    
    for entity in state_1:
        
        #non quantities are ignored
        if (entity == "id") | (entity == "prev") | (entity == "next"):
            continue
        
        for q in state_1[entity]:
            
            #ignores the defined quantity
            if q == exc_quantity:
                continue
            
            if state_1[entity][q] != state_2[entity][q]:
                #if one of the quantities is different, then the state is different.
                return False
                
    return True
    

def list_to_state(list_state, a_state):
    """transforms a list with values correctly ordered for the state into the
    state format.
    Input:
        list_state: (list(list(Quantities))) the list containing the
            quantities information of the state.
        a_state: (state format) serves as blue_print for the list_state. It 
            copies the entities that do not carachterize a state, such as "id", 
            "next" and "prev".
    
    """
    #deepcopy does the job. 
    c_state = deepcopy(a_state)
    
    count = 0
    
    for entity in c_state:
        
        #ignored values
        if (entity == "id") | (entity == "prev") | (entity == "next"):
            continue
        
        for q in c_state[entity]:
            c_state[entity][q] = list_state[count]
            count += 1
            
    return c_state

def diff_of_states(state1, state2):
    diffs = ""
    
    for entity in state1:
        
        #ignored values
        if (entity == "id") | (entity == "prev") | (entity == "next"):
            continue
        
        for q in state1[entity]:
           if state1[entity][q] != state2[entity][q]:
               diffs += str(q) + "\n"
    
    return diffs

    
def connect_states(unconnected_states, relations):
    """create phisically possible connection between states.
    NOT FULLU WORKING YET"""
    
    #add an id to each state.
    for i, s in enumerate(unconnected_states.copy()):
        s["id"] = i
        
    #For each state, check if it is possible to transition to the other state.
    for s_1 in unconnected_states:
        
        #obligatory transitions (effects of the derivatives):
        #kinda working but there are some weird stuff, 
        #commented to debug external influences
        
        #gets all the possibilities of transitions considering all quantities 
        #of entities.
        quantities = []
        for entity_1 in s_1.copy():
            
            if (entity_1 == "id") | (entity_1 == "prev") | (entity_1 == "next"):
                continue
            
            for q in s_1[entity_1]:       
                #!!! applyDerivative changes the upper bound of inflow !!!
                quantities.append(Quantity.applyDerivative(s_1[entity_1][q]))
          
        #get all combinations of possible next states.
        all_poss = list(product(*quantities))
        
        #compares all_possibilities of next states with the posssible next states.
        

        for maybe_next_state in all_poss:
            s = list_to_state(maybe_next_state, s_1)
            causalStates = applyCausalMode(s,relations)
            for cs in causalStates:
                for s_2 in unconnected_states:
                    
                    #it is slow, but it works! (and I can spare that millisecond)
                    if eq(cs, s_2):
                        #connects states
                        add_directional_connection(s_1, s_2, '∂') 
            
        #external influences:
        
        #hardcoded because I want to be over with it.
        #works because and despite some impossible states!
        #best way towards robust code is to use the rules between the quantities.
        for s_2 in unconnected_states:
            
            #open tap
            #if the tap is closed
            if s_1["Hoose"]["Inflow"].magnitude.value == 0:
                if s_1["Hoose"]["Inflow"].derivative.value == 0:
                    
                    #if the tap is opening
                    if s_2["Hoose"]["Inflow"].magnitude.value == 0:
                        if s_2["Hoose"]["Inflow"].derivative.value == 1:
                            
                            #if the rest of the state is the same
                            if compare_states_except(s_1, s_2, exc_quantity = "Inflow"):
                                #connect states
                                add_directional_connection(s_1, s_2, 'exo') 
            
            #close tap
            #if the tap is open
            if s_1["Hoose"]["Inflow"].magnitude.value == 1:
                if s_1["Hoose"]["Inflow"].derivative.value == 0:
                    
                    #if the tap is closing
                    if s_2["Hoose"]["Inflow"].magnitude.value == 1:
                        if s_2["Hoose"]["Inflow"].derivative.value == -1:
                            
                            #if the rest of the state is the same
                            if compare_states_except(s_1, s_2, exc_quantity = "Inflow"):
                                #connect states
                                add_directional_connection(s_1, s_2, 'exo') 

    # add_directional_connection(unconnected_states[3], unconnected_states[12],"hand")
    # add_directional_connection(unconnected_states[4], unconnected_states[15],"hand")
    # add_directional_connection(unconnected_states[4], unconnected_states[13],"hand")
    # add_directional_connection(unconnected_states[4], unconnected_states[14],"hand")
    # add_directional_connection(unconnected_states[5], unconnected_states[16],"hand")
    # add_directional_connection(unconnected_states[5], unconnected_states[17],"hand")
    # add_directional_connection(unconnected_states[11], unconnected_states[2],"hand")
    # add_directional_connection(unconnected_states[8], unconnected_states[1],"hand")
    return unconnected_states
        
        
        
        
        
        
        
        
        
        
        
        
        