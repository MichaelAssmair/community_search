"""girvan-newman algorithm"""

# Author: Michael Assmair

import networkx as nx
from collections import deque


def girvan_newman(G):
    """Girvan-Newman-Alogrithmus

    Berechnet die Zerlegung von als Similarity Graphen
    repräsentierten Daten, wie von Girvan u. Newman (2001) beschrieben.

    Parameters
    ----------
    G : Gerichteter oder ungerichteter Graph, der für
        die Berechnung der Communitys in einen ungerichteten
        Graphen umgewandelt wir.

    Returns
    -------
    communities : Generator der nacheinander den Graphen in
        Communitys aufgeteilt ausgibt.
    """

    g = G.copy().to_undirected()
    betweenness = {frozenset(edge): 0.0 for edge in g.edges}
    num_components = nx.number_connected_components(g)

    while g.number_of_edges() > 0:
        betweenness.update(_edge_betweenness(g))

        max_betweenness = max(betweenness, key=betweenness.get)
        betweenness[max_betweenness] = 0
        g.remove_edge(*max_betweenness)

        if num_components < nx.number_connected_components(g):
            num_components = nx.number_connected_components(g)
            yield list(nx.connected_components(g))


def _edge_betweenness(G):
    """Berechnet die Edge Betweenness des Graphen G.
    
    Die Edge Betweenness wird wie in Brandes (2008) berechnet

    Parameters
    ----------
    G : Gerichteter oder ungerichteter Graph, für den die 
        Betweenness der Kanten berechnet wird.

    Returns
    -------
    betweenness : Dictionary, welches für jede Kante (u, v) aus G
        den Wert der Betweenness von (u, v) enthält.
    """
    betweenness = {frozenset(edge): 0.0 for edge in G.edges}

    for start_node in G.nodes:
        nodes = {
            node: {"dist": float("inf"), "weight": 0, "pred": [], "dependency": 0.0} 
            for node in G.nodes
            }

        nodes[start_node]["dist"] = 0
        nodes[start_node]["weight"] = 1

        queue = deque([start_node])
        stack = deque()

        while queue:
            next_node = queue.popleft()
            stack.append(next_node)

            for neighbor in G.neighbors(next_node):
                if nodes[neighbor]["dist"] == float("inf"):
                    nodes[neighbor]["dist"] = nodes[next_node]["dist"] + 1
                    queue.append(neighbor)

                if nodes[neighbor]["dist"] == nodes[next_node]["dist"] + 1:
                    nodes[neighbor]["weight"] += nodes[next_node]["weight"]
                    nodes[neighbor]["pred"].append(next_node)
                    
        while stack:
            next_node = stack.pop()
            
            for pred_node in nodes[next_node]["pred"]:
                dependency = ((nodes[pred_node]["weight"] / nodes[next_node]["weight"]) * 
                              (1 + nodes[next_node]["dependency"]))

                betweenness[frozenset((next_node, pred_node))] += dependency
                nodes[pred_node]["dependency"] += dependency

    return betweenness