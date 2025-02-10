import math

import algorithms as alg
import graph as gh


def main() -> None:
    """
    Main function.
    """
    REGION = "BA"
    P = 6
    A = 0.01
    graph = gh.Graph(REGION)

    frac_list = alg.get_frac_list(graph)
    denominator = sum(f for f in frac_list)
    k_upper_limit = alg.get_k_upper_limit(frac_list, denominator)

    k = 0
    step = k_upper_limit

    while not math.isclose(k, k_upper_limit, rel_tol=A):
        i = 0
        elong_edges = []

        for e in graph.edges:
            edge = gh.Edge(
                e.v1, e.v2, e.cost / (1 - k * frac_list[i] / denominator)
            )
            elong_edges.append(edge)
            i += 1

        elong_dist_matrix = alg.create_dist_matrix(
            elong_edges, graph.num_of_verts
        )

        _, y = alg.solve_p_median_pulp(elong_dist_matrix, graph.vertices, P)
        with open("result.txt", "a") as file:
            file.write(f"{k} {k_upper_limit}\n")
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

        step /= 2
        k += step


if __name__ == "__main__":
    main()
