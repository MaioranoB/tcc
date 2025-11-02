from Graph import G, N
from CurrentBestClique import oset, initCBC, setCBC, CBC

# Carraghan & Pardalos - An exact algorithm for the maximum clique problem (1990)
# https://www.sciencedirect.com/science/article/pii/016763779090057C

def run_CP():
    initCBC()

    initialC = oset() # clique (current solution)
    initialK = CP_initialK() # initial vertex order
    
    CP(initialC, initialK)
    return

def CP(C: oset, K: oset):
    if len(C) > CBC():
        setCBC(C)
    
    while len(K) != 0:
        if len(C) + len(K) <= CBC():
            return
        v = K[0]
        K = K - {v}
        CP(C.union({v}), K.intersection(N(v)))
    return

def CP_initialK() -> oset:
    # ordering of the vertices of G, where v1 is the vertex of smallest degree in G, v2 the vertex of smallest degree in G - {v1}, and so on...
    sortedByDegree = oset()
    nodesDegreeDict = dict(G().degree) # dict mapping nodes to their degree (node: degree)

    for _ in G():
        minNode = min(nodesDegreeDict, key=nodesDegreeDict.get) # node with smallest degree
        sortedByDegree.add(minNode)
        del nodesDegreeDict[minNode]

        for neighbor in N(minNode):
            if neighbor not in sortedByDegree:
                nodesDegreeDict[neighbor] -= 1
    
    return sortedByDegree
