from Graph import G, N
from CurrentBestClique import oset, initCBC, setCBC, CBC
from .χ import χ_color_bound
from .DF import domainFiltering

# Torsten Fahle - Simple and Fast: Improving a Branch-And-Bound Algorithm for Maximum Clique (2002)
# https://link.springer.com/chapter/10.1007/3-540-45749-6_44

def run_χ_DF():
    # χ + DF
    initCBC()
    χ_DF(oset(), oset(G()))
    return

def χ_DF(C: oset, K: oset):
    if len(C) > CBC():
        setCBC(C)
    
    color_bound = χ_color_bound(K)
    while len(K) != 0:
        if len(C) + color_bound <= CBC():
            return
        
        v = K[0]
        K = K - {v}

        C_ = C.union({v})
        K_ = K.intersection(N(v))
        C_, K_ = domainFiltering(C_, K_)

        χ_DF(C_, K_)
    return
