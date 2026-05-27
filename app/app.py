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

from app.ui.buttons import create_buttons

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
# EVENTS
# =====================================================

from app.events.buttons_events import (
    toggle_pause,
    toggle_infection_mode,
    restart,
    reset_defaults,
)

from app.events.mouse_events import (
    on_click,
)

from app.events.drag_events import (
    on_press,
    on_motion,
    on_release,
)

# =====================================================
# CREATE BUTTONS
# =====================================================

button_objects = create_buttons(
    grid_spec=gs,
    figure=fig,
)

buttons = button_objects["buttons"]

button_reset = buttons["reset"]
button_pause = buttons["pause"]
button_defaults = buttons["defaults"]
button_infect = buttons["infect"]

# =====================================================
# STATE
# =====================================================

state = {
    # =================================================
    # CONFIG
    # =================================================

    "GRID_SIZE": GRID_SIZE,

    "EMPTY": EMPTY,
    "HEALTHY": HEALTHY,
    "INFECTED": INFECTED,
    "RECOVERED": RECOVERED,
    "DEAD": DEAD,

    "VIRUSES": VIRUSES,

    # =================================================
    # WINDOW
    # =================================================

    "fig": fig,

    "ax_map": ax1,

    "img": img,

    # =================================================
    # BUTTONS
    # =================================================

    "button_pause": button_pause,
    "button_infect": button_infect,

    # =================================================
    # SLIDERS
    # =================================================

    "slider_infection": slider_infection,
    "slider_recovery": slider_recovery,
    "slider_death": slider_death,
    "slider_speed": slider_speed,
    "slider_density": slider_density,
    "slider_infected": slider_infected,

    # =================================================
    # SIMULATION
    # =================================================

    "grid": grid,

    "paused": paused,

    "simulation_finished": simulation_finished,

    "manual_infection_mode":
        manual_infection_mode,

    "population_density":
        POPULATION_DENSITY,

    "current_virus": current_virus,

    # =================================================
    # HISTORY
    # =================================================

    "healthy_history": healthy_history,
    "infected_history": infected_history,
    "recovered_history": recovered_history,
    "dead_history": dead_history,

    # =================================================
    # STATISTICS
    # =================================================

    "stats_text": stats_text,

    "end_text": end_text,
}

# =====================================================
# BUTTON EVENTS
# =====================================================

button_pause.on_clicked(
    lambda event: toggle_pause(
        event,
        state,
    )
)

button_infect.on_clicked(
    lambda event: toggle_infection_mode(
        event,
        state,
    )
)

button_reset.on_clicked(
    lambda event: restart(
        event,
        state,
    )
)

button_defaults.on_clicked(
    lambda event: reset_defaults(
        event,
        state,
    )
)

# =====================================================
# MOUSE EVENTS
# =====================================================

fig.canvas.mpl_connect(
    "button_press_event",

    lambda event: on_click(
        event,
        state,
    )
)

# =====================================================
# DRAG DATA
# =====================================================

drag_data = {
    "ax": None,
    "x": 0,
    "y": 0,
}

state["drag_data"] = drag_data

# =====================================================
# DRAGGABLE AXES
# =====================================================

draggable_axes = [
    ax1,
    ax2,
    stats_ax,
    radio_ax,

    slider_objects["axes"]["infection"],
    slider_objects["axes"]["recovery"],
    slider_objects["axes"]["death"],
    slider_objects["axes"]["speed"],
    slider_objects["axes"]["density"],
    slider_objects["axes"]["infected"],

    button_objects["axes"]["reset"],
    button_objects["axes"]["pause"],
    button_objects["axes"]["defaults"],
    button_objects["axes"]["infect"],
]

state["draggable_axes"] = draggable_axes

# =====================================================
# DRAG EVENTS
# =====================================================

fig.canvas.mpl_connect(
    "button_press_event",

    lambda event: on_press(
        event,
        state,
    )
)

fig.canvas.mpl_connect(
    "motion_notify_event",

    lambda event: on_motion(
        event,
        state,
    )
)

fig.canvas.mpl_connect(
    "button_release_event",

    lambda event: on_release(
        event,
        state,
    )
)



plt.show()