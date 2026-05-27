"""
Файл drag_events.py

Содержит обработчики перетаскивания
элементов интерфейса.
"""


def on_press(event, state):
    """
    Начинает перетаскивание элемента.
    """

    if event.inaxes is None:
        return

    if event.button != 1:
        return

    for ax in state["draggable_axes"]:

        if ax == event.inaxes:

            state["drag_data"]["ax"] = ax

            state["drag_data"]["x"] = event.x
            state["drag_data"]["y"] = event.y

            break


def on_motion(event, state):
    """
    Перемещает элемент интерфейса.
    """

    ax = state["drag_data"]["ax"]

    if ax is None:
        return

    fig = state["fig"]

    dx = (
        event.x - state["drag_data"]["x"]
    ) / fig.bbox.width

    dy = (
        event.y - state["drag_data"]["y"]
    ) / fig.bbox.height

    position = ax.get_position()

    ax.set_position([
        position.x0 + dx,
        position.y0 + dy,
        position.width,
        position.height
    ])

    state["drag_data"]["x"] = event.x
    state["drag_data"]["y"] = event.y

    fig.canvas.draw_idle()


def on_release(event, state):
    """
    Завершает перетаскивание элемента.
    """

    ax = state["drag_data"]["ax"]

    if ax is not None:

        position = ax.get_position()

        print(
            f"{ax.get_label()}:\n"
            f"[{position.x0:.3f}, "
            f"{position.y0:.3f}, "
            f"{position.width:.3f}, "
            f"{position.height:.3f}]"
        )

    state["drag_data"]["ax"] = None