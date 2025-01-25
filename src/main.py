import algorithms as alg
import graph as gh


def main() -> None:
    """
    Main function.
    """
    graph = gh.Graph("BA")

    _, y = alg.solve_p_median_pulp(graph.dist_matrix, graph.vertices, 6)

    graph.elong_edges = alg.gravitational_formula(graph, 45.3)
    graph.elong_dist_matrix = alg.create_dist_matrix(
        graph.elong_edges, graph.num_of_verts
    )

    _, elong_y = alg.solve_p_median_pulp(
        graph.elong_dist_matrix, graph.vertices, 6
    )
    print("\n" * 25)
    print(graph.dist_matrix)
    print(graph.elong_dist_matrix)
    print([(index + 1) for index, value in enumerate(y) if value == 1.0])
    print([(index + 1) for index, value in enumerate(elong_y) if value == 1.0])


if __name__ == "__main__":
    main()
