from typing import Iterable
from Graph import G, N, nodes_sorted_by_degree

def _firstColorAvailable(usedColors: set) -> int:
    color = 1
    while color in usedColors:
        color += 1
    return color

def greedy_coloring(V: Iterable, sort = True, decreasingDegrees = True) -> tuple[dict,list,int]:
    # most common strategy is to sort from highest to lowest degree (Welsh Powell?)
    if sort:
        node_order = nodes_sorted_by_degree(V, decreasingDegrees)
    else:
        node_order = V

    colorMap = dict() # maps node to its color class
    colorList = [[]] # list of colors class: [[], [nodes with color1], [nodes with color2], ...] (+1 to ignore index 0)
    maxColor = 0
    for v in node_order:
        usedNeighborColors = {colorMap[nbr] for nbr in N(v) if nbr in colorMap}
        vColor = _firstColorAvailable(usedNeighborColors)
        colorMap[v] = vColor
        if vColor > maxColor:
            maxColor = vColor
            colorList.append([v])
        else:
            colorList[vColor].append(v)
    
    return colorMap, colorList, maxColor


def DSatur(V) -> tuple[list,int]:
    degreeSaturation = {v: 0 for v in G()} # number of different colours being used by the vertex neighbors

    colorList = []
    for _ in V:
        v = 0 # escolher próximo vértice a colorir
        maxSaturation = -1
        for u in V:
            if degreeSaturation[u] > maxSaturation:
                maxSaturation = degreeSaturation[u]
                v = u

        degreeSaturation[v] = -len(degreeSaturation) - 1 # nunca mais escolher este vértice
        for neighbor in N(v):
            degreeSaturation[neighbor] += 1

        # colorir vértice v
        newColorClass = True
        for colorClass in colorList:
            newColorClass = False
            for u in colorClass:
                if G().has_edge(v, u):
                    newColorClass = True
                    break
            if not newColorClass:
                colorClass.append(v)
                break
        if newColorClass:
            colorList.append([v])
            
    maxColor = len(colorList)
    return colorList, maxColor
