from physics import *
import random
import math


def generate_stone_square(x, y, size):
    end_x = x + size
    end_y = y - size
    for i in range(x, end_x):
        for j in range(end_y, y):
            add_substance(Stone(i, j))


def spawn_ant(start_x, start_y, num=3, radius=8, steps=100):
    def create_cave_at(x, y, radius):
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                distance = math.sqrt(dx * dx + dy * dy)
                if distance <= radius:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) in world:
                        remove_substance(nx, ny)

    ant_types = ['wanderer', 'digger', 'explorer']

    ants = []
    for i in range(num):
        ant_type = ant_types[i % len(ant_types)]

        if i == 0:
            x, y = start_x, start_y
        else:
            angle = (i / num) * 2 * math.pi
            spread = 10
            x = start_x + int(math.cos(angle) * spread)
            y = start_y + int(math.sin(angle) * spread)

        ant = {
            'id': i,
            'type': ant_type,
            'x': x,
            'y': y,
            'preferred_dx': 0,
            'preferred_dy': 0,
            'boredom': 0
        }
        if ant_type == 'digger':
            ant['preferred_dy'] = -1
        elif ant_type == 'explorer':
            ant['preferred_dx'] = 1 if random.random() > 0.5 else -1

        ants.append(ant)

    for step in range(steps):
        for ant in ants:
            old_x, old_y = ant['x'], ant['y']
            directions = []
            weights = []
            all_dirs = [
                (0, 1), (1, 1), (1, 0), (1, -1),
                (0, -1), (-1, -1), (-1, 0), (-1, 1)
            ]
            for dx, dy in all_dirs:
                weight = 1.0
                if ant['preferred_dx'] != 0:
                    if dx == ant['preferred_dx']:
                        weight *= 2.0
                    elif dx == -ant['preferred_dx']:
                        weight *= 0.5

                if ant['preferred_dy'] != 0:
                    if dy == ant['preferred_dy']:
                        weight *= 2.0
                    elif dy == -ant['preferred_dy']:
                        weight *= 0.5

                if ant.get('last_dx') is not None and ant.get('last_dy') is not None:
                    last_dx, last_dy = ant['last_dx'], ant['last_dy']
                    dot_product = dx * last_dx + dy * last_dy
                    if dot_product > 0:
                        weight *= 1.5
                    elif dot_product < 0:
                        weight *= 0.3
                directions.append((dx, dy))
                weights.append(weight)

            dx, dy = random.choices(directions, weights=weights, k=1)[0]
            step_length = random.randint(1, 3)
            new_x = old_x + dx * step_length
            new_y = old_y + dy * step_length
            ant['last_dx'], ant['last_dy'] = dx, dy
            ant['x'], ant['y'] = new_x, new_y
            create_cave_at(new_x, new_y, radius)
            distance = math.sqrt((new_x - old_x) ** 2 + (new_y - old_y) ** 2)
            if distance > 0:
                steps_in_tunnel = max(2, int(distance))
                for i in range(steps_in_tunnel + 1):
                    t = i / steps_in_tunnel
                    cx = int(old_x + (new_x - old_x) * t)
                    cy = int(old_y + (new_y - old_y) * t)
                    create_cave_at(cx, cy, max(1, radius // 2))
            ant['boredom'] += 1
            if ant['boredom'] > 20 + random.randint(0, 20):
                ant['boredom'] = 0
                if ant['type'] == 'wanderer':
                    ant['preferred_dx'] = random.choice([-1, 0, 1])
                    ant['preferred_dy'] = random.choice([-1, 0, 1])
                elif ant['type'] == 'explorer':
                    ant['preferred_dx'] *= -1


def generate_ground(left_x, top_y, width, height):
    amplitude = 5  # Амплитуда колебаний поверхности
    frequency = 0.15 # Частота волн (зависит от ширины)
    ground_thickness = height // 2  # Толщина слоя земли
    grass_layers = 2  # Количество слоёв травы
    roughness = 1  # Случайные шероховатости
    surface_profile = []
    base_surface_line = top_y - (height // 3)
    for i in range(width):
        norm_x = i / width * 10
        base_wave = math.sin(norm_x * frequency) * amplitude * 0.7
        detail_wave = math.sin(norm_x * frequency * 4) * amplitude * 0.3
        random_wave = (random.random() * 2 - 1) * roughness
        surface_y = base_surface_line + base_wave + detail_wave + random_wave
        surface_profile.append(int(surface_y))

    smoothed_profile = []
    for i in range(width):
        if i == 0:
            avg = (surface_profile[0] + surface_profile[1]) / 2
        elif i == width - 1:
            avg = (surface_profile[-2] + surface_profile[-1]) / 2
        else:
            avg = (surface_profile[i - 1] + surface_profile[i] + surface_profile[i + 1]) / 3
        smoothed_profile.append(int(avg))

    ground_cells = 0
    grass_cells = 0
    for i in range(width):
        current_x = left_x + i
        surface_y = smoothed_profile[i]
        for y_offset in range(ground_thickness):
            current_y = surface_y - y_offset
            if (current_x, current_y) in world:
                remove_substance(current_x, current_y)
            add_substance(Ground(current_x, current_y))
            ground_cells += 1

        for layer in range(grass_layers):
            grass_y = surface_y + layer
            if (current_x, grass_y) in world:
                remove_substance(current_x, grass_y)
            add_substance(Grass(current_x, grass_y))
            grass_cells += 1


def generate_rplatform(left_x, top_y, width, height, sub):
    amplitude = 5  # Амплитуда колебаний поверхности
    frequency = 0.15  # Частота волн (зависит от ширины)
    roughness = 1  # Случайные шероховатости

    surface_profile = []
    base_surface_line = top_y - (height // 3)

    for i in range(width):
        norm_x = i / width * 10
        base_wave = math.sin(norm_x * frequency) * amplitude * 0.7
        detail_wave = math.sin(norm_x * frequency * 4) * amplitude * 0.3
        random_wave = (random.random() * 2 - 1) * roughness
        surface_y = base_surface_line + base_wave + detail_wave + random_wave
        surface_profile.append(int(surface_y))

    smoothed_profile = []
    for i in range(width):
        if i == 0:
            avg = (surface_profile[0] + surface_profile[1]) / 2
        elif i == width - 1:
            avg = (surface_profile[-2] + surface_profile[-1]) / 2
        else:
            avg = (surface_profile[i - 1] + surface_profile[i] + surface_profile[i + 1]) / 3
        smoothed_profile.append(int(avg))

    platform_cells = 0

    for i in range(width):
        current_x = left_x + i
        surface_y = smoothed_profile[i]

        for y_offset in range(height):
            current_y = surface_y - y_offset

            if (current_x, current_y) in world:
                remove_substance(current_x, current_y)

            if sub == stone:
                add_substance(Stone(current_x, current_y))
            elif sub == wood:
                add_substance(Wood(current_x, current_y))
            elif sub == fire:
                add_substance(Fire(current_x, current_y))
            elif sub == water:
                add_substance(Water(current_x, current_y))
            elif sub == sand:
                add_substance(Sand(current_x, current_y))
            elif sub == acid:
                add_substance(Acid(current_x, current_y))
            elif sub == plasm:
                add_substance(Plasm(current_x, current_y))
            elif sub == petrol:
                add_substance(Petrol(current_x, current_y))
            elif sub == boom:
                add_substance(Boom(current_x, current_y))
            elif sub == lava:
                add_substance(Lava(current_x, current_y, stone))
            elif sub == powder:
                add_substance(Powder(current_x, current_y))
            elif sub == smoke:
                add_substance(Smoke(current_x, current_y))
            elif sub == steam:
                add_substance(Steam(current_x, current_y))
            elif sub == snow:
                add_substance(Snow(current_x, current_y))
            elif sub == iron:
                add_substance(Iron(current_x, current_y))
            elif sub == ground:
                add_substance(Ground(current_x, current_y))
            elif sub == grass:
                generate_ground(left_x, top_y, width, height)
                return
            else:
                # По умолчанию камень
                add_substance(Stone(current_x, current_y))

            platform_cells += 1


def generate_caves(num, x, y, size, radius=4, steps=200):
    for _ in range(0, 20):
        r_x = random.randint(x + 30, x + size - 30)
        r_y = random.randint(y - size + 30, y - 30)
        spawn_ant(
            start_x=r_x,
            start_y=r_y,
            num=1,
            radius=radius,
            steps=steps
        )


def generate_platform(x, y, w, h, sub):
    end_x = x + w
    end_y = y - h
    for i in range(x, end_x):
        for j in range(end_y, y):
            if sub == stone:
                add_substance(Stone(i, j))
            elif sub == wood:
                add_substance(Wood(i, j))
            elif sub == fire:
                add_substance(Fire(i, j))
            elif sub == water:
                add_substance(Water(i, j))
            elif sub == sand:
                add_substance(Sand(i, j))
            elif sub == acid:
                add_substance(Acid(i, j))
            elif sub == plasm:
                add_substance(Plasm(i, j))
            elif sub == petrol:
                add_substance(Petrol(i, j))
            elif sub == boom:
                add_substance(Boom(i, j))
            elif sub == lava:
                add_substance(Lava(i, j, stone))
            elif sub == powder:
                add_substance(Powder(i, j))
            elif sub == smoke:
                add_substance(Smoke(i, j))
            elif sub == steam:
                add_substance(Steam(i, j))
            elif sub == snow:
                add_substance(Snow(i, j))
            elif sub == iron:
                add_substance(Iron(i, j))
            elif sub == ground:
                add_substance(Ground(i, j))
            elif sub == grass:
                generate_ground(i, j, w, h)
                return


def generate_platforms(x, y, w, h, n):
    end_x = x + w
    end_y = y - h
    materials = [
        grass
    ]

    for i in range(n):
        sub = random.choice(materials)
        px = random.randint(x, end_x)
        py = random.randint(end_y, y)
        pw = random.randint(30, 100)
        ph = random.randint(10, 15)
        generate_platform(px, py, pw, ph, sub)


def generate_platform_level(x, y, n, sub=grass):
    px = x
    for _ in range(n):
        pw = random.randint(30, 100)
        ph = random.randint(10, 15)
        rast = random.randint(10, 30)
        px += rast + pw
        py = y - random.randint(0, 40)
        generate_rplatform(px, py, pw, ph, sub)



def generate_level1(x, y):
    size = 800
    # generate_ground(x, y, size, 100)
    # generate_stone_square(x, y - 60, size)
    # generate_caves(1000, x, y - 60, size, radius=5, steps=2000)

    # generate_platforms(x, y, 1000, 100, 10)
    generate_platform_level(x, y, 10)
