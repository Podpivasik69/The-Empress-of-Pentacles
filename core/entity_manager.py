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

        if not self.game_state.can_shoot:
            self.game_state.shoot_timer -= delta_time
            if self.game_state.shoot_timer <= 0:
                self.game_state.can_shoot = True
                self.game_state.shoot_timer = 0.0
                print('задержка посоха окончена')

        if self.game_state.player:
            self.game_state.player.update(delta_time)
        for enemy in self.game_state.enemies:
            enemy.update(delta_time)

        if self.game_state.wants_to_change_staff:
            self.switch_staff()
            self.game_state.wants_to_change_staff = False

        self.update_staff_position()
        if self.game_state.spell_system:
            self.game_state.spell_system.update(delta_time)

    def draw(self):
        """ Отрисовка всего """
        if self.game_state.player:
            self.game_state.player.draw()

        self.enemy_sprites.draw()
        self.staff_sprite_list.draw()

    def switch_staff(self):
        """ Переключение посоха P """
        staffs = [BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF]
        if self.game_state.current_staff not in staffs:
            self.game_state.current_staff = BASIC_STAFF
            current_index = 0
        else:
            current_index = staffs.index(self.game_state.current_staff)

        old_staff = self.game_state.current_staff
        old_delay = old_staff.delay if old_staff else 0.5

        # следующий посох (по кругу пустили)
        next_index = (current_index + 1) % len(staffs)
        new_staff = staffs[next_index]
        new_delay = new_staff.delay

        if not self.game_state.can_shoot and self.game_state.shoot_timer > 0:
            # вычисляем процент оставшегося времени
            if old_delay > 0:
                remaining_ratio = self.game_state.shoot_timer / old_delay
            else:
                remaining_ratio = 0
            # применяем процент
            self.game_state.shoot_timer = remaining_ratio * new_delay
            if self.game_state.shoot_timer <= 0:
                self.game_state.can_shoot = True
                self.game_state.shoot_timer = 0.0
            elif self.game_state.shoot_timer > new_delay:
                self.game_state.shoot_timer = new_delay

            print(
                f" корректировка: {old_delay:.1f}с → {new_delay:.1f}с, осталось {self.game_state.shoot_timer:.1f}с")

        self.game_state.current_staff = new_staff
        self.game_state.shoot_cooldown = new_delay

        if self.game_state.current_staff.sprite_path:
            self.game_state.staff_sprite = arcade.Sprite(self.game_state.current_staff.sprite_path, scale=2)
            self.game_state.staff_sprite.center_x = 0
            self.game_state.staff_sprite.center_y = -self.game_state.staff_sprite.height / 3

            self.staff_sprite_list.clear()
            self.staff_sprite_list.append(self.game_state.staff_sprite)
        else:
            self.game_state.staff_sprite = None
            self.staff_sprite_list.clear()

        print(f"Посох: {self.game_state.current_staff.name}")

    def update_staff_position(self):
        if not self.game_state.staff_sprite:
            return

        if not self.game_state.player:
            return

        if not self.game_state.current_staff:
            return

        # Смещение относительно центра ГГ
        # staff_x = self.player.center_x + 25  # в правой руке
        # staff_y = self.player.center_y - 10  # немного ниже центра

        # новая система с привязкой смещения к конкретному посоху
        staff_x = self.game_state.player.center_x + self.game_state.current_staff.grip_offset_x
        staff_y = self.game_state.player.center_y + self.game_state.current_staff.grip_offset_y
        # Смещаем посох ВВЕРХ, чтобы точка хвата (1/3 снизу) была в позиции staff_y
        # Если anchor в центре спрайта, а нужно на 1/3 снизу:
        # Смещение = (высота/2) - (высота/3) = высота/6
        vertical_offset = self.game_state.staff_sprite.height / 6

        self.game_state.staff_sprite.center_x = staff_x
        self.game_state.staff_sprite.center_y = staff_y + vertical_offset

        dx = self.game_state.cursor_x - self.game_state.player.center_x
        dy = self.game_state.cursor_y - self.game_state.player.center_y
        # нормирование угла
        raw_angle = -math.degrees(math.atan2(dy, dx)) - 270
        angle = raw_angle % 360
        self.game_state.staff_sprite.angle = angle
