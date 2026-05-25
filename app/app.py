import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, RadioButtons

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

    for _ in range(initial_infected):

        if len(healthy_positions) == 0:
            break

        index = np.random.randint(0, len(healthy_positions))
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

cmap = plt.cm.get_cmap("viridis", 5)

img = ax1.imshow(grid, cmap=cmap, vmin=0, vmax=4)

ax1.set_title("Epidemic Simulation")
ax1.set_xticks([])
ax1.set_yticks([])

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

button_reset = Button(reset_ax, "Restart")
button_pause = Button(pause_ax, "Pause")
button_defaults = Button(defaults_ax, "Defaults")

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

def toggle_pause(event):

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

def reset_defaults(event):

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

def restart(event):

    global grid
    global healthy_history
    global infected_history
    global recovered_history
    global dead_history
    global population_density

    population_density = slider_density.val

    grid = create_grid()

    healthy_history = []
    infected_history = []
    recovered_history = []
    dead_history = []


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

def update(frame):

    global grid

    if paused:
        return [img]

    grid = move_people(grid)

    grid = spread_infection(grid)

    healthy = np.sum(grid == HEALTHY)
    infected = np.sum(grid == INFECTED)
    recovered = np.sum(grid == RECOVERED)
    dead = np.sum(grid == DEAD)

    healthy_history.append(healthy)
    infected_history.append(infected)
    recovered_history.append(recovered)
    dead_history.append(dead)

    img.set_array(grid)

    ax2.clear()

    ax2.plot(healthy_history, label="Healthy")
    ax2.plot(infected_history, label="Infected")
    ax2.plot(recovered_history, label="Recovered")
    ax2.plot(dead_history, label="Dead")

    ax2.set_title("Statistics")
    ax2.set_xlabel("Step")
    ax2.set_ylabel("Population")

    ax2.legend()

    animation.event_source.interval = 201 - slider_speed.val

    return [img]

# =====================================================
# АНИМАЦИЯ
# =====================================================

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