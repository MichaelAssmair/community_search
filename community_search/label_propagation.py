"""Label propagation."""

# Author: Michael Assmair

import random
import networkx as nx
from networkx.utils import groups


def lpa_communities(G, weight=None, seed=None):
    """Sucht nach Communitys im Graphen G.

    Implementierung eines asynchronen Label propagation Algorithmus,
    wie in https://arxiv.org/abs/0709.2938 beschrieben.

    Parameters
    ----------
    G : Graph im Networkx-Format. Der Algorithmus funktioniert sowol
        mit gerichteten als auch mit ungerichteten Graphen.

    weight : Kantengewichte, die bei der berechnung der Communitys
        verwendet werden. Sollte kein Kantengewicht angegeben werden,
        so erhält jede Kante das Gewicht w=1.

    seed : Seed, der für den Pseudozufallszahlengenerator verwendet wird.
        Sollte kein Seed übergene werden, wird die Standardeinstellung des
        Paketes 'random' verwendet.

    Returns
    -------
    communities : Liste mit Sets von Knoten, die zur selben Community
        Gehören. Wenn die übergeben Variable G kein Netwerkx Graph ist,
        wird None zurückgegeben.
    """
    if not (type(G) == nx.DiGraph or type(G) == nx.Graph):
        return None

    random.seed(seed)
    
    #Die Startlabel werden vergeben.
    labels = {node: label for (label, node) in enumerate(G)}
    nodes = list(labels)

    finished = False
    
    #Die Schleife läuft, bis alle Knoten das selbe Label haben
    #wie die meisten seiner Nachbarknoten.
    while not finished:
        finished = True
        random.shuffle(nodes)

        #Knoten werden asynchron durchlaufen.
        for node in nodes:
            neighbor_labels = {label: 0 for label in labels.values()}

            for neighbor in G.adj[node]:
                if nx.is_weighted(G):
                    neighbor_labels[labels[neighbor]] += 1 * G.edges[node, neighbor]["weight"]
                else:
                    neighbor_labels[labels[neighbor]] += 1
            
            max_count = max(neighbor_labels.values())
            max_neighbor_labels = [k for k,v in neighbor_labels.items() if v == max_count]
            
            #Wenn der aktuell bearbeitete Knoten nicht ein Label hat
            #wie die meisten seiner Nachbarschaft, wird dich Schleife
            #moch mindestens einmal durchlaufen.
            if labels[node] not in max_neighbor_labels:
                finished = False
            
            labels[node] = random.choice(max_neighbor_labels)

    #Die Methode 'groups' bildet alle Knoten mit dem selben
    #Label auf ein Set ab.
    communities = groups(labels).values()

    return communities