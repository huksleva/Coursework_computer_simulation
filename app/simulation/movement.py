"""
File: movement.py

Functions for moving people
inside the simulation grid.
"""

# =====================================================
# IMPORTS
# =====================================================

import numpy as np

# =====================================================
# MOVE PEOPLE
# =====================================================

def move_people(
    current_grid,
    grid_size,
    movement_probability,
    empty_state,
    movable_states,
):

    new_grid = current_grid.copy()

    for x in range(grid_size):
        for y in range(grid_size):
            state = current_grid[x, y]

            if state in movable_states:
                if np.random.random() < movement_probability:
                    dx = np.random.randint(-1, 2)
                    dy = np.random.randint(-1, 2)

                    nx = x + dx
                    ny = y + dy

                    if (0 <= nx < grid_size and
                            0 <= ny < grid_size and
                            new_grid[nx, ny] == empty_state):

                        new_grid[nx, ny] = state
                        new_grid[x, y] = empty_state

    return new_grid