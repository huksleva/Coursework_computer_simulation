"""
File: cli.py

Console entry point for the epidemic simulation.
Allows launching the app with a single command: `epidemic-simulation`.
"""

import runpy


def main():
    """
    Launch the simulation window.
    """

    runpy.run_module("app.app", run_name="__main__")


if __name__ == "__main__":
    main()
