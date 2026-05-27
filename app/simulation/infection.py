"""
File: infection.py

This module contains functions responsible
for infection spreading, recovery,
and death mechanics in the simulation.
"""

import numpy as np


def spread_infection(
    current_grid,
    grid_size,
    infection_probability,
    recovery_probability,
    death_probability,
    healthy_state,
    infected_state,
    recovered_state,
    dead_state
):
    """
    Spread infection across the simulation grid.

    Args:
        current_grid (np.ndarray):
            Current simulation grid.

        grid_size (int):
            Size of simulation grid.

        infection_probability (float):
            Base infection probability.

        recovery_probability (float):
            Probability of recovery.

        death_probability (float):
            Probability of death.

        healthy_state (int):
            Integer value representing healthy state.

        infected_state (int):
            Integer value representing infected state.

        recovered_state (int):
            Integer value representing recovered state.

        dead_state (int):
            Integer value representing dead state.

    Returns:
        np.ndarray:
            Updated simulation grid.
    """

    new_grid = current_grid.copy()

    for x in range(grid_size):
        for y in range(grid_size):

            if current_grid[x, y] == infected_state:

                for dx in range(-2, 3):
                    for dy in range(-2, 3):

                        new_x = x + dx
                        new_y = y + dy

                        is_inside_grid = (
                            0 <= new_x < grid_size
                            and
                            0 <= new_y < grid_size
                        )

                        if not is_inside_grid:
                            continue

                        if current_grid[new_x, new_y] == healthy_state:

                            distance = np.sqrt(dx**2 + dy**2)

                            if distance == 0:
                                continue

                            probability = (
                                infection_probability / distance
                            )

                            if np.random.random() < probability:
                                new_grid[new_x, new_y] = infected_state

                if np.random.random() < recovery_probability:
                    new_grid[x, y] = recovered_state

                elif np.random.random() < death_probability:
                    new_grid[x, y] = dead_state

    return new_grid