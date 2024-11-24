import algorithms as alg
import graph as gh


def main() -> None:
    """
    Main function.
    """
    graph = gh.Graph("easy")
    algo = alg.Algorithms(graph)
    algo.create_dist_matrix(False)
    algo.create_floyd_matrix()
    print(algo.dist_matrix)
    algo.gravitational_formula(2)
    algo.create_dist_matrix(True)
    algo.create_floyd_matrix()
    print(algo.dist_matrix)


if __name__ == "__main__":
    main()
