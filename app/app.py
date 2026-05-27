import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.colors import ListedColormap
from matplotlib.backend_bases import Event
from matplotlib.gridspec import (
    GridSpec,
    GridSpecFromSubplotSpec
)
from app.templates.createGrid import create_grid
from app.templates.buttons_func import (
    toggle_pause,
    toggle_infection_mode
)




# =====================================================
# СОСТОЯНИЯ
# =====================================================

EMPTY = 0
HEALTHY = 1
INFECTED = 2
RECOVERED = 3
DEAD = 4

GRID_SIZE = 120

# =====================================================
# ВИРУСЫ
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
    },
    "Custom": {
        "infection": 0.35,
        "recovery": 0.02,
        "death": 0.005,
    }
}

current_virus = "COVID-19"

# =====================================================
# ПАРАМЕТРЫ
# =====================================================

movement_probability = 0.2
population_density = 0.75
initial_infected = 10

paused = False
simulation_finished = False

manual_infection_mode = False

# =====================================================
# СОЗДАНИЕ СЕТКИ
# =====================================================

grid = create_grid()

# =====================================================
# ИСТОРИЯ
# =====================================================

healthy_history = []
infected_history = []
recovered_history = []
dead_history = []

# =====================================================
# ОКНО
# =====================================================

fig = plt.figure(figsize=(16, 9))
manager = plt.get_current_fig_manager()
manager.window.wm_geometry("+0+0")
gs = GridSpec(
    8,
    12,
    figure=fig
)
gs.update(
    wspace=0.6,
    hspace=1.2
)

ax1 = fig.add_subplot(gs[0:6, 0:6])
ax1.set_position((0, 0.29, 0.38, 0.60))
ax2 = fig.add_subplot(gs[0:6, 4:10])
ax2.set_position((0.48, 0.25, 0.35, 0.60))

colors = [
    "lightgray",
    "green",
    "red",
    "blue",
    "black"
]

cmap = ListedColormap(colors)

img = ax1.imshow(
    grid,
    cmap=cmap,
    vmin=0,
    vmax=4,
    interpolation="nearest"
)

ax1.set_title("Epidemic Simulation")
ax1.set_xticks([])
ax1.set_yticks([])

# =====================================================
# ПАНЕЛЬ СТАТИСТИКИ
# =====================================================

stats_ax = fig.add_subplot(gs[0:2, 10:12])

stats_ax.set_facecolor("#f0f0f0")

stats_ax.set_xticks([])
stats_ax.set_yticks([])

stats_ax.set_title("Statistics")

stats_text = stats_ax.text(
    0.05,
    0.95,
    "",
    transform=stats_ax.transAxes,
    fontsize=10,
    verticalalignment="top"
)

end_text = fig.text(
    0.5,
    0.95,
    "",
    ha="center",
    fontsize=18,
    color="darkred",
    weight="bold"
)

# =====================================================
# ПОЛЗУНКИ
# =====================================================

# Слайдеры
slider_spec = gs[6:8, 0:10]

slider_grid = GridSpecFromSubplotSpec(
    2,
    3,
    subplot_spec=slider_spec,
    wspace=0.5,
    hspace=1.0
)

ax_infection = fig.add_subplot(slider_grid[0, 0])
ax_recovery = fig.add_subplot(slider_grid[0, 1])
ax_death = fig.add_subplot(slider_grid[0, 2])
ax_speed = fig.add_subplot(slider_grid[1, 0])
ax_density = fig.add_subplot(slider_grid[1, 1])
ax_infected = fig.add_subplot(slider_grid[1, 2])
virus_data = VIRUSES[current_virus]

slider_infected = Slider(
    ax_infected,
    "Init Infected",
    1,
    200,
    valinit=10,
    valstep=1
)

slider_infection = Slider(
    ax_infection,
    "Infection",
    0.0,
    1.0,
    valinit=virus_data["infection"]
)

slider_recovery = Slider(
    ax_recovery,
    "Recovery",
    0.0,
    0.2,
    valinit=virus_data["recovery"]
)

slider_death = Slider(
    ax_death,
    "Death",
    0.0,
    0.1,
    valinit=virus_data["death"]
)

slider_speed = Slider(
    ax_speed,
    "Speed",
    1,
    200,
    valinit=50
)

slider_density = Slider(
    ax_density,
    "Density",
    0.1,
    1.0,
    valinit=population_density
)

# =====================================================
# КНОПКИ
# =====================================================

reset_ax = fig.add_subplot(gs[2, 10:12])
pause_ax = fig.add_subplot(gs[3, 10:12])
defaults_ax = fig.add_subplot(gs[4, 10:12])
infect_ax = fig.add_subplot(gs[5, 10:12])

for ax in [reset_ax, pause_ax, defaults_ax, infect_ax]:
    ax.set_xticks([])
    ax.set_yticks([])

