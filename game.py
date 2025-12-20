from staff import BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF
from elemental_circle import ElementalCircle

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
        enemy_target = TrainingTarget(
            health=100,
            max_health=100,
            speed=0,
            x=400,
            y=300,
            melee_damage=5
        )
        enemy_target.setup_sprite(
            'media/enemies/target/target.png',
            scale=2.0,
            sprite_list=self.enemy_sprites
        )
        enemy_target.setup_animation()
        self.enemies.append(enemy_target)

        # шрифт
        # arcade.load_font('MinecraftDefault-Regular.ttf')
        # прогресс барф

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

    def on_update(self, delta_time):
        # персонаж
        self.player.update(delta_time)
        self.health_bar.set_health(self.player.player_health)

        for enemy in self.enemies:
            enemy.update(delta_time)

        self.current_fps = int(1.0 / delta_time) if delta_time > 0 else 0
        if self.show_fps:
            self.fps_text.text = str(self.current_fps)
        else:
            self.fps_text.text = ""

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
            staff_x = self.player.center_x + self.current_staff.grip_offset_x
            staff_y = self.player.center_y + self.current_staff.grip_offset_y
            # Смещаем посох ВВЕРХ, чтобы точка хвата (1/3 снизу) была в позиции staff_y
            # Если anchor в центре спрайта, а нужно на 1/3 снизу:
            # Смещение = (высота/2) - (высота/3) = высота/6
            vertical_offset = self.staff_sprite.height / 6

            self.staff_sprite.center_x = staff_x
            self.staff_sprite.center_y = staff_y + vertical_offset

        if self.staff_sprite:
            dx = self.crosshair.center_x - self.player.center_x
            dy = self.crosshair.center_y - self.player.center_y
            # нормирование угла
            raw_angle = -math.degrees(math.atan2(dy, dx)) - 270
            angle = raw_angle % 360
            self.staff_sprite.angle = angle

        # обновление таймеров для перезарядки заклинаний
        for spell_id in list(self.spell_system.spell_reload_timers.keys()):
            self.spell_system.spell_reload_timers[spell_id] -= delta_time
            if self.spell_system.spell_reload_timers[spell_id] <= 0:
                del self.spell_system.spell_reload_timers[spell_id]
                self.spell_system.spell_ready.add(spell_id)
        # прогресс бар с привязкой к спелу
        for i, spell in enumerate(self.spell_system.ready_spells):
            if i >= 4:
                break
            if spell in self.spell_system.spell_reload_timers:
                remaining = self.spell_system.spell_reload_timers[spell]
                total = SPELL_DATA[spell]["reload_time"]
                progress = 1.0 - (remaining / total)
                self.spell_progress[i] = max(0.0, min(1.0, progress))
            else:
                self.spell_progress[i] = 1.0
        for i in range(len(self.spell_system.ready_spells), 4):
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

        for i, spell in enumerate(self.spell_system.ready_spells):
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

            self.progressbar_spritelist.draw()

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
