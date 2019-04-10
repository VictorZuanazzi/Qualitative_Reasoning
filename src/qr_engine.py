from overgeneration import over_generate
from validation import pruneInvalidStates
from connect_states import connect_states

def qr_engine(state_blueprint, relations):
    states = over_generate(state_blueprint)
    pruned_states = pruneInvalidStates(states, relations) 
    connected_states = connect_states(pruned_states, relations)
    
    print("\n".join([str(s) for s in connected_states]))
    print("States after pruning:",len(connected_states))

    return connected_states