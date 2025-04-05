import numpy as np

import graph as gh


def get_frac_list(graph: gh.Graph) -> list[float]:
    """
    Calculates the fraction list for all edges in the graph.

    The fraction list is a measure of the influence of each edge based on
    vertex weights and distances, used for edge elongation calculations.

    Args:
        graph (gh.Graph): The graph object containing vertices, edges, and the
        distance matrix.

    Returns:
        list[float]: A list of fraction values, one for each edge in the graph.
    """
    frac_list = []
    for e in graph.edges:
        frac_sum = 0.0

        for v in graph.vertices:
            d_v1 = graph.dist_matrix[e.v1][v.label]
            d_v2 = graph.dist_matrix[e.v2][v.label]
            d_e_v = min(d_v1, d_v2) + (e.cost / 2)
            frac = v.weight / d_e_v
            frac_sum += frac

        frac_list.append(frac_sum)

    return frac_list


def get_k_upper_limit(frac_list: list[float], denominator: float) -> float:
    """
    Computes the upper limit for the k parameter used in edge elongation.

    The upper limit is derived by minimizing the denominator-to-fraction ratio
    across all fraction values.

    Args:
        frac_list (list[float]): A list of fraction values for each edge.
        denominator (float): The scaling factor used in edge elongation.

    Returns:
        float: The minimum permissible value of k for safe edge elongation.
    """
    x_min = float(np.inf)
    for fraction in frac_list:
        x = denominator / fraction
        x_min = min(x_min, x)
    return x_min


def get_elong_edges(
    edges: list[gh.Edge], frac_list: list[float], k_devided: float
) -> list[gh.Edge]:
    """
    Generates a list of edges with elongated costs based on a scaling factor.

    The elongation of edge costs is governed by the formula.

    Args:
        edges (list[gh.Edge]): A list of original edges in the graph.
        frac_list (list[float]): Fraction values corresponding to each edge.
        k_devided (float): The scaling factor for edge elongation.

    Returns:
        list[gh.Edge]: A list of new Edge objects with elongated costs.
    """
    elong_edges = []

    for i, e in enumerate(edges):
        new_cost = e.cost / (1 - frac_list[i] * k_devided)
        edge = gh.Edge(e.v1, e.v2, new_cost)
        elong_edges.append(edge)

    return elong_edges
