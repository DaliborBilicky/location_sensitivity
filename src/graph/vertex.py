class Vertex:
    """
    Class for storing data for vertex.
    """

    def __init__(self, label: int, weight: float = 0.0, name: str = "Junction"):
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
        return f"{self.label} {self.name}: {self.weight}"
