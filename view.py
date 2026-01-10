from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from game import GameView
import arcade


class StartMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.white = arcade.color.WHITE
        self.brown = arcade.color.COCOA_BROWN
        arcade.set_background_color(arcade.color.ASH_GREY)
        arcade.load_font('media/MinecraftDefault-Regular.ttf')

        self.menu_button = arcade.load_texture('media/ui/menu_button.png')
        self.background_texture = arcade.load_texture('media/backgroung.png')

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

        arcade.draw_texture_rect(self.menu_button, arcade.rect.XYWH(SCREEN_WIDTH // 2, 50, 200, 90), )
        arcade.draw_text('phys', SCREEN_WIDTH // 2, 50, self.white, 42,
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

        if SCREEN_WIDTH // 2 - 100 <= x <= SCREEN_WIDTH // 2 + 100 and 10 <= y <= 90:
            from world import WorldView
            world_view = WorldView()
            self.window.show_view(world_view)


class DeathScreenView(arcade.View):
    def __init__(self):
        super().__init__()
        print("DEBUG DeathScreenView: __init__ called")
        self.white = arcade.color.WHITE
        arcade.set_background_color(arcade.color.ASH_GREY)
        self._cursor_enabled = False
        arcade.load_font('media/MinecraftDefault-Regular.ttf')

        self.background_texture = arcade.load_texture('media/backgroung.png')
        self.menu_button = arcade.load_texture('media/ui/menu_button.png')

        # TODO статистика после смерти, рекорды, и тд

    def on_draw(self):
        self.clear()
        # pfujkjdjr
        arcade.draw_texture_rect(self.background_texture,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT))
        arcade.draw_text("ТИ СДОХ", SCREEN_HEIGHT // 2, 450, self.white, 50,
                         anchor_x='center', anchor_y='center', font_name="Minecraft Default")
        # начать заново
        arcade.draw_texture_rect(self.menu_button,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, 300, 200, 90))
        arcade.draw_text('ЗАНОВО', SCREEN_WIDTH // 2, 300, self.white, 42,
                         anchor_x="center", anchor_y="center",
                         font_name='Minecraft Default')
        # меню (если слабый)
        arcade.draw_texture_rect(self.menu_button,
                                 arcade.rect.XYWH(SCREEN_WIDTH // 2, 200, 200, 90))
        arcade.draw_text('В МЕНЮ', SCREEN_WIDTH // 2, 200, self.white, 42,
                         anchor_x="center", anchor_y="center",
                         font_name='Minecraft Default')

    def on_mouse_press(self, x, y, button, modifiers):
        button_width = 200
        button_height = 90
        # заново
        button_x = SCREEN_WIDTH // 2
        button_y = 300

        if (button_x - button_width / 2 <= x <= button_x + button_width / 2 and
                button_y - button_height / 2 <= y <= button_y + button_height / 2):
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        # в меню
        button_y = 200
        if (button_x - button_width / 2 <= x <= button_x + button_width / 2 and
                button_y - button_height / 2 <= y <= button_y + button_height / 2):
            menu_view = StartMenuView()
            self.window.show_view(menu_view)

    def on_show_view(self):
        print("DEBUG DeathScreenView: on_show_view called")
        if self.window:
            self.window.set_mouse_visible(True)
            self._cursor_enabled = True
            print("Курсор включен в DeathScreen")

    def on_hide(self):
        if self.window:
            self.window.set_mouse_visible(False)
