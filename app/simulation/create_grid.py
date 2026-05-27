"""
File: create_grid.py

This module contains functions for creating
the initial simulation grid.
"""

import numpy as np


def create_grid(
    grid_size,
    population_density,
    initial_infected,
    healthy_state,
    infected_state
):
    """
    Create initial epidemic simulation grid.

    Args:
        grid_size (int):
            Size of simulation grid.

        population_density (float):
            Density of population on the grid.

        initial_infected (int):
            Initial number of infected cells.

        healthy_state (int):
            Integer value representing healthy state.

        infected_state (int):
            Integer value representing infected state.

    Returns:
        np.ndarray:
            Generated simulation grid.
    """

    current_grid = np.zeros(
        (grid_size, grid_size),
        dtype=int
    )

    for x in range(grid_size):
        for y in range(grid_size):

            if np.random.random() < population_density:
                current_grid[x, y] = healthy_state

    healthy_positions = np.argwhere(
        current_grid == healthy_state
    )

    infected_count = min(
        initial_infected,
        len(healthy_positions)
    )

    selected = np.random.choice(
        len(healthy_positions),
        infected_count,
        replace=False
    )

    for index in selected:

        x, y = healthy_positions[index]

        current_grid[x, y] = infected_state

    return current_grid