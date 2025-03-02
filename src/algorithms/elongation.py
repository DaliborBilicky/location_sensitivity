import numpy as np

import graph as gh


def get_frac_list(graph: gh.Graph) -> list[float]:
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
    x_min = float(np.inf)
    for fraction in frac_list:
        x = denominator / fraction
        x_min = min(x_min, x)
    return x_min


def get_elong_edges(
    edges: list[gh.Edge], frac_list: list[float], k_devided: float
) -> list[gh.Edge]:
    i = 0
    elong_edges = []

    for e in edges:
        edge = gh.Edge(e.v1, e.v2, e.cost / (1 - frac_list[i] * k_devided))
        elong_edges.append(edge)
        i += 1
    return elong_edges
