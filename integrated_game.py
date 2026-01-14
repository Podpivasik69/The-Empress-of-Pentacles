from world import WorldView
from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import arcade
from physics import *


class IntegratedWorldView(WorldView):
    def __init__(self):
        super().__init__()
        self.player = Player()
        self.player.setup()
        self.player.witch_speed = 2
        self.camera_speed = 0

        self.gravity_speed = 3
        self.gravity = True

        self.jump_velocity = 0  # скорость прыжка
        self.jump_power = 25  # сила прыжка
        self.just_jumped = False  # флаг что только что прыгнули

        self.set_player_position(50, 150)

    def set_player_position(self, world_x, world_y):
        screen_x = world_x * 4
        screen_y = world_y * 4
        self.player.center_x = 100
        self.player.center_y = 250
        self.camera_x = screen_x - SCREEN_WIDTH // 2
        self.camera_y = screen_y - SCREEN_HEIGHT // 2

    def on_update(self, delta_time):
        self.update_camera()

        if not self.is_something_below() or self.just_jumped:
            total_velocity = self.jump_velocity - self.gravity_speed
            self.player.center_y += total_velocity
            self.jump_velocity = max(0, self.jump_velocity - 2)
            self.just_jumped = False
        else:
            self.jump_velocity = 0

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

    def update_player_movement(self, delta_time):
        dx = 0
        dy = 0

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
        old_camera_x = self.camera_x
        old_camera_y = self.camera_y

        self.camera_x = self.player.center_x - SCREEN_WIDTH // 2
        self.camera_y = self.player.center_y - SCREEN_HEIGHT // 2

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        if self.shape_list:
            self.shape_list.draw()
        self.player.draw()

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

    def is_something_above(self):
        cx, cy = self.player.center_x, self.player.center_y
        world_x = int((cx + self.camera_x) // 4)
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
        world_x = int((cx + self.camera_x) // 4)
        world_y = int((cy + self.camera_y) // 4)

        foot_y = world_y - 11

        for dx in range(-5, 6):
            if (world_x + dx, foot_y) in self.world:
                return True
        return False

    def is_something_on_right(self):
        cx, cy = self.player.center_x, self.player.center_y
        world_x = int((cx + self.camera_x) // 4)
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
        world_x = int((cx + self.camera_x) // 4)
        world_y = int((cy + self.camera_y) // 4)

        top_y = world_y + 8
        bottom_y = world_y - 8

        left_side = world_x - 7

        for y in range(bottom_y, top_y + 1):
            if (left_side - 1, y) in self.world:
                return True

        return False

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.A, arcade.key.S, arcade.key.D]:
            self.keys_pressed.add(key)

        if key == arcade.key.SPACE:
            if self.is_something_below():
                self.jump_velocity = self.jump_power
                self.just_jumped = True

        if key == arcade.key.ESCAPE:
            from view import StartMenuView
            self.window.show_view(StartMenuView())

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            self.keys_pressed.discard(key)