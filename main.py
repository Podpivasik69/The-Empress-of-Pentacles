from view import *
import arcade

font = 'Minecraft'
MENU_FONT = 'Minecraft'

print(f"Загружен шрифт: {font}")
print(f"Тип: {type(font)}")

# режим разраба (выключает меню)
TEST_MODE = True


# Точка входа в программу (как if __name__ == "__main__": в обычном скрипте)
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    if TEST_MODE:
        game_view = GameView()  # переключаем окно на игру
        game_view.setup()  # запускаем игровой setuo
        window.show_view(game_view)  # показываем окно игры

        print(f"Запуск в тестовом режиме. Шрифт меню: {MENU_FONT}")

    else:
        start_view = StartMenuView()
        window.show_view(start_view)
        print(f"Запуск через меню. Шрифт: {MENU_FONT}")

    arcade.run()


if __name__ == "__main__":
    main()
