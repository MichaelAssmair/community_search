"""Utileties"""

import numpy as np
from networkx.algorithms.community.community_utils import is_partition

def modularity(G, communities):
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
        m = m / (len(G.edges))
    else:
        m = m / (len(G.edges)*2)

    q = np.trace(m) - np.sum(np.matmul(m, m))

    return q


def _idx_lookup(node, communities):
    for idx, community in enumerate(communities):
        if node in community:
            return idx
