import arcade

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TITLE = "Rects With Cancel"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        # Список для хранения всех нарисованных прямоугольников
        self.rects = []
        # Создайте переменные для хранения параметров текущего (рисуемого)
        # прямоугольника и флаг состояния "is_drawing".
        self.now_rect = None
        self.is_draw = False

    def on_draw(self):
        self.clear()
        # Отрисуйте все сохранённые прямоугольники из self.rects.
        # Также, если пользователь сейчас рисует новый прямоугольник, отрисуйте и его.
        if self.is_draw and self.now_rect:
            left = min(self.now_rect[0], self.now_rect[2])
            bottom = min(self.now_rect[1], self.now_rect[3])
            width = abs(self.now_rect[2] - self.now_rect[0])
            height = abs(self.now_rect[3] - self.now_rect[1])

            arcade.draw_lbwh_rectangle_outline(left, bottom, width, height,
                                               arcade.color.WHITE, 2)

    def on_mouse_press(self, x, y, button, modifiers):
        # Зафиксируйте начальные координаты и активируйте флаг начала рисования.
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.now_rect = [x, y, x, y]
            self.is_draw = True
            print(self.now_rect, self.is_draw)

    def on_mouse_motion(self, x, y, button, modifiers):
        # Если флаг рисования активен, обновляйте ширину и высоту
        # текущего прямоугольника на основе положения мыши.
        if button == arcade.MOUSE_BUTTON_LEFT and self.is_draw == True:
            self.now_rect[2] = x
            self.now_rect[3] = y
            print(self.now_rect, self.is_draw)

    def on_mouse_release(self, x, y, button, modifiers):
        # Если рисование было активно, добавьте новый прямоугольник в список self.rects
        # и сбросьте флаг/временные переменные.
        if self.is_draw == True:
            self.rects.append(self.now_rect)
            self.is_draw = False
            print(self.now_rect, self.is_draw)

    def on_key_press(self, key, modifiers):
        # Реализуйте отмену последнего действия: при нажатии Ctrl+Z
        # удаляйте последний элемент из списка self.rects.
        ...


def setup_game(width=800, height=600, title="Rects With Cancel"):
    game = MyGame(width, height, title)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
