from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import arcade

class CameraManager:
    def __init__(self, game_state):
        self.game_state = game_state
        # коорды камеры
        self.camera_x = 0
        self.camera_y = 0
        self.camera_speed = 5
        self.cell_size = 4  # из world.py

    def screen_to_world(self, screen_x, screen_y):
        # переводит координаты на экране в координаты в мире
        world_pixel_x = screen_x + self.camera_x
        world_pixel_y = screen_y + self.camera_y

        world_cell_x = world_pixel_x / self.cell_size
        world_cell_y = world_pixel_y / self.cell_size

        return world_cell_x, world_cell_y

    def world_to_screen(self, world_cell_x, world_cell_y):
        """ Переводит координаты из мира в экранные корды для отрисовки"""
        world_pixel_x = world_cell_x * self.cell_size
        world_pixel_y = world_cell_y * self.cell_size

        screen_x = world_pixel_x - self.camera_x
        screen_y = world_pixel_y - self.camera_y

        return screen_x, screen_y

    def follow_player(self, player_world_x, player_world_y):
        """ Камера следит за игроком"""

        player_pixel_x = player_world_x * self.cell_size
        player_pixel_y = player_world_y * self.cell_size

        self.camera_x = player_pixel_x - SCREEN_WIDTH // 2
        self.camera_y = player_pixel_y - SCREEN_HEIGHT // 2

        self.game_state.camera_x = self.camera_x
        self.game_state.camera_y = self.camera_y
