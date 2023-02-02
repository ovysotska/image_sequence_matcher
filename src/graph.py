"""Graph structure and functions to work with it
"""
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import src.topological_sorting as ts


class Graph:
    """stores the graph structure + all the processing functions
    Attributes:
        graph (TYPE): Description
        matrix_cols (int): Description
        nodes_sort (TYPE): Description
        path (list): Description
    """

    def __init__(self):
        """Constructor"""
        self.graph = dict()
        self.matrix_cols = -1
        self.path = []
        self.nodes_sort = deque([])

    def pair2index(self, i, j):
        """Maps a pair of matrix coordinates to the index of a node in the graph
        Args:
            i (int): row index
            j (int): col index

        Returns:
            int: node index
        """
        index = i * self.matrix_cols + j
        return index

    def index2pair(self, index):
        """Maps an index of a node in the graph back to matrix row/col index

        Args:
            index (int): node index

        Returns:
            tuple: (row, col) matrix index
        """
        i = index // self.matrix_cols
        j = index - i * self.matrix_cols
        return (i, j)

    def initFromMatrix(self, cost_matrix, fanout):
        """initializes graph from a matrix
        Fanout determines how many outgoing edges in each direction the node
        will have.
        For fanout = 0, 1 child, directly under the parent. Only models the
        situations when the camera is staying in the query dataset. Don't use
        that. It is not useful
        For fanout = 1, 3 children
        For fanout = 2, 5 children

        Args:
            cost_matrix (np.ndarray): cost matrix
            fanout (int): number of outgoing edges
        """
        node_map = dict()
        self.graph = dict()
        self.matrix_cols = cost_matrix.shape[1]
        source_node_id = -1
        node_map[source_node_id] = ()
        # adding the source node to the graph
        rows, cols = cost_matrix.shape
        # print("Rows, cols:", rows, cols)

        # adding source children
        row_id = 0  # adding only the first row
        self.graph[source_node_id] = []
        for column_id in range(cols):
            index = self.pair2index(row_id, column_id)
            self.graph[source_node_id].append((index, cost_matrix[row_id, column_id]))

        # adding all the nodes in the matrix
        # iterating over parents
        for row_id in range(rows - 1):
            for col_id in range(cols):
                parent_id = self.pair2index(row_id, col_id)
                child_row_id = row_id + 1
                # checking the matrix borders
                f_begin = max(0, col_id - fanout)
                f_end = min(cols, col_id + fanout)
                # range(5) = [0,1,2,3,4]
                for k in range(f_begin, f_end):
                    child_id = self.pair2index(child_row_id, k)
                    if parent_id in self.graph:
                        self.graph[parent_id].append(
                            (child_id, cost_matrix[child_row_id, k])
                        )
                    else:
                        self.graph[parent_id] = [
                            (child_id, cost_matrix[child_row_id, k])
                        ]

        # connecting last row to the target node
        # assuming target node coords (last_row+1, 0)
        target_node_id = self.pair2index(rows, 0)
        parent_row = rows - 1
        for parent_col in range(cols):
            parent_id = self.pair2index(parent_row, parent_col)
            if parent_id in self.graph:
                self.graph[parent_id].append((target_node_id, 0))
            else:
                self.graph[parent_id] = [(target_node_id, 0)]

        # add last node to the graph
        self.graph[target_node_id] = []

        # initialize nodes sort
        rows, cols = cost_matrix.shape
        arr = np.arange(-1, rows * cols + 1)
        self.nodes_sort = deque(arr)
        print("[INFO] The graph was initialized")

    def computePath(self):
        """Estimates the shortest path in topologically sorted graph
        WARNING: the topological sort of nodes should be computed beforehand

        """
        if len(self.nodes_sort) == 0:
            print("[ERROR] No topological sort. Maybe Graph is not initialized yet.")
            return
        self.path = ts.shortestPath(self.graph, self.nodes_sort)
        print("[INFO] Path computed")

    def visualize(self, plot_edges=True):
        """plots the graph.
        Only use for debugging purposes, for matrices not bigger than 20x20.

        Args:
            plot_edges (bool, optional): plots the edges between the nodes.
        """
        # plot_edges = True
        if self.matrix_cols > 20:
            print(
                "WARNING: Graph is too big to visualize. Plotting edges will be skipped\n"
            )
            plot_edges = False

        nodes = dict()

        # make sure nodes are unique
        for parent_id, children in self.graph.items():
            for child in children:
                nodes[child[0]] = child[1]

        # transform info for plotting
        x = []
        y = []
        c = []
        for node_id, color in nodes.items():
            row, col = self.index2pair(node_id)
            y.append(row)
            x.append(col)
            c.append(color)
            s = len(nodes) * [200]

        # all constants here are just to make things more visually appealing
        if plot_edges:
            # plotting arrows
            arrow_w = 0.01
            arrow_head_w = arrow_w * 5
            arrow_head_l = arrow_w * 5
            for parent_id, children in self.graph.items():
                parent_coords = self.index2pair(parent_id)
                for child in children:
                    child_id = child[0]
                    child_coords = self.index2pair(child_id)
                    arr_x = parent_coords[1]
                    arr_y = parent_coords[0] + 0.1
                    # columns correspond to x
                    dx = 0.7 * (child_coords[1] - parent_coords[1])
                    # rows correspond to y
                    dy = 0.7 * (child_coords[0] - parent_coords[0])
                    plt.arrow(
                        arr_x,
                        arr_y,
                        dx,
                        dy,
                        width=0.01,
                        head_width=arrow_head_w,
                        head_length=arrow_head_l,
                        color="k",
                    )

        plt.scatter(x, y, c=c, cmap="gray", s=s)
        # reversing y for the thing to look like matrix
        ax = plt.gca()
        ax.set_ylim(ax.get_ylim()[::-1])

    def plotPathOverGraph(self, plot_edges=True):
        """Visualizes the path over the graph.
        Use for small graphs ONLY.

        Args:
            plot_edges (bool, optional): Description

        Returns:
            TYPE: Description
        """
        if len(self.path) == 0:
            print("[WARNING] The path is not computed yet.")
        self.visualizeGraph(plot_edges)
        x = []
        y = []
        for index in self.path:
            if not index:
                continue
            if index < 0:
                continue
            row, col = self.index2pair(index)
            y.append(row)
            x.append(col)
            # 200 - size of scatter
            s = len(self.path) * [200]

        plt.scatter(x, y, c="r", s=s)

    def getImageCorrespodences(self):
        """Returns image correspondences
            returns the pairs of matrix coordinates that correspond to
            found image associtions. (i,j) i-th query image corresponds to j-th
            reference image from the found shortest path
        Returns:
            np.array: Array of pairs
        """
        path_coords = []
        for index in self.path:
            if not index:
                continue
            if index < 0:
                continue
            row, col = self.index2pair(index)
            path_coords.append([row, col])
        path_coords = np.array(path_coords)
        print("[INFO] Image correspondences retrieved")
        return path_coords
