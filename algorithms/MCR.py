from Graph import G
from CurrentBestClique import oset, initCBC, setCBC
from .MCQ import MCQ_EXPAND, MCQ_NUMBER_SORT

# Tomita & Kameda - An Efficient Branch-and-bound Algorithm for Finding a Maximum Clique with Computational Experiments (2007)
# https://link.springer.com/article/10.1007/s10898-006-9039-7

def MCR():
    initCBC()

    initialC = oset()
    initialK = MCR_initialK()

    MCQ_EXPAND(initialC, initialK)
    return

def MCR_initialK():
    degreeDict = dict(G().degree) # dict mapping nodes to their degree

    exDegreeDict = { # dict mapping nodes to their external degree
        v: sum(degreeDict[u] for u in G()[v])
        for v in G()
    }
    
    # SORT
    i = len(G()) - 1    
    R = list(G())
    Rmin = minDegreeNodesList(degreeDict) # set of vertices with the minimum degree in R
    initialK = [0 for i in range(len(G()))] # candidate set

    while len(Rmin) != len(R):
        if len(Rmin) >= 2:
            p = min(Rmin, key=exDegreeDict.get) # a vertex in Rmin with the minimum external degree
        else:
            p = Rmin[0]
        
        initialK[i] = p
        R.remove(p)
        i -= 1

        updateDegrees(degreeDict, exDegreeDict, p)
        Rmin = minDegreeNodesList(degreeDict)
    
    # Regular subgraph
    Rmin, _ = MCQ_NUMBER_SORT(Rmin)
    for i in range(len(Rmin)):
        initialK[i] = Rmin[i]

    if degreeDict[Rmin[0]] == len(Rmin) - 1:
        setCBC(Rmin)
    
    return initialK

def minDegreeNodesList(degreeDict: dict) -> list:    
    minDegree = min(degreeDict.values())
    return [node for (node, degree) in degreeDict.items() if degree == minDegree]

def updateDegrees(degreeDict: dict, exDegreeDict: dict, v: int):
    vDegree = degreeDict[v]
    del degreeDict[v]
    del exDegreeDict[v]
    for u in degreeDict:
        if G().has_edge(v,u):
            degreeDict[u] -= 1
            exDegreeDict[u] -= vDegree

            for j in degreeDict:
                if G().has_edge(j,u):
                    exDegreeDict[j] -= 1
    return