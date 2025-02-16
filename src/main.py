import math
import statistics as stt
import sys

import numpy as np

import algorithms as alg
import graph as gh

PREVISION = 0.01


def main() -> None:
    """
    Main function.
    """
    if len(sys.argv) < 4:
        raise ValueError(
            "Too few arguments! Usage: python src/main.py <region acronym> <P> <name of result file>"
        )

    REGION = sys.argv[1]
    P = int(sys.argv[2])
    RESULT = sys.argv[3]

    graph = gh.Graph(REGION)

    frac_list = alg.get_frac_list(graph)
    denominator = sum(f for f in frac_list)
    k_upper_limit = alg.get_k_upper_limit(frac_list, denominator)

    k = 0
    step = k_upper_limit
    y_previous = []
    edges_previous = graph.edges

    while not math.isclose(k, k_upper_limit, rel_tol=PREVISION):
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

        if y_previous != y:
            y_previous = y
            cost_differ = np.zeros(len(elong_edges))

            for i in range(len(elong_edges)):
                cost_differ[i] = elong_edges[i].cost / edges_previous[i].cost

            min_cost = cost_differ.min()
            max_cost = cost_differ.max()
            mean_cost = cost_differ.mean()
            mode_cost = stt.mode(cost_differ)

            y = [(index + 1) for index, value in enumerate(y) if value == 1.0]
            with open(f"results/{RESULT}.txt", "a") as file:
                file.write(
                    f"k: {k:.4f} k-lim: {k_upper_limit:.4f} "
                    + f"min: {min_cost:.4f} max: {max_cost:.4f} "
                    + f"mean: {mean_cost:.4f} mode: {mode_cost:.4f}\n"
                )
                file.write(f"{y}\n\n")
                for i in range(len(elong_edges)):
                    if elong_edges[i].v1 in y or elong_edges[i].v2 in y:
                        file.write(
                            f"{elong_edges[i]} / {edges_previous[i]} = {cost_differ[i]}\n"
                        )
                file.write("\n\n")

        step /= 2
        k += step
        edges_previous = elong_edges


if __name__ == "__main__":
    main()
