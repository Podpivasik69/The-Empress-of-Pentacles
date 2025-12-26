from core.components.health import Health
from core.components.mana import Mana
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
        self.player_anim_static_textures = []  # текстуры

        # ходить
        self.is_moving = False
        self.movement_locked = False
        self.witch_speed = 300

        # таймеры для анимаций
        self.idle_timer = 0.0
        self.animation_frame_timer = 0.0
        self.current_animation_frame = 0
        self.is_idle_animating = False

        # система здоровья новая, через компоненты

        self.health = Health(max_health=100, current_health=100)
        self.mana = Mana(current_mana=100, max_mana=100, regen_rate=1.0)

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

        # если мы идем, то таймер 0, флаги
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
        if not self.health.is_alive:
            return
        self.mana.regen_mana(delta_time)

    # методы для здоровья (инкапсуляция от health.py)
    def take_damage(self, amount):
        return self.health.take_damage(amount)

    def take_health(self, amount):
        return self.health.heal(amount)

    def set_max_health(self, value):
        self.health.set_max_health(value)

    def set_health(self, value):
        self.health.set_health(value)

    # методы для маны
    def spend_mana(self, amount):
        self.mana.spend_mana(amount)

    def regen_mana(self, delta_time):
        self.mana.regen_mana(delta_time)

    def set_mana(self, value):
        self.mana.set_mana(value)

    def set_max_mana(self, value):
        self.mana.set_max_mana(value)

    def can_cast_spell(self, spell_name):
        mana_cost = SPELL_DATA[spell_name].get('mana_cost', 0)
        if self.mana.current_mana >= mana_cost:
            return True
        else:
            return False

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
        return self.player

    def draw(self):
        self.player_sprite_list.draw()
