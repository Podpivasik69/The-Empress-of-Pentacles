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

        self.player = Player()
        self.player.setup()
        self.player.witch_speed = 300
        self.camera_speed = 0
        self.player_world_x = 50
        self.player_world_y = 150

        self.gravity = 0.4
        self.jump_power = 12
        self.jump_velocity = 0
        self.on_ground = True

        self.game_state = GameState()
        self.game_state.world = world
        self.entity_manager = EntityManager(self.game_state)
        self.spell_manager = SpellManager(self.game_state, self.entity_manager)
        self.input_manager = InputManager(self.game_state, self.entity_manager)
        self.ui_renderer = UIRenderer(self.game_state)

        self.show_ui = True
        self.keys_pressed = set()

        self.mouse_x = SCREEN_WIDTH // 2
        self.mouse_y = SCREEN_HEIGHT // 2
        self.game_state.cursor_x = self.mouse_x
        self.game_state.cursor_y = self.mouse_y

        self.set_player_position(50, 150)
        self.setup_spell_system()

    def setup_spell_system(self):
        self.game_state.elemental_circle = ElementalCircle()
        self.game_state.spell_system = SpellSystem(self.game_state.elemental_circle)
        self.game_state.spell_manager = self.spell_manager
        self.input_manager.spell_manager = self.spell_manager
        self.game_state.player = self.player
        self.game_state.current_staff = BASIC_STAFF
        self.game_state.shoot_cooldown = BASIC_STAFF.delay

        if self.game_state.current_staff.sprite_path:
            self.game_state.staff_sprite = arcade.Sprite(
                self.game_state.current_staff.sprite_path,
                scale=2
            )
            self.entity_manager.staff_sprite_list.append(self.game_state.staff_sprite)

        self.ui_renderer.setup()

    def set_player_position(self, world_x, world_y):
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2
        self.player_world_x = world_x
        self.player_world_y = world_y
        self.camera_x = world_x * self.cell_size - SCREEN_WIDTH // 2
        self.camera_y = world_y * self.cell_size - SCREEN_HEIGHT // 2

    def on_update(self, delta_time):
        self.update_camera()
        self.on_ground = self.is_something_below()

        if not self.on_ground:
            self.jump_velocity -= self.gravity
            if self.is_something_above() and self.jump_velocity > 0:
                self.jump_velocity = 0
            if self.jump_velocity < -20:
                self.jump_velocity = -20
        else:
            if self.jump_velocity < 0:
                self.jump_velocity = 0

        self.player_world_y += self.jump_velocity / self.cell_size
        self.update_player_movement(delta_time)

        self.fps_timer += delta_time
        self.fps_counter += 1
        if self.fps_timer >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_timer = 0
            self.fps_counter = 0

        if self.physics_enabled:
            self.physics_timer += delta_time * self.physics_speed
            while self.physics_timer >= self.physics_update_rate:
                self._update_physics(self.physics_update_rate)
                self.physics_timer -= self.physics_update_rate

        self._update_visible_substances()
        self.update_shape_list()
        self.player.update(delta_time, self.keys_pressed)

        if self.is_something_below() and (self.is_something_on_right() or self.is_something_on_left()):
            self.player_world_y += 4 / self.cell_size

        self.entity_manager.update(delta_time)
        self.spell_manager.update(delta_time)
        self.ui_renderer.update(delta_time)
        self.game_state.current_fps = int(1.0 / delta_time) if delta_time > 0 else 0

    def update_player_movement(self, delta_time):
        dx = 0
        dy = 0

        if arcade.key.A in self.keys_pressed and not self.is_something_on_left():
            dx -= self.player.witch_speed * delta_time
        if arcade.key.D in self.keys_pressed and not self.is_something_on_right():
            dx += self.player.witch_speed * delta_time

        if arcade.key.W in self.keys_pressed and not self.is_something_above():
            if self.on_ground:
                self.jump_velocity = self.jump_power
        if arcade.key.S in self.keys_pressed and not self.is_something_below():
            dy -= self.player.witch_speed * delta_time

        self.player_world_x += dx / self.cell_size
        self.player_world_y += dy / self.cell_size

    def update_camera(self):
        player_pixel_x = self.player_world_x * self.cell_size
        player_pixel_y = self.player_world_y * self.cell_size
        self.camera_x = player_pixel_x - SCREEN_WIDTH // 2
        self.camera_y = player_pixel_y - SCREEN_HEIGHT // 2
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

    def on_draw(self):
        self.clear()
        self.background_list.draw()

        if self.shape_list:
            self.shape_list.draw()

        self.player.draw()
        self.spell_manager.draw()

        if self.show_ui:
            self.ui_renderer.draw()
            arcade.draw_text(
                f"FPS: {self.current_fps}",
                10, SCREEN_HEIGHT - 30,
                arcade.color.YELLOW, 16
            )
            arcade.draw_text(
                f"Скорость: {self.jump_velocity:.1f}, На земле: {self.on_ground}",
                10, SCREEN_HEIGHT - 50,
                arcade.color.YELLOW, 16
            )
            arcade.draw_text(
                f"Веществ: {len(self.world)} | На экране: {len(self.current_substances)}",
                10, SCREEN_HEIGHT - 70,
                arcade.color.LIGHT_GRAY, 12
            )

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.A, arcade.key.S, arcade.key.D]:
            self.keys_pressed.add(key)

        if key == arcade.key.SPACE or key == arcade.key.W:
            if self.on_ground and not self.is_something_above():
                self.jump_velocity = self.jump_power

        if key == arcade.key.U:
            self.show_ui = not self.show_ui

        if key == arcade.key.ESCAPE:
            from view import StartMenuView
            self.window.show_view(StartMenuView())

        self.game_state.keys_pressed.add(key)
        self.input_manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            if key in self.keys_pressed:
                self.keys_pressed.remove(key)

        if key in self.game_state.keys_pressed:
            self.game_state.keys_pressed.remove(key)
        self.input_manager.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_x = x
        self.mouse_y = y
        self.game_state.cursor_x = x
        self.game_state.cursor_y = y
        self.input_manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        self.game_state.cursor_x = x
        self.game_state.cursor_y = y
        self.input_manager.on_mouse_motion(x, y, dx, dy)

    def on_show_view(self):
        if self.window:
            self.window.set_mouse_visible(False)

    def on_hide_view(self):
        if self.window:
            self.window.set_mouse_visible(True)

    def is_something_above(self):
        world_x = int(self.player_world_x)
        world_y = int(self.player_world_y)
        head_y = world_y + 8
        left_side = world_x - 5
        right_side = world_x + 5

        for x in range(left_side, right_side + 1):
            if (x, head_y + 1) in self.world:
                return True
        return False

    def is_something_below(self):
        world_x = int(self.player_world_x)
        world_y = int(self.player_world_y)
        foot_y = world_y - 11

        for dx in range(-5, 6):
            if (world_x + dx, foot_y) in self.world:
                return True
        return False

    def is_something_on_right(self):
        world_x = int(self.player_world_x)
        world_y = int(self.player_world_y)
        top_y = world_y + 8
        bottom_y = world_y - 8
        right_side = world_x + 5

        for y in range(bottom_y, top_y + 1):
            if (right_side + 1, y) in self.world:
                return True
        return False

    def is_something_on_left(self):
        world_x = int(self.player_world_x)
        world_y = int(self.player_world_y)
        top_y = world_y + 8
        bottom_y = world_y - 8
        left_side = world_x - 7

        for y in range(bottom_y, top_y + 1):
            if (left_side - 1, y) in self.world:
                return True
        return False