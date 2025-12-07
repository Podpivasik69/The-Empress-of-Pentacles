import arcade
from arcade.types import Color

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Flying squares"


class MyGame(arcade.Window):
    def __init__(self, width, height, title, side, color):
        super().__init__(width, height, title)
        self.side = side
        self.color = color
        self.color_rgb = Color.from_hex_string(self.color)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        start_x = (SCREEN_WIDTH // 2) - self.side // 2
        start_y = 0
        # Список списков координат квадратов для рисования
        self.points = [
            [start_x, start_y],
            [start_x, start_y]
        ]

    def on_draw(self):
        """Этот метод отвечает за отрисовку содержимого окна"""
        self.clear()
        arcade.draw_lbwh_rectangle_filled(self.points[0][0], self.points[0][1], \
                                          self.side, self.side, self.color_rgb)

        arcade.draw_lbwh_rectangle_filled(self.points[1][0], self.points[1][1], \
                                          self.side, self.side, self.color_rgb)

    def on_update(self, delta_time):
        """Этот метод отвечает за обновление логики игры (анимации, взаимодействия и т. д.)"""
        self.points[0][0] -= 2
        self.points[0][1] += 2
        self.points[1][0] += 2
        self.points[1][1] += 2


def setup_game(width=900, height=600, title="Flying squares", side=100, color="#ff40ff"):
    game = MyGame(width, height, title, side, color)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
