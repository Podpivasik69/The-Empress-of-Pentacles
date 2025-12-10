from constants import *
import arcade
import math


# базовый класс врагов, от него будут наследоватся другие
class BaseEnemie:
    def __init__(self, health, max_health, speed, x, y, melee_damage):
        # начальные штучки
        self.health = health
        self.max_health = max_health
        self.speed = speed
        self.x = x
        self.y = y
        self.melee_damage = melee_damage
        self.is_alive = True

        # спрайты
        self.sprite = None
        self.sprite_scale = 1.0

    def setup(self):
        pass

    def setup_sprite(self, sprite_path, scale):
        if sprite_path:
            self.sprite = arcade.Sprite(sprite_path, scale=scale)
        else:
            self.sprite = arcade.Sprite('media/enemies/error.png', scale=scale)
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        self.sprite_path = sprite_path
        self.sprite_scale = scale

    def draw(self):
        if self.sprite and self.is_alive:
            pass
