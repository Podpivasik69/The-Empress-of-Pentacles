import arcade

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TITLE = "Drop balls"
VELOCITY = 2


class MyGame(arcade.Window):
    def __init__(self, width, height, title, velocity):
        super().__init__(width, height, title)
        # Сохраните переданную скорость в атрибут класса
        self.velocity = velocity
        self.speed = list()
        self.white = arcade.color.WHITE

    def setup(self):
        # Список для хранения координат [x, y] каждого шарика
        self.points = []
        # Параллельный список для хранения скоростей [dx, dy] каждого шарика
        self.speed = []
        # Задайте радиус шариков
        self.radius = 20

    # def on_update(self, deltatime):
    #     fix = 1 / 60
    #     for balls in range(len(self.points)):

    def on_draw(self):
        self.clear()
        # В цикле для каждого шарика:
        # 1. Проверьте столкновение со стенами и инвертируйте скорость по нужной оси.
        # 2. Обновите координаты шарика, используя его скорость.
        # 3. Отрисуйте шарик в новых координатах.
        for balls in range(len(self.points)):
            self.points[balls][0] += self.speed[balls][0]
            self.points[balls][1] += self.speed[balls][1]
            # левая стена Х
            if self.points[balls][0] - self.radius < 0:
                self.points[balls][0] = self.radius
                self.speed[balls][0] *= -1

            # правая стена Х
            if self.points[balls][0] + self.radius > SCREEN_WIDTH:
                self.points[balls][0] = SCREEN_WIDTH - self.radius
                self.speed[balls][0] *= -1

            # нижняя стена У
            if self.points[balls][1] - self.radius < 0:
                self.points[balls][1] = self.radius
                self.speed[balls][1] *= -1

            # верхняя стена У
            if self.points[balls][1] + self.radius > SCREEN_HEIGHT:
                self.points[balls][1] = SCREEN_HEIGHT - self.radius
                self.speed[balls][1] *= -1

            arcade.draw_circle_filled(self.points[balls][0], self.points[balls][1], self.radius, self.white)

    def on_mouse_press(self, x, y, button, modifiers):
        # При клике добавьте в self.points координаты нового шарика,
        # а в self.speed — его начальную скорость.
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.points.append([x, y])
            self.speed.append([-self.velocity, self.velocity])


def setup_game(width=800, height=600, title="Drop balls", velocity=2):
    game = MyGame(width, height, title, velocity)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    game = setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
