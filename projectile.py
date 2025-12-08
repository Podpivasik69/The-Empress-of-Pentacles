from constants import PROJECTILE_CATEGORIES, PROJECTILE_EXCEPTIONS, SPELL_TO_CATEGORY
from math import sqrt
from player import *
import arcade
import random, math


class Projectile:

    def __init__(self, spell_type, start_x, start_y, target_x, target_y, spread_angle=0.0):
        self.spell_type = spell_type
        self.x = start_x
        self.y = start_y
        self.target_x = target_x
        self.target_y = target_y

        properties = self._get_properties(spell_type)
        self.speed = properties["speed"]
        self.damage = properties["damage"]
        self.size = properties["size"]
        if spread_angle > 0:
            angle = math.atan2(self.target_y - start_y, self.target_x - start_x)  # вычисляем угол
            spread_rad = math.radians(spread_angle)
            angle += random.uniform(-spread_rad, spread_rad)  # добавляем рандомного отклонения
            distance = math.sqrt((self.target_x - start_x) ** 2 + (self.target_y - start_y) ** 2)
            # перерасчет
            self.target_x = start_x + math.cos(angle) * distance
            self.target_y = start_y + math.sin(angle) * distance

        # какието сложные штуки для стрельбы
        self.is_alive = True  # пулька живая
        self.max_distance = properties.get("max_distance", 500)
        self.lifetime = properties.get("lifetime", 3.0)
        self.time_alive = 0.0
        self.distance_traveled = 0.0
        self.spread_angle = spread_angle

        # пути до картинок  -пока вручную
        # TODO шаблоны названий доля спрайтов
        if spell_type == "fireball":
            sprite_path = "media/fireball_icon.png"
        elif spell_type == "waterball":
            sprite_path = "media/waterball_icon.png"
        elif spell_type == "fire_spark":
            sprite_path = "media/placeholder_icon.png"  # временно
        elif spell_type == "splashing_water":
            sprite_path = "media/placeholder_icon.png"  # временно
        else:
            sprite_path = "media/placeholder_icon.png"  # fallback

        # штуки для спрайтов
        self.sprite = arcade.Sprite(sprite_path)
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        self.sprite.scale = self.size / self.sprite.width

    def _get_properties(self, spell_type):
        # если снаряд нетакуся (уникальный, не даун!!!)
        if spell_type in PROJECTILE_EXCEPTIONS:
            return PROJECTILE_EXCEPTIONS[spell_type]
        category = SPELL_TO_CATEGORY.get(spell_type, "medium")
        return PROJECTILE_CATEGORIES[category]

    # if spell_type in

    def update(self, delta_time):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = sqrt(dx * dx + dy * dy)
        self.time_alive += delta_time

        if distance > 0:
            self.x += (dx / distance) * self.speed * delta_time
            self.y += (dy / distance) * self.speed * delta_time

            if self.time_alive > self.lifetime or self.distance_traveled > self.max_distance:
                self.is_alive = False

        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

    def draw(self):
        # рисуем спелы
        temp_list = arcade.SpriteList()
        temp_list.append(self.sprite)
        temp_list.draw()
