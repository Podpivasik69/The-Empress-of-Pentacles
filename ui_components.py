import arcade
from typing import Tuple, Optional
from constants import UI_SETTINGS





class SpellProgressBar:
    """ Класс прогресс бара"""

    def __init__(self, position, size=(56, 8), frame_texture_path="media/ui/spell_progressbar.png"):
        self.position = position
        self.width = size[0]
        self.height = size[1]
        self.progress = 0.0

        # загрузка текстур рамки
        if frame_texture_path:
            self.frame_sprite = arcade.Sprite(frame_texture_path, scale=1.0)
            self.frame_sprite.center_x = position[0]
            self.frame_sprite.center_y = position[1]
            self.frame_sprite_list = arcade.SpriteList()
            self.frame_sprite_list.append(self.frame_sprite)
        else:
            self.frame_sprite = None

    def set_progress(self, progress):
        self.progress = max(0.0, min(1.0, progress))

    def get_gradient_color(self, progress):
        """ Градиент """
        if progress <= 0:
            return (0, 0, 0, 0)
        if progress >= 1.0:
            return (0, 255, 0, 255)

        if progress < 0.5:
            ratio = progress * 2
            red = 255
            green = int(255 * ratio)
            blue = 0
        else:
            ratio = (progress - 0.5) * 2
            red = int(255 * (1 - ratio))
            green = 255
            blue = 0

        return (red, green, blue, 255)

    def draw(self):
        """ Отрисовка прогресс бара """
        if self.progress > 0:
            fill_width = self.width * self.progress
            fill_color = self.get_gradient_color(self.progress)

            fill_center_x = self.position[0] - self.width / 2 + fill_width / 2
            fill_center_y = self.position[1]

            fill_rect = arcade.rect.XYWH(
                fill_center_x,
                fill_center_y,
                fill_width,
                self.height
            )
            arcade.draw_rect_filled(fill_rect, fill_color)
        # отрисовка рамки поверх
        if self.frame_sprite:
            self.frame_sprite_list.draw()

# TODO: вынести сюда же классы для:
# 1. SpellProgressBar (прогресс-бары заклинаний)
# 2. Quickbar (панель быстрого доступа)
# 3. ElementalCircleUI (отрисовка алхимического круга)
# 4. Crosshair (прицел)
# 5. FPSDisplay (отображение FPS)

# ПРИМЕЧАНИЕ: классы выше будут вынесены постепенно,
# чтобы не сломать работающий код сразу.
