"""
File: config.py

This module contains constants, simulation parameters,
cell states, and virus presets for the epidemic simulation.
"""

# =====================================================
# CELL STATES
# =====================================================

EMPTY = 0
HEALTHY = 1
INFECTED = 2
RECOVERED = 3
DEAD = 4

# =====================================================
# GRID SETTINGS
# =====================================================

GRID_SIZE = 120

# =====================================================
# SIMULATION PARAMETERS
# =====================================================

MOVEMENT_PROBABILITY = 0.2
POPULATION_DENSITY = 0.75
INITIAL_INFECTED = 1

# =====================================================
# SIMULATION FLAGS
# =====================================================

PAUSED = False
SIMULATION_FINISHED = False
MANUAL_INFECTION_MODE = False
ENABLE_DRAGGING = False

# =====================================================
# VIRUS PRESETS
# =====================================================

VIRUSES = {
    "COVID-19": {
        "infection": 0.18,
        "recovery": 0.010,
        "death": 0.0015,
    },

    "Flu": {
        "infection": 0.08,
        "recovery": 0.025,
        "death": 0.0002,
    },

    "Measles": {
        "infection": 0.55,
        "recovery": 0.008,
        "death": 0.002,
    }
}

# =====================================================
# DEFAULT VIRUS
# =====================================================

CURRENT_VIRUS = "COVID-19"

# =====================================================
# VISUAL SETTINGS
# =====================================================

COLORS = [
    "lightgray",
    "green",
    "red",
    "blue",
    "black"
]