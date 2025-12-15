import arcade
from arcade.types import Color
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Boms"


class MyGame(arcade.Window):
    def __init__(self, width, height, title, start_radius):
        super().__init__(width, height, title)
        self.start_radius = start_radius
        arcade.set_background_color(arcade.color.ASH_GREY)

    def setup(self):
        self.circle_radius = [self.start_radius, 0]  # Список текущих значений радиусов кругов
        self.colors = [arcade.color.WHITE, arcade.color.BLACK]  # Список текущих значений цвета кругов
        self.circle_change = 1  # Скорость изменения радиусов
        self.start_x = SCREEN_WIDTH // 2
        self.start_y = SCREEN_HEIGHT // 2

    def on_draw(self):
        self.clear()
        # arcade.draw_circle_outline(500, 400, 50, arcade.color.BLACK, 2)
        # arcade.draw_circle_filled(500, 400, 45, self.fancy_color_2)

        for i in range(len(self.circle_radius)):
            arcade.draw_circle_filled(self.start_x, self.start_y, self.circle_radius[i], self.colors[i])

    def on_update(self, delta_time):
        for i in range(len(self.circle_radius)):
            self.circle_radius[i] += self.circle_change

        if self.circle_radius[-1] >= self.start_radius:
            self.circle_radius.append(0)
            if self.colors[-1] == arcade.color.WHITE:
                self.colors.append(arcade.color.BLACK)
            elif self.colors[-1] == arcade.color.BLACK:
                self.colors.append(arcade.color.WHITE)

        if len(self.circle_radius) > 12:
            self.circle_radius.pop(0)
            self.colors.pop(0)


def setup_game(width=800, height=600, title="Boms", start_radius=50):
    game = MyGame(width, height, title, start_radius)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
