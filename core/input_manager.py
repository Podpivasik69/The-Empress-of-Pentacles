# core/input_manager.py - система ввода
import arcade
import math
import random
from constants import *
from staff import BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF


class InputManager:
    def __init__(self, game_state, entity_manager, spell_manager=None):
        self.game_state = game_state
        self.entity_manager = entity_manager
        self.spell_manager = spell_manager

    def on_key_press(self, key, modifiers):
        # передаем управление игроку
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            if not self.game_state.movement_locked and self.game_state.player.health.is_alive:
                self.game_state.keys_pressed.add(key)
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
            selected_spell_name = self.game_state.spell_system.select_spell_slot(0)
            self.game_state.active_spell = selected_spell_name

        if key == arcade.key.KEY_2:
            selected_spell_name = self.game_state.spell_system.select_spell_slot(1)
            self.game_state.active_spell = selected_spell_name

        if key == arcade.key.KEY_3:
            selected_spell_name = self.game_state.spell_system.select_spell_slot(2)
            self.game_state.active_spell = selected_spell_name

        if key == arcade.key.KEY_4:
            selected_spell_name = self.game_state.spell_system.select_spell_slot(3)
            self.game_state.active_spell = selected_spell_name

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
            print(f'здоровье игрока {self.game_state.player.health.current_health}')
            if died:
                print("ты здох")
                self.game_state.player_should_die = True

        if key == arcade.key.F4:
            print('F4')
            self.game_state.player.take_health(10)
            print(f'здоровье игрока {self.game_state.player.health.current_health}')

        if key == arcade.key.F5:
            print('F5')
            self.game_state.player.spend_mana(10)
            print(f'мана игрока игрока {self.game_state.player.mana.current_mana}')

        #     гримуар кнопки
        if self.game_state.is_tab_pressed and self.game_state.grimoire:
            if key == arcade.key.F6:
                print('F6')
                self.game_state.grimoire.prev_spread()
                return True  # выполнено
            elif key == arcade.key.F7:
                print("F7")
                self.game_state.grimoire.next_spread()
                return True

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            if key in self.game_state.keys_pressed:
                self.game_state.keys_pressed.remove(key)
        elif key in self.game_state.keys_pressed:
            self.game_state.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if not self.game_state.player.health.is_alive:
            print("Игрок мертв, нельзя стрелять")
            return
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

            # двойная система перезарядки
            active_spell = self.game_state.active_spell
            if active_spell and self.game_state.spell_system:
                # проверка кд заклинания
                if active_spell not in self.game_state.spell_system.spell_ready:
                    remaining = self.game_state.spell_system.spell_reload_timers.get(active_spell, 0)
                    print(f"спел {active_spell} перезаряжается. Жди еще: {remaining:.1f}с")
                    return
            if self.game_state.player.can_cast_spell(active_spell):
                mana_cost = SPELL_DATA.get(active_spell, {}).get("mana_cost", 0)
                self.game_state.player.spend_mana(mana_cost)
            else:
                print('не хватает маны')
                return

            self.game_state.want_to_shoot = True
            self.game_state.shoot_target_x = x
            self.game_state.shoot_target_y = y

            print(f"хочу выстрел хочу выстрел: {self.game_state.active_spell}")

            # мировые координаты кончика посоха
            start_world_x, start_world_y = self.entity_manager.get_staff_position()
            # мировые координаты цели, курсора
            if self.game_state.camera_manager:
                target_world_x, target_world_y = self.game_state.camera_manager.screen_to_world(x, y)
            else:
                target_world_x, target_world_y = x, y

            print(f"экранные координаты мышки: ({x}, {y})")
            print(f"мировые координаты цели: ({target_world_x:.1f}, {target_world_y:.1f})")
            print(f"мировые координаты посоха: ({start_world_x:.1f}, {start_world_y:.1f})")

            self.game_state.spell_manager.create_shoot(
                spell_id=active_spell,
                start_x=start_world_x,  # мировые координаты начала
                start_y=start_world_y,  # мировые координаты начала
                target_x=target_world_x,  # мировые координаты цели
                target_y=target_world_y  # мировые координаты цели
            )

            # перезарядка заклинания
            reload_time = SPELL_DATA[active_spell]["reload_time"]
            self.game_state.spell_system.spell_reload_timers[active_spell] = reload_time
            self.game_state.spell_system.spell_ready.discard(active_spell)
            print(f"заклинания {active_spell} перезаряжается, осталось {reload_time}")
            # перезарядка посоха
            self.game_state.can_shoot = False
            self.game_state.shoot_timer = self.game_state.current_staff.delay
            print(
                f"посох {self.game_state.current_staff.name} перезаряжается, осталось {self.game_state.current_staff.delay}")

    def on_mouse_motion(self, x, y, dx, dy):
        self.game_state.cursor_x = x
        self.game_state.cursor_y = y
        if self.game_state.is_tab_pressed:
            self.game_state.elemental_circle.update_hover(x, y)
