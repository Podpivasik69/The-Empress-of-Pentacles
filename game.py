from staff import BASIC_STAFF, FAST_STAFF, POWER_STAFF, SNIPER_STAFF
from core.components.debug_renderer import DebugRenderer, DebugPanel
from elemental_circle import ElementalCircle
from monsters import BaseEnemie, TestEnemie
from spell_system import SpellSystem
from player import Player
from constants import *
from world import *
import monsters
import arcade
import random
import math
import json
import os

from core.game_state import GameState
from core.input_manager import InputManager
from core.camera_manager import CameraManager
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
        # менеджер камеры
        self.camera_manager = CameraManager(self.game_state)
        self.game_state.camera_manager = self.camera_manager
        # менеджер дебаг панелей
        self.debug_renderer = DebugRenderer(self.game_state)

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

        world_x, world_y = self.camera_manager.screen_to_world(400, 300)
        # просто враг
        enemy_target = TestEnemie(
            health=100,
            max_health=100,
            speed=0,
            x=world_x,
            y=world_y,
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

        # TODO удалить
        # мировые координаты
        self.game_state.player_world_x = 100
        self.game_state.player_world_y = 75
        self.camera_manager.follow_player(100, 75)

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

        # player_screen_x = self.game_state.player.center_x
        # player_screen_y = self.game_state.player.center_y
        # player_world_x, player_world_y = self.camera_manager.screen_to_world(
        #     player_screen_x,
        #     player_screen_y
        # )
        # self.game_state.player_world_x = player_world_x
        # self.game_state.player_world_y = player_world_y
        player_world_x = self.game_state.player.world_x
        player_world_y = self.game_state.player.world_y
        # print(f"Game sees world: ({player_world_x:.1f}, {player_world_y:.1f})")
        self.game_state.player_world_x = player_world_x
        self.game_state.player_world_y = player_world_y

        self.camera_manager.follow_player(player_world_x, player_world_y)
        screen_x, screen_y = self.camera_manager.world_to_screen(
            player_world_x,
            player_world_y
        )
        # print(f"World -> Screen: ({screen_x:.1f}, {screen_y:.1f})")

        self.game_state.player.center_x = screen_x
        self.game_state.player.center_y = screen_y

        # В on_update() после строк с игроком
        if self.game_state.enemies:
            enemy = self.game_state.enemies[0]
            enemy_screen_x, enemy_screen_y = self.camera_manager.world_to_screen(enemy.x, enemy.y)
            # print(f"Enemy: world({enemy.x}, {enemy.y}) -> screen({enemy_screen_x:.1f}, {enemy_screen_y:.1f})")

    def on_draw(self):
        self.clear()
        # рисуем сущностей
        self.entity_manager.draw()
        # рисуем спелы
        self.spell_manager.draw()
        # рисуем интерфейс
        self.ui_renderer.draw()
        # рисуем панели
        self.debug_renderer.draw(self.camera_manager)

    def on_key_press(self, key, modifiers):
        self.input_manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        self.input_manager.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.input_manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        # self.input_manager.on_mouse_motion(x, y, dx, dy)
        self.game_state.cursor_world_x, self.game_state.cursor_world_y = \
            self.camera_manager.screen_to_world(x, y)

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
