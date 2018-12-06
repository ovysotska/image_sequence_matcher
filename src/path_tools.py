""" Functions to  process and visualize the image associations
"""
import numpy as np
import matplotlib.pyplot as plt


def plotPathOverMatrix(path_coords_real, path_coords_hidden, matrix):
    """ Plots path over cost matrix

    Args:
        path_coords_real (np.array(N,2)): Real image associations
        path_coords_hidden (np.array(N,2)): Hidden image associations
        matrix (np.array(N,M)): Cost matrix to visualize on

    """
    plt.imshow(matrix, cmap="gray")
    if path_coords_real.size == 0:
        print("WARNING: No real nodes to plot")
    else:
        plt.plot(path_coords_real[:, 1], path_coords_real[:, 0], 'r.')
    if path_coords_hidden.size == 0:
        print("No hidden nodes to plot")
    else:
        plt.plot(path_coords_hidden[:, 1], path_coords_hidden[:, 0], 'b.')


def filterPath(matrix, path_coords, non_matching_cost):
    """ Separates the path into real and hidden matches

    Args:
        matrix (np.array(N,M)): cost matrix
        path_coords (np.array(N,2)): shortest path in matrix coordinates
        non_matching_cost (int): Cost threshold value

    Returns:
        np.array(N,2), np.array(N,2):  List of real matches, list of
        hidden matches 
    """
    path_coords_real = []
    path_coords_hidden = []
    m_rows, m_cols = matrix.shape
    for coords in path_coords:
        row = coords[0]
        col = coords[1]
        if row < 0 or row >= m_rows or col < 0 or col >= m_cols:
            # skipping the target node
            continue
        v = matrix[row, col]
        if v < non_matching_cost:
            path_coords_real.append(coords)
        else:
            path_coords_hidden.append(coords)
    path_coords_real = np.array(path_coords_real)
    path_coords_hidden = np.array(path_coords_hidden)
    return path_coords_real, path_coords_hidden
