# core/entity_manager.py - система управления сущностями
from staff import BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF
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

        self.update_enemy_screen_positions()

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

    def get_staff_position(self):
        """ Этот функция вычисляет координаты точки откуда будет вылетать снаряд - кончик посоха """

        print("проверка staff_sprite...")
        if not hasattr(self.game_state, 'staff_sprite'):
            print("ошибка - в game_state нет атрибута staff_sprite")
            return (0, 0)

        if self.game_state.staff_sprite is None:
            print("ошибка -  game_state.staff_sprite равен None")
            print("посох не создан. были возвращены координаты игрока")
            if self.game_state.player:
                return (self.game_state.player.world_x, self.game_state.player.world_y)
            return (0, 0)

        # если нет игрока вернем нулевые корды
        if not self.game_state.player:
            return (0, 0)
        # получаем корды игрока мировые
        player_world_x = self.game_state.player.world_x
        player_world_y = self.game_state.player.world_y

        # если нет посоха - вернем просто координаты игрка, выстрел будет как бы из его центра
        if not self.game_state.staff_sprite:
            return (self.game_state.player.center_x, self.game_state.player.center_y)

        # полуем угол посуха в экранных кордах
        arcade_angle = self.game_state.staff_sprite.angle  # аркейд угол
        math_angle = math.radians(90 - arcade_angle)  # математический угол

        # длинна кончика посоха - 3/4 от высоты спрайта
        staff_length = self.game_state.staff_sprite.height * 0.8

        # экранные корды кончика посоха
        staff_screen_x = self.game_state.staff_sprite.center_x + math.cos(math_angle) * staff_length
        staff_screen_y = self.game_state.staff_sprite.center_y + math.sin(math_angle) * staff_length

        # конвертация экранных кордов в мировые
        if self.game_state.camera_manager:
            staff_world_x, staff_world_y = self.game_state.camera_manager.screen_to_world(
                staff_screen_x, staff_screen_y
            )
            print(f"[DEBUG] Staff position:")
            print(f"  Screen: ({staff_screen_x:.1f}, {staff_screen_y:.1f})")
            print(f"  World: ({staff_world_x:.1f}, {staff_world_y:.1f})")
            print(f"  Player world: ({player_world_x:.1f}, {player_world_y:.1f})")
            return (staff_world_x, staff_world_y)

        return (player_world_x, player_world_y)

    def get_enemies_in_hitbox(self, center_x, center_y, hitbox_width, hitbox_height):
        """ Функция для поиска врагов в хитбоксе заклинания, где center_x, center_y - координаты центра заклинания """
        # хитбокс - прямоугольник с центром с center_x, center_y, ширина/высота - hitbox_width, hitbox_height
        # TODO сделать функцию которая возращет список врагов в нужном чанке, чтобы каждый раз не искать среди абс. всех врагов
        enemy_in_spell_hitbox = []
        left = center_x - hitbox_width / 2
        right = center_x + hitbox_width / 2
        bottom = center_y - hitbox_height / 2
        top = center_y + hitbox_height / 2
        # пропускаем мертвых врагов
        for enemy in self.game_state.enemies:
            if not enemy.is_alive:
                continue

            if (left <= enemy.x <= right and
                    bottom <= enemy.y <= top):
                enemy_in_spell_hitbox.append(enemy)

        return enemy_in_spell_hitbox

    def update_enemy_screen_positions(self):
        if not self.game_state.camera_manager:
            return

        for enemy in self.game_state.enemies:
            if enemy.sprite and enemy.is_alive:
                screen_x, screen_y = self.game_state.camera_manager.world_to_screen(
                    enemy.x, enemy.y
                )
                enemy.sprite.center_x = screen_x
                enemy.sprite.center_y = screen_y
