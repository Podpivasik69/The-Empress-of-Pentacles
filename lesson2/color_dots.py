import arcade
from arcade.types import Color
from pyglet.event import EVENT_HANDLE_STATE

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TITLE = "Color points"
COLORS = ['#ffc000', '#dc00a9', '#0065ac', '#22ad00']


class MyGame(arcade.Window):
    def __init__(self, width, height, title, colors):
        super().__init__(width, height, title)
        # Сохраните переданные цвета в атрибут класса
        self.new_colors = []
        for i in colors:
            self.new_colors.append(Color.from_hex_string(i))

        self.is_ctrl = False
        self.index = 1

    def setup(self):
        # Список для хранения параметров нарисованных фигур
        self.points_to_circle = []
        self.points_to_rect = []
        self.white_circl = []
        self.white_rect = []
        self.radius = 10
        self.white = arcade.color.WHITE

    def on_draw(self):
        self.clear()
        # В цикле отрисуйте все круги из self.points,
        # чередуя цвета из сохраненного списка
        for i in range(len(self.points_to_circle)):
            arcade.draw_circle_filled(self.points_to_circle[i][0], self.points_to_circle[i][1], self.radius,
                                      self.new_colors[self.points_to_circle[i][2] % 4])

        for j in range(len(self.points_to_rect)):
            arcade.draw_rect_filled(
                arcade.rect.XYWH(self.points_to_rect[j][0], self.points_to_rect[j][1], self.radius * 2,
                                 self.radius * 2), self.new_colors[self.points_to_rect[j][2] % 4])

        # белые
        for i1 in range(len(self.white_rect)):
            arcade.draw_rect_filled(
                arcade.rect.XYWH(self.white_rect[i1][0], self.white_rect[i1][1], self.radius * 2,
                                 self.radius * 2), self.white)

        for j2 in range(len(self.white_circl)):
            arcade.draw_circle_filled(self.white_circl[j2][0], self.white_circl[j2][1], self.radius,
                                      self.white)

    def on_mouse_press(self, x, y, button, modifiers):
        # Добавьте координаты (x, y) в self.points
        if button == arcade.MOUSE_BUTTON_LEFT and not modifiers & arcade.key.MOD_CTRL:
            self.index += 1
            self.points_to_circle.append([x, y, self.index])
            # print(self.points_to_rect)
        if button == arcade.MOUSE_BUTTON_RIGHT and not modifiers & arcade.key.MOD_CTRL:
            self.index += 1
            self.points_to_rect.append([x, y, self.index])

        if button == arcade.MOUSE_BUTTON_LEFT and modifiers & arcade.key.MOD_CTRL:
            self.index += 1
            self.white_circl.append([x, y])
        elif button == arcade.MOUSE_BUTTON_RIGHT and modifiers & arcade.key.MOD_CTRL:
            self.index += 1
            self.white_rect.append([x, y])


def setup_game(width=800, height=600, title="Color points", colors=None):
    # Если в функцию не передали список цветов, используйте COLORS по умолчанию
    game = MyGame(width, height, title, COLORS[:] if colors is None else colors)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    game = setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
