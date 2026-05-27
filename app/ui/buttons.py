"""
File: buttons.py

This module creates all control buttons
for the epidemic simulation interface.
"""

# =====================================================
# IMPORTS
# =====================================================

from matplotlib.widgets import Button

# =====================================================
# BUTTONS
# =====================================================


def create_buttons(grid_spec, figure):
    """
    Create all interface buttons.

    Parameters:
        grid_spec:
            Main GridSpec object.

        figure:
            Main matplotlib figure.

    Returns:
        dict:
            Dictionary with axes and buttons.
    """

    # =================================================
    # BUTTON AXES
    # =================================================

    reset_ax = figure.add_subplot(grid_spec[2, 10:12])

    pause_ax = figure.add_subplot(grid_spec[3, 10:12])

    defaults_ax = figure.add_subplot(grid_spec[4, 10:12])

    infect_ax = figure.add_subplot(grid_spec[5, 10:12])

    # =================================================
    # REMOVE TICKS
    # =================================================

    for ax in [
        reset_ax,
        pause_ax,
        defaults_ax,
        infect_ax
    ]:
        ax.set_xticks([])
        ax.set_yticks([])

    # =================================================
    # CREATE BUTTONS
    # =================================================

    button_reset = Button(
        reset_ax,
        "Restart"
    )

    button_pause = Button(
        pause_ax,
        "Pause"
    )

    button_defaults = Button(
        defaults_ax,
        "Defaults"
    )

    button_infect = Button(
        infect_ax,
        "Add Infection"
    )

    # =================================================
    # RETURN
    # =================================================

    return {
        "axes": {
            "reset": reset_ax,
            "pause": pause_ax,
            "defaults": defaults_ax,
            "infect": infect_ax,
        },

        "buttons": {
            "reset": button_reset,
            "pause": button_pause,
            "defaults": button_defaults,
            "infect": button_infect,
        }
    }


# =====================================================
# BUTTON FUNCTIONS
# =====================================================


def toggle_pause(
    paused,
    button_pause,
    animation
):
    """
    Toggle simulation pause state.
    """

    paused = not paused

    if paused:

        button_pause.label.set_text("Resume")

        animation.event_source.stop()

    else:

        button_pause.label.set_text("Pause")

        animation.event_source.start()

    return paused


def toggle_infection_mode(
    manual_infection_mode,
    button_infect
):
    """
    Enable or disable manual infection mode.
    """

    manual_infection_mode = (
        not manual_infection_mode
    )

    if manual_infection_mode:

        button_infect.label.set_text(
            "Click Map"
        )

    else:

        button_infect.label.set_text(
            "Add Infection"
        )

    return manual_infection_mode