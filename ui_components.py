import arcade
from typing import Tuple, Optional
from constants import UI_SETTINGS


class HealthBar:
    """Красивый health bar с рамкой и плавной анимацией - сделано с душой"""

    def __init__(self,
                 max_health: int,
                 position: Tuple[float, float] = (400, 530),  # центр health bar'а
                 size: Tuple[float, float] = (200, 20),  # размер спрайта в пикселях
                 scale: float = 1.0,
                 frame_texture_path: str = "media/ui/progressbar.png"):
        """
        Инициализация health bar'а
        :param max_health: максимальное здоровье (например, 100)
        :param position: (center_x, center_y) - позиция на экране
        :param size: (width, height) - размер спрайта в пикселях ДО scale
        :param scale: масштаб спрайта (1.0 = оригинальный размер)
        :param frame_texture_path: путь к спрайту рамки
        """
        self.max_health = max_health
        self.current_health = max_health
        self.target_health = max_health  # для плавной анимации
        self.position = position
        self.scale = scale

        # реальный размер на экране
        self.actual_width = size[0] * scale
        self.actual_height = size[1] * scale

        # TODO: сделать проверку существования файла
        self.frame_sprite = arcade.Sprite(
            frame_texture_path,
            scale=scale
        )
        self.frame_sprite.center_x = position[0]
        self.frame_sprite.center_y = position[1]

        # Создаем SpriteList для отрисовки
        self.frame_sprite_list = arcade.SpriteList()
        self.frame_sprite_list.append(self.frame_sprite)

        # отступы заполнения от краёв рамки (в пикселях после scale)
        # 4px с каждой стороны выглядит хорошо
        self.fill_margin = scale

        # максимальная ширина заполнения (когда HP = max)
        self.max_fill_width = self.actual_width - (self.fill_margin * 2)

        # для плавной анимации
        self.animation_speed = 300.0  # пикселей в секунду
        self.current_fill_width = self.max_fill_width  # начальная ширина

        # цвета градиента (можно менять под настроение)
        self.gradient_colors = {
            0.0: (255, 0, 0),  # красный при 0% (ранен!)
            0.5: (255, 255, 0),  # жёлтый при 50% (осторожно)
            1.0: (0, 255, 0)  # зелёный при 100% (всё отлично)
        }

    def update(self, delta_time: float):
        """
        Обновление анимации health bar'а
        :param delta_time: время с последнего кадра
        """
        # плавное изменение ширины заполнения
        target_width = (self.target_health / self.max_health) * self.max_fill_width

        # разница между текущей и целевой шириной
        width_diff = target_width - self.current_fill_width

        # если разница небольшая - сразу устанавливаем
        if abs(width_diff) < 0.5:
            self.current_fill_width = target_width
        else:
            # двигаемся к целевой ширине с заданной скоростью
            move_amount = self.animation_speed * delta_time
            if abs(width_diff) <= move_amount:
                self.current_fill_width = target_width
            else:
                direction = 1 if width_diff > 0 else -1
                self.current_fill_width += move_amount * direction

        # обновляем текущее здоровье для отрисовки цвета
        self.current_health = (self.current_fill_width / self.max_fill_width) * self.max_health

    def set_health(self, health: float, instant: bool = False):
        """
        Установка здоровья (можно мгновенно или с анимацией)
        :param health: новое значение здоровья
        :param instant: мгновенное изменение (без анимации)
        """
        health = max(0, min(health, self.max_health))
        self.target_health = health

        if instant:
            self.current_health = health
            self.current_fill_width = (health / self.max_health) * self.max_fill_width

    def get_gradient_color(self, health_percent: float):

        """
        Получение цвета градиента в зависимости от процента здоровья
        :param health_percent: процент здоровья (0.0 - 1.0)
        :return: цвет в формате (R, G, B, A)
        """
        health_percent = max(0.0, min(1.0, health_percent))

        # если процент попадает точно в ключ - возвращаем его
        if health_percent in self.gradient_colors:
            r, g, b = self.gradient_colors[health_percent]
            return (r, g, b, 255)

        # ищем между какими ключами находится наш процент
        sorted_keys = sorted(self.gradient_colors.keys())
        for i in range(len(sorted_keys) - 1):
            low = sorted_keys[i]
            high = sorted_keys[i + 1]

            if low <= health_percent <= high:
                # интерполяция между цветами
                t = (health_percent - low) / (high - low)

                color_low = self.gradient_colors[low]
                color_high = self.gradient_colors[high]

                r = int(color_low[0] + (color_high[0] - color_low[0]) * t)
                g = int(color_low[1] + (color_high[1] - color_low[1]) * t)
                b = int(color_low[2] + (color_high[2] - color_low[2]) * t)

                return (r, g, b, 255)

        # fallback (на всякий случай)
        return (255, 0, 0, 255)

    def draw(self):
        """
        Отрисовка health bar'а
        Порядок отрисовки:
        1. Фон (если нужен)
        2. Заполнение (цветной прямоугольник)
        3. Рамка (поверх всего)
        """
        # если ширина заполнения меньше 1px - не рисуем
        if self.current_fill_width < 1:
            return

        # 1. Рисуем заполнение (цветной прямоугольник)
        health_percent = self.current_health / self.max_health
        fill_color = self.get_gradient_color(health_percent)

        # позиция заполнения (центр относительно left edge + margin)
        fill_center_x = (self.position[0] - self.actual_width / 2 +
                         self.fill_margin + self.current_fill_width / 2)
        fill_center_y = self.position[1]

        # создаём прямоугольник для заполнения
        fill_rect = arcade.rect.XYWH(
            fill_center_x,  # center_x
            fill_center_y,  # center_y
            self.current_fill_width,  # width
            self.actual_height - (self.fill_margin * 2)  # height
        )

        # рисуем заполнение
        arcade.draw_rect_filled(fill_rect, fill_color)

        # 2. Рисуем рамку (спрайт поверх заполнения)
        self.frame_sprite_list.draw()

    def get_health_percent(self) -> float:
        """
        Получение текущего процента здоровья
        :return: процент от 0.0 до 1.0
        """
        return self.current_health / self.max_health

    def is_full(self) -> bool:
        """
        Проверка, полностью ли здоровье
        :return: True если здоровье = максимальное
        """
        return abs(self.current_health - self.max_health) < 0.1

    def is_empty(self) -> bool:
        """
        Проверка, пусто ли здоровье
        :return: True если здоровье близко к 0
        """
        return self.current_health < 0.1

# TODO: вынести сюда же классы для:
# 1. SpellProgressBar (прогресс-бары заклинаний)
# 2. Quickbar (панель быстрого доступа)
# 3. ElementalCircleUI (отрисовка алхимического круга)
# 4. Crosshair (прицел)
# 5. FPSDisplay (отображение FPS)

# ПРИМЕЧАНИЕ: классы выше будут вынесены постепенно,
# чтобы не сломать работающий код сразу.
