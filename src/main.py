import sys

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
        raise ValueError(
            "Invalid value for P. It must be a positive integer."
        ) from e

    return region, p


def main():
    """
    Main function.
    """
    try:
        region, p = parse_arguments()
        graph = gh.Graph(region)

        frac_list = alg.get_frac_list(graph)
        denominator = sum(frac_list)

        k_upper_limit = alg.get_k_upper_limit(frac_list, denominator) - 1
        alg.calculate_first_k(graph, frac_list, denominator, k_upper_limit, p)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
