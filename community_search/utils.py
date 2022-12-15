"""Utilities"""

import numpy as np
from networkx.algorithms.community import is_partition
import numpy as np

__all__ = ["modularity"]

def modularity(G, communities):
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

    modularity = np.trace(m) - np.sum(np.matmul(m, m))

    return modularity



def _idx_lookup(node, communities):
    """Liefert den Index der Community, in der sich
    der übergebene Knoten befindet.
    """
    for idx, community in enumerate(communities):
        if node in community:
            return idx