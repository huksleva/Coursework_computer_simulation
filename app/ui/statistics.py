"""
File: statistics.py

This module contains functions responsible
for creating and updating statistics.
"""

import numpy as np


def create_statistics_panel(
    figure,
    grid_spec
):
    """
    Create statistics panel.

    Args:
        figure:
            Matplotlib figure object.

        grid_spec:
            Main GridSpec object.

    Returns:
        tuple:
            Statistics axis,
            statistics text,
            end text.
    """

    stats_ax = figure.add_subplot(
        grid_spec[0:2, 10:12]
    )

    stats_ax.set_facecolor("#f0f0f0")

    stats_ax.set_xticks([])
    stats_ax.set_yticks([])

    stats_ax.set_title("Statistics")

    stats_text = stats_ax.text(
        0.05,
        0.95,
        "",
        transform=stats_ax.transAxes,
        fontsize=10,
        verticalalignment="top"
    )

    end_text = figure.text(
        0.5,
        0.95,
        "",
        ha="center",
        fontsize=18,
        color="darkred",
        weight="bold"
    )

    return stats_ax, stats_text, end_text


def calculate_statistics(
    grid,
    healthy_state,
    infected_state,
    recovered_state,
    dead_state
):
    """
    Calculate simulation statistics.

    Args:
        grid (np.ndarray):
            Current simulation grid.

        healthy_state (int):
            Healthy state value.

        infected_state (int):
            Infected state value.

        recovered_state (int):
            Recovered state value.

        dead_state (int):
            Dead state value.

    Returns:
        dict:
            Simulation statistics.
    """

    healthy = np.sum(
        grid == healthy_state
    )

    infected = np.sum(
        grid == infected_state
    )

    recovered = np.sum(
        grid == recovered_state
    )

    dead = np.sum(
        grid == dead_state
    )

    total_population = (
        healthy +
        infected +
        recovered +
        dead
    )

    return {
        "healthy": healthy,
        "infected": infected,
        "recovered": recovered,
        "dead": dead,
        "total_population": total_population,
    }


def update_statistics_text(
    stats_text,
    healthy,
    infected,
    recovered,
    dead,
):

    total_population = (
        healthy
        + infected
        + recovered
        + dead
    )

    stats_text.set_text(
        f"Population: {total_population}\n"
        f"Healthy: {healthy}\n"
        f"Infected: {infected}\n"
        f"Recovered: {recovered}\n"
        f"Dead: {dead}"
    )