from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from physics import *
import arcade


class SpatialHash:
    def __init__(self, cell_size=32):
        self.cell_size = cell_size
        self.grid = {}

    def _hash(self, x, y):
        return (x // self.cell_size, y // self.cell_size)

    def add(self, x, y, substance):
        key = self._hash(x, y)
        if key not in self.grid:
            self.grid[key] = []
        self.grid[key].append((x, y, substance))

    def get_in_area(self, min_x, max_x, min_y, max_y):
        min_cell_x = min_x // self.cell_size
        max_cell_x = max_x // self.cell_size
        min_cell_y = min_y // self.cell_size
        max_cell_y = max_y // self.cell_size

        results = []
        for cell_x in range(min_cell_x, max_cell_x + 1):
            for cell_y in range(min_cell_y, max_cell_y + 1):
                key = (cell_x, cell_y)
                if key in self.grid:
                    results.extend(self.grid[key])
        return results

    def remove(self, x, y):
        key = self._hash(x, y)
        if key in self.grid:
            for i, (sx, sy, _) in enumerate(self.grid[key]):
                if sx == x and sy == y:
                    del self.grid[key][i]
                    if not self.grid[key]:
                        del self.grid[key]
                    return True
        return False

    def update(self, x, y, new_x, new_y, substance):
        old_key = self._hash(x, y)
        new_key = self._hash(new_x, new_y)

        if old_key == new_key:
            return

        self.remove(x, y)
        self.add(new_x, new_y, substance)


class WorldView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_list = arcade.SpriteList()
        bg_sprite = arcade.Sprite("media/backgroung.png")
        bg_sprite.center_x = SCREEN_WIDTH // 2
        bg_sprite.center_y = SCREEN_HEIGHT // 2
        bg_sprite.width = SCREEN_WIDTH
        bg_sprite.height = SCREEN_HEIGHT
        self.background_list.append(bg_sprite)

        from levels import generate_level1
        generate_level1(0, 0)
        self.start_x, self.start_y = 0, 0

        self.shape_list = None
        self.last_update = 0
        self.update_interval = 1 / 30
        self.current_fps = 0
        self.fps_timer = 0
        self.fps_counter = 0

        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 5
        self.keys_pressed = set()

        self.cell_size = 4

        self.camera_x = self.start_x * self.cell_size - SCREEN_WIDTH // 2
        self.camera_y = self.start_y * self.cell_size - SCREEN_HEIGHT // 2

        self.screen_buffer_cells = 10
        self.current_substances = {}

        self.spatial_hash = SpatialHash(cell_size=32)

        self.world = world

        for (x, y), substance in world.items():
            self.spatial_hash.add(x, y, substance)

        self.physics_enabled = True
        self.physics_speed = 1.0
        self.physics_timer = 0.0
        self.physics_update_rate = 1 / 30



    def on_update(self, delta_time):
        self.fps_timer += delta_time
        self.fps_counter += 1
        if self.fps_timer >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_timer = 0
            self.fps_counter = 0

        dx, dy = 0, 0
        if arcade.key.W in self.keys_pressed:
            dy += self.camera_speed
        if arcade.key.S in self.keys_pressed:
            dy -= self.camera_speed
        if arcade.key.A in self.keys_pressed:
            dx -= self.camera_speed
        if arcade.key.D in self.keys_pressed:
            dx += self.camera_speed

        old_camera_x, old_camera_y = self.camera_x, self.camera_y
        self.camera_x += dx
        self.camera_y += dy

        camera_moved = (abs(self.camera_x - old_camera_x) > 20 or
                        abs(self.camera_y - old_camera_y) > 20)

        if self.physics_enabled:
            self.physics_timer += delta_time * self.physics_speed
            while self.physics_timer >= self.physics_update_rate:
                self._update_physics(self.physics_update_rate)
                self.physics_timer -= self.physics_update_rate

        self.last_update += delta_time
        if self.last_update >= self.update_interval or camera_moved:
            self.last_update = 0
            self._update_visible_substances()
            self.update_shape_list()


    def on_draw(self):
        self.clear()
        self.background_list.draw()
        if self.shape_list:
            self.shape_list.draw()
        arcade.draw_text(
            f"FPS: {self.current_fps}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.YELLOW, 16
        )
        arcade.draw_text(
            f"Веществ: {len(self.world)} | На экране: {len(self.current_substances)}",
            10, SCREEN_HEIGHT - 60,
            arcade.color.LIGHT_GRAY, 12
        )

    def _update_physics(self, delta_time):
        if not self.current_substances:
            return

        screen_min_x = int(self.camera_x / self.cell_size) - self.screen_buffer_cells
        screen_max_x = int((self.camera_x + SCREEN_WIDTH) / self.cell_size) + self.screen_buffer_cells
        screen_min_y = int(self.camera_y / self.cell_size) - self.screen_buffer_cells
        screen_max_y = int((self.camera_y + SCREEN_HEIGHT) / self.cell_size) + self.screen_buffer_cells

        substances_in_view = []
        for key, substance in list(self.world.items()):
            x, y = key
            if (screen_min_x <= x <= screen_max_x and
                    screen_min_y <= y <= screen_max_y):
                substances_in_view.append(substance)

        substances_to_update = []
        gases_to_update = []

        for substance in substances_in_view:
            if hasattr(substance, '__class__'):
                if substance.__class__.__name__ in ['Gas', 'Fire', 'Smoke', 'Steam', 'Plasm', 'Boom']:
                    gases_to_update.append(substance)
                elif substance.__class__.__name__ in ['Liquid', 'Water', 'Petrol', 'Acid', 'Lava']:
                    substances_to_update.insert(0, substance)
                else:
                    substances_to_update.append(substance)

        substances_to_update.extend(reversed(gases_to_update))

        for substance in substances_to_update:
            old_x, old_y = substance.x, substance.y

            try:
                substance.action()
            except Exception as e:
                continue

            new_x, new_y = substance.x, substance.y
            if (old_x, old_y) != (new_x, new_y):
                if (old_x, old_y) in self.world and self.world[(old_x, old_y)] is substance:
                    del self.world[(old_x, old_y)]
                    self.spatial_hash.remove(old_x, old_y)

                self.world[(new_x, new_y)] = substance
                self.spatial_hash.add(new_x, new_y, substance)

                old_key = (old_x, old_y)
                new_key = (new_x, new_y)

                if old_key in self.current_substances:
                    del self.current_substances[old_key]

                if (screen_min_x <= new_x <= screen_max_x and
                        screen_min_y <= new_y <= screen_max_y):
                    self.current_substances[new_key] = substance
                elif new_key in self.current_substances:
                    del self.current_substances[new_key]

        keys_to_remove = []
        for (x, y) in list(self.current_substances.keys()):
            if (x, y) not in self.world or self.world[(x, y)] is not self.current_substances[(x, y)]:
                keys_to_remove.append((x, y))

        for key in keys_to_remove:
            if key in self.current_substances:
                del self.current_substances[key]

    def _update_visible_substances(self):
        screen_min_x = int(self.camera_x / self.cell_size) - self.screen_buffer_cells
        screen_max_x = int((self.camera_x + SCREEN_WIDTH) / self.cell_size) + self.screen_buffer_cells
        screen_min_y = int(self.camera_y / self.cell_size) - self.screen_buffer_cells
        screen_max_y = int((self.camera_y + SCREEN_HEIGHT) / self.cell_size) + self.screen_buffer_cells

        self.current_substances.clear()

        visible_substances = self.spatial_hash.get_in_area(
            screen_min_x, screen_max_x,
            screen_min_y, screen_max_y
        )

        for x, y, substance in visible_substances:
            if (screen_min_x <= x <= screen_max_x and
                    screen_min_y <= y <= screen_max_y):
                if (x, y) in self.world and self.world[(x, y)] is substance:
                    self.current_substances[(x, y)] = substance

    def update_shape_list(self):
        self.shape_list = arcade.shape_list.ShapeElementList()

        for (world_x, world_y), substance in self.current_substances.items():
            if (world_x, world_y) not in self.world or self.world[(world_x, world_y)] is not substance:
                continue

            screen_x = world_x * self.cell_size - self.camera_x
            screen_y = world_y * self.cell_size - self.camera_y

            if (0 <= screen_x <= SCREEN_WIDTH and
                    0 <= screen_y <= SCREEN_HEIGHT):
                color = substance.fake_color
                rect = arcade.shape_list.create_rectangle_filled(
                    screen_x + self.cell_size // 2,
                    screen_y + self.cell_size // 2,
                    self.cell_size,
                    self.cell_size,
                    color
                )
                self.shape_list.append(rect)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

        if key == arcade.key.ESCAPE:
            menu_view = StartMenuView()
            self.window.show_view(menu_view)

        if key == arcade.key.W:
            self.keys_pressed.add(arcade.key.W)
        if key == arcade.key.A:
            self.keys_pressed.add(arcade.key.A)
        if key == arcade.key.S:
            self.keys_pressed.add(arcade.key.S)
        if key == arcade.key.D:
            self.keys_pressed.add(arcade.key.D)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)