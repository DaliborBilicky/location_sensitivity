import math
import statistics as stt

import algorithms as alg


def calculate_first_k(graph, frac_list, denominator, k_upper_limit):
    k = 0
    step = k_upper_limit / 2
    y_previous = alg.pulp_solve_p_median(
        graph.dist_matrix, graph.vertices, graph.p
    )

    while step >= 0.1:
        k += step

        elong_edges = alg.get_elong_edges(
            graph.edges, frac_list, (k / denominator)
        )

        elong_dist_matrix = alg.create_dist_matrix(
            elong_edges, graph.num_of_verts
        )

        y = alg.pulp_solve_p_median(elong_dist_matrix, graph.vertices, graph.p)
        print(f"k = {k:.5f} => {y}")

        if y != y_previous:
            k -= step
            step /= 2


def calculate_all_ks(graph, frac_list, denominator, k_upper_limit):
    k = 0
    step = k_upper_limit
    y_previous = []
    edges_previous = graph.edges

    while not math.isclose(k, k_upper_limit, rel_tol=0.001):
        elong_edges = alg.get_elong_edges(
            graph.edges, frac_list, (k / denominator)
        )

        elong_dist_matrix = alg.create_dist_matrix(
            elong_edges, graph.num_of_verts
        )

        y = alg.pulp_solve_p_median(elong_dist_matrix, graph.vertices, graph.p)

        if y_previous != y:
            y_previous = y
            cost_differ = []

            for i in range(len(elong_edges)):
                cost_differ.append(elong_edges[i].cost / edges_previous[i].cost)

            min_cost = min(cost_differ)
            max_cost = max(cost_differ)
            mean_cost = stt.mean(cost_differ)
            mode_cost = stt.mode(cost_differ)

            print(
                f"\nk: {k:.4f} k-lim: {k_upper_limit:.4f} "
                + f"min: {min_cost:.4f} max: {max_cost:.4f} "
                + f"mean: {mean_cost:.4f} mode: {mode_cost:.4f}"
                + f"\n{y}\n"
            )

        step /= 2
        k += step
        edges_previous = elong_edges
