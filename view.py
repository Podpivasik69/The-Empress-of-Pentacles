import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "The Empress of Pentacles"

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
        # иглать
        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 200 <= y <= 300:
            game_view = GameView()  # переключаем окно на игру
            game_view.setup()  # запускаем игровой setuo
            self.window.show_view(game_view)  # показываем окно игры