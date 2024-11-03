import algorithms as alg
import graph as gh


def main() -> None:
    """
    Main function.
    """

    graph = gh.Graph("easy")
    algos = alg.Algorithms(graph)
    algos.create_floyd_matrix()
    algos.gravitational_model((3 / 16))
    for e in graph.edges:
        print(e.new_cost)


if __name__ == "__main__":
    main()
