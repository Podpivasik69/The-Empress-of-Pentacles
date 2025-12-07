import arcade  # Подключаем игровые суперсилы


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background_color = arcade.color.TEA_GREEN

    def setup(self):
        # ... Предыдущий код ...
        self.brush_position = (0, 0)
        self.brush_size = 10
        self.brush_color = arcade.color.RED
        self.drawing = False
        self.points = []  # Точки для рисования

    def on_mouse_motion(self, x, y, dx, dy):
        self.brush_position = (x, y)
        if self.drawing:
            self.points.append((x, y, self.brush_color, self.brush_size))

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.drawing = True
            self.points.append((x, y, self.brush_color, self.brush_size))
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            self.points = []  # Очистка холста

    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.drawing = False

    def on_draw(self):
        self.clear()
        # Рисуем все точки
        for point in self.points:
            x, y, color, size = point
            arcade.draw_circle_filled(x, y, size, color)

        # Рисуем курсор-кисть
        x, y = self.brush_position
        arcade.draw_circle_outline(x, y, self.brush_size, self.brush_color, 2)


def main():
    game = MyGame(800, 600, "Arcade Первый Контакт")
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
