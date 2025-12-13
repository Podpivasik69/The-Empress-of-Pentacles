import arcade

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TITLE = "Moving Square"
VELOCITY = 20


class MyGame(arcade.Window):
    def __init__(self, width, height, title, velocity):
        super().__init__(width, height, title)
        # Сохраните переданную скорость в атрибут класса
        self.velocity = velocity

    def setup(self):
        # Создайте атрибуты для хранения координат центра квадрата и его стороны
        self.rect_size = 100
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2

        self.white = arcade.color.WHITE

    def on_draw(self):
        self.clear()
        # Отрисуйте квадрат, используя его текущие координаты и размеры
        arcade.draw_rect_filled(arcade.rect.XYWH(300, 300, 100, 100), self.white)

        # print(f"Rect: {rect_obj}")

    def on_key_press(self, key, modifiers):
        # 1. В зависимости от нажатой стрелки, измените координаты центра квадрата.
        # 2. После изменения, проверьте каждую из четырех границ окна.
        # 3. Если квадрат вышел за границу, скорректируйте его координату так,
        #    чтобы он касался края окна.
        if key == arcade.key.UP:
            self.player_y += self.velocity
            if (self.player_y + self.rect_size // 2) > SCREEN_HEIGHT:
                self.player_y = SCREEN_HEIGHT - self.rect_size // 2

        if key == arcade.key.DOWN:
            self.player_y -= self.velocity
            if (self.player_y - self.rect_size // 2) < 0:
                self.player_y = self.rect_size // 2

        if key == arcade.key.LEFT:
            self.player_x -= self.velocity
            if (self.player_x - self.rect_size // 2) < 0:
                self.player_x = self.rect_size // 2

        if key == arcade.key.RIGHT:
            self.player_x += self.velocity
            if (self.player_x + self.rect_size // 2) > SCREEN_WIDTH:
                self.player_x = SCREEN_WIDTH - self.rect_size // 2


def setup_game(width=800, height=600, title="Moving Square", velocity=20):
    game = MyGame(width, height, title, velocity)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    game = setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
