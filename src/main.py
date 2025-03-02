import sys
import threading

import algorithms as alg
import graph as gh


def main():
    """
    Main function.
    """
    if len(sys.argv) < 3:
        raise ValueError(
            "Too few arguments! Usage: python src/main.py <region acronym> <P>"
        )

    REGION = sys.argv[1]
    P = int(sys.argv[2])

    graph = gh.Graph(REGION, P)

    frac_list = alg.get_frac_list(graph)
    denominator = sum(f for f in frac_list)
    k_upper_limit = alg.get_k_upper_limit(frac_list, denominator)

    all_ks_arg = (graph, frac_list, denominator, k_upper_limit)
    first_k_arg = all_ks_arg

    thread1 = threading.Thread(target=alg.calculate_all_ks, args=all_ks_arg)
    thread2 = threading.Thread(target=alg.calculate_first_k, args=first_k_arg)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()


if __name__ == "__main__":
    main()
