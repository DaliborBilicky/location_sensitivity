import math

import algorithms as alg

TOLERANCE = 0.001
PRECISION = 0.01


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
    previous_medians = alg.pulp_solve_p_median(
        graph.dist_matrix, graph.vertices, graph.p
    )
    elong_edges = []
    medians = []

    while step >= PRECISION:
        k += step

        elong_edges = alg.get_elong_edges(
            graph.edges, frac_list, (k / denominator)
        )

        elong_dist_matrix = alg.create_dist_matrix(
            elong_edges, graph.num_of_verts
        )

        medians = alg.pulp_solve_p_median(
            elong_dist_matrix, graph.vertices, graph.p, True
        )

        if medians != previous_medians:
            k -= step
            step /= 2

    cost_ratios = [
        elong_edges[i].cost / graph.edges[i].cost
        for i in range(len(elong_edges))
    ]

    alg.output_solution(
        k, k_upper_limit, cost_ratios, medians, "calculate-first-k"
    )


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
    previous_medians = []
    edges_previous = graph.edges

    while not math.isclose(k, k_upper_limit, rel_tol=TOLERANCE):
        elong_edges = alg.get_elong_edges(
            graph.edges, frac_list, (k / denominator)
        )

        elong_dist_matrix = alg.create_dist_matrix(
            elong_edges, graph.num_of_verts
        )

        medians = alg.pulp_solve_p_median(
            elong_dist_matrix, graph.vertices, graph.p, True
        )

        if previous_medians != medians:
            previous_medians = medians
            cost_ratios = [
                elong_edges[i].cost / edges_previous[i].cost
                for i in range(len(elong_edges))
            ]

            alg.output_solution(
                k, k_upper_limit, cost_ratios, medians, "calculate-all-ks"
            )

        step /= 2
        k += step
        edges_previous = elong_edges
