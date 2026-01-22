from world import WorldView
from player import Player
from staff import BASIC_STAFF
from elemental_circle import ElementalCircle
from spell_system import SpellSystem
from constants import *
from physics import *
from core.ui_renderer import UIRenderer
from core.game_state import GameState
from core.managers.entity_manager import EntityManager
from core.managers.spell_manager import SpellManager
from core.managers.input_manager import InputManager
from monsters import TestEnemie
import arcade
import math


class IntegratedWorldView(WorldView):
    def __init__(self):
        super().__init__()

        self.player = Player()
        self.player.setup()
        self.player.witch_speed = 300
        self.camera_speed = 0
        self.player_world_x = 50
        self.player_world_y = 150

        self.gravity = 0.4
        self.jump_power = 12
        self.jump_velocity = 0
        self.on_ground = True

        self.game_state = GameState()
        self.game_state.world = world
        self.entity_manager = EntityManager(self.game_state)
        self.spell_manager = SpellManager(self.game_state, self.entity_manager)
        self.input_manager = InputManager(self.game_state, self.entity_manager)
        self.ui_renderer = UIRenderer(self.game_state)

        self.show_ui = True
        self.keys_pressed = set()

        self.mouse_x = SCREEN_WIDTH // 2
        self.mouse_y = SCREEN_HEIGHT // 2
        self.game_state.cursor_x = self.mouse_x
        self.game_state.cursor_y = self.mouse_y

        self.player_walking_frames = []
        self.current_walk_frame = 0
        self.walk_animation_timer = 0.0
        self.walk_frame_duration = 0.2
        self.anim_scale = 2.5
        self.is_facing_right = True
        self.jump_texture = None
        self.load_walk_animations()

        self.spawn_radius = 300
        self.enemy_num = 20

        self.background_music = None
        self.music_player = None

        self.last_safe_position = (50, 150)
        self.fall_distance_threshold = 300

        # анимации
        self.player_walking_frames = []
        self.current_walk_frame = 0
        self.walk_animation_timer = 0.0
        self.walk_frame_duration = 0.2
        self.anim_scale = 2.5
        self.is_facing_right = True
        self.jump_texture = None

        # враги и платформы
        self.spawn_radius = 300
        self.enemy_num = 20

        # падение
        self.last_safe_position = (50, 150)
        self.fall_distance_threshold = 300

        # музыка
        self.background_music = None
        self.music_player = None

        self.set_player_position(50, 150)
        self.setup_spell_system()
        self.setup_enemies_on_platforms()
        self.load_walk_animations()
        self.setup_enemies_on_platforms()

    def load_walk_animations(self):
        try:
            self.jump_texture = arcade.load_texture('media/witch/witch_anim/wizard_v_jump.png')
        except Exception as e:
            self.jump_texture = None

        for i in range(1, 4):
            try:
                texture = arcade.load_texture(f'media/witch/witch_anim/wizard_s_boku{i}.png')
                self.player_walking_frames.append(texture)
            except:
                pass

        if not self.player_walking_frames:
            try:
                fallback = arcade.load_texture('media/witch/Wizard_static2.png')
                self.player_walking_frames = [fallback]
            except:
                pass

        if self.player_walking_frames:
            self.player.player.texture = self.player_walking_frames[0]
            if not self.is_facing_right:
                self.player.player.scale_x = -abs(self.anim_scale)
                self.player.player.scale_y = abs(self.anim_scale)
            else:
                self.player.player.scale_x = abs(self.anim_scale)
                self.player.player.scale_y = abs(self.anim_scale)

    def find_platform_position(self):
        platform_positions = []
        for (x, y), substance in world.items():
            if substance.__class__.__name__ in ['Ground', 'Grass', 'Stone']:
                platform_positions.append((x, y))
        return platform_positions

    def find_suitable_enemy_position(self, platform_positions):
        suitable_positions = []
        for x, y in platform_positions:
            above_empty = (x, y + 1) not in world
            two_above_empty = (x, y + 2) not in world
            if above_empty and two_above_empty:
                platform_below = False
                for dy in range(1, 6):
                    if (x, y - dy) in world:
                        substance = world[(x, y - dy)]
                        if substance.__class__.__name__ in ['Ground', 'Grass', 'Stone']:
                            platform_below = True
                            break
                if platform_below:
                    suitable_positions.append((x, y + 1))
        return suitable_positions

    def setup_enemies_on_platforms(self):
        platform_positions = self.find_platform_position()
        enemy_positions = self.find_suitable_enemy_position(platform_positions)
        if not enemy_positions:
            enemy_positions = [(100, 150), (150, 150), (200, 150)]
        placed_enemies = []
        for i, (world_x, world_y) in enumerate(enemy_positions):
            too_close = False
            for (ex, ey) in placed_enemies:
                distance = math.sqrt((world_x - ex) ** 2 + (world_y - ey) ** 2)
                if distance < self.spawn_radius:
                    too_close = True
                    break
            if not too_close:
                adjusted_y = world_y + 20
                enemy = TestEnemie(
                    health=100,
                    max_health=100,
                    speed=0,
                    x=world_x,
                    y=adjusted_y,
                    melee_damage=5
                )
                enemy.setup_sprite(
                    'media/enemies/target/target.png',
                    scale=2.0,
                    sprite_list=self.entity_manager.enemy_sprites
                )
                self.game_state.enemies.append(enemy)
                placed_enemies.append((world_x, world_y))
                if len(placed_enemies) >= self.enemy_num:
                    break

    def setup_spell_system(self):
        self.game_state.elemental_circle = ElementalCircle()
        self.game_state.spell_system = SpellSystem(self.game_state.elemental_circle)
        self.game_state.spell_manager = self.spell_manager
        self.input_manager.spell_manager = self.spell_manager
        self.game_state.player = self.player
        self.game_state.current_staff = BASIC_STAFF
        self.game_state.shoot_cooldown = BASIC_STAFF.delay
        if self.game_state.current_staff.sprite_path:
            self.game_state.staff_sprite = arcade.Sprite(
                self.game_state.current_staff.sprite_path,
                scale=2
            )
            self.entity_manager.staff_sprite_list.append(self.game_state.staff_sprite)
        self.ui_renderer.setup()

    def set_player_position(self, world_x, world_y):
        self.player.player.center_x = SCREEN_WIDTH // 2
        self.player.player.center_y = SCREEN_HEIGHT // 2
        self.player_world_x = world_x
        self.player_world_y = world_y
        self.camera_x = world_x * self.cell_size - SCREEN_WIDTH // 2
        self.camera_y = world_y * self.cell_size - SCREEN_HEIGHT // 2

    def on_update(self, delta_time):
        self.update_camera()
        self.on_ground = self.is_something_below()

        if self.on_ground:
            self.last_safe_position = (self.player_world_x, self.player_world_y)

        if not self.on_ground:
            self.jump_velocity -= self.gravity
            if self.is_something_above() and self.jump_velocity > 0:
                self.jump_velocity = 0
            if self.jump_velocity < -20:
                self.jump_velocity = -20
        else:
            if self.jump_velocity < 0:
                self.jump_velocity = 0

        fall_distance = abs(self.player_world_y - self.last_safe_position[1])
        if fall_distance > self.fall_distance_threshold:
            self.player_world_x, self.player_world_y = self.last_safe_position
            self.jump_velocity = 0
            damage = int(self.player.health.max_health * 0.2)
            self.player.take_damage(damage)

        self.player_world_y += self.jump_velocity / self.cell_size
        self.update_player_movement(delta_time)

        is_moving = arcade.key.A in self.keys_pressed or arcade.key.D in self.keys_pressed
        if arcade.key.A in self.keys_pressed:
            self.is_facing_right = False
        elif arcade.key.D in self.keys_pressed:
            self.is_facing_right = True

        if self.on_ground:
            if is_moving and self.player_walking_frames:
                self.walk_animation_timer += delta_time
                if self.walk_animation_timer >= self.walk_frame_duration:
                    self.walk_animation_timer = 0
                    self.current_walk_frame = (self.current_walk_frame + 1) % len(self.player_walking_frames)
            if self.player_walking_frames:
                if is_moving:
                    texture = self.player_walking_frames[self.current_walk_frame]
                else:
                    texture = self.player_walking_frames[0]
                self.player.player.texture = texture
                if not self.is_facing_right:
                    self.player.player.scale_x = -abs(self.anim_scale)
                    self.player.player.scale_y = abs(self.anim_scale)
                else:
                    self.player.player.scale_x = abs(self.anim_scale)
                    self.player.player.scale_y = abs(self.anim_scale)
        else:
            if self.jump_texture:
                self.player.player.texture = self.jump_texture
                if not self.is_facing_right:
                    self.player.player.scale_x = -abs(self.anim_scale)
                    self.player.player.scale_y = abs(self.anim_scale)
                else:
                    self.player.player.scale_x = abs(self.anim_scale)
                    self.player.player.scale_y = abs(self.anim_scale)

        self.fps_timer += delta_time
        self.fps_counter += 1
        if self.fps_timer >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_timer = 0
            self.fps_counter = 0

        if self.physics_enabled:
            self.physics_timer += delta_time * self.physics_speed
            while self.physics_timer >= self.physics_update_rate:
                self._update_physics(self.physics_update_rate)
                self.physics_timer -= self.physics_update_rate

        self._update_visible_substances()
        self.update_shape_list()
        self.player.update(delta_time, self.keys_pressed)

        if self.is_something_below() and (self.is_something_on_right() or self.is_something_on_left()):
            self.player_world_y += 4 / self.cell_size

        self.entity_manager.update(delta_time)
        self.spell_manager.update(delta_time)
        self.ui_renderer.update(delta_time)
        self.game_state.current_fps = int(1.0 / delta_time) if delta_time > 0 else 0

        self.update_enemy_positions()

    def update_enemy_positions(self):
        for enemy in self.game_state.enemies:
            if enemy.sprite:
                enemy_pixel_x = enemy.x * self.cell_size - self.camera_x
                enemy_pixel_y = enemy.y * self.cell_size - self.camera_y
                enemy.sprite.center_x = enemy_pixel_x
                enemy.sprite.center_y = enemy_pixel_y

    def update_player_movement(self, delta_time):
        dx = 0
        dy = 0
        if arcade.key.A in self.keys_pressed and not self.is_something_on_left():
            dx -= self.player.witch_speed * delta_time
        if arcade.key.D in self.keys_pressed and not self.is_something_on_right():
            dx += self.player.witch_speed * delta_time
        if arcade.key.W in self.keys_pressed and not self.is_something_above():
            if self.on_ground:
                self.jump_velocity = self.jump_power
        if arcade.key.S in self.keys_pressed and not self.is_something_below():
            dy -= self.player.witch_speed * delta_time
        self.player_world_x += dx / self.cell_size
        self.player_world_y += dy / self.cell_size

    def update_camera(self):
        player_pixel_x = self.player_world_x * self.cell_size
        player_pixel_y = self.player_world_y * self.cell_size
        self.camera_x = player_pixel_x - SCREEN_WIDTH // 2
        self.camera_y = player_pixel_y - SCREEN_HEIGHT // 2
        self.player.player.center_x = SCREEN_WIDTH // 2
        self.player.player.center_y = SCREEN_HEIGHT // 2

    def on_draw(self):
        self.clear()
        self.background_list.draw()

        if self.shape_list:
            self.shape_list.draw()

        self.player.draw()

        self.entity_manager.enemy_sprites.draw()

        self.spell_manager.draw()

        if self.show_ui:
            self.ui_renderer.draw()
            arcade.draw_text(
                f"FPS: {self.current_fps}",
                10, SCREEN_HEIGHT - 30,
                arcade.color.YELLOW, 16
            )
            arcade.draw_text(
                f"Скорость: {self.jump_velocity:.1f}, На земле: {self.on_ground}",
                10, SCREEN_HEIGHT - 50,
                arcade.color.YELLOW, 16
            )
            arcade.draw_text(
                f"Веществ: {len(self.world)} | На экране: {len(self.current_substances)}",
                10, SCREEN_HEIGHT - 70,
                arcade.color.LIGHT_GRAY, 12
            )
            # Счетчик врагов (от друга)
            arcade.draw_text(
                f"Врагов: {len(self.game_state.enemies)}",
                10, SCREEN_HEIGHT - 90,
                arcade.color.LIGHT_GRAY, 12
            )

    def on_key_press(self, key, modifiers):
        if key in [arcade.key.A, arcade.key.S, arcade.key.D]:
            self.keys_pressed.add(key)
        if key == arcade.key.SPACE or key == arcade.key.W:
            if self.on_ground and not self.is_something_above():
                self.jump_velocity = self.jump_power
        if key == arcade.key.U:
            self.show_ui = not self.show_ui
        if key == arcade.key.ESCAPE:
            from view import StartMenuView
            self.window.show_view(StartMenuView())
        self.game_state.keys_pressed.add(key)
        self.input_manager.on_key_press(key, modifiers)

    def on_key_release(self, key, modifiers):
        if key in [arcade.key.W, arcade.key.A, arcade.key.S, arcade.key.D]:
            if key in self.keys_pressed:
                self.keys_pressed.remove(key)
        if key in self.game_state.keys_pressed:
            self.game_state.keys_pressed.remove(key)
        self.input_manager.on_key_release(key, modifiers)

    def on_mouse_press(self, x, y, button, modifiers):
        self.mouse_x = x
        self.mouse_y = y
        self.game_state.cursor_x = x
        self.game_state.cursor_y = y
        self.input_manager.on_mouse_press(x, y, button, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y
        self.game_state.cursor_x = x
        self.game_state.cursor_y = y
        self.input_manager.on_mouse_motion(x, y, dx, dy)

    def on_show_view(self):
        if self.window:
            self.window.set_mouse_visible(False)
        self.play_background_music()

    def on_hide_view(self):
        if self.window:
            self.window.set_mouse_visible(True)
        self.stop_background_music()

    def play_background_music(self):
        try:
            test_sound = arcade.load_sound(":resources:music/1918.mp3")
            arcade.play_sound(test_sound, volume=0.5)
        except:
            pass

    def stop_background_music(self):
        if self.music_player:
            try:
                self.music_player.pause()
            except:
                pass
        if self.background_music:
            try:
                self.background_music.stop()
            except:
                pass

    def is_something_above(self):
        world_x = int(self.player_world_x)
        world_y = int(self.player_world_y)
        head_y = world_y + 8
        left_side = world_x - 5
        right_side = world_x + 5
        for x in range(left_side, right_side + 1):
            if (x, head_y + 1) in self.world:
                return True
        return False

    def is_something_below(self):
        world_x = int(self.player_world_x)
        world_y = int(self.player_world_y)
        foot_y = world_y - 11
        for dx in range(-5, 6):
            if (world_x + dx, foot_y) in self.world:
                return True
        return False

    def is_something_on_right(self):
        world_x = int(self.player_world_x)
        world_y = int(self.player_world_y)
        top_y = world_y + 8
        bottom_y = world_y - 8
        right_side = world_x + 5
        for y in range(bottom_y, top_y + 1):
            if (right_side + 1, y) in self.world:
                return True
        return False

    def is_something_on_left(self):
        world_x = int(self.player_world_x)
        world_y = int(self.player_world_y)
        top_y = world_y + 8
        bottom_y = world_y - 8
        left_side = world_x - 7
        for y in range(bottom_y, top_y + 1):
            if (left_side - 1, y) in self.world:
                return True
        return False

    def load_walk_animations(self):
        """Загрузка анимаций ходьбы и прыжка (от друга)"""
        try:
            self.jump_texture = arcade.load_texture('media/witch/witch_anim/wizard_v_jump.png')
        except Exception as e:
            self.jump_texture = None

        for i in range(1, 4):
            try:
                texture = arcade.load_texture(f'media/witch/witch_anim/wizard_s_boku{i}.png')
                self.player_walking_frames.append(texture)
            except:
                pass

        if not self.player_walking_frames:
            try:
                fallback = arcade.load_texture('media/witch/Wizard_static2.png')
                self.player_walking_frames = [fallback]
            except:
                pass

        if self.player_walking_frames:
            self.player.player.texture = self.player_walking_frames[0]
            if not self.is_facing_right:
                self.player.player.scale_x = -abs(self.anim_scale)
                self.player.player.scale_y = abs(self.anim_scale)
            else:
                self.player.player.scale_x = abs(self.anim_scale)
                self.player.player.scale_y = abs(self.anim_scale)

    def find_platform_position(self):
        """Поиск позиций платформ (от друга)"""
        platform_positions = []
        for (x, y), substance in world.items():
            if substance.__class__.__name__ in ['Ground', 'Grass', 'Stone']:
                platform_positions.append((x, y))
        return platform_positions

    def find_suitable_enemy_position(self, platform_positions):
        """Поиск подходящих позиций для врагов (от друга)"""
        suitable_positions = []
        for x, y in platform_positions:
            above_empty = (x, y + 1) not in world
            two_above_empty = (x, y + 2) not in world
            if above_empty and two_above_empty:
                platform_below = False
                for dy in range(1, 6):
                    if (x, y - dy) in world:
                        substance = world[(x, y - dy)]
                        if substance.__class__.__name__ in ['Ground', 'Grass', 'Stone']:
                            platform_below = True
                            break
                if platform_below:
                    suitable_positions.append((x, y + 1))
        return suitable_positions

    def setup_enemies_on_platforms(self):
        platform_positions = self.find_platform_position()
        enemy_positions = self.find_suitable_enemy_position(platform_positions)
        if not enemy_positions:
            enemy_positions = [(100, 150), (150, 150), (200, 150)]

        placed_enemies = []
        for i, (world_x, world_y) in enumerate(enemy_positions):
            too_close = False
            for (ex, ey) in placed_enemies:
                distance = math.sqrt((world_x - ex) ** 2 + (world_y - ey) ** 2)
                if distance < self.spawn_radius:
                    too_close = True
                    break
            if not too_close:
                adjusted_y = world_y + 20
                enemy = TestEnemie(
                    health=100,
                    max_health=100,
                    speed=0,
                    x=world_x,
                    y=adjusted_y,
                    melee_damage=5
                )
                enemy.setup_sprite(
                    'media/enemies/target/target.png',
                    scale=2.0,
                    sprite_list=self.entity_manager.enemy_sprites
                )
                self.game_state.enemies.append(enemy)
                placed_enemies.append((world_x, world_y))
                if len(placed_enemies) >= self.enemy_num:
                    break

    def update_enemy_positions(self):
        for enemy in self.game_state.enemies:
            if enemy.sprite:
                enemy_pixel_x = enemy.x * self.cell_size - self.camera_x
                enemy_pixel_y = enemy.y * self.cell_size - self.camera_y
                enemy.sprite.center_x = enemy_pixel_x
                enemy.sprite.center_y = enemy_pixel_y

    def play_background_music(self):
        try:
            test_sound = arcade.load_sound(":resources:music/1918.mp3")
            arcade.play_sound(test_sound, volume=0.5)
        except:
            pass

    def stop_background_music(self):
        if self.music_player:
            try:
                self.music_player.pause()
            except:
                pass
        if self.background_music:
            try:
                self.background_music.stop()
            except:
                pass
