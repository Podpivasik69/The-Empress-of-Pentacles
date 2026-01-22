import arcade
from constants import PAUSE_MENU_SETTINGS
from constants import SCREEN_TITLE, SCREEN_HEIGHT, SCREEN_WIDTH


class PauseMenu:
    def __init__(self, game_state):
        self.game_state = game_state
        self.data = PAUSE_MENU_SETTINGS
        self.buttons = []
        self.menu_button_texture = arcade.load_texture('media/ui/menu_button.png')

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

    def menu_open(self):
        """ хуйня которая открывает меню паузы"""
        if self.game_state.is_game_paused:  # если уже открыто скип
            return

        self.game_state.is_game_paused = True
        self.game_state.current_screen = "pause"

        if not self.buttons:  # кнопок нет? создадим
            self.setup()

    def menu_close(self):
        if not self.game_state.is_game_paused:
            return
        self.game_state.is_game_paused = False
        self.game_state.current_screen = "game"

    def menu_toggle(self):
        if self.game_state.is_game_paused:
            self.menu_close()
        else:
            self.menu_open()

    def resume_game(self):
        """ Возабновить изыскание"""
        self.menu_close()

    def open_settings(self):
        """ Открыть настройки"""
        print("треба открыть настройки")

        self.game_state.next_action = "open_settings"  # след действие - открыть настройки
        self.menu_close()  # выключаем паузу

    def exit_to_main_menu(self):
        """ Выход в главное меню"""
        self.game_state.next_action = "exit_to_main_menu"  # ливаем нахуй
        self.menu_close()

    def create_button(self, text, action, position, size):
        """ хуйня создает кнопки"""
        return {
            'text': text,
            'action': action,
            'position': position,
            'size': size,
            'rect': arcade.rect.XYWH(position[0], position[1], size[0], size[1])
        }

    def on_draw(self):
        """ рисовать паузу"""
        # не рисовать паузу
        if not self.game_state.is_game_paused:
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
    def __init__(self, game_state):
        self.game_state = game_state
        self.settings = {}  # все текучие настройки
        self.elements = []  # все текучие элементы UI

    def settings_open(self):
        self.game_state.current_screen = "settings"

    def settings_close(self):
        if self.game_state.current_screen == "settings":
            self.game_state.current_screen = "game"

    def settings_toggle(self):
        if self.game_state.current_screen == "settings":
            self.settings_close()
        else:
            self.settings_open()


