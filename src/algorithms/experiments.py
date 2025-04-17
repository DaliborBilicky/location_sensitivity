import math

import algorithms as alg
import graph as gh

TOLERANCE = 0.001
PRECISION = 0.1


def calculate_first_k(
    graph: gh.Graph,
    frac_list: list[float],
    denominator: float,
    k_upper_limit: float,
    p: int,
):
    """
    Calculates the first significant value of k where the p-median solution
    changes.

    This function uses a binary search approach to find the smallest value of k
    that results in a different solution to the p-median problem when edge
    lengths are elongated by a factor based on k.

    Args:
        graph (gh.Graph): The graph object containing vertices, edges, and the
        distance matrix.
        frac_list (list[float]): A list of fraction values used to scale edge
        costs.
        denominator (float): The scaling denominator applied to k for edge
        elongation.
        k_upper_limit (float): The maximum value to test for k.
        p (int): Number of weighted p medians.
    """
    k = 0
    step = k_upper_limit / 2
    print(f"Solving for k: {k:.4f}")
    previous_medians, previous_objective = alg.pulp_solve(
        graph.dist_matrix, graph.vertices, p, alg.P_MEDIAN, graph.city_bound
    )
    elong_edges = []
    medians = []
    objective = 0.0
    cost_ratios = [1.0 for _ in graph.edges]

    alg.output_solution(
        k,
        k_upper_limit,
        cost_ratios,
        previous_medians,
        previous_objective,
        f"{graph.region}-{p}-calculate-first-k",
    )
    alg.output_edge_behavior(
        graph.edges,
        graph.edges,
        previous_medians,
        f"{graph.region}-{p}-calculate-first-k",
    )

    while step >= PRECISION and k + step <= k_upper_limit:
        k += step

        elong_edges = alg.get_elong_edges(
            graph.edges, frac_list, (k / denominator)
        )

        elong_dist_matrix = alg.create_dist_matrix(
            elong_edges, graph.num_of_verts
        )

        print(f"Solving for k: {k:.4f}")
        medians, objective = alg.pulp_solve(
            elong_dist_matrix, graph.vertices, p, alg.P_MEDIAN, graph.city_bound
        )

        if medians != previous_medians:
            k -= step
            step /= 2

    cost_ratios = [
        graph.edges[i].cost / elong_edges[i].cost
        for i in range(len(elong_edges))
    ]

    alg.output_solution(
        k,
        k_upper_limit,
        cost_ratios,
        medians,
        objective,
        f"{graph.region}-{p}-calculate-first-k",
    )
    alg.output_edge_behavior(
        graph.edges,
        elong_edges,
        medians,
        f"{graph.region}-{p}-calculate-first-k",
    )


def calculate_all_ks(
    graph: gh.Graph,
    frac_list: list[float],
    denominator: float,
    k_upper_limit: float,
    p: int,
):
    """
    Iteratively calculates values of k and evaluates the p-median problem
    for each step until k approaches the upper limit.

    This function progressively increases k, adjusting edge lengths and solving
    the p-median problem. It also computes and displays statistical data about
    edge cost elongations, such as min, max, mean, and mode of the cost ratios.

    Args:
        graph (gh.Graph): The graph object containing vertices, edges, and the
        distance matrix.
        frac_list (list[float]): A list of fraction values used to scale edge
        costs.
        denominator (float): The scaling denominator applied to k for edge
        elongation.
        k_upper_limit (float): The maximum value to increment k towards.
        p (int): Number of weighted p medians.
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

        print(f"Solving for k: {k:.4f}")
        medians, objective = alg.pulp_solve(
            elong_dist_matrix, graph.vertices, p, alg.P_MEDIAN, graph.city_bound
        )

        if previous_medians != medians:
            previous_medians = medians
            cost_ratios = [
                edges_previous[i].cost / elong_edges[i].cost
                for i in range(len(elong_edges))
            ]

            alg.output_solution(
                k,
                k_upper_limit,
                cost_ratios,
                medians,
                objective,
                f"{graph.region}-{p}-calculate-all-ks",
            )
            alg.output_edge_behavior(
                edges_previous,
                elong_edges,
                medians,
                f"{graph.region}-{p}-calculate-all-ks",
            )

        step /= 2
        k += step
        edges_previous = elong_edges
