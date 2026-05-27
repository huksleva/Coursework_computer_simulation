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
INITIAL_INFECTED = 10

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
        "infection": 0.45,
        "recovery": 0.015,
        "death": 0.003,
    },

    "Flu": {
        "infection": 0.25,
        "recovery": 0.04,
        "death": 0.0005,
    },

    "Measles": {
        "infection": 0.8,
        "recovery": 0.02,
        "death": 0.01,
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