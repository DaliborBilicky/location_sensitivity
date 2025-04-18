import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import floyd_warshall

import graph as gh


def read_edges(file_path: str) -> list[gh.Edge]:
    """
    Reads edges from a file and returns them as a list of Edge objects.

    The input file is expected to have lines with three integers each:
        vertex_1 vertex_2 weight
    Vertices are assumed to be 1-indexed in the file and are converted to
    0-indexing.

    Args:
        file_path (str): The path to the file containing edge data.

    Returns:
        list[gh.Edge]: A list of Edge objects representing the graph's edges.
    """
    edges = []
    with open(file_path, "r", encoding='utf-8') as file:
        file.readline()
        for line in file:
            vertex_1, vertex_2, weight = map(int, line.split())
            edges.append(gh.Edge(vertex_1 - 1, vertex_2 - 1, float(weight)))

    return edges


def read_vertices(file_path: str) -> tuple[list[gh.Vertex], int]:
    """
    Reads vertices from a file and returns them as a list of Vertex objects.

    The input file should have lines in the format:
        label weight name
    The label is mandatory, while weight and name are optional.
    Vertices are assumed to be 1-indexed in the file and are converted to
    0-indexing.

    Args:
        file_path (str): The path to the file containing vertex data.

    Returns:
        tuple:
            - list[gh.Vertex]: A list of Vertex objects with label, weight,
            and name attributes.
            - int: The index boundary (city_bound) separating city nodes from
            junction nodes.
    """
    vertices = []
    city_bound = 0
    with open(file_path, "r", encoding='utf-8') as file:
        file.readline()
        for line in file:
            parts = line.strip().split(maxsplit=2)
            label = int(parts[0]) - 1
            if len(parts) < 3:
                vertices.append(gh.Vertex(label))
                if city_bound == 0:
                    city_bound = label
            else:
                weight = float(parts[1])
                name = parts[2]
                vertices.append(gh.Vertex(label, weight, name))

    return vertices, city_bound


def create_dist_matrix(edges: list[gh.Edge], num_of_verts: int) -> np.ndarray:
    """
    Creates a distance matrix for the given edges and vertices using the
    Floyd-Warshall algorithm.

    The resulting matrix contains the shortest path distances between all pairs
    of vertices.
    Diagonal elements are 0, and non-connected vertices have a distance of
    infinity.

    Args:
        edges (list[gh.Edge]): A list of edges connecting vertices in the graph.
        num_of_verts (int): The total number of vertices in the graph.

    Returns:
        np.ndarray: A 2D array representing the shortest path distance matrix.
    """
    dist_matrix = np.full((num_of_verts, num_of_verts), float(np.inf))

    np.fill_diagonal(dist_matrix, 0)

    for e in edges:
        dist_matrix[e.v1, e.v2] = e.cost
        dist_matrix[e.v2, e.v1] = e.cost

    sparse_matrix = csr_matrix(dist_matrix)
    dist_matrix = floyd_warshall(csgraph=sparse_matrix, directed=False)

    return dist_matrix
