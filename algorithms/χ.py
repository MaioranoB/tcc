from Graph import G, N, nodes_sorted_by_degree
from CurrentBestClique import oset, initCBC, setCBC, CBC
from coloring import greedy_coloring, DSatur

# Torsten Fahle - Simple and Fast: Improving a Branch-And-Bound Algorithm for Maximum Clique (2002)
# https://link.springer.com/chapter/10.1007/3-540-45749-6_44

def run_χ():
    initCBC()
    χ(oset(), oset(G()))
    return

def χ(C: oset, K: oset):
    if len(K) == 0:
        if len(C) > CBC():
            setCBC(C)
        return
    
    color_bound = χ_color_bound(K)
    while len(K) != 0:
        if len(C) + color_bound <= CBC():
            return
        v = K[0]
        K = K - {v}
        χ(C.union({v}), K.intersection(N(v)))
    return


def χ_color_bound(V: oset) -> int:
    nodes_decreasing_order = nodes_sorted_by_degree(V, decreasingDegrees = True)
    nodes_increasing_order = list(reversed(nodes_decreasing_order))

    _, _, color1 = greedy_coloring(nodes_decreasing_order, sort=False)
    _, _, color2 = greedy_coloring(nodes_increasing_order, sort=False)

    _, color3 = DSatur(nodes_decreasing_order)
    _, color4 = DSatur(nodes_increasing_order)

    return min(color1, color2, color3, color4)