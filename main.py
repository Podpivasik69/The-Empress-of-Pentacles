from view import *

font = 'Minecraft'

print(f"Загружен шрифт: {font}")
print(f"Тип: {type(font)}")


# Точка входа в программу (как if __name__ == "__main__": в обычном скрипте)
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartMenuView()
    # window.show_view(start_view)
    game_view = GameView()  # переключаем окно на игру
    game_view.setup()  # запускаем игровой setuo
    window.show_view(game_view)  # показываем окно игры

    arcade.run()


if __name__ == "__main__":
    main()
