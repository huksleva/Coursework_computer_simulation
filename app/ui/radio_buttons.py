"""
File: radio_buttons.py

This module contains functions responsible
for virus selection radio buttons.
"""

from matplotlib.widgets import RadioButtons


def create_radio_buttons():
    """
    Create virus selection radio buttons.

    Returns:
        tuple:
            Radio axis and RadioButtons object.
    """

    import matplotlib.pyplot as plt

    radio_ax = plt.axes(
        (0.83, 0.11, 0.14, 0.14)
    )

    radio = RadioButtons(
        radio_ax,
        (
            "COVID-19",
            "Flu",
            "Measles",
            "Custom"
        )
    )

    return radio_ax, radio


def change_virus(
    label,
    viruses,
    slider_infection,
    slider_recovery,
    slider_death
):
    """
    Change current virus parameters.

    Args:
        label (str):
            Selected virus name.

        viruses (dict):
            Dictionary with virus presets.

        slider_infection:
            Infection slider.

        slider_recovery:
            Recovery slider.

        slider_death:
            Death slider.

    Returns:
        str:
            Selected virus name.
    """

    virus = viruses[label]

    slider_infection.set_val(
        virus["infection"]
    )

    slider_recovery.set_val(
        virus["recovery"]
    )

    slider_death.set_val(
        virus["death"]
    )

    return label