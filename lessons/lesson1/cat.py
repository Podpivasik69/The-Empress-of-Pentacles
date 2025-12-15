import arcade

SCREEN_TITLE = "Origami Cat"
PART = 25


class MyGame(arcade.Window):
    def __init__(self, width, height, title, part):
        super().__init__(width, height, title)
        self.part = part
        self.color = arcade.color.COOL_BLACK
        arcade.set_background_color(arcade.color.BEIGE)

    def on_draw(self):
        self.clear()
        # голова
        arcade.draw_line(PART, PART * 18, PART * 4, PART * 15, self.color, 4)
        arcade.draw_line(PART * 4, PART * 15, PART * 6, PART * 15, self.color, 4)
        arcade.draw_line(PART * 6, PART * 15, PART * 9, PART * 18, self.color, 4)
        arcade.draw_line(PART, PART * 18, PART * 2, PART * 12, self.color, 4)
        arcade.draw_line(PART * 2, PART * 12, PART * 4, PART * 15, self.color, 4)
        arcade.draw_line(PART * 6, PART * 15, PART * 8, PART * 12, self.color, 4)
        arcade.draw_line(PART * 8, PART * 12, PART * 9, PART * 18, self.color, 4)
        arcade.draw_line(PART * 2, PART * 12, PART * 5, PART * 9, self.color, 4)
        arcade.draw_line(PART * 5, PART * 9, PART * 8, PART * 12, self.color, 4)
        arcade.draw_line(PART * 5, PART * 9, PART * 5, PART * 15, self.color, 4)
        # тело
        arcade.draw_line(PART * 3, PART * 11, PART * 5, PART * 3, self.color, 4)
        arcade.draw_line(PART * 5, PART * 3, PART * 7, PART * 11, self.color, 4)
        arcade.draw_line(PART * 5, PART * 3, PART * 5, PART * 9, self.color, 4)
        arcade.draw_line(PART * 5, PART * 3, PART * 9, PART * 3, self.color, 4)
        arcade.draw_line(PART * 9, PART * 3, PART * 11, PART * 7, self.color, 4)
        arcade.draw_line(PART * 7, PART * 11, PART * 11, PART * 7, self.color, 4)
        # жопа
        arcade.draw_line(PART * 11, PART * 3, PART * 11, PART * 7, self.color, 4)
        arcade.draw_line(PART * 8, PART * 1, PART * 9, PART * 3, self.color, 4)
        arcade.draw_line(PART * 8, PART * 1, PART * 11, PART * 3, self.color, 4)


def setup_game(width=300, height=475, title="Origami Cat", part=25):
    game = MyGame(width, height, title, part)
    return game


def main():
    setup_game(PART * 12, PART * 19, SCREEN_TITLE, PART)
    arcade.run()


if __name__ == "__main__":
    main()
