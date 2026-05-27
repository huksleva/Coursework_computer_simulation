"""
File: app.py

Main entry point of the epidemic simulation project.
This file creates the interface, connects all modules,
and starts the animation loop.
"""

# =====================================================
# IMPORTS
# =====================================================

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import (
    GridSpecFromSubplotSpec
)

# =====================================================
# CONFIG
# =====================================================

from app.config import (
    EMPTY,
    HEALTHY,
    INFECTED,
    RECOVERED,
    DEAD,
    GRID_SIZE,
    MOVEMENT_PROBABILITY,
    POPULATION_DENSITY,
    INITIAL_INFECTED,
    VIRUSES,
    CURRENT_VIRUS,
    COLORS,
)

# =====================================================
# SIMULATION
# =====================================================

from app.simulation.create_grid import create_grid

from app.simulation.movement import move_people

from app.simulation.infection import spread_infection

# =====================================================
# UI
# =====================================================

from app.ui.window import create_window

from app.ui.sliders import create_sliders

from app.ui.buttons import (
    toggle_pause,
    toggle_infection_mode,
)

from app.ui.radio_buttons import (
    create_radio_buttons,
    change_virus,
)

from app.ui.statistics import (
    create_statistics_panel,
    calculate_statistics,
    update_statistics_text,
)

# =====================================================
# HELPERS
# =====================================================

from app.utils.helpers import (
    clear_history,
    reset_statistics_texts,
    update_simulation_image,
)

# =====================================================
# GLOBAL VARIABLES
# =====================================================

paused = False
simulation_finished = False
manual_infection_mode = False

current_virus = CURRENT_VIRUS

# =====================================================
# CREATE GRID
# =====================================================

grid = create_grid(
    grid_size=GRID_SIZE,
    population_density=POPULATION_DENSITY,
    initial_infected=INITIAL_INFECTED,
    healthy_state=HEALTHY,
    infected_state=INFECTED,
)

# =====================================================
# CREATE WINDOW
# =====================================================

window = create_window(
    grid=grid,
    colors=COLORS,
)

fig = window["figure"]

gs = window["grid_spec"]

ax1 = window["simulation_ax"]

ax2 = window["graph_ax"]

img = window["image"]

# =====================================================
# CREATE STATISTICS PANEL
# =====================================================

stats_ax, stats_text, end_text = (
    create_statistics_panel(
        figure=fig,
        grid_spec=gs,
    )
)

# =====================================================
# CREATE SLIDERS
# =====================================================

slider_spec = gs[6:8, 0:10]

slider_grid = GridSpecFromSubplotSpec(
    2,
    3,
    subplot_spec=slider_spec,
    wspace=0.5,
    hspace=1.0,
)

virus_data = VIRUSES[current_virus]

slider_objects = create_sliders(
    figure=fig,
    slider_grid=slider_grid,
    virus_data=virus_data,
    population_density=POPULATION_DENSITY,
    initial_infected=INITIAL_INFECTED,
)

sliders = slider_objects["sliders"]

slider_infection = sliders["infection"]
slider_recovery = sliders["recovery"]
slider_death = sliders["death"]
slider_speed = sliders["speed"]
slider_density = sliders["density"]
slider_infected = sliders["infected"]

# =====================================================
# HISTORY
# =====================================================

healthy_history = []
infected_history = []
recovered_history = []
dead_history = []

# =====================================================
# GRAPH
# =====================================================

healthy_line, = ax2.plot(
    [],
    [],
    label="Healthy",
    color="green"
)

infected_line, = ax2.plot(
    [],
    [],
    label="Infected",
    color="red"
)

recovered_line, = ax2.plot(
    [],
    [],
    label="Recovered",
    color="blue"
)

dead_line, = ax2.plot(
    [],
    [],
    label="Dead",
    color="black"
)

ax2.set_title("Statistics")

ax2.set_xlabel("Step")

ax2.set_ylabel("Population")

ax2.legend()

# =====================================================
# RADIO BUTTONS
# =====================================================

radio_ax, radio = create_radio_buttons()

# =====================================================
# BUTTONS
# =====================================================

# Кнопки пока оставь как у себя.
# Мы вынесем их позже.