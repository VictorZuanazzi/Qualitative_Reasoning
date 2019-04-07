from relationFunctions import getFunc
from derivative import DValue

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

def applyCausalMode(state, exo_state, relations, magnitudes):
    possibleDerivatives = {}
    for rel in relations:
        if(rel["type"] is "EX"):
            continue
        # get implemetation for relation
        func = getFunc(rel["type"], rel["args"])
        
        # get head and tail quantity
        if(rel["type"][0:1] is "I"):
            head, tail = getRelationQuantities(exo_state, rel)
        else:
            head, tail = getRelationQuantities(state, rel)
        new_tail = tail.copy()

        # apply relation
        func(head, new_tail)

        if rel["type"] == "VC":
            if new_tail != tail:
                magnitudes[rel["Q2"]] = new_tail.magnitude.value
        else:
            if not rel["Q2"] in possibleDerivatives:
                possibleDerivatives[rel["Q2"]] = [0]

            if not new_tail.derivative.value in possibleDerivatives[rel["Q2"]]:
                possibleDerivatives[rel["Q2"]] = addDerivatives([new_tail.derivative.value], possibleDerivatives[rel["Q2"]])

    return magnitudes, possibleDerivatives

def isStateValid(state, relations):
    isValid = True

    # check boundary cases
    for _, e in state.items():
        for _, q in e.items():
            isValid &= not (q.magnitude.isAtUpperBound() and q.derivative.value == DValue.PLUS)
            isValid &= not (q.magnitude.isAtLowerBound() and q.derivative.value == DValue.MINUS)

    magnitudes, derivatives = checkExogenous(state, relations)

    exo_state = state_copy(state)
    for key, value in derivatives.items():
        exo_state[key[0]][key[1]].derivative.value = value

    magnitudes, possibleDerivatives = applyCausalMode(state, exo_state, relations, magnitudes)

    # check if state changed to valid option
    for eKey, e in state.items():
        for qKey, q in e.items():
            key = (eKey, qKey)
            if key in possibleDerivatives:
                if not q.derivative.value in possibleDerivatives[key]:
                    isValid &= False
                    break
            elif not q.derivative.value is derivatives[key]:
                isValid &= False
                break

            if magnitudes[key] != q.magnitude.value:
                isValid &= False
                break

    return isValid
