import arcade
from pyglet.graphics import Batch

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
TITLE = "Writing Machine"


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        # Создайте атрибут для хранения набираемого текста (изначально пустую строку).
        self.text = ''
        self.yellow = arcade.color.BANANA_YELLOW
        self.font = 100

    def on_key_press(self, key, modifiers):
        # 1. Преобразуйте код клавиши (key) в символ.
        # 2. Проверьте параметр modifiers, чтобы определить, нажат ли Shift.
        # 3. Добавьте полученный символ (в нужном регистре) к вашей текстовой строке.
        if key == arcade.key.Q and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'q'
        if key == arcade.key.Q and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'Q'

        if key == arcade.key.W and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'w'
        if key == arcade.key.W and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'W'

        if key == arcade.key.E and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'e'
        if key == arcade.key.E and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'E'

        if key == arcade.key.R and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'r'
        if key == arcade.key.R and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'R'

        if key == arcade.key.T and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 't'
        if key == arcade.key.T and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'T'

        if key == arcade.key.Y and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'y'
        if key == arcade.key.Y and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'Y'

        if key == arcade.key.U and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'u'
        if key == arcade.key.U and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'U'

        if key == arcade.key.I and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'i'
        if key == arcade.key.I and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'I'

        if key == arcade.key.O and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'o'
        if key == arcade.key.O and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'O'

        if key == arcade.key.P and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'p'
        if key == arcade.key.P and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'P'

        if key == arcade.key.BRACKETLEFT:
            self.text += '['

        if key == arcade.key.BRACKETRIGHT:
            self.text += ']'

        # 2 ряд ------------------------------------------------------------------------------------------
        if key == arcade.key.A and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'a'
        if key == arcade.key.A and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'A'

        if key == arcade.key.S and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 's'
        if key == arcade.key.S and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'S'

        if key == arcade.key.D and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'd'
        if key == arcade.key.D and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'D'

        if key == arcade.key.F and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'f'
        if key == arcade.key.F and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'F'
        if key == arcade.key.G and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'g'
        if key == arcade.key.G and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'G'

        if key == arcade.key.H and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'h'
        if key == arcade.key.H and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'H'

        if key == arcade.key.J and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'j'
        if key == arcade.key.J and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'J'

        if key == arcade.key.K and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'k'
        if key == arcade.key.K and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'K'

        if key == arcade.key.L and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'l'
        if key == arcade.key.L and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'L'

        if key == arcade.key.SEMICOLON:
            self.text += ';'

        if key == arcade.key.APOSTROPHE:
            self.text += "'"

        #     3 РЯД !!! -------------------------------
        if key == arcade.key.Z and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'z'
        if key == arcade.key.Z and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'Z'

        if key == arcade.key.X and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'x'
        if key == arcade.key.X and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'X'

        if key == arcade.key.C and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'c'
        if key == arcade.key.C and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'C'

        if key == arcade.key.V and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'v'
        if key == arcade.key.V and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'V'
        if key == arcade.key.B and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'b'
        if key == arcade.key.B and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'B'

        if key == arcade.key.N and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'n'
        if key == arcade.key.N and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'N'

        if key == arcade.key.M and not modifiers & arcade.key.MOD_SHIFT:
            self.text += 'm'
        if key == arcade.key.M and modifiers & arcade.key.MOD_SHIFT:
            self.text += 'M'

        if key == arcade.key.COMMA:
            self.text += ','

        if key == arcade.key.PERIOD:
            self.text += '.'

        if key == arcade.key.SLASH:
            self.text += '/'

        if key == arcade.key.BACKSPACE and self.text:
            self.text = self.text[:-1]
        if key == arcade.key.SPACE:
            self.text += ' '

    def on_draw(self):
        self.clear()
        self.batch = Batch()
        # Создайте объект arcade.Text с текущим текстом и нужными параметрами.
        # Для точного центрирования используйте anchor_x="center" и anchor_y="center".
        # Не забудьте отрисовать batch.
        self.draw_text = arcade.Text(f"{self.text}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                     self.yellow, self.font, font_name="Calibri", anchor_y='center', anchor_x='center',
                                     batch=self.batch)
        self.batch.draw()


def setup_game(width=800, height=600, title="Writing Machine"):
    game = MyGame(width, height, title)
    game.setup()
    return game


# Блок для вашего локального тестирования (необязателен для сдачи)
def main():
    setup_game()
    arcade.run()


if __name__ == "__main__":
    main()
