import numpy as np
from src.graph import Graph
import src.path_tools as pt
import matplotlib.pyplot as plt
import sys


if __name__ == "__main__":
    print("=== Image sequence matcher ===")
    if len(sys.argv) < 4:
        print("[ERROR] Not enough input paramters")
        print("Proper usage: python3 img_seq_matcher.py cost_matrix.txt fanout non_matching_cost")
        sys.exit()

    cost_matrix = np.loadtxt(sys.argv[1])
    # inverting the costs, so that the better the match the smaller is the
    # matching cost
    fanout = int(sys.argv[2])
    # non_matching_cost = 7.5
    non_matching_cost = float(sys.argv[3])

    print("Size of the matrix", cost_matrix.shape)
    print("Max value ", np.max(np.max(cost_matrix)))
    print("Min value ", np.min(np.min(cost_matrix)))
    print("non_matching_cost ", non_matching_cost)
    print("fanout ", fanout)

    graph = Graph()
    graph.initFromMatrix(cost_matrix, fanout)
    graph.computePath()
    img_path = graph.getImageCorrespodences()

    # filter result
    path_coords_real, path_coords_hidden = pt.filterPath(
        cost_matrix, img_path, non_matching_cost)
    print("Done.")

    plt.figure(1)
    pt.plotPathOverMatrix(path_coords_real, path_coords_hidden, cost_matrix)
    plt.show()
