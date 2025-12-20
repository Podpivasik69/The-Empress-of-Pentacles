# core/entity_manager.py - система управления сущностями
from staff import BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF
from projectile import SunStrikeProjectile, Projectile
from constants import *
from staff import *
import random
import arcade
import math


class EntityManager:
    def __init__(self, game_state):
        self.game_state = game_state

        self.staff_sprite = None

        self.enemy_sprites = arcade.SpriteList(use_spatial_hash=True)
        self.staff_sprite_list = arcade.SpriteList()

    def update(self, delta_time):
        """ Логика обновления всего """
        if self.game_state.player:
            self.game_state.player.update(delta_time)
        for enemy in self.game_state.enemies:
            enemy.update(delta_time)

        if self.game_state.wants_to_change_staff:
            self.switch_staff()
            self.game_state.wants_to_change_staff = False

    def draw(self):
        """ Отрисовка всего """
        if self.game_state.player:
            self.game_state.player.draw()

    def switch_staff(self):
        """ Переключение посоха P """
        staffs = [BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF]
        current_index = staffs.index(
            self.game_state.current_staff) if self.game_state.current_staff in staffs else 0

        # следующий посох (по кругу пустили)
        next_index = (current_index + 1) % len(staffs)
        self.game_state.current_staff = staffs[next_index]
        if self.game_state.current_staff.sprite_path:
            self.game_state.staff_sprite = arcade.Sprite(self.game_state.current_staff.sprite_path, scale=2)
            self.game_state.staff_sprite.center_x = 0
            self.game_state.staff_sprite.center_y = -self.game_state.staff_sprite.height / 3

            self.game_state.staff_sprite_list.clear()
            self.game_state.staff_sprite_list.append(self.game_state.staff_sprite)
        else:
            self.game_state.staff_sprite = None
            self.game_state.staff_sprite_list.clear()

        # Обновить cooldown
        self.game_state.shoot_cooldown = self.game_state.current_staff.delay
        print(
            f"Посох: {self.game_state.current_staff.name}")
