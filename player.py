from constants import *
import monsters
import arcade
import random
import math
import json
import os


class Player:
    def __init__(self):
        self.player = None
        self.player_sprite_list = None
        # текстуры
        self.player_anim_static_textures = []

        # ходить
        self.is_moving = False
        self.movement_locked = False
        self.witch_speed = 300

        # таймеры для анимаций
        self.idle_timer = 0.0
        self.animation_frame_timer = 0.0
        self.current_animation_frame = 0
        self.is_idle_animating = False

        # система здоровья новая
        self.player_max_health = 100
        self.player_health = self.player_max_health  # текущее здоровье = максимальное при запуске
        self.is_player_alive = True

        self.player_max_mana = 100
        self.player_mana = self.player_max_mana

    def setup(self):
        for i in range(1, 5):
            texture = arcade.load_texture(f'media/witch/Wizard_static_anim{i}.png')
            self.player_anim_static_textures.append(texture)

        self.player_sprite_list = arcade.SpriteList()

        self.player = arcade.Sprite('media/witch/Wizard_static2.png', scale=1.5)
        self.static_texture = arcade.load_texture('media/witch/Wizard_static2.png')

        self.player.texture = self.static_texture
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.player_sprite_list.append(self.player)

    def update(self, delta_time, keys_pressed=None):
        # Движение героя
        dx, dy = 0, 0
        if not self.movement_locked:
            if not self.movement_locked and keys_pressed:
                if arcade.key.A in keys_pressed:
                    dx -= self.witch_speed * delta_time
            if not self.movement_locked and keys_pressed:
                if arcade.key.D in keys_pressed:
                    dx += self.witch_speed * delta_time
            if not self.movement_locked and keys_pressed:
                if arcade.key.W in keys_pressed:
                    dy += self.witch_speed * delta_time
            if not self.movement_locked and keys_pressed:
                if arcade.key.S in keys_pressed:
                    dy -= self.witch_speed * delta_time

        # Нормализация диагонального движения
        if dx != 0 and dy != 0:
            factor = 0.7071  # ≈ 1/√2
            dx *= factor
            dy *= factor

        self.player.center_x += dx
        self.player.center_y += dy

        self.player.center_x = max(20, min(SCREEN_WIDTH - 20, self.player.center_x))
        self.player.center_y = max(20, min(SCREEN_HEIGHT - 20, self.player.center_y))

        # если мы идем то таймер 0, флаги
        if dx != 0 or dy != 0:
            self.idle_timer = 0
            self.is_moving = True
            self.is_idle_animating = False
        # если стоим то таймер растер
        else:
            self.idle_timer += delta_time
            self.is_moving = False
        # если мы стоим И СТОИМ ДОЛЬШЕ 1 СЕКУНДЫ
        if self.idle_timer >= 1.0 and self.is_moving == False:
            self.is_idle_animating = True
            self.animation_frame_timer += delta_time

        if self.is_idle_animating:
            if self.animation_frame_timer >= 0.2:
                self.current_animation_frame = (self.current_animation_frame + 1) % 4
                self.animation_frame_timer = 0
                # меняем текстурку
                self.player.texture = self.player_anim_static_textures[self.current_animation_frame]
        if not self.is_player_alive:
            return

    def take_damage(self, amount):
        if self.is_player_alive and amount > 0:
            self.player_health = max(0, self.player_health - amount)
            # self.health_bar.set_health(self.player_health)
            if self.player_health <= 0:
                self.is_player_alive = False
                # self._on_player_death()
                return True
            return False

    # def spend_mana(self, amount):
    #     if amount > 0:
    #         self.player_mana =

    def take_health(self, amount):
        if self.is_player_alive and amount > 0:
            self.player_health = min(self.player_max_health, self.player_health + amount)
            # self.health_bar.set_health(self.player_health)

    def draw(self):
        self.player_sprite_list.draw()

    @property
    def health(self):
        return self.player_health

    @property
    def max_health(self):
        return self.player_max_health

    @property
    def center_x(self):
        return self.player.center_x if self.player else SCREEN_WIDTH // 2

    @center_x.setter
    def center_x(self, value):
        if self.player:
            self.player.center_x = value

    @property
    def center_y(self):
        return self.player.center_y if self.player else SCREEN_HEIGHT // 2

    @center_y.setter
    def center_y(self, value):
        if self.player:
            self.player.center_y = value

    @property
    def sprite(self):
        """Альтернативное имя для совместимости"""
        return self.player
