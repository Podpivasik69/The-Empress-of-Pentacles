import arcade

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TITLE = "Changing Circle"
VELOCITY = 1


class MyGame(arcade.Window):
    def __init__(self, width, height, title, velocity):
        super().__init__(width, height, title)
        # Сохраните переданную скорость в атрибут класса
        self.velocity = velocity
        self.color = arcade.color.GREEN_YELLOW

    def setup(self):
        self.radius = 20
        # Создайте флаги для отслеживания состояний (рост/уменьшение)
        self.is_growing = False

    def on_draw(self):
        self.clear()
        # Отрисуйте круг в центре окна, используя текущий self.radius
        arcade.draw_circle_filled(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self.radius, self.color)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            # Установите флаги в состояние "рост"
            self.is_growing = True
            # print(self.is_growing)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            # Установите флаги в состояние "уменьшение"
            self.is_growing = False
            # print(self.is_growing)

    def on_update(self, delta_time):
        # В зависимости от флагов, изменяйте self.radius.
        # Не забудьте остановить уменьшение, когда радиус достигнет 20.
        if self.is_growing:
            self.radius += self.velocity
        if not self.is_growing and self.radius > 20:
            self.radius -= self.velocity


def setup_game(width=800, height=600, title="Changing Circle", velocity=1):
    game = MyGame(width, height, title, velocity)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    game = setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
