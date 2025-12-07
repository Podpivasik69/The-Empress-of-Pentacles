import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Просто сломанный телек"
DOTS_COUNT = 10000


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.dots_list = arcade.shape_list.ShapeElementList()
        # Простой текст
        arcade.draw_text("Добро пожаловать в Arcade!", 50, 550, arcade.color.BLACK, 20)

        # Текст с фоном (прямоугольник-подложка)
        text = "Счёт: 0000"
        text_width = 150  # Примерная ширина, можно вычислить точнее позже.
        arcade.draw_rect_filled(arcade.rect.XYWH(700, 50, text_width + 20, 30), arcade.color.LIGHT_GRAY)
        arcade.draw_text(text, 700 - text_width // 2, 40, arcade.color.NAVY_BLUE, 16, width=text_width, align="center")

    def setup(self):
        # первый квадрат
        self.square_x = SCREEN_WIDTH //2  # Стартовая позиция X
        self.square_y = 0  # Стартовая позиция Y
        self.square_size = 50  # Размер стороны
        self.square_color = arcade.color.BLUE  # Начальный цвет
        self.square_speed_x = 1000  # Скорость по X (пикселей в секунду!)
        self.square_speed_y = 1500  # Скорость по Y (пикселей в секунду!)


    def on_draw(self):
        """Этот метод отвечает за отрисовку содержимого окна"""
        self.clear()
        arcade.draw_rect_filled(arcade.rect.XYWH(self.square_x, self.square_y, self.square_size, self.square_size), self.square_color)

    def on_update(self, delta_time: float):
        """ Логика игры. Вызывается ~60 раз в секунду.
        delta_time (dt) — Время, прошедшее с предыдущего вызова, в секундах. """

        # 1. Двигаем квадрат по формуле: Новая_Позиция = Старая_Позиция + Скорость * Время
        self.square_x += self.square_speed_x * delta_time
        self.square_y += self.square_speed_y * delta_time

        # 2. Проверяем границы экрана и «отражаем» квадрат
        # Если квадрат ушёл за правую границу (X > ширины окна) или за левую (X < 0)
        if self.square_x > self.width or self.square_x < 0:
            self.square_speed_x *= -1  # Меняем направление по X на противоположное
            self.square_color = arcade.types.Color.random()  # Меняем цвет на случайный!
        # Если квадрат ушёл за верхнюю границу (Y > высоты окна) или за нижнюю (Y < 0)
        if self.square_y > self.height or self.square_y < 0:
            self.square_speed_y *= -1  # Меняем направление по Y на противоположное
            self.square_color = arcade.types.Color.random()  # И снова меняем цвет!


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()