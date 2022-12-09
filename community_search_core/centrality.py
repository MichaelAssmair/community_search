"""girvan and newman algorithm"""

import networkx as nx
from collections import deque
import random

def girvan_newman(G: nx.Graph):
    """Algorithmus berechnet Communitys des Graphen G"""

    g = G.copy().to_undirected()

    while g.number_of_edges() > 0:
        g.remove_edge(_edge_betweenness(g))


def _edge_betweenness(G: nx.Graph):
    """berechnet die edge betweenness"""

    edges = {edge: 0.0 for edge in G.edges}

    for node in G.nodes:
        nodes = {node: {"dist": 0, "weight": 0} for node in G.nodes}
        queue = deque(G.adj[node])
        nodes[node]["weight"] = 1

        for adj_node in queue:
            nodes[adj_node]["weight"] = 1
            nodes[adj_node]["dist"] = 1

        while queue:
            next_node = queue.popleft()
            
            for adj_node in G.adj[next_node]:
                if adj_node == node:
                    continue

                if nodes[adj_node]["dist"] == 0:
                    nodes[adj_node]["dist"] = nodes[next_node]["dist"] + 1
                    nodes[adj_node]["weight"] = nodes[next_node]["weight"]
                    queue.append(adj_node)

                elif nodes[adj_node]["dist"] == nodes[next_node]["dist"] + 1:
                    nodes[adj_node]["weight"] += nodes[next_node]["weight"]


_edge_betweenness(nx.krackhardt_kite_graph())