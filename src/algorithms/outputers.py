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
            "----------\n"
            f"k: {k:.4f}, upper limit: {k_lim:.4f}\n"
            f"Weighted p-medians:\n{medians}\n"
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
    Outputs the edge elongation behavior, including smallest and biggest ratio changes, and incident edges.

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

    smallest_decline = sorted_edges[:10]
    biggest_decline = sorted_edges[-10:]

    incident_edges = [
        (original, elongated)
        for original, elongated in zip(original_edges, elongated_edges)
        if original.v1 in medians or original.v2 in medians
    ]

    incident_edge_ratios = [
        (original, elongated, elongated.cost / original.cost)
        for original, elongated in incident_edges
    ]

    with open(f"results/{file}.txt", "a") as f:

        def write_zipped_edges(label, zipped_edges):
            f.write(
                "----------\n"
                f"{label}\nSpeed decline, edge -> elongated cost\n"
            )
            for original, elongated in zipped_edges:
                ratio = elongated.cost / original.cost
                speed = AVG_SPEED - AVG_SPEED / ratio
                f.write(f"{speed:.4f}, {original} -> {elongated.cost:.4f}\n")

        write_zipped_edges("Smallest speed declines:", smallest_decline)
        write_zipped_edges("Biggest speed declines:", biggest_decline)

        f.write(
            "----------\n"
            + "Incident edges to medians:\n"
            + "Speed decline, edge -> elongated cost\n"
        )

        for original, elongated, ratio in incident_edge_ratios:
            speed = AVG_SPEED - AVG_SPEED / ratio
            f.write(f"{speed:.4f}, {original} -> {elongated.cost:.4f}\n")
        f.write("\n")
