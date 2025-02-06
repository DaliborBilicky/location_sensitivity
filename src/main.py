import algorithms as alg
import graph as gh


def main() -> None:
    """
    Main function.
    """
    REGION = "BA"
    P = 6
    graph = gh.Graph(REGION)

    k = 0
    step = 2

    while True:
        elong_edges = alg.gravitational_formula(graph, k)

        if not elong_edges:
            break

        elong_dist_matrix = alg.create_dist_matrix(
            elong_edges, graph.num_of_verts
        )

        _, y = alg.solve_p_median_pulp(elong_dist_matrix, graph.vertices, P)

        with open(f"results/{REGION}_result_p-{P}.txt", "a") as file:
            file.write(
                str(
                    [
                        (index + 1)
                        for index, value in enumerate(y)
                        if value == 1.0
                    ]
                )
            )
            file.write("\n")
            counter = 0
            for edge in elong_edges:
                file.write(str(edge))
                counter += 1
                if counter == 5:
                    file.write("\n")
                    counter = 0

            file.write("\n_____________________________________________\n")
            file.write("\n")

        k += step


if __name__ == "__main__":
    main()
