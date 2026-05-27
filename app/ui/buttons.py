"""
File: buttons.py

This module contains button callback functions
for simulation controls.
"""


def toggle_pause(
    paused,
    button_pause,
    animation
):
    """
    Toggle simulation pause state.

    Args:
        paused (bool):
            Current pause state.

        button_pause:
            Matplotlib pause button.

        animation:
            FuncAnimation object.

    Returns:
        bool:
            Updated pause state.
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
    Toggle manual infection mode.

    Args:
        manual_infection_mode (bool):
            Current infection mode state.

        button_infect:
            Matplotlib infection button.

    Returns:
        bool:
            Updated infection mode state.
    """

    manual_infection_mode = (
        not manual_infection_mode
    )

    if manual_infection_mode:
        button_infect.label.set_text("Click Map")

    else:
        button_infect.label.set_text("Add Infection")

    return manual_infection_mode