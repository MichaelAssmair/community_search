"""label propagation."""

# Author: Michael Assmair

import random
import networkx as nx
from networkx.utils import groups
from community_search import main

__all__ = ["async_lpa", "semi_sync_lpa"]


def _lpa(_, max_neighbor_labels):
    """Alle Labes haben die selbe Wahrscheinlichkeit."""
    return random.choice(max_neighbor_labels)


def _lpa_prec(old_label, max_neighbor_labels):
    """Das Label aus der voherigen Iteration wird wenn in der Menge
    der maximalen Labels enthalten bevorzugt, sonst wird ein Label zufällig
    gewählt.
    """
    if old_label in max_neighbor_labels:
        return old_label
    else:
        return random.choice(max_neighbor_labels)

def _lpa_max(_, max_neighbor_labels):
    """Das Label mit der höchsten Nummer mir gewählt."""
    return max(max_neighbor_labels)


def _lpa_prec_max(old_label, max_neighbor_labels):
    """Das Label aus der vorherigen Iteration wird wenn in der Menge
    der maximalen Labels enthalten bevorzugt, sonst wir das Label mit der
    höchsten Nummer gewählt.
    """
    if old_label in max_neighbor_labels:
        return old_label
    else:
        return max(max_neighbor_labels)


_STRATEGIES = {
    "lpa": _lpa,
    "lpa_prec": _lpa_prec,
    "lpa_max": _lpa_max,
    "lpa_prec_max": _lpa_prec_max
}


def async_lpa(G: nx.Graph, weight=None, seed=None, strategy="lpa", to_undirectet=False):
    """Sucht nach Communitys im Graphen G.

    Implementierung eines asynchronen Label propagation Algorithmus,
    wie in [1] beschrieben.

    Parameters
    ----------
    G : nx.Graph or nx.DiGraph
        Graph im Networkx-Format. Der Algorithmus funktioniert sowol
        mit gerichteten als auch mit ungerichteten Graphen. Bei gerichteten
        Graphen werden, falls 'to_undirectet=False' nur die eingehenden
        Kanten für die Berechnung verwendet.

    weight : string or None
        Kantengewichte, die bei der berechnung der Communitys
        verwendet werden. Sollte kein Kantengewicht angegeben werden,
        so erhält jede Kante das Gewicht 1.

    seed : int or None
        Seed, der für den Pseudozufallszahlengenerator verwendet wird.
        Sollte kein Seed übergene werden, wird die Standardeinstellung des
        Paketes 'random' verwendet.

    strategy : string
        Strategie mit der falls mehrere Labels für einen Knoten maximal sind
        das Label für den nächsten Iterationsschritt ausgewählt wird. Falls kein
        Parameter für die Strategie übergeben wurde, wird 'lpa' verwendet. Diese
        Strategien werden in [2] beschrieben.

        * "lpa"
        * "lpa_prec"
        * "lpa_max"
        * "lpa_prec_max"

    to_undirectet : bool
        Wenn für den Parameter True übergeben wird und G ein gerichteter Graph ist,
        wird für die berechnung der Labels der Graph in einen ungerichteten Graph
        umgewandelt.

    Returns
    -------
    communities : list[set]
        Liste mit Sets von Knoten, die zur selben Community
        Gehören. Wenn die übergeben Variable G kein Netwerkx Graph ist,
        wird None zurückgegeben.

    Raises
    ------
    ValueError
        Falls eine ungültige Strategie übergeben wurde.

    References
    ----------
    .. [1] Raghavan, Usha Nandini, Réka Albert, and Soundar Kumara. "Near
           linear time algorithm to detect community structures in large-scale
           networks." Physical Review E 76.3 (2007): 036106.
    .. [2] Cordasco, G., & Gargano, L. (2010, December). Community detection
           via semi-synchronous label propagation algorithms. In Business
           Applications of Social Network Analysis (BASNA), 2010 IEEE International
           Workshop on (pp. 1-8). IEEE.
    """
    if strategy not in _STRATEGIES:
        raise ValueError

    if to_undirectet and G.is_directed():
        g = G.to_undirected(as_view=True)
    else:
        g = G

    random.seed(seed)
    
    nodes = list(g)
    labels = {node: label for label, node in enumerate(nodes)}
    
    while not _stop_criterion(g, labels, weight):
        random.shuffle(nodes)

        for node in nodes:
            max_neighbor_labels = _get_max_labels(g, labels, weight, node)    
            labels[node] = _STRATEGIES[strategy](labels[node], max_neighbor_labels)
                 
    communities = list(groups(labels).values())

    return communities


