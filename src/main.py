import numpy as np

import algorithms as alg
import graph as gh


def main() -> None:
    """
    Main function.
    """
    graph = gh.Graph("BA")
    print(graph.dist_matrix)

    for k in np.arange(0, 10, 0.1):
        print(f"\nk = {k}:")
        graph.elong_edges = alg.gravitational_formula(graph, k)
        graph.elong_dist_matrix = alg.create_dist_matrix(
            graph.elong_edges, graph.num_of_verts
        )
        print(graph.elong_dist_matrix)


if __name__ == "__main__":
    main()
