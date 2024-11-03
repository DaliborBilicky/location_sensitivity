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
        self.dist_matrix = np.full(
            (self.graph.num_of_verts, self.graph.num_of_verts), float(np.inf)
        )

    def create_floyd_matrix(self) -> None:
        """
        Takes base distance matrix and enhance it with Floyd Warshall algorithm
        """

        for i in range(self.graph.num_of_verts):
            self.dist_matrix[i][i] = 0

        for edge in self.graph.edges:
            self.dist_matrix[edge.v1, edge.v2] = edge.cost
            self.dist_matrix[edge.v2, edge.v1] = edge.cost

        # for k in range(self.graph.num_of_verts):
        #     for i in range(self.graph.num_of_verts):
        #         for j in range(self.graph.num_of_verts):
        #             print(i, j, k)
        #             self.dist_matrix = min(
        #                 self.dist_matrix[i][j],
        #                 self.dist_matrix[i][k] + self.dist_matrix[k][j],
        #             )

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

                total_cost += self.graph.vertices[u.name].weight

            if total_cost < min_cost:
                min_cost = total_cost
                best_medians = list(medians)

        return best_medians

    def sum_fractions(self, edge: Edge) -> float:
        """
        Sum all vertex cost divided by distances to edge

        Args:
            edge (Edge): edge to witch distance its calculated.

        Returns:
            summed fractions
        """
        frac_sum = 0.0

        for v in self.graph.vertices:
            d_v1 = self.dist_matrix[edge.v1][v.name]
            d_v2 = self.dist_matrix[edge.v2][v.name]
            d_e_v = min(d_v1, d_v2) + (edge.cost / 2)
            frac = self.graph.vertices[v.name].weight / d_e_v
            frac_sum += frac
        return frac_sum

    def gravitational_model(self, k: float) -> None:
        """
        Elongates all edges in graph

        Args:
            k (float):

        """
        for e in self.graph.edges:
            e.new_cost = e.cost / (1 - k * self.sum_fractions(e))
