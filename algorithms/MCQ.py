from Graph import G, N, nodes_sorted_by_degree
from CurrentBestClique import oset, initCBC, setCBC, CBC
from coloring import greedy_coloring

# Tomita & Seki - An Efficient Branch-and-Bound Algorithm for Finding a Maximum Clique (2003)
# https://link.springer.com/chapter/10.1007/3-540-45066-1_22

def MCQ():
    initCBC()

    initialC = oset()
    initialK = oset(nodes_sorted_by_degree(G(), decreasingDegrees = True))

    MCQ_EXPAND(initialC, initialK)
    return

def MCQ_EXPAND(C: oset, K: oset):
    if len(K) == 0:
        if len(C) > CBC():
            setCBC(C)
        return
    
    while len(K) != 0:
        if len(C) + len(K) <= CBC(): # CP pruning
            return
        
        K, graphColor = MCQ_NUMBER_SORT(K)
        if len(C) + graphColor <= CBC(): # improve |C|+|K| upper bound
            return
        
        v = K.pop() # last node (i.e. highest color class)
        MCQ_EXPAND(C.union({v}), K.intersection(N(v)))
    return

def MCQ_NUMBER_SORT(candidateSet: oset) -> oset:
    # NUMBER (color)
    _, colorList, color = greedy_coloring(candidateSet)

    # SORT (by color number/class)
    flatColorOrderedSet = oset(node for colorSublist in colorList for node in colorSublist)

    return flatColorOrderedSet, color
