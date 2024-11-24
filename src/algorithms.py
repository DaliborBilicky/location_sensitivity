from itertools import combinations

import numpy as np

from graph import Edge, Graph, Vertex


class Algorithms:
    """
    Class for storing algorithms.
    """

    def __init__(self, graph: Graph) -> None:
        """
        Constructor for class Algorithms.

        Args:
            graph (Graph): graph which algorithms are working with
        """
        self.graph = graph
        self.ratios_list = []

    def create_dist_matrix(self, elongated: bool) -> None:
        """
        Make base distance matrix

        Args:
            elongated (bool): if we are making dist matrix for modified graph
        """
        self.dist_matrix = np.full(
            (self.graph.num_of_verts, self.graph.num_of_verts), float(np.inf)
        )

        for i in range(self.graph.num_of_verts):
            self.dist_matrix[i][i] = 0

        for edge in self.graph.edges:
            if elongated:
                self.dist_matrix[edge.v1, edge.v2] = edge.new_cost
                self.dist_matrix[edge.v2, edge.v1] = edge.new_cost
            else:
                self.dist_matrix[edge.v1, edge.v2] = edge.cost
                self.dist_matrix[edge.v2, edge.v1] = edge.cost

    def create_floyd_matrix(self) -> None:
        """
        Takes base distance matrix and enhance it with Floyd Warshall algorithm
        """

        for k in range(self.graph.num_of_verts):
            for i in range(self.graph.num_of_verts):
                for j in range(self.graph.num_of_verts):
                    self.dist_matrix[i][j] = min(
                        self.dist_matrix[i][j],
                        self.dist_matrix[i][k] + self.dist_matrix[k][j],
                    )

    def brutForce(self, p: int) -> list[Vertex]:
        """
        Create possible solution using Brut-force method

        Args:
            p (int): Number of medians to choose.

        Returns:
            medians
        """

        min_cost = float(np.inf)
        best_medians = []
        for medians in combinations(self.graph.vertices, p):
            total_cost = 0
            for u in self.graph.vertices:
                min_distance = float(np.inf)
                for v in medians:
                    min_distance = min(
                        min_distance, self.dist_matrix[u.name][v.name]
                    )

                total_cost += self.graph.vertices[u.name].weight * min_distance

            if total_cost < min_cost:
                min_cost = total_cost
                best_medians = list(medians)

        return best_medians

    def fill_ratio_list(self):
        for e in self.graph.edges:
            frac_sum = 0.0

            for v in self.graph.vertices:
                d_v1 = self.dist_matrix[e.v1][v.name]
                d_v2 = self.dist_matrix[e.v2][v.name]
                d_e_v = min(d_v1, d_v2) + (e.cost / 2)
                frac = v.weight / d_e_v
                frac_sum += frac

            self.ratios_list.append(frac_sum)

    def gravitational_formula(self, k: float) -> None:
        """
        Elongates all edges in graph

        Args:
            k (float): scaling factor
        """

        self.fill_ratio_list()

        denominator = 0.0
        for i in range(len(self.ratios_list)):
            denominator += self.ratios_list[i]

        i = 0
        for e in self.graph.edges:
            e.new_cost = e.cost / (1 - k * (self.ratios_list[i] / denominator))
            i += 1
