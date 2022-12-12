"""spectral clustering algorithm"""

# Author: Michael assmair

import networkx as nx
from networkx.utils import groups
import random
import numpy as np
import scipy.sparse.linalg
from sklearn.cluster import SpectralClustering

def spectral_clustering(G: nx.Graph, k):
    """spectral clustering"""

    g = G.copy(as_view=True).to_undirected()

    adj_matrix = _adj_matrix(g)
    dist_matrix = _dist_matrix(g)

    lap_matrix = dist_matrix - adj_matrix

    eigval, eigvec = scipy.sparse.linalg.eigsh(lap_matrix, k=k, which="SM")

    clusters = k_means(eigvec, k)
    print("my spec:    ", clusters)

    communities = {node: cluster for node, cluster in zip(G.nodes, clusters)}

    return list(groups(communities).values())


def k_means(D, k):
    means = _choice_means(D, k)
    clusters = [0 for i in range(len(D))]

    finished = False

    while not finished:
        finished = True
        
        for i, point in enumerate(D):
            dist = float("inf")
            new_mean = None
            for n, mean in enumerate(means):
                new_dist = np.linalg.norm(mean - point)
                if new_dist < dist:
                    dist = new_dist
                    new_mean = n
                
            if new_mean != clusters[i]:
                clusters[i] = new_mean
                finished = False
    
    for n in range(k):
        means[n] = [0 for i in range(k)]
        count = 0
        for j, point in enumerate(D):
            if clusters[j] == n:
                means[n] += D[j]
                count += 1
            
        means[n] = means[n]/count

    return clusters
                    

def _choice_means(D, k):
    """Auswahl der Startpunkte"""

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


def _adj_matrix(G, weight=None):
    """Gibt die gewichtete Adjazenzmatrix der Graphen G zurück."""

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


def _dist_matrix(G, weight=None):
    """Gibt die Gradmatrix des Graphen G zurück."""

    dist_matrix = np.zeros(shape=(G.number_of_nodes(), G.number_of_nodes()))

    for i, node in enumerate(G.nodes):
        for neighbor in G.adj[node]:
            
            if nx.is_weighted(G, weight=weight):
                dist_matrix[i][i] += G[node][neighbor][weight]
            else:
                dist_matrix[i][i] += 1

    return dist_matrix



graph = nx.les_miserables_graph()

clustering = SpectralClustering(n_clusters=11, affinity="precomputed").fit(_adj_matrix(graph))
print("sklearn_spec", list(clustering.labels_))
clustering.eigen_tol

spectral_clustering(graph, 11)