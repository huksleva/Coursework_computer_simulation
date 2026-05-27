"""
File: window.py

This module contains functions responsible
for creating the main application window.
"""

import matplotlib.pyplot as plt

from matplotlib.colors import ListedColormap
from matplotlib.gridspec import GridSpec


def create_window(
    grid,
    colors
):
    """
    Create main simulation window.

    Args:
        grid:
            Initial simulation grid.

        colors (list):
            List of colors for grid states.

    Returns:
        dict:
            Window objects and axes.
    """

    figure = plt.figure(
        figsize=(16, 9)
    )

    manager = plt.get_current_fig_manager()

    manager.window.wm_geometry("+0+0")

    grid_spec = GridSpec(
        8,
        12,
        figure=figure
    )

    grid_spec.update(
        wspace=0.6,
        hspace=1.2
    )

    simulation_ax = figure.add_subplot(
        grid_spec[0:6, 0:6]
    )

    simulation_ax.set_position(
        (0.014, 0.361, 0.314, 0.600)
    )

    graph_ax = figure.add_subplot(
        grid_spec[0:6, 4:10]
    )

    graph_ax.set_position(
        (0.416, 0.364, 0.350, 0.600)
    )

    color_map = ListedColormap(colors)

    image = simulation_ax.imshow(
        grid,
        cmap=color_map,
        vmin=0,
        vmax=4,
        interpolation="nearest"
    )

    simulation_ax.set_title(
        "Epidemic Simulation"
    )

    simulation_ax.set_xticks([])
    simulation_ax.set_yticks([])

    return {
        "figure": figure,
        "grid_spec": grid_spec,
        "simulation_ax": simulation_ax,
        "graph_ax": graph_ax,
        "image": image,
        "color_map": color_map,
    }