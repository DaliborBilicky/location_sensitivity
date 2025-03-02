import algorithms as alg

class Graph:
    """
    Class for storing data of Graph.
    """

    def __init__(self, region: str, p: int):
        """
        Constructor for class Graph.

        Args:
            folder (str): folder name containing graph
            p (int): number of weighted medians

            f"./res/graphs/easy/vertices.txt"
            f"./res/graphs/easy/edges.txt"
        """

        self.vertices = alg.read_vertices(
            f"./res/Kraje_input_data/VUC140318_{region}_nodes.txt"
        )
        self.edges = alg.read_edges(
            f"./res/Kraje_input_data/VUC140318_{region}_edges.txt"
        )
        self.num_of_verts = len(self.vertices)

        self.dist_matrix = alg.create_dist_matrix(self.edges, self.num_of_verts)
        self.p = p

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
