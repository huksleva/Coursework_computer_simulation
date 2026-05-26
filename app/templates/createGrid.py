def create_grid():
    current_grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):

            if np.random.random() < population_density:
                current_grid[x, y] = HEALTHY

    healthy_positions = np.argwhere(current_grid == HEALTHY)

    infected_count = min(int(slider_infected.val), len(healthy_positions))

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

