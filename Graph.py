import networkx as nx
from typing import Iterable

GRAPH = nx.Graph()

def G() -> nx.Graph:
	return GRAPH

def N(v: int) -> Iterable:
    return GRAPH.neighbors(v)

def read_dimacs_graph(filePath: str) -> nx.Graph:
	global GRAPH

	edges = []
	file = open(filePath, 'r')
	for line in file:
		if line.startswith('c'): continue # comment
		elif line.startswith('p'):
			_, type, nNodes, nEdges = line.split()
		elif line.startswith('e'):
			_, v, u = line.split()
			edge = (int(v), int(u))
			edges.append(edge)
	
	file.close()

	total_edges_read = len(edges)
	if total_edges_read != int(nEdges):
		print(f"WARNING: expected {nEdges} edges, but read {total_edges_read} edges!")

	GRAPH = nx.Graph(edges)
	return GRAPH

def nodes_sorted_by_degree(nodes: Iterable, decreasingDegrees = False) -> list:
	return sorted(
		nodes,
		key = lambda v: GRAPH.degree[v],
		# key = lambda v: GRAPH.subgraph(nodes).degree[v], # grau do subgrafo induzido
		reverse = decreasingDegrees
	)
