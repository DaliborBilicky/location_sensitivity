import algorithms as alg
import graph as gh


def main() -> None:
    """
    Main function.
    """
    REGION = "BA"
    P = 6
    graph = gh.Graph(REGION)

    y_results = alg.run_test(graph, P)

    for y in y_results:
        print(y)


if __name__ == "__main__":
    main()
