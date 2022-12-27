"""Utilities"""

# Authon: Michael Assmair

from networkx.algorithms.community import is_partition
import numpy as np
import networkx as nx

__all__ = ["modularity"]

def modularity(G, communities):
    """Berechnet die Modulatität des Graphen G anhand
    der übergebenen Liste von Communitys.

    Parameters
    ----------
    G : Ein Networkx Graph

    communities : Eines Liste, die beschreibt, wie der
        Graph in Communitys aufgeteilt ist.
        
    Returns
    -------
    modularity : Wert der die Güte der Aufteilung eines
        Graphen in Communitys messt. Wenn die Übergebene Liste
        der Communitys keine Partitionierung des Graphen G ist,
        wird -1 als Wert zurückgegeben
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


def to_graphml_with_communities(G, communities, path):
    for idx, community in enumerate(communities):
        for node in community:
            G.nodes[node][f"c{idx}"] = 1

    nx.write_graphml(G, path)