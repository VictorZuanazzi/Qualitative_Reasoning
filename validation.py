from relationFunctions import getFunc
from derivative import DValue
from itertools import product

def getRelationQuantities(state, relation):
    entity1, quan1 = relation["Q1"]
    entity2, quan2 = relation["Q2"]
    head = state[entity1][quan1]
    tail = state[entity2][quan2]
    return head, tail

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

def addDerivatives(a, b):
    # already ambigous
    if len(a) > 1 or len(b) > 1:
        return [-1,0,1]
    else:
        return {
            (0,0) : [0],
            (-1,0) : [-1],
            (0,-1) : [-1],
            (-1,-1) : [-1],
            (1,0) : [1],
            (0,1) : [1],
            (1,1) : [1],
            (-1,1) : [-1,0,1],
            (1,-1) : [-1,0,1],
        }.get((a[0],b[0]))


def checkExogenous(state, relations):
    derivatives = {}
    magnitudes = {}

    exoRelations = list(filter(lambda rel: rel["type"] is "EX", relations))
    exoQuantities = [rel["Q2"] for rel in exoRelations]

    for eKey, e in state.items():
        for qKey, q in e.items():
            if (eKey, qKey) in exoQuantities:
                derivatives[(eKey, qKey)] = q.derivative.value
            else:
                derivatives[(eKey, qKey)] = DValue.ZERO
            magnitudes[(eKey, qKey)] = q.magnitude.value

    return magnitudes, derivatives

def toStates(state, possibleDerivatives):
    stateList = []
    ds = product(*list(possibleDerivatives.values()))
    for d in ds:
        copy = state_copy(state)
        for i, key in enumerate(possibleDerivatives.keys()):
            copy[key[0]][key[1]].derivative.value = d[i]
        stateList.append(copy)

    return stateList

def applyCausalMode(state, relations):
    states = [[] for i in range(len(relations) + 1)]
    # Assume no exogenous influence in inital state
    states[0] = [state_copy(state)]
    for _, e in states[0][0].items():
        for _, q in e.items():
            q.derivative.value = DValue.ZERO

    for i, rel in enumerate(relations):
        if(rel["type"] is "EX"):
            _, tail = getRelationQuantities(state, rel)
            _, s_tail = getRelationQuantities(states[i][0], rel)
            s_tail.derivative.value = tail.derivative.value
            states[i+1] = [state_copy(states[i][0])]
            continue

         # get implemetation for relation
        func = getFunc(rel["type"], rel["args"])

        for s in states[i]:
            # get head and tail quantity
            head, tail = getRelationQuantities(s, rel)
            new_tail = tail.copy()

            # apply relation
            func(head, new_tail)

            if rel["type"] == "VC":
                new_s = state_copy(s)
                _, new_s_tail = getRelationQuantities(new_s, rel)
                new_s_tail.magnitude.value = new_tail.magnitude.value
                states[i+1].append(new_s)
            else:
                _, s_tail = getRelationQuantities(s, rel)
                ds = addDerivatives([new_tail.derivative.value], [s_tail.derivative.value])
                for d in ds:
                    new_s = state_copy(s)
                    _, new_s_tail = getRelationQuantities(new_s, rel)
                    new_s_tail.derivative.value = d
                    states[i+1].append(new_s)

    return states[-1]

def isStateValid(state, relations):
    isValid = True

    # check boundary cases
    for _, e in state.items():
        for _, q in e.items():
            isValid &= not (q.magnitude.isAtUpperBound() and q.derivative.value == DValue.PLUS)
            isValid &= not (q.magnitude.isAtLowerBound() and q.derivative.value == DValue.MINUS)

    causalStates = applyCausalMode(state, relations)
    isValid &= state in causalStates

    return isValid
