import time
from itertools import combinations

import numpy as np
import pulp as pl

import graph as gh


def create_lp_variables(n: int, m: int) -> tuple[dict, dict]:
    """
    Creates the linear programming variables for the p-median problem.

    Args:
        n (int): Number of vertices.
        m (int): Number of potential medians.

    Returns:
        tuple[dict, dict]: Dictionaries of assignment (x) and median selection (y) variables.
    """
    x = pl.LpVariable.dicts(
        "x", [(i, j) for i in range(n) for j in range(m)], cat="Binary"
    )
    y = pl.LpVariable.dicts("y", [j for j in range(m)], cat="Binary")
    return x, y


def add_constraints(
    problem: pl.LpProblem, x: dict, y: dict, n: int, m: int, p: int
):
    """
    Adds constraints to the p-median linear programming problem.

    Args:
        problem (pl.LpProblem): The LP problem to add constraints to.
        x (dict): Assignment variables.
        y (dict): Median selection variables.
        n (int): Number of vertices.
        m (int): Number of potential medians.
        p (int): Number of medians to select.
    """
    for i in range(n):
        problem += pl.lpSum(x[(i, j)] for j in range(m)) == 1

    for i in range(n):
        for j in range(m):
            problem += x[(i, j)] <= y[j]

    problem += pl.lpSum(y[j] for j in range(m)) == p


def set_objective(
    problem: pl.LpProblem,
    x: dict,
    dist_matrix: np.ndarray,
    vertices: list[gh.Vertex],
):
    """
    Sets the objective function for minimizing the weighted distance.

    Args:
        problem (pl.LpProblem): The LP problem to set the objective for.
        x (dict): Assignment variables.
        dist_matrix (np.ndarray): Distance matrix.
        vertices (list[gh.Vertex]): List of vertex objects with weights.
    """
    problem += pl.lpSum(
        vertices[i].weight * dist_matrix[i][j] * x[(i, j)]
        for i in range(len(vertices))
        for j in range(len(vertices))
    )


def pulp_solve_p_median(
    dist_matrix: np.ndarray,
    vertices: list[gh.Vertex],
    p: int,
    output: bool = False,
) -> list[int]:
    """
    Solves the weighted p-median problem using linear programming with PuLP.

    Args:
        dist_matrix (np.ndarray): Distance matrix of the graph.
        vertices (list[gh.Vertex]): List of vertex objects with weights.
        p (int): Number of medians to select.
        output (bool, optional): If True, prints solver status and details.

    Returns:
        list[int]: List of selected median indices.
    """
    start_time = time.time()
    n, m = dist_matrix.shape

    problem = pl.LpProblem("Weighted_p-Median", pl.LpMinimize)

    x, y = create_lp_variables(n, m)

    set_objective(problem, x, dist_matrix, vertices)

    add_constraints(problem, x, y, n, m, p)

    solver = pl.getSolver("PULP_CBC_CMD", msg=False)
    problem.solve(solver)

    selected_medians = [j for j in range(m) if y[j].varValue == 1.0]

    if output:
        print(f"Solver Status: {pl.LpStatus[problem.status]}")
        print(f"Time Taken: {time.time() - start_time:.4f} seconds")
        print(f"Objective Value: {pl.value(problem.objective):.4f}")
        print(f"Selected Medians: {selected_medians}")

    return selected_medians


def brut_force(graph: gh.Graph, p: int) -> list[gh.Vertex]:
    """
    Solves the p-median problem using a brute-force approach.

    This method evaluates all possible combinations of p medians from the
    graph's vertices and selects the combination that minimizes the total
    weighted distance.

    Args:
        graph (gh.Graph): The graph containing vertices, edges, and distance matrix.
        p (int): The number of medians to select.

    Returns:
        list[gh.Vertex]: A list of Vertex objects representing the best medians.
    """
    min_cost = float(np.inf)
    best_medians = []

    for medians in combinations(graph.vertices, p):
        total_cost = 0

        for u in graph.vertices:
            min_distance = float(np.inf)
            for v in medians:
                min_distance = min(
                    min_distance, graph.dist_matrix[u.label][v.label]
                )
            total_cost += u.weight * min_distance

        if total_cost < min_cost:
            min_cost = total_cost
            best_medians = list(medians)

    return best_medians