button_reset = Button(reset_ax, "Restart")
button_pause = Button(pause_ax, "Pause")
button_defaults = Button(defaults_ax, "Defaults")
button_infect = Button(infect_ax, "Add Infection")
button_infect.on_clicked(toggle_infection_mode(manual_infection_mode))

# =====================================================
# ВЫБОР ВИРУСА
# =====================================================

radio_ax = plt.axes((0.83, 0.11, 0.14, 0.14))

radio = RadioButtons(
    radio_ax,
    ("COVID-19", "Flu", "Measles", "Custom")
)

# =====================================================
# ПЕРЕКЛЮЧЕНИЕ ВИРУСА
# =====================================================

def change_virus(label):

    global current_virus

    current_virus = label

    virus = VIRUSES[label]

    slider_infection.set_val(virus["infection"])
    slider_recovery.set_val(virus["recovery"])
    slider_death.set_val(virus["death"])


radio.on_clicked(change_virus)

# =====================================================
# ПАУЗА
# =====================================================

button_pause.on_clicked(toggle_pause(paused))

# =====================================================
# СБРОС ПАРАМЕТРОВ
# =====================================================

def reset_defaults(_):

    virus = VIRUSES[current_virus]

    slider_infection.reset()
    slider_recovery.reset()
    slider_death.reset()
    slider_speed.reset()
    slider_density.reset()

    slider_infection.set_val(virus["infection"])
    slider_recovery.set_val(virus["recovery"])
    slider_death.set_val(virus["death"])


button_defaults.on_clicked(reset_defaults)

# =====================================================
# ПЕРЕЗАПУСК
# =====================================================

def restart(_):

    global grid
    global healthy_history
    global infected_history
    global recovered_history
    global dead_history
    global population_density
    global simulation_finished

    population_density = slider_density.val
    grid = create_grid()

    healthy_history = []
    infected_history = []
    recovered_history = []
    dead_history = []

    simulation_finished = False
    end_text.set_text("")
    stats_text.set_text("")

    img.set_array(grid)

    # 🔥 важно: принудительно обновить экран
    fig.canvas.draw_idle()

    if paused:
        button_pause.label.set_text("Resume")
    else:
        button_pause.label.set_text("Pause")


button_reset.on_clicked(restart)

# =====================================================
# ДВИЖЕНИЕ
# =====================================================

def move_people(current_grid):

    new_grid = current_grid.copy()

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):

            state = current_grid[x, y]

            if state in [HEALTHY, INFECTED, RECOVERED]:
                if np.random.random() < movement_probability:
                    dx = np.random.randint(-1, 2)
                    dy = np.random.randint(-1, 2)

                    nx = x + dx
                    ny = y + dy

                    if (
                        0 <= nx < GRID_SIZE and
                        0 <= ny < GRID_SIZE and
                        new_grid[nx, ny] == EMPTY
                    ):
                        new_grid[nx, ny] = state
                        new_grid[x, y] = EMPTY

    return new_grid

# =====================================================
# ЗАРАЖЕНИЕ
# =====================================================

def spread_infection(current_grid):

    new_grid = current_grid.copy()

    infection_prob = slider_infection.val
    recovery_prob = slider_recovery.val
    death_prob = slider_death.val

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):

            if current_grid[x, y] == INFECTED:

                for dx in range(-2, 3):
                    for dy in range(-2, 3):

                        nx = x + dx
                        ny = y + dy

                        if (
                            0 <= nx < GRID_SIZE and
                            0 <= ny < GRID_SIZE
                        ):

                            if current_grid[nx, ny] == HEALTHY:

                                distance = np.sqrt(dx**2 + dy**2)

                                if distance == 0:
                                    continue

                                probability = infection_prob / distance

                                if np.random.random() < probability:
                                    new_grid[nx, ny] = INFECTED

                if np.random.random() < recovery_prob:
                    new_grid[x, y] = RECOVERED

                elif np.random.random() < death_prob:
                    new_grid[x, y] = DEAD

    return new_grid

# =====================================================
# ОБНОВЛЕНИЕ
# =====================================================

healthy_line, = ax2.plot([], [], label="Healthy", color="green")
infected_line, = ax2.plot([], [], label="Infected", color="red")
recovered_line, = ax2.plot([], [], label="Recovered", color="blue")
dead_line, = ax2.plot([], [], label="Dead", color="black")

ax2.set_title("Statistics")
ax2.set_xlabel("Step")
ax2.set_ylabel("Population")
ax2.legend()

frame_counter = 0

