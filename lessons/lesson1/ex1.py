import arcade
import random

# Размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Тормозящий сломанный телек"
DOTS_COUNT = 10000


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.dots = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(DOTS_COUNT)]

    def on_draw(self):
        """Этот метод отвечает за отрисовку содержимого окна"""
        self.clear()
        for dot in self.dots:
            a = arcade.draw_circle_filled(dot[0], dot[1], 1, arcade.color.WHITE)

    def on_update(self, delta_time):
        """Этот метод отвечает за обновление логики игры (анимации, взаимодействия и т. д.)"""
        pass


def main():
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()