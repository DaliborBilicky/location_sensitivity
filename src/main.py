import algorithms as alg
import graph as gh


def main() -> None:
    """
    Main function.
    """

    graph = gh.Graph("test")
    algos = alg.Algorithms(graph)
    algos.create_dist_matrix(False)
    algos.create_floyd_matrix()
    medians = algos.brutForce(5)
    for m in medians:
        print(m)

    algos.gravitational_model((3 / 16))
    algos.create_dist_matrix(True)
    algos.create_floyd_matrix()
    medians = algos.brutForce(5)
    for m in medians:
        print(m)


if __name__ == "__main__":
    main()
