from relationFunctions import getFunc

def getRelationQuantities(state, relation):
    entity1, quan1 = relation["Q1"]
    entity2, quan2 = relation["Q2"]
    head = state[entity1][quan1]
    tail = state[entity2][quan2]
    return head, tail

def isStateValid(state, relations):
    isValid = True

    for rel in relations:
        # get implemetation for relation
        func = getFunc(rel["type"])
        # get head and tail quantity
        head, tail = getRelationQuantities(state, rel)
        new_tail = tail.copy()

        # apply relation
        func(head, new_tail)
        
        # check if state changed
        if not new_tail == tail:
            isValid = False
            break

    return isValid
