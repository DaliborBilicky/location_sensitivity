import time
from itertools import combinations

import numpy as np
import pulp as pl

import graph as gh


def pulp_solve_p_median(
    dist_matrix: np.ndarray,
    vertices: list[gh.Vertex],
    p: int,
    output: bool = False,
) -> list[int]:

    start_time = time.time()
    matrix = dist_matrix
    n, m = matrix.shape

    problem = pl.LpProblem("Weighted_p-Median", pl.LpMinimize)

    x = pl.LpVariable.dicts(
        "x",
        [(i, j) for i in range(n) for j in range(m)],
        lowBound=0,
        upBound=1,
        cat="Binary",
    )
    y = pl.LpVariable.dicts(
        "y", [j for j in range(m)], lowBound=0, upBound=1, cat="Binary"
    )

    problem += pl.lpSum(
        vertices[i].weight * matrix[i][j] * x[(i, j)]
        for i in range(n)
        for j in range(m)
    )

    for i in range(n):
        problem += pl.lpSum(x[(i, j)] for j in range(m)) == 1

    for i in range(n):
        for j in range(m):
            problem += x[(i, j)] <= y[j]

    problem += pl.lpSum(y[j] for j in range(m)) == p

    solver = pl.getSolver("PULP_CBC_CMD", msg=False)
    problem.solve(solver)

    y = [j for j in range(m) if y[j].varValue == 1.0]

    elapsed_time = time.time() - start_time

    if output:
        print(f"Solver Status: {pl.LpStatus[problem.status]}")
        print(f"Time Taken: {elapsed_time:.4f} seconds")
        print(f"Objective Value: {pl.value(problem.objective):.4f}")
        print(f"Selected Facilities: {y}")

    return y


def brut_force(graph: gh.Graph, p: int) -> list[gh.Vertex]:
    """
    Create possible solution using Brut-force method

    Args:
        p (int): Number of medians to choose.

    Returns:
        medians
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

            total_cost += graph.vertices[u.label].weight * min_distance

        if total_cost < min_cost:
            min_cost = total_cost
            best_medians = list(medians)

    return best_medians
