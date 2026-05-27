"""
File: movement.py

This module contains functions responsible
for population movement inside the simulation.
"""

import numpy as np


def move_people(
    current_grid,
    grid_size,
    movement_probability,
    empty_state,
    movable_states
):
    """
    Move people randomly across the simulation grid.

    Args:
        current_grid (np.ndarray):
            Current simulation grid.

        grid_size (int):
            Size of simulation grid.

        movement_probability (float):
            Probability of movement for each cell.

        empty_state (int):
            Integer value representing empty cell.

        movable_states (list[int]):
            States that are allowed to move.

    Returns:
        np.ndarray:
            Updated simulation grid.
    """

    new_grid = current_grid.copy()

    for x in range(grid_size):
        for y in range(grid_size):

            state = current_grid[x, y]

            if state in movable_states:

                if np.random.random() < movement_probability:

                    dx = np.random.randint(-1, 2)
                    dy = np.random.randint(-1, 2)

                    new_x = x + dx
                    new_y = y + dy

                    is_inside_grid = (
                        0 <= new_x < grid_size
                        and
                        0 <= new_y < grid_size
                    )

                    if (
                        is_inside_grid
                        and
                        new_grid[new_x, new_y] == empty_state
                    ):
                        new_grid[new_x, new_y] = state
                        new_grid[x, y] = empty_state

    return new_grid