from Graph import G, N
from CurrentBestClique import oset, initCBC, setCBC, CBC
from coloring import greedy_coloring

# Östergård - A fast algorithm for the maximum clique problem (2002)
# https://www.sciencedirect.com/science/article/pii/S0166218X01002906

def run_Cliquer():
    global c, found
    c = [0] * (len(G()) + 1)

    initCBC()

    V = Cliquer_initialOrder()
    
    for i in range(len(V), 0, -1): # for i = n downto 1
        found = False
        v_i = V[i-1]
        initialC = oset([v_i])
        initialK = oset(V[i-1:]) # {Vn}, {Vn-1,Vn}, ...
        Cliquer(initialC, initialK.intersection(N(v_i)))
        c[v_i]  = CBC()
    return

def Cliquer(C: oset, K: oset):
    global c, found
    
    if len(K) == 0:
        if len(C) > CBC():
            setCBC(C) # new record; save it
            found = True
        return
    
    while len(K) != 0:
        if len(C) + len(K) <= CBC(): # prune as CP algorithm
            return
        
        v = K[0]
        if len(C) + c[v] <= CBC(): # new pruning technique
            return
        K = K - {v}
        Cliquer(C.union({v}), K.intersection(N(v)))
        if found: # stopping condition
            return
    return

def Cliquer_initialOrder() -> list:
    # For good performance of the algorithm, a proper heuristic for ordering the vertices has to be chosen.
    # One can think of several ways of doing this, and these orderings may have different effects for different types of graphs.
    # Vertex-coloring could be used in some way to get a good initial ordering
    # Using a coloring that can be found in reasonable time, the vertices are ordered so that those belonging to the same color class are grouped

    _, colorList, _ = greedy_coloring(G(), sort=True, decreasingDegrees=True)

    flatColorOrderedList = list(node for colorSublist in colorList for node in colorSublist)
    return flatColorOrderedList
