"""
Файл mouse_events.py

Содержит обработчики кликов мыши.
"""

from matplotlib.backend_bases import Event


def on_click(event: Event, state):
    """
    Обрабатывает клик по карте
    и добавляет заражённую клетку.
    """

    if not state["manual_infection_mode"]:
        return

    if event.inaxes != state["ax_map"]:
        return

    if event.xdata is None or event.ydata is None:
        return

    x = int(event.ydata)
    y = int(event.xdata)

    grid_size = state["GRID_SIZE"]

    if 0 <= x < grid_size and 0 <= y < grid_size:

        state["grid"][x, y] = state["INFECTED"]

        state["img"].set_array(state["grid"])

        state["fig"].canvas.draw_idle()