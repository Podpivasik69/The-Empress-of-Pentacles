import arcade

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Smile Silence"


class MyGame(arcade.Window):
    def __init__(self, width, height, title, radius):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.radius = radius
        self.color_yellow = (255, 192, 0)
        self.color_black = (0, 0, 0)

    def on_draw(self):
        """Этот метод отвечает за отрисовку содержимого окна"""
        self.clear()
        arcade.draw_circle_filled(450, 300, 200, self.color_yellow)
        arcade.draw_circle_filled(450 - self.radius // 2, 300 + self.radius // 2, 15, self.color_black)
        arcade.draw_circle_filled(450 + self.radius // 2, 300 + self.radius // 2, 15, self.color_black)
        arcade.draw_arc_outline(450, 300, self.radius * 3 // 2, self.radius * 3 // 2, \
                                self.color_black, 180, 360, self.radius //20)


def setup_game(width=900, height=600, title="Smile Silence", radius=200):
    game = MyGame(width, height, title, radius)
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
