class Edge:
    """
    Class for storing data for edge.
    """

    def __init__(self, v1: int, v2: int, cost: float):
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
