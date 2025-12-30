from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from game import GameView
from player import Player
from physics import *
import arcade


class StartMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.white = arcade.color.WHITE
        self.brown = arcade.color.COCOA_BROWN
        arcade.set_background_color(arcade.color.ASH_GREY)
        arcade.load_font('media/MinecraftDefault-Regular.ttf')

        self.menu_button = arcade.load_texture('media/ui/menu_button.png')
        self.background_texture = arcade.load_texture('media/backgroung.png')

    def on_show(self):
        # Вызывается при показе View
        pass

    def on_draw(self):
        # картинка задний фон
        arcade.draw_texture_rect(self.background_texture,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        # Назван е
        # arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, (SCREEN_HEIGHT * 3) // 4,
        #                                           600, 100), self.white, 1, )
        arcade.draw_text(SCREEN_TITLE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4,
                         self.white, 50, anchor_x="center", anchor_y="center", font_name='Minecraft Default')
        # Кнопка играть
        # arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, 250, 200, 100), self.brown, 1)
        arcade.draw_texture_rect(self.menu_button, arcade.rect.XYWH(SCREEN_WIDTH // 2, 250, 200, 90), )
        arcade.draw_text('иглать', SCREEN_WIDTH // 2, 250, self.white, 42,
                         anchor_x="center", anchor_y="center", font_name='Minecraft Default')
        # кглпка выохода
        # arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, 150, 200, 100), self.brown, 1)
        arcade.draw_texture_rect(self.menu_button, arcade.rect.XYWH(SCREEN_WIDTH // 2, 150, 200, 90), )
        arcade.draw_text('вихад', SCREEN_WIDTH // 2, 150, self.white, 42,
                         anchor_x="center", anchor_y="center", font_name='Minecraft Default')

        arcade.draw_texture_rect(self.menu_button, arcade.rect.XYWH(SCREEN_WIDTH // 2, 50, 200, 90), )
        arcade.draw_text('phys', SCREEN_WIDTH // 2, 50, self.white, 42,
                         anchor_x="center", anchor_y="center", font_name='Minecraft Default')

    def on_mouse_press(self, x, y, button, modifiers):
        # жмяк и выход
        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 110 <= y <= 190:
            arcade.close_window()
        # иглать
        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 210 <= y <= 290:
            game_view = GameView()  # переключаем окно на игру
            game_view.setup()  # запускаем игровой setuo
            self.window.show_view(game_view)  # показываем окно игры

        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 10 <= y <= 90:
            world_view = WorldView()
            self.window.show_view(world_view)


class DeathScreenView(arcade.View):
    def __init__(self):
        super().__init__()
        print("DEBUG DeathScreenView: __init__ called")
        self.white = arcade.color.WHITE
        arcade.set_background_color(arcade.color.ASH_GREY)
        self._cursor_enabled = False
        arcade.load_font('media/MinecraftDefault-Regular.ttf')

        self.background_texture = arcade.load_texture('media/backgroung.png')
        self.menu_button = arcade.load_texture('media/ui/menu_button.png')

        # TODO статистика после смерти, рекорды, и тд

    def on_draw(self):
        self.clear()
        # pfujkjdjr
        arcade.draw_texture_rect(self.background_texture,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        arcade.draw_text("ТИ СДОХ", SCREEN_HEIGHT // 2, 450, self.white, 50,
                         anchor_x='center', anchor_y='center', font_name="Minecraft Default")
        # начать заново
        arcade.draw_texture_rect(self.menu_button,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, 300, 200, 90))
        arcade.draw_text('ЗАНОВО', SCREEN_WIDTH // 2, 300, self.white, 42,
                         anchor_x="center", anchor_y="center",
                         font_name='Minecraft Default')
        # меню (если слабый)
        arcade.draw_texture_rect(self.menu_button,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, 200, 200, 90))
        arcade.draw_text('В МЕНЮ', SCREEN_WIDTH // 2, 200, self.white, 42,
                         anchor_x="center", anchor_y="center",
                         font_name='Minecraft Default')

    def on_mouse_press(self, x, y, button, modifiers):
        button_width = 200
        button_height = 90
        # заново
        button_x = SCREEN_WIDTH // 2
        button_y = 300

        if (button_x - button_width / 2 <= x <= button_x + button_width / 2 and
                button_y - button_height / 2 <= y <= button_y + button_height / 2):
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        # в меню
        button_y = 200
        if (button_x - button_width / 2 <= x <= button_x + button_width / 2 and
                button_y - button_height / 2 <= y <= button_y + button_height / 2):
            menu_view = StartMenuView()
            self.window.show_view(menu_view)

    def on_show_view(self):
        print("DEBUG DeathScreenView: on_show_view called")
        if self.window:
            self.window.set_mouse_visible(True)
            self._cursor_enabled = True
            print("Курсор включен в DeathScreen")

    def on_hide(self):
        if self.window:
            self.window.set_mouse_visible(False)


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
        self.window.set_update_rate(1 / 30)

        from levels import generate_level1
        generate_level1(-400, 0)
        self.start_x, self.start_y = 0, 0

        self.shape_list = None
        self.last_update = 0
        self.update_interval = 1 / 30
        self.current_fps = 0
        self.fps_timer = 0
        self.fps_counter = 0

        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 10
        self.keys_pressed = set()

        self.cell_size = 4

        self.camera_x = self.start_x * self.cell_size - SCREEN_WIDTH // 2
        self.camera_y = self.start_y * self.cell_size - SCREEN_HEIGHT // 2

        self.screen_buffer_cells = 10
        self.current_substances = {}

        self.spatial_hash = SpatialHash(cell_size=32)

        for (x, y), substance in world.items():
            self.spatial_hash.add(x, y, substance)

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

        self.last_update += delta_time

        if self.last_update >= self.update_interval or camera_moved:
            self.last_update = 0
            self._update_visible_substances()
            self.update_shape_list()

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
                self.current_substances[(x, y)] = substance

    def update_shape_list(self):
        self.shape_list = arcade.shape_list.ShapeElementList()

        for (world_x, world_y), substance in self.current_substances.items():
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

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.BLACK)

        if self.shape_list:
            self.shape_list.draw()

        arcade.draw_text(
            f"FPS: {self.current_fps}",
            10, SCREEN_HEIGHT - 30,
            arcade.color.YELLOW, 16
        )

        arcade.draw_text(
            f"WASD - движение камеры | B: буфер | R: обновить индекс",
            10, SCREEN_HEIGHT - 60,
            arcade.color.WHITE, 14
        )

        arcade.draw_text(
            f"Всего веществ: {len(world)} | На экране: {len(self.current_substances)}",
            10, SCREEN_HEIGHT - 90,
            arcade.color.LIGHT_GRAY, 12
        )

        arcade.draw_text(
            f"Ячеек SpatialHash: {len(self.spatial_hash.grid)}",
            10, SCREEN_HEIGHT - 120,
            arcade.color.LIGHT_GRAY, 12
        )

        arcade.draw_text(
            f"Камера: ({int(self.camera_x)}, {int(self.camera_y)})",
            10, SCREEN_HEIGHT - 150,
            arcade.color.LIGHT_GRAY, 12
        )

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

        if key == arcade.key.ESCAPE:
            from view import StartMenuView
            menu_view = StartMenuView()
            self.window.show_view(menu_view)

        if key == arcade.key.HOME:
            self.camera_x = self.start_x * self.cell_size - SCREEN_WIDTH // 2
            self.camera_y = self.start_y * self.cell_size - SCREEN_HEIGHT // 2
            self._update_visible_substances()
            self.update_shape_list()

        if key == arcade.key.B:
            if self.screen_buffer_cells == 10:
                self.screen_buffer_cells = 20
            elif self.screen_buffer_cells == 20:
                self.screen_buffer_cells = 5
            else:
                self.screen_buffer_cells = 10

            self._update_visible_substances()
            self.update_shape_list()

        if key == arcade.key.R:
            self.spatial_hash = SpatialHash(cell_size=32)
            for (x, y), substance in world.items():
                self.spatial_hash.add(x, y, substance)
            self._update_visible_substances()
            self.update_shape_list()

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)