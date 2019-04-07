from relationFunctions import getFunc
from derivative import DValue

def getRelationQuantities(state, relation):
    entity1, quan1 = relation["Q1"]
    entity2, quan2 = relation["Q2"]
    head = state[entity1][quan1]
    tail = state[entity2][quan2]
    return head, tail

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

def applyCausalMode(state, relations, magnitudes):
    possibleDerivatives = {}
    for rel in relations:
        if(rel["type"] is "EX"):
            continue
        # get implemetation for relation
        func = getFunc(rel["type"], rel["args"])
        
        # get head and tail quantity
        head, tail = getRelationQuantities(state, rel)
        new_tail = tail.copy()

        # apply relation
        func(head, new_tail)

        if rel["type"] == "VC":
            if new_tail != tail:
                magnitudes[rel["Q2"]] = new_tail.magnitude.value
        else:
            if not rel["Q2"] in possibleDerivatives:
                possibleDerivatives[rel["Q2"]] = []

            if not new_tail.derivative.value in possibleDerivatives[rel["Q2"]]:
                possibleDerivatives[rel["Q2"]].append(new_tail.derivative.value)

            if len(possibleDerivatives[rel["Q2"]]) == 2 and possibleDerivatives[rel["Q2"]][0]== -1 * possibleDerivatives[rel["Q2"]][1]:
                # add derivative = 0 for continuity
                possibleDerivatives[rel["Q2"]].append(0)

    return magnitudes, possibleDerivatives

def isStateValid(state, relations):
    isValid = True

    # check boundary cases
    for _, e in state.items():
        for _, q in e.items():
            isValid &= not (q.magnitude.isAtUpperBound() and q.derivative.value == DValue.PLUS)
            isValid &= not (q.magnitude.isAtLowerBound() and q.derivative.value == DValue.MINUS)

    magnitudes, derivatives = checkExogenous(state, relations)
    magnitudes, possibleDerivatives = applyCausalMode(state, relations, magnitudes)
    
    # check if state changed to valid option
    for eKey, e in state.items():
        for qKey, q in e.items():
            key = (eKey, qKey)
            if key in possibleDerivatives:
                if not q.derivative.value in possibleDerivatives[key]:
                    isValid &= False
                    break
            elif not q.derivative.value  is derivatives[key]:
                isValid &= False
                break

            if magnitudes[key] != q.magnitude.value:
                isValid &= False
                break

    return isValid
