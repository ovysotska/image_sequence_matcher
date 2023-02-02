import numpy as np
from src.graph import Graph
import src.path_tools as pt
import matplotlib.pyplot as plt
import argparse
from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Image sequence matcher ")
    parser.add_argument(
        "--cost_matrix_file",
        type=Path,
        required=True,
        help="Cost matrix file as .txt",
    )
    parser.add_argument(
        "--non_matching_cost",
        type=float,
        required=True,
        help="The value of non-matching cost.",
    )
    parser.add_argument(
        "--fan_out",
        type=int,
        default=3,
        help="Fan out parameter",
    )
    args = parser.parse_args()

    cost_matrix = np.loadtxt(args.cost_matrix_file)
    # inverting the costs, so that the better the match the smaller is the
    # matching cost
    fanout = args.fan_out
    # non_matching_cost = 7.5
    non_matching_cost = args.non_matching_cost

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
        cost_matrix, img_path, non_matching_cost
    )
    print("Done.")

    plt.figure(1)
    pt.plotPathOverMatrix(path_coords_real, path_coords_hidden, cost_matrix)
    plt.show()
