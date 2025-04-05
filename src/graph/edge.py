class Edge:
    """
    Represents an edge in a graph with a start vertex, an end vertex, and
    a cost associated with traversing the edge.
    """

    def __init__(self, v1: int, v2: int, cost: float):
        """
        Initializes an Edge instance.

        Args:
            v1 (int): The starting vertex of the edge.
            v2 (int): The ending vertex of the edge.
            cost (float): The cost associated with this edge. Can represent
            distance, weight, or any metric.


        """
        self.v1 = v1
        self.v2 = v2
        self.cost = cost

    def __str__(self) -> str:
        """
        Returns a string representation of the edge in the format:
        (v1)--cost--(v2).

        Returns:
            str: A human-readable string representation of the edge.
        """
        return f"({self.v1})--{self.cost:.4f}--({self.v2})"
