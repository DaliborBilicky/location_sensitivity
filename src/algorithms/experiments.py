import math
import statistics as stt

import algorithms as alg


def calculate_first_k(graph, frac_list, denominator, k_upper_limit):
    """
    Calculates the first significant value of k where the p-median solution changes.

    This function uses a binary search approach to find the smallest value of k
    that results in a different solution to the p-median problem when edge lengths
    are elongated by a factor based on k.

    Args:
        graph (gh.Graph): The graph object containing vertices, edges, and the distance matrix.
        frac_list (list[float]): A list of fraction values used to scale edge costs.
        denominator (float): The scaling denominator applied to k for edge elongation.
        k_upper_limit (float): The maximum value to test for k.
    """
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
    """
    Iteratively calculates values of k and evaluates the p-median problem
    for each step until k approaches the upper limit.

    This function progressively increases k, adjusting edge lengths and solving
    the p-median problem. It also computes and displays statistical data about
    edge cost elongations, such as min, max, mean, and mode of the cost ratios.

    Args:
        graph (gh.Graph): The graph object containing vertices, edges, and the distance matrix.
        frac_list (list[float]): A list of fraction values used to scale edge costs.
        denominator (float): The scaling denominator applied to k for edge elongation.
        k_upper_limit (float): The maximum value to increment k towards.
    """
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
            cost_differ = [
                elong_edges[i].cost / edges_previous[i].cost
                for i in range(len(elong_edges))
            ]

            min_cost = min(cost_differ)
            max_cost = max(cost_differ)
            mean_cost = stt.mean(cost_differ)
            mode_cost = stt.mode(cost_differ)

            print(
                f"\nk: {k:.4f} k-lim: {k_upper_limit:.4f} "
                f"min: {min_cost:.4f} max: {max_cost:.4f} "
                f"mean: {mean_cost:.4f} mode: {mode_cost:.4f}"
                f"\n{y}\n"
            )

        step /= 2
        k += step
        edges_previous = elong_edges
