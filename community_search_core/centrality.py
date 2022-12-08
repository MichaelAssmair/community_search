"""girvan and newman algorithm"""

import networkx as nx
from collections import deque
import random

def girvan_newman(G: nx.Graph):
    """Algorithmus berechnet Communitys des Graphen G"""

    edges = list(G.edges)
    while edges:
        edges.remove(edge_betweenness(G, edges))


def edge_betweenness(G, edges):
    
    return random.choice(edges)


girvan_newman(nx.karate_club_graph())