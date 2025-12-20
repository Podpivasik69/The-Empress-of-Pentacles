import arcade

# Константы
SCREEN_WIDTH = 820
SCREEN_HEIGHT = 620
SCREEN_TITLE = "Balls"
CELL_SIZE = 40
INDENT = 10  # Отступ от края окна

# Цвета шариков (по кругу)
COLORS = [
    arcade.color.RED,
    arcade.color.GREEN,
    arcade.color.BLUE,
    arcade.color.YELLOW,
    arcade.color.VIOLET
]


class GridGame(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title):
        super().__init__(screen_width, screen_height, screen_title)

        self.rows = (screen_height - 2 * INDENT) // CELL_SIZE
        self.cols = (screen_width - 2 * INDENT) // CELL_SIZE
        self.cell_size = CELL_SIZE
        self.radius = CELL_SIZE // 2 - 2
        self.gray = arcade.color.GRAY

    def setup(self):
        # Создаём пустую сетку нужного размера
        self.grid = [[None for _ in range(self.cols)] for _ in range(self.rows)]

    def on_draw(self):
        self.clear()
        # Рисуем сетку, цвет arcade.color.GRAY
        for row in range(self.rows):
            for col in range(self.cols):
                x = INDENT + col * self.cell_size + self.cell_size // 2
                y = INDENT + row * self.cell_size + self.cell_size // 2

                arcade.draw_rect_outline(arcade.rect.XYWH(x, y,
                                                          self.cell_size - 2,
                                                          self.cell_size - 2),
                                         arcade.color.GRAY, 1)
        # Рисуем шарики, если они есть
        for row in range(self.rows):
            for col in range(self.cols):
                color = self.grid[row][col]
                if color is not None:
                    x = INDENT + col * self.cell_size + self.cell_size // 2
                    y = INDENT + row * self.cell_size + self.cell_size // 2
                    color = COLORS[color]
                    arcade.draw_circle_filled(x, y, self.radius, color)

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мыши"""
        col = int((x - INDENT) // self.cell_size)
        row = int((y - INDENT) // self.cell_size)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if button == arcade.MOUSE_BUTTON_LEFT:
                if self.grid[row][col] is None:
                    self.grid[row][col] = 0
                else:
                    self.grid[row][col] = (self.grid[row][col] + 1) % len(COLORS)


def setup_game(width=820, height=620, title="Balls"):
    game = GridGame(width, height, title)
    game.setup()
    return game


def main():
    setup_game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
