import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Balls"


class MyGame(arcade.Window):
    def __init__(self, width, height, title, radius):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.white = arcade.color.WHITE
        self.start_x = SCREEN_WIDTH // 2
        self.start_y = SCREEN_HEIGHT // 2
        self.radius = radius

    def setup(self):
        # Список списков координат шариков
        self.balls = list()
        for i in range(12):
            self.balls.append([self.start_x, self.start_y])
        # Список списков скоростей шариков
        self.change = list()
        self.change_4 = list()
        self.change_8 = list()
        # l1 = [1, -1]
        # l2 = [-1, 1]
        # for i in l1:
        #     for j in l2:
        #         self.change_4.append([i, j])

        # print(self.change_4)

        # l4 = [1, 2, -1, -2]
        # l41 = [1, 2, -1, -2]
        #
        # for _1 in l4:
        #     for _2 in l41:
        #         if (abs(_1) == 1 and abs(_2) == 2) or (abs(_1) == 2 and abs(_2) == 1):
        #             self.change_8.append([_1, _2])
        self.change_4 = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
        self.change_8 = [[1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
        # print(self.change_8)
        self.change = self.change_4 + self.change_8
        # print(self.change)

    def on_draw(self):
        self.clear()
        for i in range(12):
            arcade.draw_circle_filled(self.balls[i][0], self.balls[i][1], self.radius, arcade.color.WHITE)

    def on_update(self, delta_time):
        for i in range(12):
            self.balls[i][0] += self.change[i][0] * delta_time
            self.balls[i][1] += self.change[i][1] * delta_time

            if self.balls[i][0] - self.radius < 0:
                # левая стенка Х
                self.change[i][0] *= -1
                self.balls[i][0] = self.radius

            if self.balls[i][0] + self.radius > SCREEN_WIDTH:
                # правая стенка Х
                self.change[i][0] *= -1
                self.balls[i][0] = SCREEN_WIDTH - self.radius

            if self.balls[i][1] + self.radius > SCREEN_HEIGHT:
                # верхняя граница У
                self.change[i][1] *= -1
                self.balls[i][1] = SCREEN_HEIGHT - self.radius

            if self.balls[i][1] - self.radius < 0:
                # нижняя граница У
                self.change[i][1] *= -1
                self.balls[i][1] = self.radius

            # if self.balls[i][0] - self.radius < 0 or self.balls[i][0] + self.radius > SCREEN_WIDTH:
            #     self.change[i][0] *= -1
            # if self.balls[i][1] - self.radius < 0 or self.balls[i][1] + self.radius > SCREEN_HEIGHT:
            #     self.change[i][1] *= -1


def setup_game(width=800, height=600, title="Balls", radius=10):
    game = MyGame(width, height, title, radius)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
