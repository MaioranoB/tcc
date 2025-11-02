from orderedset import OrderedSet as oset

# Current Best Clique (C*)

_CBC = 0
# _CBC = oset()

def initCBC():
    global _CBC
    _CBC = 0
    # _CBC = oset()

def setCBC(clique: oset):
    global _CBC
    _CBC = len(clique)
    # _CBC = clique

def CBC():
    return _CBC
