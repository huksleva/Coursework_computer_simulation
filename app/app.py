import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# =========================
# ПАРАМЕТРЫ МОДЕЛИ
# =========================

# Размер сетки
GRID_SIZE = 100

# Состояния клеток
SUSCEPTIBLE = 0   # Здоровый
INFECTED = 1      # Заражённый
RECOVERED = 2     # Выздоровевший

# Вероятность заражения
infection_probability = 0.3

# Вероятность выздоровления
recovery_probability = 0.05

# Количество начально заражённых
initial_infected = 5

# Количество шагов симуляции
STEPS = 300

# =========================
# СОЗДАНИЕ СЕТКИ
# =========================

# Создаём поле из здоровых людей
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# Случайно заражаем несколько клеток
for _ in range(initial_infected):
    x = np.random.randint(0, GRID_SIZE)
    y = np.random.randint(0, GRID_SIZE)
    grid[x, y] = INFECTED

# =========================
# СПИСКИ ДЛЯ ГРАФИКОВ
# =========================

susceptible_history = []
infected_history = []
recovered_history = []

# =========================
# ФУНКЦИЯ ОБНОВЛЕНИЯ
# =========================

def update(frame):
    global grid

    # Копия сетки
    new_grid = grid.copy()

    # Проходим по всем клеткам
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):

            # Если клетка заражена
            if grid[x, y] == INFECTED:

                # Проверяем соседей
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:

                        # Пропускаем саму клетку
                        if dx == 0 and dy == 0:
                            continue

                        nx = x + dx
                        ny = y + dy

                        # Проверка границ
                        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:

                            # Если сосед здоров
                            if grid[nx, ny] == SUSCEPTIBLE:

                                # Заражение с некоторой вероятностью
                                if np.random.random() < infection_probability:
                                    new_grid[nx, ny] = INFECTED

                # Выздоровление
                if np.random.random() < recovery_probability:
                    new_grid[x, y] = RECOVERED

    # Обновляем сетку
    grid = new_grid

    # Подсчёт статистики
    susceptible_count = np.sum(grid == SUSCEPTIBLE)
    infected_count = np.sum(grid == INFECTED)
    recovered_count = np.sum(grid == RECOVERED)

    susceptible_history.append(susceptible_count)
    infected_history.append(infected_count)
    recovered_history.append(recovered_count)

    # Обновление изображения
    img.set_array(grid)

    # Обновление графиков
    ax2.clear()

    ax2.plot(susceptible_history, label='Susceptible')
    ax2.plot(infected_history, label='Infected')
    ax2.plot(recovered_history, label='Recovered')

    ax2.set_title("SIR Model Statistics")
    ax2.set_xlabel("Step")
    ax2.set_ylabel("People")

    ax2.legend()

    return [img]

# =========================
# СОЗДАНИЕ ОКНА
# =========================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Цветовая карта
cmap = plt.cm.get_cmap('viridis', 3)

# Отображение сетки
img = ax1.imshow(grid, cmap=cmap, vmin=0, vmax=2)

# Заголовок
ax1.set_title("Epidemic Spread Simulation")

# Убираем оси
ax1.set_xticks([])
ax1.set_yticks([])

# =========================
# АНИМАЦИЯ
# =========================

animation = FuncAnimation(
    fig,
    update,
    frames=STEPS,
    interval=50,
    repeat=False
)

# =========================
# ЗАПУСК
# =========================

plt.tight_layout()
plt.show()

