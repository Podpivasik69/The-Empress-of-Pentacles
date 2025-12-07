import arcade  # Подключаем игровые суперсилы

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The Empress of Pentacles"
font = 'minecraft.ttf'

print(f"Загружен шрифт: {font}")
print(f"Тип: {type(font)}")


class StartMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.white = arcade.color.WHITE
        self.brown = arcade.color.COCOA_BROWN
        arcade.set_background_color(arcade.color.ASH_GREY)

        self.menu_button = arcade.load_texture('media/menu_button.png')

    def on_show(self):
        # Вызывается при показе View
        pass

    def on_draw(self):
        # Назван е
        arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, (SCREEN_HEIGHT * 3) // 4,
                                                  600, 100), self.white, 1)
        arcade.draw_text(SCREEN_TITLE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4,
                         self.white, 42, anchor_x="center", anchor_y="center")
        # Кнопка играть
        arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, 250, 200, 100), self.brown, 1)
        arcade.draw_texture_rect(self.menu_button, arcade.rect.XYWH(SCREEN_WIDTH // 2, 250, 200, 100), )
        arcade.draw_text('иглать', SCREEN_WIDTH // 2, 250, self.white, 42, anchor_x="center", anchor_y="center")
        # кглпка выохода
        arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, 150, 200, 100), self.brown, 1)
        arcade.draw_texture_rect(self.menu_button, arcade.rect.XYWH(SCREEN_WIDTH // 2, 150, 200, 100), )
        arcade.draw_text('вихад', SCREEN_WIDTH // 2, 150, self.white, 42, anchor_x="center", anchor_y="center")

    def on_mouse_press(self, x, y, button, modifiers):
        # жмяк и выход
        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 100 <= y <= 200:
            arcade.close_window()

        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 200 <= y <= 300:
            game_view = GameView()
            self.window.show_view(game_view)


class GameView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_draw(self):
        self.clear()
        arcade.draw_text("тут типа игра", 400, 300, arcade.color.WHITE, 50, anchor_x="center", anchor_y="center")


# Точка входа в программу (как if __name__ == "__main__": в обычном скрипте)
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartMenuView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
