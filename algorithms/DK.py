from Graph import G, N
from CurrentBestClique import oset, initCBC, setCBC, CBC
from coloring import greedy_coloring

# Deniss Kumlander - Problems of optimization: an exact algorithm for finding a maximum clique optimized for dense graphs (2005)
# https://kirj.ee/wp-content/plugins/kirj/pub/phys-2-2005-79-86_20211016172808.pdf

def run_DK():
    initCBC()
    
    initialC = oset()
    initialK = DK_initialK()

    DK(initialC, initialK)
    return

def DK(C: oset, K: oset):
    if len(K) == 0:
        if len(C) > CBC():
            setCBC(C)
        return

    while len(K) != 0:
        if len(C) + subgraphDegree(K) <= CBC():
            return
        
        v = K[0]
        K = K - {v}
        DK(C.union({v}), K.intersection(N(v)))
    return

def subgraphDegree(V: oset) -> int:
    # Kumlander Definition 1: A colour class is called existing on a subgraph Gp if any vertex from this colour class belongs to the subgraph Gp.
    # Kumlander Definition 2: The degree of a subgraph Gp equals the number of colour classes existing on that subgraph.
    colors = set(colorMap[v] for v in V)
    return len(colors)

def DK_initialK() -> oset:
    # Find a vertex-colouring and reorder vertices so that the first vertices belong to the last found colour class,
    # then come vertices of the last colour class but one, etc. – the last vertices should belong to the first colour class.
    global colorMap
    colorMap, colorList, _ = greedy_coloring(G(), sort=False)

    # re-sort the vertices in the order they are added into colour classes
    flatColorReorderedSet = oset(node for colorSublist in colorList[::-1] for node in colorSublist[::-1])
    return flatColorReorderedSet
