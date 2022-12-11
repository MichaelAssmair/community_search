"""girvan and newman algorithm"""

import networkx as nx
from collections import deque
import random
import heapq
from queue import PriorityQueue
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


def _edge_betweenness(G: nx.Graph) -> dict:
    """berechnet die edge betweenness"""

    edges = {edge: 0.0 for edge in G.edges}

    start_time = timeit.default_timer()

    for node in G.nodes:
        path_graph = nx.DiGraph()
        path_graph.add_nodes_from(G)

        path_graph.nodes[node]["dist"] = 0
        path_graph.nodes[node]["weight"] = 1

        queue = deque([node])
        
        while queue:
            next_node = queue.popleft()
            
            for adj_node in G.adj[next_node]:

                if "dist" not in path_graph.nodes[adj_node]:
                    path_graph.nodes[adj_node]["dist"] = path_graph.nodes[next_node]["dist"] + 1
                    path_graph.nodes[adj_node]["weight"] = path_graph.nodes[next_node]["weight"]
                    path_graph.add_edge(next_node, adj_node)
                    queue.append(adj_node)

                elif path_graph.nodes[adj_node]["dist"] == path_graph.nodes[next_node]["dist"] + 1:
                    path_graph.nodes[adj_node]["weight"] += path_graph.nodes[next_node]["weight"]
                    path_graph.add_edge(next_node, adj_node)
                
        print("path", timeit.default_timer() - start_time)
        start_time = timeit.default_timer()

        node_heap = PriorityQueue()
        for node in (node for node in path_graph.nodes if path_graph.out_degree(node) == 0):
            for pred_node in path_graph.predecessors(node):
                path_graph.edges[pred_node, node]["betweenness"] = (
                    path_graph.nodes[pred_node]["weight"] / path_graph.nodes[node]["weight"]
                    )
                
                if (-path_graph.nodes[pred_node]["dist"], pred_node) not in node_heap.queue:
                    node_heap.put((-path_graph.nodes[pred_node]["dist"], pred_node))
        

        while not node_heap.empty():
            succ_node = node_heap.get()[1]
            for pred_node in path_graph.predecessors(succ_node):
                edge_weight_sum = (
                    sum(path_graph.edges[edge]["betweenness"] 
                    for edge in path_graph.out_edges(succ_node)) + 1
                    )

                path_graph.edges[pred_node, succ_node]["betweenness"] = (
                    edge_weight_sum * (path_graph.nodes[pred_node]["weight"] / 
                    path_graph.nodes[succ_node]["weight"])
                    )
                node_heap.put((-path_graph.nodes[pred_node]["dist"], pred_node))

        for edge in path_graph.edges:
            if edge in edges.keys():
                edges[edge] += path_graph.edges[edge]["betweenness"]/2
            else:
                edges[(edge[1], edge[0])] += path_graph.edges[edge]["betweenness"]/2

        print("between", timeit.default_timer() - start_time)
        
    return edges