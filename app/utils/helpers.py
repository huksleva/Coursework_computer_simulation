"""
File: helpers.py

Utility helper functions used
across the epidemic simulation project.
"""


def clear_history(*history_lists):
    """
    Clear simulation history lists.

    Args:
        *history_lists:
            Any number of history lists.
    """

    for history in history_lists:
        history.clear()


def reset_statistics_texts(
    stats_text,
    end_text
):
    """
    Reset statistics texts.

    Args:
        stats_text:
            Statistics text object.

        end_text:
            End simulation text object.
    """

    stats_text.set_text("")
    end_text.set_text("")


def update_simulation_image(
    image,
    grid,
    figure
):
    """
    Update simulation image
    and redraw canvas.

    Args:
        image:
            Matplotlib image object.

        grid:
            Current simulation grid.

        figure:
            Matplotlib figure object.
    """

    image.set_array(grid)

    figure.canvas.draw_idle()


def is_inside_grid(
    x,
    y,
    grid_size
):
    """
    Check whether coordinates
    are inside the grid.

    Args:
        x (int):
            X coordinate.

        y (int):
            Y coordinate.

        grid_size (int):
            Simulation grid size.

    Returns:
        bool:
            True if coordinates are valid.
    """

    return (
        0 <= x < grid_size
        and
        0 <= y < grid_size
    )