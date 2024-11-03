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
        self.new_cost = cost

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

    def __init__(self, name: int, weight: float) -> None:
        """
        Constructor for class Vertex.

        Args:
            name (int): name of vertex.
            weight (float): vertex weight.
        """
        self.name = name
        self.weight = weight

    def __str__(self) -> str:
        """
        Str function to put instance into string.

        Returns:
            Vertex in string.
        """
        return f"{self.name}: {self.weight}"


class Graph:
    """
    Class for storing data of Graph.
    """

    def __init__(self, folder: str) -> None:
        """
        Constructor for class Graph.

        Args:
            folder (str): folder name containing graph
        """
        self.vertices = read_vertices(f"./res/graphs/{folder}/vertices.txt")
        self.edges = read_edges(f"./res/graphs/{folder}/edges.txt")
        self.num_of_verts = len(self.vertices)

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
        for line in file:
            vertex_1, vertex_2, weight = map(int, line.split())
            edges.append(Edge(vertex_1, vertex_2, float(weight)))

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
    name = 0
    with open(file_path, "r") as file:
        for line in file:
            weight = line.strip()
            vertices.append(Vertex(name, float(weight)))
            name += 1

    return vertices
