#!/usr/bin/python

import unittest
import sys
import os
import numpy as np
from src.graph import Graph
import src.path_tools as PT

sys.path.append(os.path.dirname('src/'))
sys.path.append(os.path.dirname('../src/'))


class TestMatrix(unittest.TestCase):
    def test_full(self):
        test_matrix = np.matrix('0.1, 0.2, 4.0; 3.0, 2.0, 0.2')
        fanout = 2
        non_matching_cost = 0.24
        graph = Graph()
        graph.initFromMatrix(test_matrix, fanout)
        graph.computePath()
        img_path = graph.getImageCorrespodences()
        path_real, path_hidden = PT.filterPath(
            test_matrix, img_path, non_matching_cost)
        path_real_true = np.array([[1, 2], [0, 1]])
        self.assertEqual(np.sum(path_real - path_real_true), 0)
        self.assertEqual(len(path_hidden), 0)