def update(_):

    global frame_counter
    global grid
    global paused
    global simulation_finished

    # =====================================================
    # ПАУЗА
    # =====================================================

    if paused:
        return [
            img,
            healthy_line,
            infected_line,
            recovered_line,
            dead_line,
            stats_text
        ]

    frame_counter += 1

    # =====================================================
    # ОБНОВЛЕНИЕ СИМУЛЯЦИИ
    # =====================================================

    grid = move_people(grid)
    grid = spread_infection(grid)

    # =====================================================
    # ПОДСЧЁТ СОСТОЯНИЙ
    # =====================================================

    healthy = np.sum(grid == HEALTHY)
    infected = np.sum(grid == INFECTED)
    recovered = np.sum(grid == RECOVERED)
    dead = np.sum(grid == DEAD)

    total_population = (
        healthy +
        infected +
        recovered +
        dead
    )

    # =====================================================
    # ЗАВЕРШЕНИЕ ЭПИДЕМИИ
    # =====================================================

    if infected == 0 and not simulation_finished:

        simulation_finished = True
        paused = True

        button_pause.label.set_text("Resume")

        end_text.set_text("Epidemic ended")

    # =====================================================
    # ОБНОВЛЕНИЕ ТЕКСТОВОЙ СТАТИСТИКИ
    # =====================================================

    stats_text.set_text(
        f"Population: {total_population}\n"
        f"Healthy: {healthy}\n"
        f"Infected: {infected}\n"
        f"Recovered: {recovered}\n"
        f"Dead: {dead}"
    )

    # =====================================================
    # СОХРАНЕНИЕ ИСТОРИИ
    # =====================================================

    if frame_counter % 2 == 0:

        healthy_history.append(healthy)
        infected_history.append(infected)
        recovered_history.append(recovered)
        dead_history.append(dead)

    # =====================================================
    # ОБНОВЛЕНИЕ КАРТЫ
    # =====================================================

    img.set_array(grid)

    # =====================================================
    # ОБНОВЛЕНИЕ ГРАФИКА
    # =====================================================

    if frame_counter % 5 == 0:

        healthy_line.set_data(
            range(len(healthy_history)),
            healthy_history
        )

        infected_line.set_data(
            range(len(infected_history)),
            infected_history
        )

        recovered_line.set_data(
            range(len(recovered_history)),
            recovered_history
        )

        dead_line.set_data(
            range(len(dead_history)),
            dead_history
        )

        ax2.set_xlim(
            max(0, len(healthy_history) - 500),
            len(healthy_history) + 10
        )

        ax2.set_ylim(
            0,
            GRID_SIZE * GRID_SIZE
        )

    # =====================================================
    # СКОРОСТЬ АНИМАЦИИ
    # =====================================================

    animation.event_source.interval = (
        201 - slider_speed.val
    )

    # =====================================================
    # ВОЗВРАТ ОБЪЕКТОВ
    # =====================================================

    return [
        img,
        healthy_line,
        infected_line,
        recovered_line,
        dead_line,
        stats_text
    ]

# =====================================================
# АНИМАЦИЯ
# =====================================================

def on_click(event: Event) -> None:

    global grid

    if not manual_infection_mode:
        return
    if event.inaxes != ax1:
        return
    if event.xdata is None or event.ydata is None:
        return

    x = int(event.ydata)
    y = int(event.xdata)

    if 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE:
        grid[x, y] = INFECTED
        img.set_array(grid)
        fig.canvas.draw_idle()


fig.canvas.mpl_connect(
    "button_press_event",
    on_click
)

animation = FuncAnimation(
    fig,
    update,
    interval=100,
    cache_frame_data=False
)

# =====================================================
# ЗАПУСК
# =====================================================

drag_data = {
    "ax": None,
    "x": 0,
    "y": 0
}

draggable_axes = [
    ax1,
    ax2,
    stats_ax,
    radio_ax,
    ax_infection,
    ax_infected,
    ax_recovery,
    ax_death,
    ax_speed,
    ax_density,
    reset_ax,
    pause_ax,
    defaults_ax,
    infect_ax
]


def on_press(event):

    if event.inaxes is None:
        return

    if event.button != 1:
        return

    for ax in draggable_axes:

        if ax == event.inaxes:

            drag_data["ax"] = ax
            drag_data["x"] = event.x
            drag_data["y"] = event.y

            break


def on_motion(event):

    ax = drag_data["ax"]

    if ax is None:
        return

    dx = (event.x - drag_data["x"]) / fig.bbox.width
    dy = (event.y - drag_data["y"]) / fig.bbox.height

    pos = ax.get_position()

    ax.set_position([
        pos.x0 + dx,
        pos.y0 + dy,
        pos.width,
        pos.height
    ])

    drag_data["x"] = event.x
    drag_data["y"] = event.y

    fig.canvas.draw_idle()


def on_release(event):

    ax = drag_data["ax"]

    if ax is not None:

        pos = ax.get_position()

        print(
            f"{ax.get_label()}:\n"
            f"[{pos.x0:.3f}, "
            f"{pos.y0:.3f}, "
            f"{pos.width:.3f}, "
            f"{pos.height:.3f}]"
        )

    drag_data["ax"] = None


fig.canvas.mpl_connect(
    "button_press_event",
    on_press
)

fig.canvas.mpl_connect(
    "motion_notify_event",
    on_motion
)

fig.canvas.mpl_connect(
    "button_release_event",
    on_release
)



plt.show()