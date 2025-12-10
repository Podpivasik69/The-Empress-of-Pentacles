from constants import SPELL_DATA, TRAJECTORY_CONFIG
from math import sqrt
import random, math
import arcade


class Projectile:

    def __init__(self, spell_type, start_x, start_y, target_x, target_y, spread_angle=0.0, launch_angle=None):
        self.spell_type = spell_type
        self.x = start_x
        self.y = start_y
        # вычисление угла полета снаряда!
        if launch_angle is None:
            launch_angle = math.atan2(target_y - start_y, target_x - start_x)
        self.original_target_x = target_x  # оригинальный курсор
        self.original_target_y = target_y
        # меняем угол с учетом разброса
        self.direction_x = math.cos(launch_angle)
        self.direction_y = math.sin(launch_angle)
        # для быстрых снарядов оставляет только таргет
        self.target_x = target_x
        self.target_y = target_y
        self.launch_angle = launch_angle
        #

        if spell_type in SPELL_DATA:
            spell_info = SPELL_DATA[spell_type]
            self.speed = spell_info["speed"]
            self.damage = spell_info["damage"]
            self.size = spell_info["size"]
            self.rotates = spell_info.get("rotates", False)
        else:
            self.speed = 500
            self.damage = 20
            self.size = 32
            self.rotates = False

        #

        # Получаем категорию заклинания
        self.category = SPELL_DATA.get(spell_type, {}).get("category", "medium")

        # Получаем конфиг траектории
        trajectory_config = TRAJECTORY_CONFIG.get(self.category, TRAJECTORY_CONFIG["medium"])
        self.gravity = trajectory_config["gravity"]
        self.lifetime = trajectory_config["lifetime"]  # ЗАМЕНИТЬ текущее self.lifetime
        self.max_distance = trajectory_config["max_distance"]  # ЗАМЕНИТЬ текущее self.max_distance

        # Для баллистических снарядов
        self.velocity_x = 0
        self.velocity_y = 0
        # TODO почистить
        if self.category == "medium":
            # Используем launch_angle как основное направление
            power = self.speed * 0.7  # 70% скорости для параболы

            # Добавляем вертикальный компонент для дуги
            # Чем выше цель - тем круче дуга (но всегда вверх относительно направления)
            vertical_boost = 0.3  # 30% дополнительно вверх

            # Если стреляем вниз (цель ниже старта) - меньше дуги
            if target_y < start_y:
                vertical_boost = 0.1  # 10% вверх (пологая дуга)

            # Создаем новый угол: основной направление + немного вверх
            # launch_angle - это угол к цели (уже с учетом spread)
            vertical_angle = math.radians(15) * vertical_boost  # 15° * 0.3 = 4.5°
            angle_adjusted = launch_angle + vertical_angle

            self.velocity_x = math.cos(angle_adjusted) * power
            self.velocity_y = math.sin(angle_adjusted) * power
        #
        #

        # какието сложные штуки для стрельбы
        self.rotates = SPELL_DATA.get(spell_type, {}).get("rotates", False)
        self.is_alive = True  # пулька живая
        # self.max_distance = 500
        # self.lifetime = 3.0
        print(f"Projectile {spell_type}: rotates = {self.rotates}")

        self.time_alive = 0.0
        self.distance_traveled = 0.0
        self.spread_angle = spread_angle

        # испрввил на шаблоный с новым словарем
        sprite_path = SPELL_DATA.get(spell_type, {}).get("icon", "media/placeholder_icon.png")

        # штуки для спрайтов
        self.sprite = arcade.Sprite(sprite_path)
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y
        self.sprite.scale = self.size / self.sprite.width

    # def _get_properties(self, spell_type):
    #     # если снаряд нетакуся (уникальный, не даун!!!)
    #     if spell_type in PROJECTILE_EXCEPTIONS:
    #         return PROJECTILE_EXCEPTIONS[spell_type]
    #     category = SPELL_TO_CATEGORY.get(spell_type, "medium")
    #     return PROJECTILE_CATEGORIES[category]

    # if spell_type in

    def update(self, delta_time):
        if not self.is_alive:
            return

        self.time_alive += delta_time

        # УНИЧТОЖЕНИЕ ПО ВРЕМЕНИ
        if self.time_alive > self.lifetime:
            self.is_alive = False
            return

        # ДВИЖЕНИЕ В ЗАВИСИМОСТИ ОТ КАТЕГОРИИ
        if self.category == "medium":
            # ПАРАБОЛИЧЕСКАЯ ТРАЕКТОРИЯ
            self.velocity_y -= self.gravity * delta_time  # ГРАВИТАЦИЯ!
            self.x += self.velocity_x * delta_time
            self.y += self.velocity_y * delta_time

            # УНИЧТОЖЕНИЕ ПРИ ПАДЕНИИ НА ЗЕМЛЮ
            if self.y < 50:  # Нижняя граница экрана
                self.is_alive = False
                print(f"{self.spell_type} упал на землю")
                return



        else:

            # FAST и UNIQUE снаряды - прямая траектория ПО НАПРАВЛЕНИЮ (с учетом spread)
            # НЕ к фиксированной точке!
            # Двигаемся по направлению launch_angle (уже с spread)

            move_x = self.direction_x * self.speed * delta_time
            move_y = self.direction_y * self.speed * delta_time
            self.x += move_x
            self.y += move_y

            # Отслеживаем пройденное расстояние
            self.distance_traveled += sqrt(move_x * move_x + move_y * move_y)

            # Уничтожаем если пролетели максимальную дистанцию
            if self.distance_traveled > self.max_distance:
                self.is_alive = False

                return

        # ОБНОВЛЕНИЕ СПРАЙТА
        self.sprite.center_x = self.x
        self.sprite.center_y = self.y

        # ROTATION
        if self.rotates:
            if self.category == "medium":
                # Для параболы - угол по текущей скорости
                angle = math.degrees(math.atan2(self.velocity_y, self.velocity_x))
                self.sprite.angle = angle
                print(f"{self.spell_type} rotation: {angle:.1f}°")
            else:
                # Для прямой - угол к цели
                dx = self.target_x - self.x
                dy = self.target_y - self.y
                if dx != 0 or dy != 0:
                    angle = math.degrees(math.atan2(dy, dx))
                    self.sprite.angle = angle

    def draw(self):
        # рисуем спелы
        temp_list = arcade.SpriteList()
        temp_list.append(self.sprite)
        temp_list.draw()
