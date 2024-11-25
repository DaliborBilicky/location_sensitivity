import numpy as np

import algorithms as alg


class Edge:
    """
    Class for storing data for edge.
    """

    def __init__(self, v1: int, v2: int, cost: float) -> None:
        """
        Constructor for class Edge.

        Args:
            v1 (int):  vertex 1.
            v2 (int): vertex 2.
            cost (float): cost of edge.
        """
        self.v1 = v1
        self.v2 = v2
        self.cost = cost

    def __str__(self) -> str:
        """
        Str function to put instance into string.

        Returns:
            Edge in string.
        """
        return f"({self.v1})--{self.cost}--({self.v2})"


class Vertex:
    """
    Class for storing data for vertex.
    """

    def __init__(
        self, label: int, weight: float = 0.0, name: str = "Junction"
    ) -> None:
        """
        Constructor for class Vertex.

        Args:
            name (int): name of vertex.
            weight (float): vertex weight.
        """
        self.label = label
        self.weight = weight
        self.name = name

    def __str__(self) -> str:
        """
        Str function to put instance into string.

        Returns:
            Vertex in string.
        """
        return f"{self.label}: {self.weight}"


class Graph:
    """
    Class for storing data of Graph.
    """

    def __init__(self, region: str) -> None:
        """
        Constructor for class Graph.

        Args:
            folder (str): folder name containing graph

            f"./res/graphs/{folder}/vertices.txt"
            f"./res/graphs/{folder}/edges.txt"
        """
        self.vertices = alg.read_vertices(
            f"./res/Kraje_input_data/VUC140318_{region}_nodes.txt"
        )
        self.edges = alg.read_edges(
            f"./res/Kraje_input_data/VUC140318_{region}_edges.txt"
        )
        self.elong_edges = self.edges
        self.num_of_verts = len(self.vertices)

        self.dist_matrix = alg.create_dist_matrix(self.edges, self.num_of_verts)

        self.elong_dist_matrix = self.dist_matrix

    def __str__(self) -> str:
        """
        Str function to put instance into string.

        Returns:
            Edge in string.
        """
        str_edges = []
        str_vertecis = []
        for edge in self.edges:
            str_edges.append(str(edge) + "\n")
        for vertex in self.vertices:
            str_vertecis.append(str(vertex) + "\n")
        return "".join(str_edges) + "\n" + "".join(str_vertecis)