def semi_sync_lpa(G, weight=None, strategy="lpa", to_undirectet=False):
    """Sucht nach Communitys im Graphen G.

    Implementierung eines semi-synchronen Label propagation Algorithmus,
    wie in [1] beschrieben.

    Parameters
    ----------
    G : nx.Graph or nx.DiGraph
        Graph im Networkx-Format. Der Algorithmus funktioniert sowol
        mit gerichteten als auch mit ungerichteten Graphen. Bei gerichteten
        Graphen werden, falls 'to_undirectet=False' nur die eingehenden
        Kanten für die Berechnung verwendet.

    weight : string or None
        Kantengewichte, die bei der berechnung der Communitys
        verwendet werden. Sollte kein Kantengewicht angegeben werden,
        so erhält jede Kante das Gewicht 1.

    strategy : string
        Strategie mit der falls mehrere Labels für einen Knoten maximal sind
        das Label für den nächsten Iterationsschritt ausgewählt wird. Falls kein
        Parameter für die Strategie übergeben wurde, wird 'lpa' verwendet. Diese
        Strategien werden in [1] beschrieben.

        * "lpa"
        * "lpa_prec"
        * "lpa_max"
        * "lpa_prec_max"

    to_undirectet : bool
        Wenn für den Parameter True übergeben wird und G ein gerichteter Graph ist,
        wird für die berechnung der Labels der Graph in einen ungerichteten Graph
        umgewandelt.

    Returns
    -------
    communities : list[set]
        Liste mit Sets von Knoten, die zur selben Community
        Gehören. Wenn die übergeben Variable G kein Netwerkx Graph ist,
        wird None zurückgegeben.

    Raises
    ------
    ValueError
        Falls eine ungültige Strategie übergeben wurde.

    References
    ----------
    .. [1] Cordasco, G., & Gargano, L. (2010, December). Community detection
           via semi-synchronous label propagation algorithms. In Business
           Applications of Social Network Analysis (BASNA), 2010 IEEE International
           Workshop on (pp. 1-8). IEEE.
    """
    if strategy not in _STRATEGIES:
        raise ValueError

    if to_undirectet and G.is_directed():
        g = G.to_undirected(as_view=True)
    else:
        g = G

    labels = {node: label for label, node in enumerate(g)}
    coloring = groups(nx.algorithms.coloring.greedy_color(g))

    #To-Do: Paralelle verarbeitung von Knoten, die mit der
    #selben Farbe markiert wurden. multiprocessing oder concurrent.futures
    #haben für die Erzeugung eines neuen Prozessen wahrscheinlich einen
    #zu großen Overhead.
    while not _stop_criterion(g, labels, weight):
        for color in coloring.values():
            for node in color:     
                max_neighbor_labels = _get_max_labels(g, labels, weight, node)       
                labels[node] = _STRATEGIES[strategy](labels[node], max_neighbor_labels)

    communities = list(groups(labels).values())

    return communities


def _stop_criterion(G, labels, weight):
    """Wenn mindestens ein Knoten nicht ein maximales Label
    hat, wird False zurückgegeben sonst True.
    """
    for node in G:
        if labels[node] not in _get_max_labels(G, labels, weight, node):
            return False

    return True


def _get_max_labels(G, labels, weight, node):
    """Findet maximale Labels
    
    Ein Label ist dann maximal, wenn die Summe der 
    Labels seiner Nachbarkonten maximal ist.
    Wenn der übergebene Graph gerichtet ist, weden für
    die Berechnung der maximalen Labels nur die Knoten
    verwendet, die ein Vorgänger vom aktuell betrachteten
    Knoten sind.
    """
    if G.is_directed():
        neighbors = G.pred[node]
    else:
        neighbors = G.adj[node]

    if len(neighbors) == 0:
        return [labels[node]]

    neighbor_labels = {labels[neighbor]: 0.0 for neighbor in neighbors}

    for neighbor in neighbors:
        if weight != None:
            neighbor_labels[labels[neighbor]] += 1 * G.edges[node, neighbor][weight]
        else:
            neighbor_labels[labels[neighbor]] += 1
            
    max_count = max(neighbor_labels.values())
    max_neighbor_labels = [k for k,v in neighbor_labels.items() if v == max_count]

    return max_neighbor_labels