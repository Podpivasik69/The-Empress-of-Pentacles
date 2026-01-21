import arcade
from constants import PAUSE_MENU_SETTINGS
from constants import SCREEN_TITLE, SCREEN_HEIGHT, SCREEN_WIDTH


class PauseMenu:
    def __init__(self, game_view):
        self.game_view = game_view
        self.data = PAUSE_MENU_SETTINGS
        self.is_menu_open = False
        self.buttons = []

        self.menu_button_texture = arcade.load_texture('media/ui/menu_button.png')

    def menu_open(self):
        if self.is_menu_open:
            return
        self.is_menu_open = True

    def menu_close(self):
        if not self.is_menu_open:
            return
        self.is_menu_open = False

    def menu_toggle(self):
        if self.is_menu_open:
            self.is_menu_open = False
        else:
            self.is_menu_open = True

    def setup(self):
        resume_button = self.create_button(
            'Возобновить изыскание',
            self.resume_game,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60),
            (300, 60),
        )
        self.buttons.append(resume_button)

        settings_button = self.create_button(
            'Настройки',
            self.open_settings,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            (300, 60)
        )
        self.buttons.append(settings_button)

        exit_button = self.create_button(
            "Выход",
            self.exit_to_main_menu,
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60),
            (300, 60)
        )
        self.buttons.append(exit_button)

    def resume_game(self):
        """ Возабновить изыскание"""
        self.menu_close()

    def open_settings(self):
        """ Открыть настройки"""
        print("треба открыть настройки")

    def exit_to_main_menu(self):
        """ Выход в главное меню"""
        from view import StartMenuView
        self.menu_close()
        self.game_view.window.show_view(StartMenuView())

    def create_button(self, text, action, position, size):
        """ хуйня создает кнопки"""
        return {
            'text': text,
            'action': action,
            'position': position,
            'size': size,
            'rect': arcade.rect.XYWH(position[0], position[1], size[0], size[1])
        }

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.resume_game()
            return

    def on_draw(self):
        """ рисовать паузу"""
        if not self.is_menu_open:
            return
        # серая фоновая заливка
        arcade.draw_rect_filled(
            arcade.rect.XYWH(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
                SCREEN_WIDTH,
                SCREEN_HEIGHT
            ),
            (50, 50, 50, 150)
        )
        arcade.draw_text(
            "ИГРА ПРИСТАНОВЛЕНА",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            arcade.color.WHITE,
            48,
            anchor_x="center",
            anchor_y="center"
        )
        for button in self.buttons:
            arcade.draw_texture_rect(
                self.menu_button_texture,
                button['rect'],
            )
            arcade.draw_text(
                button['text'],
                button['position'][0],
                button['position'][1],
                arcade.color.WHITE,
                20,
                anchor_x="center",
                anchor_y="center",
            )


class SettingsView:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.is_settings_open = False
        self.settings = {} # все текучие настройки
        self.elements = [] # все текучие элементы UI