import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import floyd_warshall

import graph as gh


def read_edges(file_path: str) -> list[gh.Edge]:
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
            edges.append(gh.Edge(vertex_1 - 1, vertex_2 - 1, float(weight)))

    return edges


def read_vertices(file_path: str) -> list[gh.Vertex]:
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
                vertices.append(gh.Vertex(label))
            else:
                weight = float(parts[1])
                name = parts[2]
                vertices.append(gh.Vertex(label, weight, name))

    return vertices


def create_dist_matrix(edges: list[gh.Edge], num_of_verts: int) -> np.ndarray:
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
