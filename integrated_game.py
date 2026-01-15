from world import WorldView
from player import Player
from staff import BASIC_STAFF
from elemental_circle import ElementalCircle
from spell_system import SpellSystem
from constants import *
from physics import *
from core.ui_renderer import UIRenderer
from core.game_state import GameState
from core.entity_manager import EntityManager
from core.spell_manager import SpellManager
from core.input_manager import InputManager
import arcade
import math


class IntegratedWorldView(WorldView):
    def __init__(self):
        super().__init__()

        # Инициализация игрока
        self.player = Player()
        self.player.setup()
        self.player.witch_speed = 2
        self.camera_speed = 0  # Камера будет следовать за игроком

        # Физика платформера (как в оригинальном integrated_game.py)
        self.gravity_speed = 3
        self.gravity = True
        self.jump_velocity = 0
        self.jump_power = 25
        self.just_jumped = False

        # Система заклинаний (аналогично GameView)
        self.game_state = GameState()
        self.game_state.world = world
        self.entity_manager = EntityManager(self.game_state)
        self.spell_manager = SpellManager(self.game_state, self.entity_manager)
        self.input_manager = InputManager(self.game_state, self.entity_manager)
        self.ui_renderer = UIRenderer(self.game_state)

        # Состояние UI
        self.show_ui = True
        self.keys_pressed = set()

        # Для хранения позиции мыши
        self.mouse_x = SCREEN_WIDTH // 2
        self.mouse_y = SCREEN_HEIGHT // 2
        self.game_state.cursor_x = self.mouse_x
        self.game_state.cursor_y = self.mouse_y

        # Установка начальной позиции
        self.set_player_position(50, 150)

        # Инициализация системы заклинаний
        self.setup_spell_system()

    def setup_spell_system(self):
        """Настройка системы заклинаний"""
        # Элементальный круг
        self.game_state.elemental_circle = ElementalCircle()

        # Система заклинаний
        self.game_state.spell_system = SpellSystem(self.game_state.elemental_circle)
        self.game_state.spell_manager = self.spell_manager
        self.input_manager.spell_manager = self.spell_manager

        # Установка игрока
        self.game_state.player = self.player

        # Дефолтный посох
        self.game_state.current_staff = BASIC_STAFF
        self.game_state.shoot_cooldown = BASIC_STAFF.delay

        # Спрайт посоха
        if self.game_state.current_staff.sprite_path:
            self.game_state.staff_sprite = arcade.Sprite(
                self.game_state.current_staff.sprite_path,
                scale=2
            )
            self.entity_manager.staff_sprite_list.append(self.game_state.staff_sprite)

        # Инициализация UI
        self.ui_renderer.setup()

    def set_player_position(self, world_x, world_y):
        screen_x = world_x * 4  # cell_size = 4
        screen_y = world_y * 4

        # Игрок всегда в центре экрана
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        # Камера смещается так, чтобы мировая позиция была в центре
        self.camera_x = screen_x - SCREEN_WIDTH // 2
        self.camera_y = screen_y - SCREEN_HEIGHT // 2

    def on_update(self, delta_time):
        # Обновление камеры (как в оригинале)
        self.update_camera()

        # Физика прыжка (как в оригинале)
        if not self.is_something_below() or self.just_jumped:
            total_velocity = self.jump_velocity - self.gravity_speed
            self.player.center_y += total_velocity
            self.jump_velocity = max(0, self.jump_velocity - 2)
            self.just_jumped = False
        else:
            self.jump_velocity = 0

        # Обновление движения игрока
        self.update_player_movement(delta_time)

        # Обновление FPS счетчика
        self.fps_timer += delta_time
        self.fps_counter += 1
        if self.fps_timer >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_timer = 0
            self.fps_counter = 0

        # Физика мира
        if self.physics_enabled:
            self.physics_timer += delta_time * self.physics_speed
            while self.physics_timer >= self.physics_update_rate:
                self._update_physics(self.physics_update_rate)
                self.physics_timer -= self.physics_update_rate

        # Обновление видимых веществ
        self._update_visible_substances()
        self.update_shape_list()

        # Обновление игрока
        self.player.update(delta_time, self.keys_pressed)

        # Обновление системы заклинаний
        self.entity_manager.update(delta_time)
        self.spell_manager.update(delta_time)
        self.ui_renderer.update(delta_time)
        self.game_state.current_fps = int(1.0 / delta_time) if delta_time > 0 else 0

    def update_player_movement(self, delta_time):
        dx = 0
        dy = 0

        # ТОЧНО КАК В ОРИГИНАЛЕ - проверки столкновений и движение
        if arcade.key.W in self.keys_pressed and not self.is_something_above():
            dy += self.player.witch_speed
        if arcade.key.S in self.keys_pressed and not self.is_something_below():
            dy -= self.player.witch_speed
        if arcade.key.A in self.keys_pressed and not self.is_something_on_left():
            dx -= self.player.witch_speed
        if arcade.key.D in self.keys_pressed and not self.is_something_on_right():
            dx += self.player.witch_speed

        self.player.center_x += dx
        self.player.center_y += dy

    def update_camera(self):
        """Обновление камеры (как в оригинале)"""
        old_camera_x = self.camera_x
        old_camera_y = self.camera_y

        # Камера следует за игроком
        self.camera_x = self.player.center_x - SCREEN_WIDTH // 2
        self.camera_y = self.player.center_y - SCREEN_HEIGHT // 2

    def on_draw(self):
        self.clear()

        # Фон
        self.background_list.draw()

        # Вещества мира
        if self.shape_list:
            self.shape_list.draw()

        # Игрок
        self.player.draw()

        # Заклинания
        self.spell_manager.draw()

        # UI интерфейс (если включен)
        if self.show_ui:
            self.ui_renderer.draw()

            # Дополнительная информация (как в оригинале)
            arcade.draw_text(
                f"FPS: {self.current_fps}",
                10, SCREEN_HEIGHT - 30,
                arcade.color.YELLOW, 16
            )
            arcade.draw_text(
                f"На земле: {self.jump_velocity}, {self.is_something_below()}",
                10, SCREEN_HEIGHT - 50,
                arcade.color.YELLOW, 16
            )

            # Дополнительная информация о заклинаниях
            arcade.draw_text(
                f"Веществ: {len(self.world)} | На экране: {len(self.current_substances)}",
                10, SCREEN_HEIGHT - 70,
                arcade.color.LIGHT_GRAY, 12
            )


    def on_key_press(self, key, modifiers):
        # Обработка ввода через InputManager для заклинаний
        self.input_manager.on_key_press(key, modifiers)

        # Движение платформера (как в оригинале)
        if key in [arcade.key.A, arcade.key.S, arcade.key.D]:
            self.keys_pressed.add(key)

        # Прыжок (как в оригинале)
        if key == arcade.key.SPACE:
            if self.is_something_below():
                self.jump_velocity = self.jump_power
                self.just_jumped = True

        # Переключение UI
        if key == arcade.key.U:
            self.show_ui = not self.show_ui

        # Выход в меню (как в оригинале)
        if key == arcade.key.ESCAPE:
            from view import StartMenuView
            self.window.show_view(StartMenuView())

    def on_key_release(self, key, modifiers):
        # Обработка отпускания клавиш через InputManager
        self.input_manager.on_key_release(key, modifiers)

        # Управление движением (как в оригинале)
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            self.keys_pressed.discard(key)

    def on_mouse_press(self, x, y, button, modifiers):
        # Обновляем позицию мыши
        self.mouse_x = x
        self.mouse_y = y
        self.game_state.cursor_x = x
        self.game_state.cursor_y = y

        # Обработка мыши через InputManager
        self.input_manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        # Обновление позиции курсора
        self.mouse_x = x
        self.mouse_y = y
        self.game_state.cursor_x = x
        self.game_state.cursor_y = y

        # Обработка движения мыши через InputManager
        self.input_manager.on_mouse_motion(x, y, dx, dy)

    def on_show_view(self):
        """Вызывается при показе View"""
        if self.window:
            self.window.set_mouse_visible(False)

    def on_hide_view(self):
        """Вызывается при скрытии View"""
        if self.window:
            self.window.set_mouse_visible(True)

    # МЕТОДЫ ПРОВЕРКИ СТОЛКНОВЕНИЙ - ТОЧНЫЕ КОПИИ ИЗ ОРИГИНАЛЬНОГО integrated_game.py
    def is_something_above(self):
        cx, cy = self.player.center_x, self.player.center_y
        world_x = int((cx + self.camera_x) // 4)  # cell_size = 4
        world_y = int((cy + self.camera_y) // 4)

        head_y = world_y + 8

        left_side = world_x - 5
        right_side = world_x + 5

        for x in range(left_side, right_side + 1):
            if (x, head_y + 1) in self.world:
                return True

        return False

    def is_something_below(self):
        cx, cy = self.player.center_x, self.player.center_y
        world_x = int((cx + self.camera_x) // 4)  # cell_size = 4
        world_y = int((cy + self.camera_y) // 4)

        foot_y = world_y - 11

        for dx in range(-5, 6):
            if (world_x + dx, foot_y) in self.world:
                return True
        return False

    def is_something_on_right(self):
        cx, cy = self.player.center_x, self.player.center_y
        world_x = int((cx + self.camera_x) // 4)  # cell_size = 4
        world_y = int((cy + self.camera_y) // 4)

        top_y = world_y + 8
        bottom_y = world_y - 8

        right_side = world_x + 5

        for y in range(bottom_y, top_y + 1):
            if (right_side + 1, y) in self.world:
                return True

        return False

    def is_something_on_left(self):
        cx, cy = self.player.center_x, self.player.center_y
        world_x = int((cx + self.camera_x) // 4)  # cell_size = 4
        world_y = int((cy + self.camera_y) // 4)

        top_y = world_y + 8
        bottom_y = world_y - 8

        left_side = world_x - 7

        for y in range(bottom_y, top_y + 1):
            if (left_side - 1, y) in self.world:
                return True

        return False