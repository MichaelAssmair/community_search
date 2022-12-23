import unittest

import networkx as nx
from community.label_propagation import async_lpa

class Test_async_lpa(unittest.TestCase):

    def test_empty_graph(self):
        G = nx.empty_graph()
        self.assertEqual(async_lpa(G), [])

    def test_singel_node(self):
        G = nx.Graph()
        G.add_node(1)
        self.assertEqual(async_lpa(G), [{1}])

    def test_without_edges(self):
        G = nx.Graph()
        G.add_nodes_from([1, 2, 3])
        self.assertEqual(async_lpa(G), [{1},{2},{3}])

    def test_undef_strategy(self):
        G = nx.empty_graph()
        with self.assertRaises(ValueError):
            async_lpa(G, strategy="")

    def test_weighted_graph(self):
        G = nx.les_miserables_graph()
        self.assertIsInstance(async_lpa(G, weight="weight"), list)

    def test_directed_graph(self):
        G = nx.DiGraph()
        G.add_edges_from([("a", "b"),("b", "c"),("c", "a")])
        self.assertEqual(async_lpa(G), [{"a", "b", "c"}])

    def test_lpa_prec_strategies(self):
        G = nx.karate_club_graph()
        self.assertGreater(len(async_lpa(G, strategy="lpa_prec")), 0)

    def test_lpa_max_strategies(self):
        G = nx.karate_club_graph()
        self.assertGreater(len(async_lpa(G, strategy="lpa_max")), 0)

    def test_lpa_prec_max_strategies(self):
        G = nx.karate_club_graph()
        self.assertGreater(len(async_lpa(G, strategy="lpa_prec_max")), 0)