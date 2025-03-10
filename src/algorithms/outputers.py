import statistics as stt

import graph as gh

AVG_SPEED = 110  # Define constant for average speed


def output_solution(
    k: float,
    k_lim: float,
    cost_ratios: list[float],
    medians: list[int],
    file: str,
):
    """
    Outputs the solution data (speed declines, p-medians) to a file.

    Args:
        k (float): The value of k for the elongation.
        k_lim (float): The upper limit for k.
        cost_ratios (list[float]): List of cost ratios for edge elongation.
        medians (list[int]): List of the p-median vertex labels.
        file (str): The name of the output file.
    """

    minimum = AVG_SPEED - AVG_SPEED / min(cost_ratios)
    maximum = AVG_SPEED - AVG_SPEED / max(cost_ratios)
    average = AVG_SPEED - AVG_SPEED / stt.mean(cost_ratios)
    modus = AVG_SPEED - AVG_SPEED / stt.mode(cost_ratios)

    with open(f"results/{file}.txt", "a") as f:
        f.write(
            f"k: {k:.4f} upper limit: {k_lim:.4f}\n"
            f"Weighted p-medians: {medians}\n"
            f"Average speed for ambulance: {AVG_SPEED}\n"
            f"Min speed decline: {minimum:.4f}\n"
            f"Max speed decline: {maximum:.4f}\n"
            f"Average speed decline: {average:.4f}\n"
            f"Most often speed decline: {modus:.4f}\n"
        )


def output_edge_behavior(
    original_edges: list[gh.Edge],
    elongated_edges: list[gh.Edge],
    medians: list[int],
    file: str,
):
    """
    Outputs the edge elongation behavior, including smallest and biggest ratio changes.

    Args:
        original_edges (list[gh.Edge]): The original edges.
        elongated_edges (list[gh.Edge]): The elongated edges.
        medians (list[int]): List of the p-median vertex labels.
        file (str): The name of the output file.
    """

    edges_with_ratios = zip(original_edges, elongated_edges)
    sorted_edges = sorted(
        edges_with_ratios, key=lambda pair: pair[1].cost / pair[0].cost
    )

    smallest_ratio = sorted_edges[:10]
    biggest_ratio = sorted_edges[-10:]

    incident_edges = [
        e for e in original_edges if e.v1 in medians or e.v2 in medians
    ]

    with open(f"results/{file}.txt", "a") as f:

        def write_zipped_edges(label, zipped_edges):
            f.write(f"{label}\n")
            for original, elongated in zipped_edges:
                ratio = elongated.cost / original.cost
                f.write(
                    f"Ratio: {ratio:.4f}, "
                    f"{original} -> {elongated.cost:.4f}\n"
                )

        write_zipped_edges("Smallest cost differences:", smallest_ratio)
        write_zipped_edges("Biggest cost differences:", biggest_ratio)

        f.write(
            f"Edges incident to medians:\n"
            + "\n".join(map(str, incident_edges))
            + "\n\n"
        )
