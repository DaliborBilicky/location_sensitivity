import algorithms as alg
import graph as gh


def main() -> None:
    """
    Main function.
    """

    graph = gh.Graph("easy")
    algos = alg.Algorithms(graph)
    algos.create_floyd_matrix()


if __name__ == "__main__":
    main()
