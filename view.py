import arcade

from player import *




class StartMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.white = arcade.color.WHITE
        self.brown = arcade.color.COCOA_BROWN
        arcade.set_background_color(arcade.color.ASH_GREY)
        arcade.load_font('MinecraftDefault-Regular.ttf')

        self.menu_button = arcade.load_texture('media/menu_button_2.png')
        self.background_texture = arcade.load_texture('media/new_backgroung_2.png')

    def on_show(self):
        # Вызывается при показе View
        pass

    def on_draw(self):
        # картинка задний фон
        arcade.draw_texture_rect(self.background_texture,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        # Назван е
        # arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, (SCREEN_HEIGHT * 3) // 4,
        #                                           600, 100), self.white, 1, )
        arcade.draw_text(SCREEN_TITLE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4,
                         self.white, 50, anchor_x="center", anchor_y="center", font_name='Minecraft Default')
        # Кнопка играть
        # arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, 250, 200, 100), self.brown, 1)
        arcade.draw_texture_rect(self.menu_button, arcade.rect.XYWH(SCREEN_WIDTH // 2, 250, 200, 90), )
        arcade.draw_text('иглать', SCREEN_WIDTH // 2, 250, self.white, 42,
                         anchor_x="center", anchor_y="center", font_name='Minecraft Default')
        # кглпка выохода
        # arcade.draw_rect_outline(arcade.rect.XYWH(SCREEN_WIDTH // 2, 150, 200, 100), self.brown, 1)
        arcade.draw_texture_rect(self.menu_button, arcade.rect.XYWH(SCREEN_WIDTH // 2, 150, 200, 90), )
        arcade.draw_text('вихад', SCREEN_WIDTH // 2, 150, self.white, 42,
                         anchor_x="center", anchor_y="center", font_name='Minecraft Default')

    def on_mouse_press(self, x, y, button, modifiers):
        # жмяк и выход
        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 110 <= y <= 190:
            arcade.close_window()
        # иглать
        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 210 <= y <= 290:
            game_view = GameView()  # переключаем окно на игру
            game_view.setup()  # запускаем игровой setuo
            self.window.show_view(game_view)  # показываем окно игры
