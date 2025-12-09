import math

from constants import *
import arcade
from projectile import Projectile
from staff import BASIC_STAFF
from staff import BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player = None
        self.player_sprite_list = None
        self.staff_sprite = None

        # текстуры
        self.player_anim_static_textures = []
        self.current_texture = 0
        self.animation_taimer = 0
        # ходить
        self.is_moving = False
        self.witch_speed = 300
        self.keys_pressed = set()
        # таймеры для анимаций
        self.idle_timer = 0.0
        self.animation_frame_timer = 0.0
        self.current_animation_frame = 0
        self.is_idle_animating = False

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

        self.current_staff = BASIC_STAFF  # дефолт посох
        self.staff_sprite_list = arcade.SpriteList()
        self.crosshair_list = arcade.SpriteList()
        self.shoot_cooldown = self.current_staff.cooldown
        # self.shoot_timer = 0.0
        # self.can_shoot = True

    def setup(self):
        # выключаем видимость системного курсора
        self.window.set_mouse_visible(False)
        self.crosshair = arcade.Sprite('media/staffs/crosshair.png', scale=1.0)
        self.crosshair.center_x = SCREEN_WIDTH // 2
        self.crosshair.center_y = SCREEN_HEIGHT // 2
        self.crosshair_list.append(self.crosshair)

        for i in range(1, 5):
            texture = arcade.load_texture(f'media/witch/Wizard_static_anim{i}.png')
            self.player_anim_static_textures.append(texture)

        self.player_sprite_list = arcade.SpriteList()

        self.player = arcade.Sprite('media/witch/Wizard_static2.png', scale=1.5)
        self.static_texture = arcade.load_texture('media/witch/Wizard_static2.png')
        self.slot_highlight = arcade.load_texture("media/slot_highlight.png")
        self.quickbar = arcade.load_texture('media/Quickbar.png')
        self.player.texture = self.static_texture
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.player_sprite_list.append(self.player)
        # заклинания
        self.spell_icons = {
            "fire_spark": arcade.load_texture("media/placeholder_icon.png"),
            "fireball": arcade.load_texture("media/fireball_icon.png"),
            "sun_strike": arcade.load_texture('media/placeholder_icon.png'),

            "splashing_water": arcade.load_texture("media/placeholder_icon.png"),
            "waterball": arcade.load_texture("media/waterball_icon.png"),
            "water_cannon": arcade.load_texture("media/placeholder_icon.png")

        }
        if self.current_staff.sprite_path:
            self.staff_sprite = arcade.Sprite(self.current_staff.sprite_path, scale=2)
            self.staff_sprite_list.clear()
            self.staff_sprite_list.append(self.staff_sprite)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        if key == arcade.key.UP:
            if len(self.spell_combo) < self.max_spell:
                self.spell_combo.append("UP")
                self.combo_timer = 0.0
                print(f"Комбо: {self.spell_combo}")
            else:
                print(f"Максимум {self.max_spell} стрелки")

        if key == arcade.key.DOWN:
            if len(self.spell_combo) < self.max_spell:
                self.spell_combo.append("DOWN")
                self.combo_timer = 0.0
                print(f"Комбо: {self.spell_combo}")
            else:
                print(f"Максимум {self.max_spell} стрелки")
        if key == arcade.key.LEFT:
            if len(self.spell_combo) < self.max_spell:
                self.spell_combo.append("LEFT")
                self.combo_timer = 0.0
                print(f"Комбо: {self.spell_combo}")
            else:
                print(f"Максимум {self.max_spell} стрелки")
        if key == arcade.key.RIGHT:
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
                if first_element == "UP":
                    element = "fire"
                elif first_element == "LEFT":
                    element = "water"
                else:
                    element = "unknown"

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
                    self.ready_spells.append(self.casted_spell)
                    print(f'в квик бар добавлено заклинание {self.casted_spell} занято {len(self.ready_spells)} слотов')
                else:
                    print("квикбар полон. макс 4 спела")

                print(f"Создано заклинание: {self.casted_spell}")
                self.is_ready_to_fire = True
                self.spell_combo = []
                self.combo_timer = 0.0

        if key == arcade.key.KEY_1:
            if self.selected_spell_index == 0:
                self.selected_spell_index = -1
                self.active_spell = None
                print("Слот 1 отменен")
            else:
                if 0 < len(self.ready_spells):
                    self.selected_spell_index = 0
                    self.active_spell = self.ready_spells[0]
                    print("Выбран слот 1")
                else:
                    print("Слот 1 пуст")
        if key == arcade.key.KEY_2:
            if self.selected_spell_index == 1:
                self.selected_spell_index = -1
                self.active_spell = None
                print("Слот 2 отменен")
            else:
                if 0 < len(self.ready_spells):
                    self.selected_spell_index = 1
                    self.active_spell = self.ready_spells[1]
                    print("Выбран слот 2")
                else:
                    print("Слот 2 пуст")
        if key == arcade.key.KEY_3:
            if self.selected_spell_index == 2:
                self.selected_spell_index = -1
                self.active_spell = None
                print("Слот 3 отменен")
            else:
                if 0 < len(self.ready_spells):
                    self.selected_spell_index = 2
                    self.active_spell = self.ready_spells[2]
                    print("Выбран слот 3")
                else:
                    print("Слот 3 пуст")
        if key == arcade.key.KEY_4:
            if self.selected_spell_index == 3:
                self.selected_spell_index = -1
                self.active_spell = None
                print("Слот 4 отменен")
            else:
                if 0 < len(self.ready_spells):
                    self.selected_spell_index = 3
                    self.active_spell = self.ready_spells[3]
                    print("Выбран слот 4")
                else:
                    print("Слот 4 пуст")
        if key == arcade.key.P:
            staffs = [BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF]
            current_index = staffs.index(self.current_staff) if self.current_staff in staffs else 0

            # Следующий посох (по кругу)
            next_index = (current_index + 1) % len(staffs)
            self.current_staff = staffs[next_index]
            if self.current_staff.sprite_path:
                self.staff_sprite = arcade.Sprite(
                    self.current_staff.sprite_path,
                    scale=2,
                    center_x=0,
                    center_y=-self.staff_sprite.height / 3  # смещаем anchor вниз
                )
                self.staff_sprite_list.clear()
                self.staff_sprite_list.append(self.staff_sprite)
            else:
                self.staff_sprite = None
                self.staff_sprite_list.clear()

            # Обновить cooldown
            self.shoot_cooldown = self.current_staff.cooldown
            print(
                f"Посох: {self.current_staff.name}, КД: {self.current_staff.cooldown}с, Разброс: {self.current_staff.spread_angle}°")

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_press(self, x, y, button, modifiers):
        # нажал лкм
        if button == arcade.MOUSE_BUTTON_LEFT:
            # если снаряд существует
            if self.active_spell is not None:
                # пока что стартовая точка - координаты игрока
                # TODO модификаторы изменения точки расположения снаряда

                if self.can_shoot:

                    spread = self.current_staff.spread_angle  # угол разброса
                    # стрельба
                    start_x = self.player.center_x
                    start_y = self.player.center_y
                    projectile = Projectile(
                        spell_type=self.active_spell,
                        start_x=start_x,
                        start_y=start_y,
                        target_x=self.crosshair.center_x,
                        target_y=self.crosshair.center_y,
                        spread_angle=spread
                    )

                    self.active_projectiles.append(projectile)
                    # типо после выстрела ты не можещь стрелять и идет кд
                    self.can_shoot = False
                    self.shoot_timer = self.shoot_cooldown

                    print(f"Выстрел: {self.active_spell} в ({x}, {y}), КД: {self.shoot_cooldown}")

                else:
                    print(f'ПЕРЕЗАРЯДКА {self.shoot_cooldown}')

            else:
                print("Нет выбранного заклинания! Выберите слот 1-4")

    def on_mouse_motion(self, x, y, dx, dy):
        self.crosshair.center_x = x
        self.crosshair.center_y = y

    def on_update(self, delta_time):

        if self.is_moving:
            self.player.texture = self.static_texture
        # Движение героя
        dx, dy = 0, 0
        if arcade.key.A in self.keys_pressed:
            dx -= self.witch_speed * delta_time
        if arcade.key.D in self.keys_pressed:
            dx += self.witch_speed * delta_time
        if arcade.key.W in self.keys_pressed:
            dy += self.witch_speed * delta_time
        if arcade.key.S in self.keys_pressed:
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
        if self.staff_sprite:
            # Смещение относительно центра ГГ
            # staff_x = self.player.center_x + 25  # в правой руке
            # staff_y = self.player.center_y - 10  # немного ниже центра

            # новая система с привязкой смещения к конкретному посоху
            staff_x = self.player.center_x + self.current_staff.grip_offset_x
            staff_y = self.player.center_y + self.current_staff.grip_offset_y
            # Смещаем посох ВВЕРХ, чтобы точка хвата (1/3 снизу) была в позиции staff_y
            # Если anchor в центре спрайта, а нужно на 1/3 снизу:
            # Смещение = (высота/2) - (высота/3) = высота/6
            vertical_offset = self.staff_sprite.height / 6

            self.staff_sprite.center_x = staff_x
            self.staff_sprite.center_y = staff_y + vertical_offset

        dx = self.crosshair.center_x - self.player.center_x
        dy = self.crosshair.center_y - self.player.center_y
        angle = -math.degrees(math.atan2(dy, dx)) - 270

        if self.staff_sprite:
            self.staff_sprite.angle = angle

    def on_draw(self):
        self.clear()
        self.player_sprite_list.draw()
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
                    arcade.draw_texture_rect(
                        self.spell_icons[spell],
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
        # рисуем спелы
        for projectile in self.active_projectiles:
            projectile.draw()
