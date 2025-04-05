from itertools import combinations

import numpy as np
import pulp as pl

import graph as gh

P_MEDIAN = "p-median"
P_CENTER = "p-center"


def create_lp_variables(
    n: int, m: int
) -> tuple[dict[tuple, pl.LpVariable], dict[int, pl.LpVariable], pl.LpVariable]:
    """
    Creates the linear programming variables for the p-median or p-center
    problem.

    Args:
        n (int): Number of demand nodes (vertices).
        m (int): Number of potential facility locations (medians).

    Returns:
        tuple: A tuple containing:
            - x (dict[tuple, pl.LpVariable]): Assignment variables (binary),
            indicating whether vertex i is assigned to median j.
            - y (dict[int, pl.LpVariable]): Facility selection variables
            (binary), indicating whether a median is placed at location j.
            - z (pl.LpVariable): Maximum distance variable (continuous),
            used in the p-center problem.
    """
    x = pl.LpVariable.dicts(
        "x", [(i, j) for i in range(n) for j in range(m)], cat="Binary"
    )
    y = pl.LpVariable.dicts("y", [j for j in range(m)], cat="Binary")
    z = pl.LpVariable("z", lowBound=0, cat="Continuous")
    return x, y, z


def add_constraints(
    problem: pl.LpProblem,
    x: dict[tuple, pl.LpVariable],
    y: dict[int, pl.LpVariable],
    n: int,
    m: int,
    p: int,
):
    """
    Adds standard assignment and facility selection constraints to the problem.

    Each vertex must be assigned to exactly one median, and only to open
    medians. Exactly p medians must be selected.

    Args:
        problem (pl.LpProblem): The LP problem to add constraints to.
        x (dict[tuple, pl.LpVariable]): Assignment variables.
        y (dict[int, pl.LpVariable]): Facility selection variables.
        n (int): Number of demand nodes (vertices).
        m (int): Number of potential medians (facilities).
        p (int): Number of medians to select.
    """
    for i in range(n):
        problem += pl.lpSum(x[(i, j)] for j in range(m)) == 1

    for i in range(n):
        for j in range(m):
            problem += x[(i, j)] <= y[j]

    problem += pl.lpSum(y[j] for j in range(m)) == p


def add_additional_constraint(
    problem: pl.LpProblem,
    x: dict[tuple, pl.LpVariable],
    z: pl.LpVariable,
    dist_matrix: np.ndarray,
):
    """
    Adds the max-distance constraint used in the p-center problem.

    Ensures that no vertex is assigned to a facility farther than z.

    Args:
        problem (pl.LpProblem): The LP problem to add constraints to.
        x (dict[tuple, pl.LpVariable]): Assignment variables.
        z (pl.LpVariable): Maximum distance variable.
        dist_matrix (np.ndarray): Matrix of distances between vertices and
        medians.
    """
    n, m = dist_matrix.shape
    for j in range(m):
        problem += (
            pl.lpSum(dist_matrix[i][j] * x[(i, j)] for i in range(n)) <= z
        )


def set_objective(
    problem: pl.LpProblem,
    x: dict[tuple, pl.LpVariable],
    dist_matrix: np.ndarray,
    vertices: list[gh.Vertex],
):
    """
    Sets the objective function for the p-median problem.

    Minimizes the total weighted distance between vertices and assigned medians.

    Args:
        problem (pl.LpProblem): The LP problem to set the objective for.
        x (dict[tuple, pl.LpVariable]): Assignment variables.
        dist_matrix (np.ndarray): Matrix of distances between vertices and
        medians.
        vertices (list[gh.Vertex]): List of vertex objects, each with a weight
        attribute.
    """
    n, m = dist_matrix.shape
    problem += pl.lpSum(
        vertices[i].weight * dist_matrix[i][j] * x[(i, j)]
        for i in range(n)
        for j in range(m)
    )


def pulp_solve(
    dist_matrix: np.ndarray,
    vertices: list[gh.Vertex],
    p: int,
    problem_type: str,
) -> list[int]:
    """
    Solves the p-median or p-center problem using PuLP.

    Args:
        dist_matrix (np.ndarray): Distance matrix of the graph.
        vertices (list[gh.Vertex]): List of vertex objects with weights.
        p (int): Number of medians to select.
        problem_type (str): Type of problem to solve ('p_median' or 'p_center').

    Returns:
        list[int]: Indices of the selected median locations.
    """
    n, m = dist_matrix.shape

    problem = pl.LpProblem(f"Weighted_{problem_type}", pl.LpMinimize)

    x, y, z = create_lp_variables(n, m)

    add_constraints(problem, x, y, n, m, p)

    if problem_type == P_MEDIAN:
        set_objective(problem, x, dist_matrix, vertices)
    elif problem_type == P_CENTER:
        add_additional_constraint(problem, x, z, dist_matrix)
        problem += z
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

    solver = pl.getSolver("PULP_CBC_CMD", msg=True)
    problem.solve(solver)

    selected_set = [j for j in range(m) if y[j].varValue == 1.0]

    print(f"Selected set: {selected_set}\n")

    return selected_set


def brut_force(graph: gh.Graph, p: int) -> list[gh.Vertex]:
    """
    Solves the p-median problem using a brute-force approach.

    This method evaluates all possible combinations of p medians from the
    graph's vertices and selects the combination that minimizes the total
    weighted distance.

    Args:
        graph (gh.Graph): The graph containing vertices, edges, and distance
        matrix.
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
