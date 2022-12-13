"""girvan-newman algorithm"""

# Author: Michael Assmair

import networkx as nx
from collections import deque
import timeit

def girvan_newman(G: nx.Graph):
    """Algorithmus berechnet Communitys des Graphen G"""

    g = G.copy().to_undirected()
    num_communuties = nx.number_connected_components(g)


    while g.number_of_edges() > 0:
        betweenness = _edge_betweenness(g)
        max_betweenness = max(betweenness, key=betweenness.get)

        g.remove_edge(max_betweenness[0], max_betweenness[1])

        if num_communuties < nx.number_connected_components(g):
            num_communuties = nx.number_connected_components(g)
            yield nx.connected_components(g)


def _edge_betweenness(G: nx.Graph):
    """Edge Betweenness"""

    betweenness = {edge: 0.0 for edge in G.edges}

    for start_node in G.nodes:
        nodes = {node: {"dist": None, "weight": None} for node in G.nodes}
        edges = {edge: 0.0 for edge in G.edges}
        nodes[start_node]["dist"] = 0
        nodes[start_node]["weight"] = 1

        queue = deque([start_node])

        while queue:
            next_node = queue.popleft()

            for adj_node in G.adj[next_node]:

                if nodes[adj_node]["dist"] == None:
                    nodes[adj_node]["dist"] = nodes[next_node]["dist"] + 1
                    nodes[adj_node]["weight"] = nodes[next_node]["weight"]
                    queue.append(adj_node)

                elif nodes[adj_node]["dist"] == nodes[next_node]["dist"] + 1:
                    nodes[adj_node]["weight"] += nodes[next_node]["weight"]

        for node, _ in sorted(nodes.items(), key=lambda item: item[1]["dist"], reverse=True):
            weight_sum = 1

            for adj_node in G.adj[node]:
                edge = (node, adj_node) if node < adj_node else (adj_node, node)
                weight_sum += edges[edge]
            
            for adj_node in G.adj[node]:
                edge = (node, adj_node) if node < adj_node else (adj_node, node)
                if nodes[node]["dist"] > nodes[adj_node]["dist"]:
                    edges[edge] = weight_sum * nodes[adj_node]["weight"]/nodes[node]["weight"]
                    betweenness[edge] += edges[edge]

    return betweenness