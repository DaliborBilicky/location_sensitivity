import statistics as stt

import graph as gh

AVG_SPEED = 110


def output_solution(
    k: float,
    k_lim: float,
    cost_ratios: list[float],
    medians: list[int],
    file_prefix: str,
):
    minimum = AVG_SPEED - AVG_SPEED / min(cost_ratios)
    maximum = AVG_SPEED - AVG_SPEED / max(cost_ratios)
    average = AVG_SPEED - AVG_SPEED / stt.mean(cost_ratios)
    modus = AVG_SPEED - AVG_SPEED / stt.mode(cost_ratios)

    with open(f"results/{file_prefix}-result.txt", "a") as f:
        f.write(
            f"k: {k:.4f} upper limit: {k_lim:.4f}\n"
            f"Weighted p-medians: {medians}\n"
            f"Average speed for ambulance: {AVG_SPEED}\n"
            f"Min speed decline: {minimum:.4f}\n"
            f"Max speed decline: {maximum:.4f}\n"
            f"Average speed decline: {average:.4f}\n"
            f"Most often speed decline: {modus:.4f}\n\n"
        )


def output_edge_behavior(k: float, edges: list[gh.Edge], meadias: list[int]):
    pass
