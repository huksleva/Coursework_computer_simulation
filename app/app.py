import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.colors import ListedColormap
from matplotlib.backend_bases import Event

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

movement_probability = 0.8
population_density = 0.75
initial_infected = 10

paused = False
simulation_finished = False

manual_infection_mode = False

# =====================================================
# СОЗДАНИЕ СЕТКИ
# =====================================================

def create_grid():

    current_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):

            if np.random.random() < population_density:
                current_grid[x, y] = HEALTHY

    healthy_positions = np.argwhere(current_grid == HEALTHY)

    infected_count = min(initial_infected, len(healthy_positions))

    selected = np.atleast_1d(
        np.random.choice(
            len(healthy_positions),
            infected_count,
            replace=False
        )
    )

    for index in selected:
        x, y = healthy_positions[index]

        current_grid[x, y] = INFECTED

    return current_grid


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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))

plt.subplots_adjust(left=0.08, bottom=0.38, right=0.82)

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

stats_ax = plt.axes((0.83, 0.72, 0.15, 0.18))

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

ax_infection = plt.axes((0.15, 0.28, 0.55, 0.03))
ax_recovery = plt.axes((0.15, 0.23, 0.55, 0.03))
ax_death = plt.axes((0.15, 0.18, 0.55, 0.03))
ax_speed = plt.axes((0.15, 0.13, 0.55, 0.03))
ax_density = plt.axes((0.15, 0.08, 0.55, 0.03))

virus_data = VIRUSES[current_virus]

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

reset_ax = plt.axes((0.75, 0.26, 0.12, 0.05))
pause_ax = plt.axes((0.75, 0.19, 0.12, 0.05))
defaults_ax = plt.axes((0.75, 0.12, 0.12, 0.05))
infect_ax = plt.axes((0.75, 0.05, 0.12, 0.05))

button_reset = Button(reset_ax, "Restart")
button_pause = Button(pause_ax, "Pause")
button_defaults = Button(defaults_ax, "Defaults")
button_infect = Button(infect_ax, "Add Infection")

def toggle_infection_mode(_):

    global manual_infection_mode

    manual_infection_mode = not manual_infection_mode

    if manual_infection_mode:
        button_infect.label.set_text("Click Map")
    else:
        button_infect.label.set_text("Add Infection")


button_infect.on_clicked(toggle_infection_mode)

# =====================================================
# ВЫБОР ВИРУСА
# =====================================================

radio_ax = plt.axes((0.83, 0.45, 0.14, 0.2))

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

def toggle_pause(_):

    global paused

    paused = not paused

    if paused:
        button_pause.label.set_text("Resume")
    else:
        button_pause.label.set_text("Pause")


button_pause.on_clicked(toggle_pause)

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

    img.set_array(grid)

    stats_text.set_text("")

    ax2.clear()

button_reset.on_clicked(restart)

# =====================================================
# ДВИЖЕНИЕ
# =====================================================

def move_people(current_grid):

    new_grid = current_grid.copy()

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):

            state = current_grid[x, y]

            if state in [HEALTHY, INFECTED]:

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

def update(_):

    global grid
    global paused
    global simulation_finished

    if paused:
        grid = move_people(grid)
        grid = spread_infection(grid)

    healthy = np.sum(grid == HEALTHY)
    infected = np.sum(grid == INFECTED)

    global simulation_finished
    global paused

    if infected == 0 and not simulation_finished:
        simulation_finished = True

        paused = True

        button_pause.label.set_text("Resume")

        end_text.set_text("Epidemic ended")

    recovered = np.sum(grid == RECOVERED)
    dead = np.sum(grid == DEAD)

    total_population = (
            healthy +
            infected +
            recovered +
            dead
    )

    stats_text.set_text(
        f"Population: {total_population}\n"
        f"Healthy: {healthy}\n"
        f"Infected: {infected}\n"
        f"Recovered: {recovered}\n"
        f"Dead: {dead}"
    )

    healthy_history.append(healthy)
    infected_history.append(infected)
    recovered_history.append(recovered)
    dead_history.append(dead)

    img.set_array(grid)

    ax2.clear()

    ax2.plot(
        healthy_history,
        label="Healthy",
        color="green"
    )

    ax2.plot(
        infected_history,
        label="Infected",
        color="red"
    )

    ax2.plot(
        recovered_history,
        label="Recovered",
        color="blue"
    )

    ax2.plot(
        dead_history,
        label="Dead",
        color="black"
    )

    ax2.set_title("Statistics")
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Population")

    ax2.legend()

    animation.event_source.interval = 201 - slider_speed.val

    return [img]

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

    if (
        0 <= x < GRID_SIZE and
        0 <= y < GRID_SIZE
    ):

        grid[x, y] = INFECTED


fig.canvas.mpl_connect(
    "button_press_event",
    on_click
)

animation = FuncAnimation(
    fig,
    update,
    interval=50,
    cache_frame_data=False
)

# =====================================================
# ЗАПУСК
# =====================================================

plt.show()