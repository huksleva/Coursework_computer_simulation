"""
Файл buttons_events.py

Содержит обработчики кнопок интерфейса:
- пауза
- перезапуск
- сброс параметров
- режим ручного заражения
"""

from app.simulation.create_grid import create_grid


def toggle_pause(_, state):
    """
    Переключает паузу симуляции.
    """

    state["paused"] = not state["paused"]

    if state["paused"]:
        state["button_pause"].label.set_text("Resume")
        state["animation"].event_source.stop()

    else:
        state["button_pause"].label.set_text("Pause")
        state["animation"].event_source.start()


def toggle_infection_mode(_, state):
    """
    Включает или выключает режим
    ручного заражения клеток.
    """

    state["manual_infection_mode"] = (
        not state["manual_infection_mode"]
    )

    if state["manual_infection_mode"]:
        state["button_infect"].label.set_text("Click Map")

    else:
        state["button_infect"].label.set_text("Add Infection")


def reset_defaults(_, state):
    """
    Сбрасывает параметры симуляции
    к значениям вируса по умолчанию.
    """

    current_virus = state["current_virus"]

    virus = state["VIRUSES"][current_virus]

    state["slider_infection"].reset()
    state["slider_recovery"].reset()
    state["slider_death"].reset()
    state["slider_speed"].reset()
    state["slider_density"].reset()

    state["slider_infection"].set_val(
        virus["infection"]
    )

    state["slider_recovery"].set_val(
        virus["recovery"]
    )

    state["slider_death"].set_val(
        virus["death"]
    )


def restart(_, state):
    """
    Полностью перезапускает симуляцию.
    """

    state["population_density"] = (
        state["slider_density"].val
    )

    state["grid"] = create_grid(
        grid_size=state["GRID_SIZE"],
        population_density=state["population_density"],
        initial_infected=int(
            state["slider_infected"].val
        ),
        healthy_state=state["HEALTHY"],
        infected_state=state["INFECTED"],
    )

    state["healthy_history"].clear()
    state["infected_history"].clear()
    state["recovered_history"].clear()
    state["dead_history"].clear()

    # =====================================================
    # CLEAR GRAPH
    # =====================================================

    state["healthy_line"].set_data([], [])
    state["infected_line"].set_data([], [])
    state["recovered_line"].set_data([], [])
    state["dead_line"].set_data([], [])

    state["simulation_finished"] = False

    state["end_text"].set_text("")
    state["stats_text"].set_text("")

    state["img"].set_array(state["grid"])

    state["fig"].canvas.draw_idle()

    if state["paused"]:
        state["button_pause"].label.set_text(
            "Resume"
        )

    else:
        state["button_pause"].label.set_text(
            "Pause"
        )