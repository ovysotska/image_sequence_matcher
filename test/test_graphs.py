#!/usr/bin/python

import unittest
import sys
import os
import src.topological_sorting as TS
from collections import deque

sys.path.append(os.path.dirname('src/'))
sys.path.append(os.path.dirname('../src/'))


class TestMyAwesomeClass(unittest.TestCase):
    def testTopologicalSort(self):
        # declaring the directed graph with weights
        # g[i] = [(j,k)] - a graph has an edge from node i to node j with 
        # weight k
        g = dict()
        g[0] = [(1, 1), (2, 2), (3, 3)]
        g[1] = [(4, 2), (5, 1)]
        g[2] = [(4, 2), (5, 1), (6, 2)]
        g[3] = [(5, 1), (6, 2)]
        g[4] = [(7, 0)]
        g[5] = [(7, 0)]
        g[6] = [(7, 0)]
        g[7] = []

        S = TS.topologicalSorting(g, 0)
        S_true = deque([0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(S, S_true)

    def testShortestPath(self):
        g = dict()
        g[0] = [(1, 1), (2, 2), (3, 3)]
        g[1] = [(4, 2), (5, 1)]
        g[2] = [(4, 2), (5, 1), (6, 2)]
        g[3] = [(5, 1), (6, 2)]
        g[4] = [(7, 0)]
        g[5] = [(7, 0)]
        g[6] = [(7, 0)]
        g[7] = []
        S = deque([0, 1, 2, 3, 4, 5, 6, 7])
        path = TS.shortestPath(g, S)
        path_true = [7, 5, 1, 0]

        self.assertEqual(path, path_true)

    def test_full(self):

        g2 = dict()
        g2[0] = [(1, 0.3), (2, 0.7), (5, 0.5)]
        g2[1] = [(3, 0.7), (4, 0.4)]
        g2[2] = [(4, 0.7)]
        g2[3] = [(6, 0)]
        g2[4] = [(6, 0)]
        g2[5] = [(4, 0.01)]
        g2[6] = []

        S = [0, 1, 2, 3, 4, 6, 5]
        path = TS.shortestPath(g2, S)
        # this should be a wrong solution
        S_top = TS.topologicalSorting(g2, 0)
        S_top_true = deque([0, 1, 2, 5, 3, 4, 6])

        self.assertEqual(S_top, S_top_true)

        path_after = TS.shortestPath(g2, S_top)
        path_after_true = [6, 4, 5, 0]
        self.assertEqual(path_after, path_after_true)
