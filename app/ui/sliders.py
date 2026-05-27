"""
File: sliders.py

This module contains functions responsible
for creating simulation sliders.
"""

from matplotlib.widgets import Slider

from app.ui.layout import (
    INFECTED_SLIDER_POSITION,
    INFECTION_SLIDER_POSITION,
    RECOVERY_SLIDER_POSITION,
    DEATH_SLIDER_POSITION,
    SPEED_SLIDER_POSITION,
    DENSITY_SLIDER_POSITION,
)


def create_sliders(
    figure,
    slider_grid,
    virus_data,
    population_density,
    initial_infected
):
    """
    Create all simulation sliders.

    Args:
        figure:
            Matplotlib figure object.

        slider_grid:
            GridSpec object for sliders.

        virus_data (dict):
            Current virus parameters.

        population_density (float):
            Initial population density.

        initial_infected (int):
            Initial infected count.

    Returns:
        dict:
            Dictionary containing sliders and axes.
    """

    ax_infection = figure.add_subplot(
        slider_grid[0, 0]
    )

    ax_recovery = figure.add_subplot(
        slider_grid[0, 1]
    )

    ax_death = figure.add_subplot(
        slider_grid[0, 2]
    )

    ax_speed = figure.add_subplot(
        slider_grid[1, 0]
    )

    ax_density = figure.add_subplot(
        slider_grid[1, 1]
    )

    ax_infected = figure.add_subplot(
        slider_grid[1, 2]
    )

    ax_recovery.set_position(RECOVERY_SLIDER_POSITION)
    ax_infection.set_position(INFECTION_SLIDER_POSITION)
    ax_infected.set_position(INFECTED_SLIDER_POSITION)
    ax_density.set_position(DENSITY_SLIDER_POSITION)
    ax_speed.set_position(SPEED_SLIDER_POSITION)
    ax_death.set_position(DEATH_SLIDER_POSITION)

    slider_infection = Slider(
        ax_infection,
        "Infection",
        0.0,
        1.0,
        valinit=virus_data["infection"]
    )

    slider_recovery = Slider(
        ax_recovery,
        "Recovery",
        0.0,
        0.2,
        valinit=virus_data["recovery"]
    )

    slider_death = Slider(
        ax_death,
        "Death",
        0.0,
        0.1,
        valinit=virus_data["death"]
    )

    slider_speed = Slider(
        ax_speed,
        "Speed",
        1,
        200,
        valinit=50
    )

    slider_density = Slider(
        ax_density,
        "Density",
        0.1,
        1.0,
        valinit=population_density
    )

    slider_infected = Slider(
        ax_infected,
        "Init Infected",
        1,
        200,
        valinit=initial_infected,
        valstep=1
    )

    return {
        "axes": {
            "infection": ax_infection,
            "recovery": ax_recovery,
            "death": ax_death,
            "speed": ax_speed,
            "density": ax_density,
            "infected": ax_infected,
        },

        "sliders": {
            "infection": slider_infection,
            "recovery": slider_recovery,
            "death": slider_death,
            "speed": slider_speed,
            "density": slider_density,
            "infected": slider_infected,
        }
    }