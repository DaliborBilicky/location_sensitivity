class Vertex:
    """
    Represents a vertex in a graph with a label, optional weight, and a
    descriptive name.
    """

    def __init__(self, label: int, weight: float = 0.0, name: str = "Junction"):
        """
        Initializes a Vertex instance.

        Args:
            label (int): A unique identifier for the vertex.
            weight (float, optional): The weight or value associated with the
            vertex. Default is 0.0.
            name (str, optional): A human-readable name for the vertex. Default
            is "Junction".
        """
        self.label = label
        self.weight = weight
        self.name = name

    def __str__(self) -> str:
        """
        Returns a string representation of the vertex in the format:
        label name: weight.

        Returns:
            str: A formatted string representation of the vertex.
        """
        return f"{self.label} {self.name}: {self.weight}"
