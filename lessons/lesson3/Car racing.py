import arcade
import random

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Car racing"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.WHITE)
        self.cars = arcade.SpriteList()
        # Список для хранения параметров финишных прямоугольников
        self.rects = []
        self.start = False
        self.car_scale = 0.5
        self.blue = arcade.color.BLUE
        self.green = arcade.color.GREEN
        self.red = arcade.color.RED
        self.orange = arcade.color.ORANGE
        self.colors = [self.orange, self.red, self.green, self.blue]

    def setup(self):
        """Настройка игры"""
        # В цикле создайте 4 спрайта машинок.
        # Для каждой задайте: начальную позицию (через .right и .bottom),
        # масштаб 0.5, случайная начальная скорость от 10 до 20 пикселей и соответствующий цвет
        # для финишного прямоугольника (можно сохранить в кастомном атрибуте).
        for _ in range(4):
            car = arcade.Sprite(f'images/cars/car{_ + 1}.png', self.car_scale)
            car.bottom = _ * 100
            car.speed = random.randint(10, 20)
            car.car_color = self.colors[_]
            car.gotovo = False
            self.cars.append(car)
            self.cars[_].right = 300

            # self.rects.append([100 * _, car.car_color])

    def on_draw(self):
        self.clear()
        # Отрисуйте список машинок self.cars.draw().
        # В цикле отрисуйте все финишные прямоугольники из self.rects.
        self.cars.draw()
        for _2 in range(len(self.rects)):
            arcade.draw_rect_filled(arcade.rect.XYWH(SCREEN_WIDTH - 5, self.rects[_2][0], 10, 100),
                                    color=self.rects[_2][1])

    def on_update(self, delta_time: float):
        """Обновление состояния игры"""
        # Если гонка началась (проверьте флаг self.start):
        #   В цикле для каждой машинки:
        #   1. Увеличьте её координату .right на сумму начальной скорости с
        #        произведением ускорения от 10 до 20 пикселей на время кадра.
        #   2. Проверьте, не достигла ли она правого края окна.
        #   3. Если достигла: остановите её и добавьте параметры
        #      для финишного прямоугольника в self.rects.
        if self.start:
            for i, car in enumerate(self.cars):
                if car.right >= SCREEN_WIDTH:
                    car.speed = 0
                    car.center_x = SCREEN_WIDTH - car.width / 2
                    if not car.gotovo:
                        car.gotovo = True
                        self.rects.append([car.center_y, car.car_color])
                car.right += car.speed

    def on_key_press(self, symbol: int, modifiers: int):
        """Обработка нажатия на клавишу"""
        # При нажатии на Пробел установите флаг self.start в True.
        if symbol == arcade.key.SPACE:
            self.start = True


def setup_game(width=1200, height=400, title="Car racing"):
    game = MyGame(width, height, title)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
