"""label propagation is an algorithm to find communities in large networks"""

import random
import networkx as nx
from networkx.utils import groups

def lpa_communities(G: nx.Graph, weight=None, seed=None):
    """Uses the asynchrones label propagation algorithm to find communities
    in the graph G

    Return: communities: iteratable
    """

    if not (type(G) == nx.DiGraph or type(G) == nx.Graph):
        return set()
    
    labels = {node: label for (label, node) in enumerate(G)}
    graph_is_weighted = nx.is_weighted(G)
    nodes = list(labels)
    random.seed(seed)
    finished = False

    while not finished:
        finished = True
        random.shuffle(nodes)

        for node in nodes:
            neighbor_labels = {label: 0 for label in labels.values()}

            for neighbor in G.adj[node]:
                if graph_is_weighted:
                    neighbor_labels[labels[neighbor]] += 1 * G.edges[node, neighbor]["weight"]
                else:
                    neighbor_labels[labels[neighbor]] += 1
            
            max_count = max(neighbor_labels.values())
            max_neighbor_labels = [k for k,v in neighbor_labels.items() if v == max_count]

            if labels[node] not in max_neighbor_labels:
                finished = False
            
            labels[node] = random.choice(max_neighbor_labels)


    yield from groups(labels).values()