# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 20:44:27 2019

@author: Victor Zuanazzi
"""

import pydot

def state_to_string(state):
    """returns a string version of the state.
    Input:
        state (state dict), one state in the dict format.
    Ouput: (str) quantities described as string with \n between different 
        quantities and different entities.
    """
    
    description = ""
    
    for entity in state:
        
        #ignores non quantities 
        if (entity == "id") | (entity == "prev") | (entity == "next"):
            continue
        
        #new line for entity
        
        for q in state[entity]:
            #new line for each quantity
            description += "\n" + str(q[0:1]) + ": " + str(state[entity][q])
            
    return description

def make_state_graph(states, name="state_graph"):
    """make and save as png a state_graph.
    Input:
        states: (states dict format), the states to be translated into a graph.
        name: name of the file to be saved.
    Ouput: (.png) image with the state graph
    """
    
    #create the graph
    graph = pydot.Dot(graph_type='digraph')
    graph.set_graph_defaults(sep=0.5, overlap=False, splines=True)
    
    #create a list with empity nodes
    node = [pydot.Node()]*len(states)
    
    #create all states and add them to the graph
    for i, s in enumerate(states):
        
        #fetches the string description of the graph
        description = state_to_string(s)
        
        #creates the node state
        node[i] = pydot.Node( str(i), label=str(i)+description, shape="box")
        
        #add the node to the graph.
        graph.add_node(node[i])
        
    #conect the states
    for i, s in enumerate(states):
        
        #fetch the outgoing states from the current state
        next_ss = list(s.get("next", []))
        
        #perform all the edges
        for n_s in next_ss:
            graph.add_edge(pydot.Edge(node[i], node[n_s], label=s["next"][n_s]))
    
    print("Graph nodes:",len(graph.get_node_list()), "edges:",len(graph.get_edge_list()))
    #saves the graph.
    graph.write_png(name+'.png', prog='neato')
        