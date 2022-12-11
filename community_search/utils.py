"""Utilities"""

import numpy as np
import networkx as nx
from networkx.algorithms.community import is_partition


def modularity(G: nx.Graph, communities):
    """Berechnet die Modularität der Graphen G mit 
    den übergebenen Communities
    """

    if not isinstance(communities, list):
        communities = list(communities)
    if not is_partition(G, communities):
        return -1

    m = np.zeros(shape=(len(communities), len(communities)))

    for i in range(m.shape[0]):
        for node in communities[i]:
            for neighbor in G.neighbors(node):
                m[i][_idx_lookup(neighbor, communities)] += 1

    if G.is_directed():       
        m = m / (G.number_of_edges())
    else:
        m = m / (G.number_of_edges()*2)


    return np.trace(m) - np.sum(np.matmul(m, m))



def _idx_lookup(node, communities):
    """Liefert den Index der Community, in der sich
    der Knoten node befindet
    """

    for idx, community in enumerate(communities):
        if node in community:
            return idx
