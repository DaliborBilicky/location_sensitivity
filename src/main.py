import sys
import threading

import algorithms as alg
import graph as gh


def parse_arguments() -> tuple[str, int]:
    """
    Parse and validate command line arguments.

    Returns:
        tuple[str, int]: Region acronym and the number of weighted medians (P).

    Raises:
        ValueError: If arguments are missing or invalid.
    """
    if len(sys.argv) < 3:
        raise ValueError(
            "Too few arguments! Usage: python src/main.py <region acronym> <P>"
        )

    region = sys.argv[1].upper()
    try:
        p = int(sys.argv[2])
        if p <= 0:
            raise ValueError("P must be a positive integer.")
    except ValueError as e:
        raise ValueError("Invalid value for P. It must be a positive integer.") from e

    return region, p


def calculate_k_values(graph: gh.Graph, frac_list: list[float], denominator: float):
    """
    Starts threads for calculating all K values and the first K value.

    Args:
        graph (gh.Graph): The graph instance.
        frac_list (list[float]): Fractional list for K calculation.
        denominator (float): Denominator for K calculations.
    """
    k_upper_limit = alg.get_k_upper_limit(frac_list, denominator)
    args = (graph, frac_list, denominator, k_upper_limit)

    thread_all_ks = threading.Thread(target=alg.calculate_all_ks, args=args)
    thread_first_k = threading.Thread(target=alg.calculate_first_k, args=args)

    thread_all_ks.start()
    thread_first_k.start()

    thread_all_ks.join()
    thread_first_k.join()


def main():
    """
    Main function.
    """
    try:
        region, p = parse_arguments()
        graph = gh.Graph(region, p)

        frac_list = alg.get_frac_list(graph)
        denominator = sum(frac_list)

        calculate_k_values(graph, frac_list, denominator)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
