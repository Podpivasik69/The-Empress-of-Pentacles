# core/input_manager.py - система ввода
import arcade
import math
import random
from constants import *
from projectile import SunStrikeProjectile, Projectile
from staff import BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF


class InputManager:
    def __init__(self, game_state, entity_manager):
        self.game_state = game_state
        self.entity_manager = entity_manager

    def on_key_press(self, key, modifiers):
        # передаем управление игроку
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            if not self.game_state.movement_locked:
                self.game_state.player.keys_pressed.add(key)
        else:
            self.game_state.keys_pressed.add(key)

        if key == arcade.key.UP:
            if self.game_state.spell_system.add_to_combo("UP"):
                print(f"Комбо: {self.game_state.spell_system.spell_combo}")
            else:
                print(f"Максимум {self.game_state.spell_system.max_spell} стрелки")

        if key == arcade.key.DOWN:
            if self.game_state.spell_system.add_to_combo("DOWN"):
                print(f"Комбо: {self.game_state.spell_system.spell_combo}")
            else:
                print(f"Максимум {self.game_state.spell_system.max_spell} стрелки")

        if key == arcade.key.LEFT:
            if self.game_state.spell_system.add_to_combo("LEFT"):
                print(f"Комбо: {self.game_state.spell_system.spell_combo}")
            else:
                print(f"Максимум {self.game_state.spell_system.max_spell} стрелки")

        if key == arcade.key.RIGHT:
            if self.game_state.spell_system.add_to_combo("RIGHT"):
                print(f"Комбо: {self.game_state.spell_system.spell_combo}")
            else:
                print(f"Максимум {self.game_state.spell_system.max_spell} стрелки")

        if key == arcade.key.ENTER:
            spell_name = self.game_state.spell_system.create_spell_from_combo()
            if spell_name:
                success = self.game_state.spell_system.add_spell_to_quickbar(spell_name)
                if success:
                    self.game_state.spell_system.is_ready_to_fire = True
            else:
                print("Не удалось создать заклинание")

        # не вручную, методом
        if key == arcade.key.KEY_1:
            self.game_state.spell_system.select_spell_slot(0)

        if key == arcade.key.KEY_2:
            self.game_state.spell_system.select_spell_slot(1)

        if key == arcade.key.KEY_3:
            self.game_state.spell_system.select_spell_slot(2)

        if key == arcade.key.KEY_4:
            self.game_state.spell_system.select_spell_slot(3)
        if key == arcade.key.P:
            self.game_state.wants_to_change_staff = True
        if key == arcade.key.TAB:
            self.game_state.is_tab_pressed = not self.game_state.is_tab_pressed  # toggle
            print(f"Режим редактирования круга: {'ВКЛ' if self.game_state.is_tab_pressed else 'ВЫКЛ'}")
        # счетчик фпс
        if key == arcade.key.F1:
            self.game_state.show_fps = not self.game_state.show_fps
            print(f"FPS display: {'ON' if self.game_state.show_fps else 'OFF'}")
        if key == arcade.key.F2:
            self.game_state.movement_locked = not self.game_state.movement_locked
            if self.game_state.movement_locked:
                movement_keys = {arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D}
                for movement_key in movement_keys:
                    if movement_key in self.game_state.player.keys_pressed:
                        self.game_state.player.keys_pressed.remove(movement_key)
            print(f"хаждение: {'заблокировано!' if self.game_state.movement_locked else 'РАзбакировано'}")

        if key == arcade.key.F3:
            print('F3')
            died = self.game_state.player.take_damage(10)
            print(f'здоровье игрока {self.game_state.player.player_health}')
            if died:
                print("ты здох")
                self.game_state._on_player_death()

        if key == arcade.key.F4:
            print('F4')
            self.game_state.player.take_health(10)
            print(f'здоровье игрока {self.game_state.player.player_health}')

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            if key in self.game_state.player.keys_pressed:
                self.game_state.player.keys_pressed.remove(key)
        elif key in self.game_state.keys_pressed:
            self.game_state.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_state.is_tab_pressed and button == arcade.MOUSE_BUTTON_LEFT:
            for direction, rect in self.game_state.elemental_circle.slot_rects.items():
                left = rect.x - rect.width / 2
                right = rect.x + rect.width / 2
                bottom = rect.y - rect.height / 2
                top = rect.y + rect.height / 2

                if left <= x <= right and bottom <= y <= top:
                    new_element = self.game_state.elemental_circle.cycle_element(direction)
                    print(f"Смена {direction} → {new_element}")
                    return
        # нажал лкм
        if button == arcade.MOUSE_BUTTON_LEFT:
            # если снаряд существует
            if self.game_state.active_spell is None:
                print("нет активного заклинания")
                return

            # пока что стартовая точка - координаты игрока
            # TODO модификаторы изменения точки расположения снаряда

            if not self.game_state.can_shoot:
                print(f'Задержка посоха! Осталось: {self.game_state.shoot_timer:.1f}с')
                return

            self.game_state.want_to_shoot = True
            self.game_state.shoot_target_x = x
            self.game_state.shoot_target_y = y

            print(f"хочу выстрел хочу выстрел: {self.game_state.active_spell}")

    def on_mouse_motion(self, x, y, dx, dy):
        self.game_state.cursor_x = x
        self.game_state.cursor_y = y
        if self.game_state.is_tab_pressed:
            self.game_state.elemental_circle.update_hover(x, y)
