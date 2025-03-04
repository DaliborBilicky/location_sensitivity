import algorithms as alg


class Graph:
    """
    Represents a graph with vertices and edges, supporting operations such as distance matrix creation.
    """

    def __init__(self, region: str, p: int):
        """
        Initializes a Graph instance by loading vertices and edges from region-specific files.

        Args:
            region (str): The region name used to locate the input files containing graph data.
            p (int): The number of weighted medians for the algorithm.

        The class expects the following input files in the ./res/Kraje_input_data/ directory:
            - Nodes file: VUC140318_<region>_nodes.txt
            - Edges file: VUC140318_<region>_edges.txt
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
        Returns a string representation of the graph.

        The output includes all edges and vertices formatted as:
            - Each edge on a new line with its details.
            - Each vertex on a new line with its label and weight.

        Returns:
            str: A formatted string representation of the graph's edges and vertices.
        """
        str_edges = [str(edge) + "\n" for edge in self.edges]
        str_vertices = [str(vertex) + "\n" for vertex in self.vertices]
        return "".join(str_edges) + "\n" + "".join(str_vertices)
