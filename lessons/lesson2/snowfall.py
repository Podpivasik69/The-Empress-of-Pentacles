
import arcade

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TITLE = "Snowfalls"
VELOCITY = 2


class MyGame(arcade.Window):
    def __init__(self, width, height, title, velocity):
        super().__init__(width, height, title)
        self.velocity = velocity

    def setup(self):
        # Список для хранения координат [x, y] центров снежинок
        self.points = []
        # Сторона квадрата, в который вписана снежинка
        self.side = 20

    def on_draw(self):
        self.clear()
        # В цикле для каждой снежинки:
        # 1. Обновите её y-координату (падение вниз).
        # 2. Проверьте, не достигла ли она нижнего края, и остановите её, если да.
        # 3. Отрисуйте 4 линии, составляющие снежинку, относительно её центра.
        ...

    def on_mouse_press(self, x, y, button, modifiers):
        # Добавьте в self.points координаты центра новой снежинки
        ...


def setup_game(width=800, height=600, title="Snowfalls", velocity=2):
    game = MyGame(width, height, title, velocity)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    game = setup_game()
    arcade.run()


if __name__ == "__main__":
    main()