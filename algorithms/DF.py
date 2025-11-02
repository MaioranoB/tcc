from Graph import G, N
from CurrentBestClique import oset, initCBC, setCBC, CBC

# Torsten Fahle - Simple and Fast: Improving a Branch-And-Bound Algorithm for Maximum Clique (2002)
# https://link.springer.com/chapter/10.1007/3-540-45749-6_44

def run_DF():
    initCBC()
    DF(oset(), oset(G()))
    return

def domainFiltering(C: oset, K: oset) -> tuple[oset, oset]:
    # calculates degrees in subgraph G[K]
    subgraphDegrees = {
        v: sum(1 for u in N(v) if u in K)
        for v in K
    }

    # reduce possible set
    # remove vertices with degree lower than the minimum required to be at a clique greater than the current largest
    deleteList = [v for v in subgraphDegrees if len(C) + subgraphDegrees[v] < CBC()] # lemma 1

    while deleteList:
        v = deleteList.pop()
        K = K - {v}
        del subgraphDegrees[v]

        for u in N(v):
            if u in subgraphDegrees:
                subgraphDegrees[u] -= 1
                if len(C) + subgraphDegrees[u] < CBC() and u not in deleteList:
                    deleteList.append(u)
    
    # increase required set
    # move to C vertices that have degree equal to |K| − 1
    minimumDegree = len(K) - 1 # lemma 2
    for v in subgraphDegrees:
        if subgraphDegrees[v] == minimumDegree:
            C = C.union({v})
            K = K - {v}
    
    return C, K

def DF(C: oset, K: oset):
    if len(C) > CBC():
        setCBC(C)
    
    while len(K) != 0:
        if len(C) + len(K) <= CBC():
            return
        
        v = K[0]
        K = K - {v}

        C_ = C.union({v})
        K_ = K.intersection(N(v))
        C_, K_ = domainFiltering(C_, K_)

        DF(C_, K_)
    return
