import arcade

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Perspective"


class MyGame(arcade.Window):
    def __init__(self, width, height, title, width_rect, height_rect, color_rect: tuple[int, int, int]):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)
        self.width_rect = width_rect
        self.height_rect = height_rect
        self.color_rect = color_rect

    def on_draw(self):
        self.clear()
        arcade.draw_lbwh_rectangle_filled((SCREEN_WIDTH // 2 - self.width_rect // 2), 20, \
                                          self.width_rect, self.height_rect, self.color_rect)

        new_x = (SCREEN_WIDTH // 2 - self.width_rect // 2) + 20
        new_y = 20 + self.height_rect
        new_color = self.color_rect[0] - 20, self.color_rect[1] - 20, self.color_rect[2] - 20
        new_wieght = self.width_rect - 40
        for i in range(9):
            arcade.draw_lbwh_rectangle_filled(new_x, new_y, \
                                              new_wieght, 20, new_color)
            new_x += 20
            new_y += 20
            new_wieght -= 40
            new_color = new_color[0] - 20, new_color[1] - 20, new_color[2] - 20,


def setup_game(width=900, height=600, title="Perspective", width_rect=500, height_rect=300,
               color_rect=(192, 255, 0)):
    game = MyGame(width, height, title, width_rect, height_rect, color_rect)
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
