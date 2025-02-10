import math
from itertools import combinations

import numpy as np
import pulp as pl
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import floyd_warshall

from graph import Edge, Graph, Vertex


def read_edges(file_path: str) -> list[Edge]:
    """
    Reads file with records of edges.

    Args:
        file_path (str): path to file.

    Returns:
        list of read edges.
    """
    edges = []
    with open(file_path, "r") as file:
        file.readline()
        for line in file:
            vertex_1, vertex_2, weight = map(int, line.split())
            edges.append(Edge(vertex_1 - 1, vertex_2 - 1, float(weight)))

    return edges


def read_vertices(file_path: str) -> list[Vertex]:
    """
    Reads file with records of vertices.

    Args:
        file_path (str): path to file.

    Returns:
        list of read vertices.
    """
    vertices = []
    with open(file_path, "r") as file:
        file.readline()
        for line in file:
            parts = line.strip().split(maxsplit=2)
            label = int(parts[0]) - 1
            if len(parts) < 3:
                vertices.append(Vertex(label))
            else:
                weight = float(parts[1])
                name = parts[2]
                vertices.append(Vertex(label, weight, name))

    return vertices


def create_dist_matrix(edges: list[Edge], num_of_verts: int) -> np.ndarray:
    """
    Make base distance matrix

    Args:
        elongated (bool): if we are making dist matrix for modified graph
    """

    dist_matrix = np.full((num_of_verts, num_of_verts), float(np.inf))

    for i in range(num_of_verts):
        dist_matrix[i][i] = 0

    for e in edges:
        dist_matrix[e.v1, e.v2] = e.cost
        dist_matrix[e.v2, e.v1] = e.cost

    sparse_matrix = csr_matrix(dist_matrix)
    dist_matrix = floyd_warshall(csgraph=sparse_matrix, directed=False)

    return dist_matrix


def solve_p_median_pulp(
    dist_matrix: np.ndarray, vertices: list[Vertex], p: int
):
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

    problem.solve()

    x_result = [[x[(i, j)].varValue for j in range(m)] for i in range(n)]
    y_result = [y[j].varValue for j in range(m)]

    return x_result, y_result


def brutForce(graph: Graph, p: int) -> list[Vertex]:
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


def get_frac_list(graph: Graph) -> list[float]:
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


def get_k_upper_limit(frac_list: list, denominator: float) -> float:
    x_min = float(np.inf)
    for fraction in frac_list:
        x = denominator / fraction
        x_min = min(x_min, x)
    return x_min


def run_test(graph: Graph, p: int):
    y_results = []

    frac_list = get_frac_list(graph)
    denominator = sum(f for f in frac_list)
    k_upper_limit = get_k_upper_limit(frac_list, denominator)

    k = 0
    step = k_upper_limit

    while not math.isclose(k, k_upper_limit, rel_tol=0.01):
        print(k_upper_limit)
        print(k)
        i = 0
        elong_edges = []

        for e in graph.edges:
            edge = Edge(
                e.v1, e.v2, e.cost / (1 - k * frac_list[i] / denominator)
            )
            elong_edges.append(edge)
            i += 1

        elong_dist_matrix = create_dist_matrix(elong_edges, graph.num_of_verts)

        _, y = solve_p_median_pulp(elong_dist_matrix, graph.vertices, p)
        print([(index + 1) for index, value in enumerate(y) if value == 1.0])

        step /= 2
        k += step

    return y_results
