"""spectral clustering algorithm"""

import networkx as nx
import random
import numpy as np
import scipy.sparse.linalg

def spectral_clustering(G: nx.Graph, k):
    """spectral clustering"""

    g = G.copy(as_view=True).to_undirected()

    adj_matrix = _adj_matrix(g)
    dist_matrix = _dist_matrix(g)

    lap_matrix = dist_matrix - adj_matrix
    eigval, eigvec = scipy.sparse.linalg.eigsh(lap_matrix, k=k, which="SM")

    k_means(eigvec, k)


def k_means(D, k):
    means = _choice_means(D, k)
    clusters = {}

    finished = False

    while not finished:
        finished = True
        
        for point in D:
            tmp_dist = float("inf")
            for mean in means:
                new_dist = np.linalg.norm(mean - point)
                if new_dist < tmp_dist:
                    tmp_dist = new_dist





    
def _choice_means(D, k):
    means = []
    means.append(random.choice(D))

    for i in range(k-1):
        vec_dist = []
        for point in D:
            dist = float("inf")
            for mean in means:
                new_dist = np.linalg.norm(mean - point)
                dist = new_dist if new_dist < dist else dist
            
            vec_dist.append(dist**2)
            
        means.append(random.choices(D, weights=vec_dist, k=1)[0])

    return means


def _adj_matrix(G: nx.Graph, weight=None):
    """Gewichtete Adjazenzmatrix"""

    adj_matrix = np.zeros(shape=(G.number_of_nodes(), G.number_of_nodes()))

    for i, node_i in enumerate(G.nodes):
        for j, node_j in enumerate(G.nodes):

            if not (node_i, node_j) in G.edges:
                continue
            elif nx.is_weighted(G, weight=weight):
                adj_matrix[i][j] = G[node_i][node_j][weight]
            else:
                adj_matrix[i][j] = 1
    
    return adj_matrix


def _dist_matrix(G: nx.Graph, weight=None):
    """Eine Diagonalmatrix"""

    dist_matrix = np.zeros(shape=(G.number_of_nodes(), G.number_of_nodes()))

    for i, node in enumerate(G.nodes):
        for neighbor in G.adj[node]:
            
            if nx.is_weighted(G, weight=weight):
                dist_matrix[i][i] += G[node][neighbor][weight]
            else:
                dist_matrix[i][i] += 1

    return dist_matrix



    

    




(spectral_clustering(nx.karate_club_graph(), 3))

#graph = nx.florentine_families_graph()
#print(_adj_matrix(graph))
#adj_mat = nx.adjacency_matrix(graph)
#print(adj_mat)
#graph.nodes["Medici"]["id"] = 1
#print(*graph.nodes.items())
#print(graph.edges)
