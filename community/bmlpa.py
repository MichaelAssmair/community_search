"""balenced multi-label propagation algorithmus"""

import networkx as nx

__all__ = ["bmlpa"]


def _get_rough_cores(G: nx.Graph):
    """"""

    cores = []
    #Liste von Knoten, absteigen nach Grad sortiert
    nodes = {node: "free" for (node, _) in (sorted(G.degree, key=lambda x: x[1], reverse=True))}
    
    for node_i, value_i in nodes.items():
        if G.degree[node_i] >= 3 and value_i:
            new_core = set([node_i])

            node_j = max(
                (node for node in G.adj[node_i] if nodes[node]), 
                key=lambda x:G.degree[x], default = None
                )

            if node_j:
                new_core.add(node_j)
                #Liste von gemeinsamen Nachbarn aufsteigen nach Grad sortiert
                comm_neighbors = sorted(set(G.adj[node_i]) & set(G.adj[node_j]), key=lambda x: G.degree[x])


                while comm_neighbors:
                    neighbor = comm_neighbors.pop(0)
                    new_core.add(neighbor)

                    for node in comm_neighbors.copy():
                        if node not in G.adj[neighbor]:
                            comm_neighbors.remove(node)

            if len(new_core) >= 3:
                for node in new_core:
                    nodes[node] = False

                cores.append(new_core)

    return cores


def _normalize(label: dict):
    """Normalisiert den Lable-Vektor"""
    tmp_sum = sum(label.values())

    for community, value in label.items():
        label[community] = value / tmp_sum


def _init(G: nx.Graph):
    """Inizialisiert die Labels mit den Rough Cores"""

    labeling = {node: {label: 1} for label, node in enumerate(G)}

    for label, core in enumerate(_get_rough_cores(G)):
        for node in core:
            labeling[node][label + len(labeling)] = 1

    for idx, (node, label) in enumerate(labeling.items()):
        _normalize(labeling[node])

    return labeling


def _propagate(G, node, vec_old, vec_new, p_parm):
    vec_new[node] = {}

    for neighbor in G.adj[node]:
        for label, value in vec_old[neighbor].items():
            if label not in vec_new[node].keys():
                vec_new[node][label] = value
            else:
                vec_new[node][label] += value

    if not vec_new[node]:
        vec_new[node] = vec_old[node]

    b_max = max(vec_new[node].values())
    
    for label, value in list(vec_new[node].items()):
        if value / b_max < p_parm:
            vec_new[node].pop(label)

    _normalize(vec_new[node])
    

def _vec_id(label_vec):
    ids = set()

    for node in label_vec:
        ids.update(label_vec[node].keys())

    return ids


def count(vec):
    counts = {}
    
    for node, labels in vec.items():
        for label, value in labels.items():
            if label in counts.keys():
                counts[label] += 1
            else:
                counts[label] = 1

    return counts


def mc(cs1, cs2):
    cs = {}

    for (c, n1), (c, n2) in zip(sorted(cs1.items()), sorted(cs2.items())):
        cs[c] = min(n1, n2)

    return cs

def _put_in_groups(labling):
    groups = {}

    for node, labels in labling.items():
        for label, value in labels.items():
            if label in groups.keys():
                groups[label].append((node, value))

            else:
                groups[label] = [(node, value)]

    return groups
    

def bmlpa(G, p_parm=0.75):
    labeling_old = _init(G)
    labeling_new = dict.fromkeys(G)
    oldmin = dict()

    while True:
        for node in G:
            _propagate(G, node, labeling_old, labeling_new, p_parm)

        if (_vec_id(labeling_old)) == (_vec_id(labeling_new)):
            min = mc(count(labeling_old), count(labeling_new))
        else:
            min = count(labeling_new)


        if set(tuple(min.items())) != set(tuple(oldmin.items())):
            labeling_old = labeling_new
            labeling_new = dict.fromkeys(G)
            oldmin = min
        else:
            return labeling_new