# levels.py
def generate_level1():
    from physics import Stone, world_w, world_h, world, add_substance, remove_substance
    import random
    import math

    max_x = world_w
    max_y = world_h

    stone_count = 0
    for x in range(max_x):
        for y in range(max_y):
            add_substance(Stone(x, y))
            stone_count += 1

    start_x = max_x // 2
    start_y = max_y // 2

    for x in range(start_x - 15, start_x + 15):
        for y in range(start_y - 15, start_y + 15):
            if 0 <= x < max_x and 0 <= y < max_y:
                remove_substance(x, y)

    ant_steps = 100
    cave_radius = 10

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

    ant1_x = start_x
    ant1_y = start_y
    ant1_direction = get_random_direction()

    ant2_x = start_x
    ant2_y = start_y
    ant2_direction = get_random_direction()

    total_cells_removed = 0

    for step in range(ant_steps):
        ant1_x, ant1_y, ant1_direction = ant_step(ant1_x, ant1_y, ant1_direction)
        cells_removed = create_cave_at(ant1_x, ant1_y, cave_radius)
        total_cells_removed += cells_removed

        ant2_x, ant2_y, ant2_direction = ant_step(ant2_x, ant2_y, ant2_direction)
        cells_removed = create_cave_at(ant2_x, ant2_y, cave_radius)
        total_cells_removed += cells_removed

    distance = math.sqrt((ant1_x - ant2_x) ** 2 + (ant1_y - ant2_y) ** 2)
    if distance > cave_radius * 4:
        steps = int(distance) * 2
        for i in range(steps + 1):
            t = i / steps
            cx = int(ant1_x + (ant2_x - ant1_x) * t)
            cy = int(ant1_y + (ant2_y - ant1_y) * t)
            cells_removed = create_cave_at(cx, cy, cave_radius // 2)
            total_cells_removed += cells_removed

    return start_x, start_y