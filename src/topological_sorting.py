"""Summary
"""
import numpy as np
from collections import deque
import math


def constructIncomingGraph(og):
    """Construct the graph.

    No weights preserved. Return grapg ig, where ig[i] = j, there is an edge
    from node j to node i.

    Args:
        og (dict): Graph with ougoing edges.

    Returns:
        dict: Graph with incoming edges.
    """
    ig = dict()
    for node_from, nodes_to in og.items():
        for node_to in nodes_to:
            if node_to[0] in ig:
                ig[node_to[0]].append(node_from)
            else:
                ig[node_to[0]] = [node_from]
    return ig


def topologicalSorting(graph, start_node):
    """Summary

    Args:
        graph (TYPE): Description
        start_node (TYPE): Description

    Returns:
        TYPE: Description
    """
    ig = constructIncomingGraph(graph)
    # queue of sorted nodes (result)
    sorted_nodes = deque([])
    # queue of nodes with no incoming edges
    in_set = deque([start_node])
    while(in_set):  # I is not empty
        n = in_set.popleft()
        # if out of I than no incoming
        sorted_nodes.append(n)
        if n not in graph:
            print("Your graph is missing node", n)
        children = graph[n]  # children of type [(j,k)]
        for child in children:
            # remove an incoming edge (release the node from a parent :))
            child_id = child[0]
            ig[child_id].remove(n)
            if not ig[child_id]:
                # no incoming edges -> add to I
                in_set.append(child_id)
    print("sorting done")
    return sorted_nodes


def shortestPath(graph, S):
    """ Computes the shortest path
    Only computes the path in the topologically sorted graph
    The result is the list of graph node ids  that are in the shortest path
    Args:
        graph (dict): constructed graph
        S (deque): topological sorting of the node ids

    Returns:
        list(int): shortest path
    """
    # For algorithm to work the nodes ids should be positive int in sequence
    # Shortest path to the last element in the queue
    # Incoming: graph - graph with outgoing edges
    # S - queue of sorted nodes
    N = len(S)  # total number of nodes in S
    if N > len(graph):
        print("ERROR: More sorted nodes than in the graph")
    if N < len(graph):
        print("ERROR: Less sorted nodes than in the graph")

    # initialization of the dist and p based on graph
    dist = dict()
    p = dict()
    for node_id, children in graph.items():
        dist[node_id] = math.inf
        p[node_id] = None

    dist[S[0]] = 0
    for el in S:
        u = el
        children = graph[u]
        for child in children:
            v = child[0]  # node to
            w = child[1]  # weight between u and v
#             print("Edge", u,"->", v, ":", w)
            if (dist[v] > dist[u] + w):
                dist[v] = dist[u] + w
                p[v] = u

    # retrieving path
    path = []
    par_id = S[-1]
    # print("Retrieving path from last node: ", S[-1])
    path.append(par_id)
    while par_id:
        par_id = p[par_id]
        path.append(par_id)

    return path
