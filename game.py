from staff import BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF
from elemental_circle import ElementalCircle
from ui_components import HealthBar
from projectile import Projectile
from monsters import BaseEnemie
from player import Player
from constants import *
import monsters
import arcade
import random
import math
import json
import os


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ASH_GREY)
        # создание игрока и его кнопок
        self.player = Player()
        self.keys_pressed = set()

        self.staff_sprite = None
        self.show_fps = False  # счетчик фпс
        self.current_fps = 0
        # TODO сделать врагов
        # враги
        self.enemies = []  # список врагов
        self.enemy_sprites = arcade.SpriteList(use_spatial_hash=True)

        # малый алхимический круг
        self.elemental_circle = ElementalCircle()
        self.is_tab_pressed = False

        # новый красивый health bar
        self.health_bar = HealthBar(
            max_health=self.player.player_max_health,
            position=(400, 530),  # середина экрана, чуть выше квикбара
            size=(200, 20),  # размер вашего спрайта
            scale=1.0,  # или 1.5 если хотите крупнее
            frame_texture_path="media/ui/hp_progressbar.png"
        )

        # стрелять
        self.spell_combo = []  # список комбинаций клавишь
        self.combo_timer = 0.0
        self.is_ready_to_fire = False  # хочу выстрел хочу выстрел хочу выстрел
        self.spells_list = []
        self.casted_spell = None  # текущее скастованое заклинание
        self.ready_spells = []  # список скастованых готовых к стрельбе заклинаний
        self.max_spell = 3  # пока что можно делать заклинания из 3 стихий

        self.selected_spell_index = -1  # 0-3 это у нас 1-4 слоты. -1 = ничего не выбрано
        self.active_spell = None  # выбранное заклинание
        self.active_projectiles = []  # список готовых снарядов

        # self.shoot_cooldown = 0.5  # время на перезарядку посоха
        self.shoot_timer = 0.0  # задержка заклинаний
        self.can_shoot = True  # флаг, можно ли стрелять сейчас

        self.spell_reload_timers = {}  # кароче словарь для соответствия заклинаний и их времени кд
        self.spell_ready = set()  # готовые заклинания

        self.current_staff = BASIC_STAFF  # дефолт посох
        self.staff_sprite_list = arcade.SpriteList()
        self.crosshair_list = arcade.SpriteList()
        self.shoot_cooldown = self.current_staff.delay
        # self.shoot_timer = 0.0
        # self.can_shoot = True
        self._death_triggered = False

        self.spell_icons = {}  # кэш для картинок спелов
        self.spell_progressbar_sprite = arcade.Sprite('media/ui/spell_progressbar.png', scale=1.0)
        # прогресс бар
        self.spell_progress = [0.0, 0.0, 0.0, 0.0]  # прогресс шкалы прогресс бара

        # шрифт
        arcade.load_font('media/MinecraftDefault-Regular.ttf')
        self.fps_text = arcade.Text(
            "",
            0, SCREEN_HEIGHT,
            arcade.color.YELLOW,
            20,
            font_name='Minecraft Default',
            anchor_x="left",
            anchor_y="top"
        )

    def setup(self):
        # загрузка текстур игрока
        self.player.setup()
        # пугало
        enemy_target = monsters.BaseEnemie(-1, -1, 0, 400, 300, 5)
        enemy_target.setup_sprite('media/enemies/target/target.png', 2.0)
        self.enemies.append(enemy_target)
        self.enemy_sprites.append(enemy_target.sprite)

        # шрифт
        # arcade.load_font('MinecraftDefault-Regular.ttf')
        # прогресс бар
        self.hp_bar_background = arcade.Sprite('media/ui/spell_progressbar.png', )

        # выключаем видимость системного курсора
        self.window.set_mouse_visible(False)
        self.crosshair = arcade.Sprite('media/staffs/crosshair.png', scale=1.0)
        self.crosshair.center_x = SCREEN_WIDTH // 2
        self.crosshair.center_y = SCREEN_HEIGHT // 2
        self.crosshair_list.append(self.crosshair)

        self.slot_highlight = arcade.load_texture("media/slot_highlight.png")
        self.quickbar = arcade.load_texture('media/ui/Quickbar.png')
        # заклинания

        if self.current_staff.sprite_path:
            self.staff_sprite = arcade.Sprite(self.current_staff.sprite_path, scale=2)
            self.staff_sprite_list.clear()
            self.staff_sprite_list.append(self.staff_sprite)
        # кеширование
        for spell_id, spell_data in SPELL_DATA.items():
            try:
                self.spell_icons[spell_id] = arcade.load_texture(spell_data["icon"])
                print(f"Загружена иконка: {spell_id}")
            except Exception as e:
                print(f"Ошибка загрузки иконки {spell_id}: {e}")
                self.spell_icons[spell_id] = arcade.load_texture("media/placeholder_icon.png")

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            self.player.keys_pressed.add(key)

        if key == arcade.key.UP:
            element = self.elemental_circle.get_element("UP")
            if element is None:  # ← ЕСЛИ ПУСТОЙ СЛОТ
                print("Стрелка UP не назначена!")
                return
            if len(self.spell_combo) < self.max_spell:
                self.spell_combo.append("UP")
                self.combo_timer = 0.0
                print(f"Комбо: {self.spell_combo}")
            else:
                print(f"Максимум {self.max_spell} стрелки")

        if key == arcade.key.DOWN:
            element = self.elemental_circle.get_element("DOWN")
            if element is None:  # ← ЕСЛИ ПУСТОЙ СЛОТ
                print("Стрелка DOWN не назначена!")
                return
            if len(self.spell_combo) < self.max_spell:
                self.spell_combo.append("DOWN")
                self.combo_timer = 0.0
                print(f"Комбо: {self.spell_combo}")
            else:
                print(f"Максимум {self.max_spell} стрелки")
        if key == arcade.key.LEFT:
            element = self.elemental_circle.get_element("LEFT")
            if element is None:  # ← ЕСЛИ ПУСТОЙ СЛОТ
                print("Стрелка LEFT не назначена!")
                return
            if len(self.spell_combo) < self.max_spell:
                self.spell_combo.append("LEFT")
                self.combo_timer = 0.0
                print(f"Комбо: {self.spell_combo}")
            else:
                print(f"Максимум {self.max_spell} стрелки")
        if key == arcade.key.RIGHT:
            element = self.elemental_circle.get_element("RIGHT")
            if element is None:  # ← ЕСЛИ ПУСТОЙ СЛОТ
                print("Стрелка RIGHT не назначена!")
                return
            if len(self.spell_combo) < self.max_spell:
                self.spell_combo.append("RIGHT")
                self.combo_timer = 0.0
                print(f"Комбо: {self.spell_combo}")
            else:
                print(f"Максимум {self.max_spell} стрелки")

        if key == arcade.key.ENTER:
            if len(self.spell_combo) >= 1:
                combo_length = len(self.spell_combo)
                first_element = self.spell_combo[0]

                # определения типа стихии по первому элементу из каста
                # измено - определении типа стихии по алхимическому кругу
                element = self.elemental_circle.get_element(first_element)
                if element is None:
                    return

                if element == "fire":
                    if combo_length == 1:
                        self.casted_spell = "fire_spark"
                    elif combo_length == 2:
                        self.casted_spell = "fireball"
                    elif combo_length == 3:
                        self.casted_spell = "sun_strike"
                if element == "water":
                    if combo_length == 1:
                        self.casted_spell = "splashing_water"
                    elif combo_length == 2:
                        self.casted_spell = "waterball"
                    elif combo_length == 3:
                        self.casted_spell = "water_cannon"

                if len(self.ready_spells) < 4:
                    if self.casted_spell not in self.ready_spells:
                        self.ready_spells.append(self.casted_spell)
                        self.spell_ready.add(self.casted_spell)
                        print(
                            f'в квик бар добавлено заклинание {self.casted_spell} занято {len(self.ready_spells)} слотов')
                    else:
                        print(f'спел {self.casted_spell} уже есть в квикбаре!')

                else:
                    print("квикбар полон. макс 4 спела")

                print(f"Создано заклинание: {self.casted_spell}")
                self.is_ready_to_fire = True
                self.spell_combo = []
                self.combo_timer = 0.0

        # не вручную, методом
        if key == arcade.key.KEY_1:
            self._select_spell_slot(0)

        if key == arcade.key.KEY_2:
            self._select_spell_slot(1)

        if key == arcade.key.KEY_3:
            self._select_spell_slot(2)

        if key == arcade.key.KEY_4:
            self._select_spell_slot(3)
        if key == arcade.key.P:
            staffs = [BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF]
            current_index = staffs.index(self.current_staff) if self.current_staff in staffs else 0

            # следующий посох (по кругу пустили)
            next_index = (current_index + 1) % len(staffs)
            self.current_staff = staffs[next_index]
            if self.current_staff.sprite_path:
                self.staff_sprite = arcade.Sprite(self.current_staff.sprite_path, scale=2)
                self.staff_sprite.center_x = 0
                self.staff_sprite.center_y = -self.staff_sprite.height / 3

                self.staff_sprite_list.clear()
                self.staff_sprite_list.append(self.staff_sprite)
            else:
                self.staff_sprite = None
                self.staff_sprite_list.clear()

            # Обновить cooldown
            self.shoot_cooldown = self.current_staff.delay
            print(
                f"Посох: {self.current_staff.name}, КД: {self.current_staff.delay}с, Разброс: {self.current_staff.spread_angle}°")

        if key == arcade.key.TAB:
            self.is_tab_pressed = not self.is_tab_pressed  # toggle
            print(f"Режим редактирования круга: {'ВКЛ' if self.is_tab_pressed else 'ВЫКЛ'}")
        # счетчик фпс
        if key == arcade.key.F1:
            self.show_fps = not self.show_fps
            print(f"FPS display: {'ON' if self.show_fps else 'OFF'}")
        if key == arcade.key.F2:
            self.movement_locked = not self.movement_locked
            if self.movement_locked:
                self.keys_pressed.clear()
            print(f"хаждение: {'заблокировано!' if self.movement_locked else 'РАзбакировано'}")

        if key == arcade.key.F3:
            died = self.player.take_damage(10)
            if died:
                self._on_player_death()

        if key == arcade.key.F4:
            self.player.take_health(10)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            if key in self.player.keys_pressed:
                self.player.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_tab_pressed and button == arcade.MOUSE_BUTTON_LEFT:
            for direction, rect in self.elemental_circle.slot_rects.items():
                left = rect.x - rect.width / 2
                right = rect.x + rect.width / 2
                bottom = rect.y - rect.height / 2
                top = rect.y + rect.height / 2

                if left <= x <= right and bottom <= y <= top:
                    new_element = self.elemental_circle.cycle_element(direction)
                    print(f"Смена {direction} → {new_element}")
                    return
        # нажал лкм
        if button == arcade.MOUSE_BUTTON_LEFT:
            # если снаряд существует
            if self.active_spell is not None:
                # пока что стартовая точка - координаты игрока
                # TODO модификаторы изменения точки расположения снаряда

                if self.can_shoot:
                    if self.active_spell in self.spell_ready:
                        spread = self.current_staff.spread_angle  # угол разброса
                        # стрельба

                        if self.staff_sprite:
                            # вычисление угла в радианах
                            arcade_angle = self.staff_sprite.angle
                            math_angle = math.radians(90 - self.staff_sprite.angle)
                            print(f"ДЕБАГ УГЛОВ:")
                            print(f"  Посох (Arcade): {self.staff_sprite.angle:.1f}°")
                            print(f"  Преобразование: {self.staff_sprite.angle} - 90 = {self.staff_sprite.angle - 90}")
                            print(f"  Math угол (рад): {math_angle:.3f}")
                            print(f"  Math угол (град): {math.degrees(math_angle):.1f}°")
                            print(f"  Что значит {math.degrees(math_angle):.1f}° в математике:")
                            print(f"    0° = вправо, 90° = вверх, 180° = влево, 270° = вниз")

                            # примерно 3/4 от высоты
                            staff_length = self.staff_sprite.height * 0.5

                            # точка на конце посоха
                            start_x = self.staff_sprite.center_x + math.cos(math_angle) * staff_length
                            start_y = self.staff_sprite.center_y + math.sin(math_angle) * staff_length

                            # В момент выстрела (после вычисления start_x, start_y):
                            print("=== ДЕБАГ ВЫСТРЕЛА ===")
                            print(f"Посох угол (Arcade): {self.staff_sprite.angle:.1f}°")
                            print(f"Посох центр: ({self.staff_sprite.center_x:.0f}, {self.staff_sprite.center_y:.0f})")
                            print(f"Точка вылета: ({start_x:.0f}, {start_y:.0f})")
                            print(f"Курсор: ({self.crosshair.center_x:.0f}, {self.crosshair.center_y:.0f})")

                            print(f"Spread: {spread}°")

                            # ПРИМЕНЯЕМ SPREAD К УГЛУ
                            if spread > 0:
                                spread_rad = math.radians(spread)
                                math_angle += random.uniform(-spread_rad, spread_rad)
                                print(f"  Spread применен: {spread}°")
                                print(f"  Новый угол после spread: {math.degrees(math_angle):.1f}°")

                            launch_angle = math_angle
                            # точка вылета
                            print(
                                f"выстрел : ({start_x:.0f}, {start_y:.0f}), угол: {self.staff_sprite.angle:.0f}°")
                        else:
                            # Fallback на персонажа (на всякий случай)
                            start_x = self.player.center_x
                            start_y = self.player.center_y
                            launch_angle = None

                        projectile = Projectile(
                            spell_type=self.active_spell,
                            start_x=start_x,
                            start_y=start_y,
                            target_x=self.crosshair.center_x,
                            target_y=self.crosshair.center_y,
                            spread_angle=spread,
                            launch_angle=math_angle,
                        )

                        self.active_projectiles.append(projectile)
                        # типо после выстрела ты не можещь стрелять и идет кд
                        self.can_shoot = False  # задержка посоха
                        self.shoot_timer = self.current_staff.delay

                        reload_time = SPELL_DATA.get(self.active_spell, {}).get("reload_time", 3.0)
                        self.spell_reload_timers[self.active_spell] = reload_time
                        self.spell_ready.discard(self.active_spell)

                        print(
                            f"Выстрел: {self.active_spell} в ({self.crosshair.center_x:.0f}, {self.crosshair.center_y:.0f}), КД: {self.shoot_cooldown}")
                    else:
                        remaining = self.spell_reload_timers.get(self.active_spell, 0)
                        print(f"Заклинание {self.active_spell} перезаряжается! Осталось: {remaining:.1f}с")
                else:
                    print(f'Задержка посоха! Осталось: {self.shoot_timer:.1f}с')

    def on_mouse_motion(self, x, y, dx, dy):
        self.crosshair.center_x = x
        self.crosshair.center_y = y
        if self.is_tab_pressed:
            self.elemental_circle.update_hover(x, y)

    def on_update(self, delta_time):
        # персонаж
        self.player.update(delta_time)

        self.current_fps = int(1.0 / delta_time) if delta_time > 0 else 0
        if self.show_fps:
            self.fps_text.text = str(self.current_fps)
        else:
            self.fps_text.text = ""

        # стреляем спелами
        for projectile in self.active_projectiles:
            projectile.update(delta_time)
        # удаляем старье
        self.active_projectiles = [p for p in self.active_projectiles if p.is_alive]

        if not self.can_shoot:
            self.shoot_timer -= delta_time
            if self.shoot_timer <= 0:
                self.can_shoot = True
                self.shoot_timer = 0.0

        # TODO ПОЧИCТИТИТЬ
        # TODO ДАДЕЛАТЬ НЕЕЕРАБОТАЕТ
        if self.staff_sprite:
            # Смещение относительно центра ГГ
            # staff_x = self.player.center_x + 25  # в правой руке
            # staff_y = self.player.center_y - 10  # немного ниже центра

            # новая система с привязкой смещения к конкретному посоху
            staff_x = self.player.player.center_x + self.current_staff.grip_offset_x
            staff_y = self.player.player.center_y + self.current_staff.grip_offset_y
            # Смещаем посох ВВЕРХ, чтобы точка хвата (1/3 снизу) была в позиции staff_y
            # Если anchor в центре спрайта, а нужно на 1/3 снизу:
            # Смещение = (высота/2) - (высота/3) = высота/6
            vertical_offset = self.staff_sprite.height / 6

            self.staff_sprite.center_x = staff_x
            self.staff_sprite.center_y = staff_y + vertical_offset

        dx = self.crosshair.center_x - self.player.player.center_x
        dy = self.crosshair.center_y - self.player.player.center_y
        # нормирование угла
        raw_angle = -math.degrees(math.atan2(dy, dx)) - 270
        angle = raw_angle % 360

        if self.staff_sprite:
            self.staff_sprite.angle = angle

        # обновление таймеров для перезарядки заклинаний
        for spell_id in list(self.spell_reload_timers.keys()):
            self.spell_reload_timers[spell_id] -= delta_time
            if self.spell_reload_timers[spell_id] <= 0:
                del self.spell_reload_timers[spell_id]
                self.spell_ready.add(spell_id)
        # прогресс бар с привязкой к спелу
        for i, spell in enumerate(self.ready_spells):
            if i >= 4:
                break
            if spell in self.spell_reload_timers:
                remaining = self.spell_reload_timers[spell]
                total = SPELL_DATA[spell]["reload_time"]
                progress = 1.0 - (remaining / total)
                self.spell_progress[i] = max(0.0, min(1.0, progress))
            else:
                self.spell_progress[i] = 1.0
        for i in range(len(self.ready_spells), 4):
            self.spell_progress[i] = 0.0

        self.health_bar.update(delta_time)

    def on_draw(self):
        self.clear()
        # рисуем врагов
        self.enemy_sprites.draw()
        # рисуем игрока
        self.player.draw()
        # рисуем посох
        self.staff_sprite_list.draw()
        self.crosshair_list.draw()
        # отрисовка квик бара
        arcade.draw_texture_rect(self.quickbar, arcade.rect.XYWH(150, 550, 256, 64), )

        slot_positions = [(54, 550), (118, 550), (182, 550), (246, 550)]
        # квик бар
        for i, spell in enumerate(self.ready_spells):
            if i < 4:
                if spell in self.spell_icons:
                    texture = self.spell_icons[spell]
                    arcade.draw_texture_rect(
                        texture,
                        arcade.rect.XYWH(slot_positions[i][0], slot_positions[i][1], 48, 48)
                    )
        # подсветка иконок
        if 0 <= self.selected_spell_index < 4:
            highlight_x = slot_positions[self.selected_spell_index][0]
            highlight_y = slot_positions[self.selected_spell_index][1]
            arcade.draw_texture_rect(
                self.slot_highlight,
                arcade.rect.XYWH(highlight_x, highlight_y, 64, 64)
            )
        # если мы под кд
        if not self.can_shoot:
            progress = 1 - (self.shoot_timer / self.shoot_cooldown)
            bar_width = 100 * progress
            arcade.draw_rect_filled(arcade.rect.XYWH(400, 580, bar_width, 10), arcade.color.RED)
        #
        self.health_bar.draw()
        # slot_positions = [(54, 550), (118, 550), (182, 550), (246, 550)]
        #
        #

        # рисуем спелы
        for projectile in self.active_projectiles:
            projectile.draw()
        # малый алхимический круг
        self.elemental_circle.draw(is_editing=self.is_tab_pressed)
        # затепнени на таб
        if self.is_tab_pressed:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                (0, 0, 0, 120)
            )

        if self.show_fps:
            self.fps_text.draw()
        progress_bar_y = 513

        for i, spell in enumerate(self.ready_spells):
            if i >= 4:
                break
            # рисуем прогресс ьар
            slot_x = slot_positions[i][0]
            progress = self.spell_progress[i]

            if progress > 0:
                fill_width = 56 * progress
                fill_color = self.get_gradient_color(progress)

                rect = arcade.rect.XYWH(
                    slot_x - 28 + fill_width / 2,  # center_x
                    progress_bar_y,  # center_y
                    fill_width,  # width
                    6  # height
                )
                arcade.draw_rect_filled(rect, fill_color)

            self.spell_progressbar_sprite.center_x = slot_x
            self.spell_progressbar_sprite.center_y = progress_bar_y

            temp_list = arcade.SpriteList()
            temp_list.append(self.spell_progressbar_sprite)
            temp_list.draw()

    # метод для выбора слотов
    def _select_spell_slot(self, slot_index):
        if self.selected_spell_index == slot_index:
            self.selected_spell_index = -1
            self.active_spell = None
            print(f'слот {slot_index + 1} отменен')
        else:
            if slot_index < len(self.ready_spells):
                self.selected_spell_index = slot_index
                self.active_spell = self.ready_spells[slot_index]
                print(f'выбран слот {slot_index + 1}')
            else:
                print(f'слот {slot_index + 1} пустой')

    # гридиент для прогресс бара
    def get_gradient_color(self, progress):
        if progress <= 0:
            return (0, 0, 0, 0)
        if progress >= 1.0:
            return (0, 255, 0, 255)

        if progress < 0.5:
            ratio = progress * 2  # 0.0 → 1.0
            red = 255
            green = int(255 * ratio)
            blue = 0
        else:
            ratio = (progress - 0.5) * 2  # 0.0 → 1.0
            red = int(255 * (1 - ratio))
            green = 255
            blue = 0

        return (red, green, blue, 255)

    def _on_player_death(self):
        from view import DeathScreenView
        """экран смерти"""
        if hasattr(self, '_death_triggered') and self._death_triggered:
            return

        self._death_triggered = True
        print("ты сдох...")
        death_screen = DeathScreenView()
        death_screen.window = self.window
        self.window.show_view(death_screen)
