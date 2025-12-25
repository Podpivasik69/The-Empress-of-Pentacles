from physics import Stone, world_w, world_h, world, add_substance, remove_substance
import random
import math


def generate_level1():

    ant_count = 4  # количество муравьёв
    ant_steps = 50  # количество шагов каждого муравья
    cave_radius = 10  # радиус пещеры
    clearing_radius = 15  # радиус очистки в начальной точке

    max_x = world_w + 100
    max_y = world_h + 100

    for x in range(max_x):
        for y in range(max_y):
            add_substance(Stone(x, y))

    start_x = max_x // 2
    start_y = max_y // 2

    # Очищаем стартовую зону
    for x in range(start_x - clearing_radius, start_x + clearing_radius):
        for y in range(start_y - clearing_radius, start_y + clearing_radius):
            if 0 <= x < max_x and 0 <= y < max_y:
                remove_substance(x, y)

    def get_random_direction():
        return random.random() * 2 * math.pi

    def create_cave_at(x, y, radius):
        cells_removed = 0
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= radius:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < max_x and 0 <= ny < max_y:
                        remove_substance(nx, ny)
                        cells_removed += 1
        return cells_removed

    def ant_step(current_x, current_y, direction):
        step_length = random.randint(5, 15)
        direction_change = random.uniform(-0.5, 0.5)
        new_direction = direction + direction_change
        new_direction = new_direction % (2 * math.pi)
        new_x = current_x + math.cos(new_direction) * step_length
        new_y = current_y + math.sin(new_direction) * step_length
        new_x = max(0, min(max_x - 1, new_x))
        new_y = max(0, min(max_y - 1, new_y))
        return int(new_x), int(new_y), new_direction

    # Создаём муравьёв
    ants = []
    for i in range(ant_count):
        ant = {
            'x': start_x,
            'y': start_y,
            'direction': get_random_direction()
        }
        ants.append(ant)

    total_cells_removed = 0

    # Движение муравьёв
    for step in range(ant_steps):
        for ant in ants:
            ant['x'], ant['y'], ant['direction'] = ant_step(
                ant['x'], ant['y'], ant['direction']
            )
            cells_removed = create_cave_at(ant['x'], ant['y'], cave_radius)
            total_cells_removed += cells_removed

    # Соединяем последние позиции муравьёв туннелями
    if len(ants) >= 2:
        # Берём первые двух муравьёв для соединения
        ant1 = ants[0]
        ant2 = ants[1] if len(ants) > 1 else ants[0]

        distance = math.sqrt((ant1['x'] - ant2['x']) ** 2 + (ant1['y'] - ant2['y']) ** 2)
        if distance > cave_radius * 4:
            steps = int(distance) * 2
            for i in range(steps + 1):
                t = i / steps
                cx = int(ant1['x'] + (ant2['x'] - ant1['x']) * t)
                cy = int(ant1['y'] + (ant2['y'] - ant1['y']) * t)
                cells_removed = create_cave_at(cx, cy, cave_radius // 2)
                total_cells_removed += cells_removed

    return start_x, start_y

def generate_level0():
    pass