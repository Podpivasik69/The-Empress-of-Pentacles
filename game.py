from staff import BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF
from monsters import BaseEnemie, TestEnemie
from elemental_circle import ElementalCircle
from spell_system import SpellSystem
from player import Player
from constants import *
import monsters
import arcade
from world import *
import random
import math
import json
import os

from core.game_state import GameState
from core.input_manager import InputManager
from core.entity_manager import EntityManager
from core.spell_manager import SpellManager
from core.ui_renderer import UIRenderer


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.ASH_GREY)

        # шрифт
        arcade.load_font('media/MinecraftDefault-Regular.ttf')

        # менеджер состояния игры
        self.game_state = GameState()
        self.game_state.world = world
        # менеджер существ
        self.entity_manager = EntityManager(self.game_state)
        # менеджер заклинаний
        self.spell_manager = SpellManager(self.game_state, self.entity_manager)
        # менеджер ввода
        self.input_manager = InputManager(self.game_state, self.entity_manager)
        # менеджер отрисовки UI
        self.ui_renderer = UIRenderer(self.game_state)

    def setup(self):
        # выключаем видимость системного курсора
        self.window.set_mouse_visible(False)

        # загрузка игрока
        player = Player()
        player.setup()
        self.game_state.player = player
        # элементальный круг
        self.game_state.elemental_circle = ElementalCircle()
        # система заклинаний
        self.game_state.spell_system = SpellSystem(self.game_state.elemental_circle)
        self.game_state.spell_manager = self.spell_manager
        self.input_manager.spell_manager = self.spell_manager

        # просто враг
        enemy_target = TestEnemie(
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
            sprite_list=self.entity_manager.enemy_sprites
        )
        self.game_state.enemies.append(enemy_target)

        # дефолтный посох, задержка
        self.game_state.current_staff = BASIC_STAFF
        self.game_state.shoot_cooldown = BASIC_STAFF.delay
        # спрайт посоха
        if self.game_state.current_staff.sprite_path:
            self.game_state.staff_sprite = arcade.Sprite(
                self.game_state.current_staff.sprite_path,
                scale=2
            )
            self.entity_manager.staff_sprite_list.append(self.game_state.staff_sprite)
        # инициализация UI
        self.ui_renderer.setup()

    def on_update(self, delta_time):
        self.entity_manager.update(delta_time)
        self.spell_manager.update(delta_time)
        self.ui_renderer.update(delta_time)
        self.game_state.current_fps = int(1.0 / delta_time) if delta_time > 0 else 0
        # обновление игрока
        if self.game_state.player:
            self.game_state.player.update(delta_time, self.game_state.keys_pressed)

        # логика смерти
        if self.game_state.player_should_die and not self.game_state.is_game_over:
            print("Игрок умер, переход на экран смерти...")
            self.game_state.is_game_over = True
            self._on_player_death()
            self.game_state.player_should_die = False

    def on_draw(self):
        self.clear()
        # рисуем сущностей
        self.entity_manager.draw()
        # рисуем спелы
        self.spell_manager.draw()
        # рисуем интерфейс
        self.ui_renderer.draw()

    def on_key_press(self, key, modifiers):
        self.input_manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.input_manager.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.input_manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.input_manager.on_mouse_motion(x, y, dx, dy)

    def _on_player_death(self):
        from view import DeathScreenView
        """экран смерти"""
        if hasattr(self, '_death_triggered') and self._death_triggered:
            return

        self._death_triggered = True
        print("ты сдох...")
        death_screen = DeathScreenView()
        self.window.show_view(death_screen)
