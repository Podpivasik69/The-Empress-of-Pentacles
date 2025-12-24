# core/game_state.py - состояние игры
from elemental_circle import ElementalCircle
from projectile import SunStrikeProjectile
from spell_system import SpellSystem
from monsters import TrainingTarget
from player import Player
from constants import *


class GameState:
    def __init__(self):
        # создание игрока и его кнопок
        self.player = None  # игрок и его данные
        self.keys_pressed = set()  # множество нажатых кнопок
        self.want_to_shoot = False
        self.wants_to_change_staff = False
        self.shoot_target_x = 0
        self.shoot_target_y = 0
        self.active_spell = None

        # малый алхимический круг
        self.elemental_circle = None

        # система заклинаний
        self.spell_system = None
        self.ready_spells = []  # список готовых заклинаний для отображения в квик баре
        self.selected_spell_index = -1
        self.spell_progress = [0.0, 0.0, 0.0, 0.0]  # прогресс шкалы прогресс бара

        self.show_fps = False  # счетчик фпс
        self.current_fps = 0
        # TODO сделать врагов
        # враги

        self.is_tab_pressed = False
        self.enemies = []  # список врагов
        self.current_staff = None  # дефолт посох, не задан сначала

        self.shoot_timer = 0.0  # задержка заклинаний
        self.can_shoot = True  # флаг, можно ли стрелять сейчас
        self.shoot_cooldown = 0.0
        self.movement_locked = False
        self.staff_sprite = None
        self.crosshair = None
        self.enemy_sprites = None

        # self.shoot_timer = 0.0
        # self.can_shoot = True
        self._death_triggered = False
        self.player_should_die = False
        self.is_game_over = False


        self.cursor_x = SCREEN_WIDTH // 2
        self.cursor_y = SCREEN_HEIGHT // 2
